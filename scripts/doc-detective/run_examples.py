#!/usr/bin/env python3
"""Run annotated SenseML examples from the docs against the Sensible API.

An example is marked up in a doc with HTML comments, inside a Doc Detective test:

    <!-- test {"testId": "extract_auto_insurance_anyco"} -->
    <!-- example document -->
    | Example document | [Download link](https://.../auto_insurance_anyco.pdf) |
    <!-- example config -->
    ```json
    { "fields": [ ... ] }
    ```
    <!-- example output -->
    ```json
    { "policy_number": { ... } }
    ```
    <!-- test end -->

For each example, the runner:
  1. Parses the config (allowing /* */ comments and trailing commas)
  2. Uploads it as configuration <testId> in document type DOC_TYPE, published to development
  3. Extracts from the example document with the Python SDK. The URL comes from the first link
     after <!-- example document -->, so the visible download link is the only copy
  4. Checks that the docs output is a subset of the actual parsed_document
At the end of the run, it deletes DOC_TYPE (configs included). Extraction history stays in the app.

Usage:
  run_examples.py --file "docs/document extraction/getting-started.md" --test extract_auto_insurance_anyco
  run_examples.py --file <doc> --list

Requires SENSIBLE_API_KEY in the environment.
"""

import argparse
import json
import os
import re
import sys

# Local installs: pip install --target scripts/doc-detective/.deps -r scripts/doc-detective/requirements.txt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".deps"))

import requests
from sensibleapi import SensibleSDK

API = "https://api.sensible.so/v0"
DOC_TYPE = "docs_ci_examples"
ENVIRONMENT = "development"

TEST_RE = re.compile(r"<!--\s*test\s+(\{.*?\})\s*-->(.*?)<!--\s*test end\s*-->", re.S)
MARKER_RE = re.compile(r"<!--\s*example\s+(config|document|output)\s*(\{.*?\})?\s*-->", re.S)
FENCE_RE = re.compile(r"\s*```[a-zA-Z0-9]*\n(.*?)\n```", re.S)
# First Markdown link on the next non-blank line, for example the example document's download link
LINK_RE = re.compile(r"\s*[^\n]*?\]\((https?://[^)\s]+)\)")


class ExampleError(Exception):
    """A failure with a category, so a report can tell docs bugs from product drift."""

    def __init__(self, category, message):
        super().__init__(f"{category}: {message}")
        self.category = category


def strip_json5(text):
    """Remove /* */ and // comments and trailing commas, leaving strings intact."""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i : j + 1])
            i = j + 1
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        elif text.startswith("//", i):
            end = text.find("\n", i)
            i = n if end == -1 else end
        else:
            out.append(c)
            i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def parse_examples(path):
    """Return {testId: {"config", "document_url", "output"}} for annotated tests in a doc."""
    text = open(path, encoding="utf-8").read()
    examples = {}
    for test_match in TEST_RE.finditer(text):
        test = json.loads(test_match.group(1))
        body = test_match.group(2)
        parts = {}
        for marker in MARKER_RE.finditer(body):
            role = marker.group(1)
            options = json.loads(marker.group(2)) if marker.group(2) else {}
            if role == "document":
                link = LINK_RE.match(body, marker.end())
                if not link:
                    raise ExampleError("DOCS_MALFORMED", f"{test['testId']}: <!-- example document --> isn't followed by a line with a link")
                parts["document_url"] = link.group(1)
                continue
            fence = FENCE_RE.match(body, marker.end())
            if not fence:
                raise ExampleError("DOCS_MALFORMED", f"{test['testId']}: <!-- example {role} --> isn't followed by a code block")
            parts[role] = fence.group(1)
        if parts:
            missing = {"config", "document_url", "output"} - parts.keys()
            if missing:
                raise ExampleError("DOCS_MALFORMED", f"{test['testId']}: missing example {', '.join(sorted(missing))}")
            examples[test["testId"]] = parts
    return examples


def subset_diffs(expected, actual, path="$"):
    """List the ways `expected` isn't contained in `actual`. Arrays are positional and length-checked."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{path}: expected an object, got {json.dumps(actual)}"]
        diffs = []
        for key, value in expected.items():
            if key not in actual:
                diffs.append(f"{path}.{key}: missing from actual output")
            else:
                diffs += subset_diffs(value, actual[key], f"{path}.{key}")
        return diffs
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            return [f"{path}: expected {json.dumps(expected)}, got {json.dumps(actual)}"]
        return [d for i, (e, a) in enumerate(zip(expected, actual)) for d in subset_diffs(e, a, f"{path}[{i}]")]
    if isinstance(expected, float) or isinstance(actual, float):
        if isinstance(actual, (int, float)) and abs(expected - actual) < 1e-9:
            return []
    elif expected == actual:
        return []
    return [f"{path}: expected {json.dumps(expected)}, got {json.dumps(actual)}"]


def api(method, path, key, **kwargs):
    response = requests.request(method, f"{API}{path}", headers={"Authorization": f"Bearer {key}"}, timeout=60, **kwargs)
    return response


def ensure_doc_type(key):
    response = api("GET", "/document_types", key)
    response.raise_for_status()
    for doc_type in response.json():
        if doc_type["name"] == DOC_TYPE:
            return doc_type["id"]
    response = api("POST", "/document_types", key, json={"name": DOC_TYPE, "schema": {"fingerprint_mode": "fallback_to_all"}})
    response.raise_for_status()
    return response.json()["id"]


def delete_doc_type(key):
    response = api("GET", "/document_types", key)
    response.raise_for_status()
    for doc_type in response.json():
        if doc_type["name"] == DOC_TYPE:
            api("DELETE", f"/document_types/{doc_type['id']}", key).raise_for_status()
            return True
    return False


def upload_config(key, type_id, name, config):
    body = {"configuration": json.dumps(config), "publish_as": ENVIRONMENT}
    existing = api("GET", f"/document_types/{type_id}/configurations/{name}", key)
    if existing.status_code == 404:
        response = api("POST", f"/document_types/{type_id}/configurations", key, json={"name": name, **body})
    else:
        response = api("PUT", f"/document_types/{type_id}/configurations/{name}", key, json=body)
    if not response.ok:
        raise ExampleError("CONFIG_INVALID", f"config upload returned {response.status_code}: {response.text[:500]}")


def run_example(key, test_id, example):
    response = requests.head(example["document_url"], allow_redirects=True, timeout=30)
    if response.status_code != 200:
        raise ExampleError("DOCUMENT_UNREACHABLE", f"{example['document_url']} returned {response.status_code}")

    try:
        config = json.loads(strip_json5(example["config"]))
        expected = json.loads(strip_json5(example["output"]))
    except json.JSONDecodeError as e:
        raise ExampleError("DOCS_MALFORMED", f"can't parse config or output block: {e}")

    type_id = ensure_doc_type(key)
    upload_config(key, type_id, test_id, config)

    sensible = SensibleSDK(key)
    request = sensible.extract(
        url=example["document_url"],
        document_type=DOC_TYPE,
        configuration_name=test_id,
        environment=ENVIRONMENT,
        document_name=f"ci__{test_id}.pdf",
    )
    result = sensible.wait_for(request)
    if result.get("status") != "COMPLETE":
        raise ExampleError("EXTRACTION_ERROR", f"status {result.get('status')}: {json.dumps(result.get('errors'))[:500]}")

    diffs = subset_diffs(expected, result.get("parsed_document") or {})
    if diffs:
        raise ExampleError("OUTPUT_DRIFT", "docs output doesn't match the extraction:\n  " + "\n  ".join(diffs))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", required=True, help="Markdown file with annotated examples")
    parser.add_argument("--test", action="append", help="testId to run (repeatable). Default: all in the file")
    parser.add_argument("--list", action="store_true", help="List annotated examples and exit")
    parser.add_argument("--keep", action="store_true", help=f"Don't delete {DOC_TYPE} after the run (for debugging in the app)")
    args = parser.parse_args()

    examples = parse_examples(args.file)
    if args.list:
        for test_id, example in examples.items():
            print(f"{test_id}  {example['document_url']}")
        return 0

    key = os.environ.get("SENSIBLE_API_KEY")
    if not key:
        print("SENSIBLE_API_KEY isn't set", file=sys.stderr)
        return 2

    selected = args.test or list(examples)
    failed = 0
    try:
        for test_id in selected:
            if test_id not in examples:
                print(f"FAIL {test_id}  DOCS_MALFORMED: no annotated example with this testId in {args.file}")
                failed += 1
                continue
            try:
                run_example(key, test_id, examples[test_id])
                print(f"PASS {test_id}")
            except ExampleError as e:
                print(f"FAIL {test_id}  {e}")
                failed += 1
    finally:
        if not args.keep and delete_doc_type(key):
            print(f"Deleted document type {DOC_TYPE}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
