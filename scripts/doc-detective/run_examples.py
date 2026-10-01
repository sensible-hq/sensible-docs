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
  1. Checks syntax, before any network call:
     - config: JSON plus /* */ and // comments and trailing commas (Sensible accepts these)
     - output: JSON plus /* */ and // comments and `...`. No trailing commas: Sensible never outputs them
     - both: no duplicate keys, no NaN or Infinity. Errors give the line in the doc
  2. Uploads the config exactly as the doc shows it, as configuration <testId> in document type
     DOC_TYPE, published to development
  3. Extracts from the example document with the Python SDK. The URL comes from the first link
     after <!-- example document -->, so the visible download link is the only copy
  4. Checks that every key and value shown in the docs output agrees with the actual parsed_document.
     Keys the docs leave out are ignored. `...` (bare, or as the string "...") marks what not to check:
     a value, or the rest of an array ([first, second, ...], [first, ..., last]).
     An array without `...` must match in full.
  5. Sends mismatches that an LLM method (Query Group, List, NLP Table) produced, at any depth in
     the config, to an LLM judge (llm_judge.py; model: --judge-model, DOC_EXAMPLES_JUDGE_MODEL, or
     claude-sonnet-5-5). pass = OK; partial or a low-confidence pass = WARNING, the test still
     passes; fail = LLM_DRIFT. Everything else stays exact.
At the end of the run, it deletes DOC_TYPE (configs included). Extraction history stays in the app.

With --propose-fixes (or DOC_EXAMPLES_PROPOSE_FIXES=1, which CI sets), an OUTPUT_DRIFT failure also
rewrites the mismatched values in the doc's output block to the actual values, as a proposed docs fix
for a human to review. It doesn't touch output blocks that contain comments or a bare `...`.

Usage:
  run_examples.py --file "docs/document extraction/getting-started.md" --test extract_auto_insurance_anyco
  run_examples.py --file <doc> --list
  run_examples.py --file <doc> --check-syntax    (no API key or network needed)

Requires SENSIBLE_TEST_API_KEY (the docs test account's key) in .env at the repo root or in the environment.
Judging LLM fields also requires ANTHROPIC_API_KEY (or ANTHROPIC_KEY), from the same places.
It deliberately doesn't fall back to SENSIBLE_API_KEY, so a missing key can't run tests against another account.
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

import llm_judge

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


ELLIPSIS = "__ELLIPSIS__"


def is_ellipsis(value):
    return value in (ELLIPSIS, "...", "\u2026")


def strip_json5(text, trailing_commas=True):
    """Remove /* */ and // comments and trailing commas, leaving strings intact.

    Removed comments keep their newlines, so parse errors report the right line. With
    trailing_commas=False, a trailing comma raises SyntaxIssue instead of being removed.

    A bare `...` becomes the ELLIPSIS string. In an object's key position it becomes an
    `"__ELLIPSIS__": null` member, which drop_ellipsis_keys removes after parsing.
    """
    out = []
    stack = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if text.startswith("...", i):
            previous = "".join(out).rstrip()[-1:]
            key_position = bool(stack) and stack[-1] == "{" and previous in ("{", ",")
            out.append(f'"{ELLIPSIS}": null' if key_position else f'"{ELLIPSIS}"')
            i += 3
        elif c in "{[":
            stack.append(c)
            out.append(c)
            i += 1
        elif c in "}]":
            if stack:
                stack.pop()
            out.append(c)
            i += 1
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i : j + 1])
            i = j + 1
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end == -1:
                raise SyntaxIssue("unclosed /* comment", text.count("\n", 0, i) + 1)
            out.append("\n" * text.count("\n", i, end))
            i = end + 2
        elif text.startswith("//", i):
            end = text.find("\n", i)
            i = n if end == -1 else end
        else:
            out.append(c)
            i += 1
    stripped = "".join(out)
    if not trailing_commas:
        match = re.search(r",(\s*[}\]])", stripped)
        if match:
            raise SyntaxIssue("trailing comma", stripped.count("\n", 0, match.start()) + 1)
    return re.sub(r",(\s*[}\]])", r"\1", stripped)


class SyntaxIssue(Exception):
    def __init__(self, message, line):
        super().__init__(message)
        self.line = line


def strict_pairs(pairs):
    keys = [k for k, _ in pairs if k != ELLIPSIS]
    duplicates = sorted({k for k in keys if keys.count(k) > 1})
    if duplicates:
        raise ValueError(f"duplicate key {json.dumps(duplicates[0])}")
    return dict(pairs)


def reject_constant(name):
    raise ValueError(f"{name} isn't valid JSON")


def parse_block(text, trailing_commas):
    """Parse a docs code block, raising SyntaxIssue with a line number relative to the block."""
    stripped = strip_json5(text, trailing_commas)
    try:
        value = json.loads(stripped, object_pairs_hook=strict_pairs, parse_constant=reject_constant)
    except json.JSONDecodeError as e:
        raise SyntaxIssue(e.msg, e.lineno)
    except ValueError as e:
        raise SyntaxIssue(str(e), None)
    return drop_ellipsis_keys(value)


def drop_ellipsis_keys(value):
    if isinstance(value, dict):
        return {k: drop_ellipsis_keys(v) for k, v in value.items() if k != ELLIPSIS}
    if isinstance(value, list):
        return [drop_ellipsis_keys(v) for v in value]
    return value


def parse_json5(text):
    return parse_block(text, trailing_commas=True)


def check_syntax(test_id, example):
    """Return (config, expected output), or raise DOCS_MALFORMED with the doc line of the problem."""
    parsed = {}
    for role, trailing_commas in (("config", True), ("output", False)):
        try:
            parsed[role] = parse_block(example[role], trailing_commas)
        except SyntaxIssue as e:
            where = f"line {example[role + '_line'] + e.line}" if e.line else f"{role} block at line {example[role + '_line']}"
            raise ExampleError("DOCS_MALFORMED", f"{role} block: {e} ({example['file']}, {where})")
    return parsed["config"], parsed["output"]


def has_bare_ellipsis(text):
    return ELLIPSIS in strip_json5(text) and ELLIPSIS not in text


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
            start = test_match.start(2) + fence.start(1)
            parts[role + "_line"] = text.count("\n", 0, start)
            parts[role + "_span"] = (start, test_match.start(2) + fence.end(1))
            parts["file"] = path
        if parts:
            missing = {"config", "document_url", "output"} - parts.keys()
            if missing:
                raise ExampleError("DOCS_MALFORMED", f"{test['testId']}: missing example {', '.join(sorted(missing))}")
            examples[test["testId"]] = parts
    return examples


MISSING = object()


def subset_diffs(expected, actual, path=()):
    """List (path, expected, actual) where what the docs show disagrees with `actual`.

    Paths index into `expected`, so a fix can be applied to the docs output. Keys the docs omit are
    ignored, as is anything marked with `...`. Arrays match positionally: items before a `...` match
    the start of the actual array, items after it match the end. Without `...`, lengths must match.
    A key missing from `actual` reports actual as MISSING.
    """
    if is_ellipsis(expected):
        return []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [(path, expected, actual)]
        diffs = []
        for key, value in expected.items():
            if key not in actual:
                diffs.append((path + (key,), value, MISSING))
            else:
                diffs += subset_diffs(value, actual[key], path + (key,))
        return diffs
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return [(path, expected, actual)]
        cut = next((i for i, e in enumerate(expected) if is_ellipsis(e)), None)
        if cut is None:
            if len(actual) != len(expected):
                return [(path, expected, actual)]
            pairs = [(i, i) for i in range(len(expected))]
        else:
            head = list(range(cut))
            tail = [i for i in range(cut + 1, len(expected)) if not is_ellipsis(expected[i])]
            if len(actual) < len(head) + len(tail):
                return [(path, expected, actual)]
            offset = len(actual) - len(expected)
            pairs = [(i, i) for i in head] + [(i, i + offset) for i in tail]
        return [d for i, j in pairs for d in subset_diffs(expected[i], actual[j], path + (i,))]
    if isinstance(expected, bool) or isinstance(actual, bool):
        # In Python, True == 1 and False == 0. JSON booleans and numbers must not match.
        if type(expected) is type(actual) and expected == actual:
            return []
    elif isinstance(expected, float) or isinstance(actual, float):
        if isinstance(actual, (int, float)) and abs(expected - actual) < 1e-9:
            return []
    elif expected == actual:
        return []
    return [(path, expected, actual)]


def coverage_notes(expected, actual, path=(), notes=None):
    """Record what the comparison didn't check: `...` markers, shortened arrays, and keys the docs leave out.

    Returns {"skipped": [paths], "abbreviated": [(path, shown, total)], "extra_top_level": [keys],
    "extra_nested": count}.
    """
    if notes is None:
        notes = {"skipped": [], "abbreviated": [], "extra_top_level": [], "extra_nested": 0}
    if is_ellipsis(expected):
        notes["skipped"].append(path)
    elif isinstance(expected, dict) and isinstance(actual, dict):
        extra = [k for k in actual if k not in expected]
        if path:
            notes["extra_nested"] += len(extra)
        else:
            notes["extra_top_level"] += extra
        for k in expected:
            if k in actual:
                coverage_notes(expected[k], actual[k], path + (k,), notes)
    elif isinstance(expected, list) and isinstance(actual, list):
        cut = next((i for i, e in enumerate(expected) if is_ellipsis(e)), None)
        if cut is None:
            pairs = list(zip(range(len(expected)), range(len(actual)))) if len(expected) == len(actual) else []
        else:
            shown = [i for i, e in enumerate(expected) if not is_ellipsis(e)]
            notes["abbreviated"].append((path, len(shown), len(actual)))
            offset = len(actual) - len(expected)
            pairs = [(i, i) for i in shown if i < cut] + [(i, i + offset) for i in shown if i > cut]
            pairs = [(i, j) for i, j in pairs if 0 <= j < len(actual)]
        for i, j in pairs:
            coverage_notes(expected[i], actual[j], path + (i,), notes)
    return notes


def print_comparison(test_id, expected, actual, index, exact, judged_results):
    """Print what was compared and how, for the Doc Detective report and the failure issue."""
    notes = coverage_notes(expected, actual)
    def count(n, word):
        return f"{n} {word}" + ("" if n == 1 else "s")

    details = []
    left_out = []
    if notes["extra_top_level"]:
        left_out.append(count(len(notes["extra_top_level"]), "field"))
    if notes["extra_nested"]:
        left_out.append(count(notes["extra_nested"], "nested key"))
    if left_out:
        details.append("docs leave out " + " and ".join(left_out))
    marked = len(notes["skipped"]) + len(notes["abbreviated"])
    if marked:
        details.append(count(marked, "part") + " marked ... not checked")
    if judged_results:
        details.append(count(len(judged_results), "LLM value") + " differ" + ("s" if len(judged_results) == 1 else "") + ", decided by the judge")
    if exact or any(v == "fail" for _, _, _, v in judged_results):
        overall = "mismatch"
    elif not details and not diffs_exist(actual, expected):
        overall = "identical"
    else:
        overall = "matches, not identical" + (f" ({'; '.join(details)})" if details else "")

    print(f"Comparison for {test_id}")
    print(f"  Docs output vs parsed_document: {overall}")
    print("  Fields shown in the docs:")
    keys = list(expected) if isinstance(expected, dict) else []
    width = max((len(k) for k in keys), default=0)
    for key in keys:
        kind = ("fallback" if key in index.other else "LLM") if key in index.llm else ("layout" if key in index.other else "other")
        events = [f"exact mismatch at {format_path(d[0])}" for d in exact if d[0][:1] == (key,)]
        events += [
            f"judged {format_path(d[0])}: {r['match']} ({r['confidence']:.2f}, {model}) -> {verdict.upper()}"
            for d, model, r, verdict in judged_results
            if d[0][:1] == (key,)
        ]
        if is_ellipsis(expected[key]):
            events = ["not checked (...)"]
        print(f"    {key.ljust(width)}  {kind.ljust(8)}  {'; '.join(events) or 'exact match'}")
    if notes["skipped"] or notes["abbreviated"]:
        print("  Not checked (...):")
        for path in notes["skipped"]:
            print(f"    {format_path(path)}")
        for path, shown, total in notes["abbreviated"]:
            print(f"    {format_path(path)}: docs show {shown} of {total} items")
    if notes["extra_top_level"]:
        print(f"  In parsed_document, not in the docs: {', '.join(notes['extra_top_level'])}")
    if notes["extra_nested"]:
        print(f"  Nested keys in parsed_document, not in the docs: {notes['extra_nested']}")
    if judged_results:
        print("  Judge reasoning:")
        for d, model, r, verdict in judged_results:
            print(f"    {format_path(d[0])}: {r['reasoning']}")


def diffs_exist(expected, actual):
    return bool(subset_diffs(expected, actual))


def format_path(path):
    return "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in path)


def format_diff(diff):
    path, expected, actual = diff
    if actual is MISSING:
        return f"{format_path(path)}: missing from actual output"
    return f"{format_path(path)}: expected {json.dumps(expected)}, got {json.dumps(actual)}"


def apply_fixes(expected, diffs):
    """Return a copy of `expected` with each mismatched value replaced by the actual value."""
    fixed = json.loads(json.dumps(expected))
    for path, _, actual in diffs:
        if not path:
            return actual
        parent = fixed
        for step in path[:-1]:
            parent = parent[step]
        if actual is MISSING:
            del parent[path[-1]]
        else:
            parent[path[-1]] = actual
    return fixed


def propose_fix(path, example, fixed_output):
    """Rewrite the example's output block in the doc with `fixed_output`."""
    if "/*" in example["output"] or "//" in example["output"] or has_bare_ellipsis(example["output"]):
        print("  Not proposing a fix: the output block has comments or a bare ...", file=sys.stderr)
        return False
    text = open(path, encoding="utf-8").read()
    start, end = example["output_span"]
    if text[start:end] != example["output"]:
        print("  Not proposing a fix: the doc changed during the run", file=sys.stderr)
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(text[:start] + json.dumps(fixed_output, indent=2, ensure_ascii=False) + text[end:])
    return True


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


def upload_config(key, type_id, name, config_text):
    """Upload the config as the doc shows it, comments and all: Sensible accepts JSON5-style configs."""
    body = {"configuration": config_text, "publish_as": ENVIRONMENT}
    existing = api("GET", f"/document_types/{type_id}/configurations/{name}", key)
    if existing.status_code == 404:
        response = api("POST", f"/document_types/{type_id}/configurations", key, json={"name": name, **body})
    else:
        response = api("PUT", f"/document_types/{type_id}/configurations/{name}", key, json=body)
    if not response.ok:
        raise ExampleError("CONFIG_INVALID", f"config upload returned {response.status_code}: {response.text[:500]}")


def run_example(key, test_id, example, fix_path=None, judge_model_override=None):
    """Run one example. Returns a list of warnings; raises ExampleError on failure."""
    config, expected = check_syntax(test_id, example)

    response = requests.head(example["document_url"], allow_redirects=True, timeout=30)
    if response.status_code != 200:
        raise ExampleError("DOCUMENT_UNREACHABLE", f"{example['document_url']} returned {response.status_code}")

    type_id = ensure_doc_type(key)
    upload_config(key, type_id, test_id, example["config"])

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
    index = llm_judge.FieldIndex(config)
    routes = [index.route(d[0]) for d in diffs]
    exact = [d for d, route in zip(diffs, routes) if route is None]
    judged = [(d, route) for d, route in zip(diffs, routes) if route is not None]

    failures = [format_diff(d) for d in exact]
    fixable = list(exact)
    warnings = []
    judged_results = []
    if judged:
        # ANTHROPIC_KEY: the name some local shells use for the same key
        judge_key = load_key("ANTHROPIC_API_KEY") or load_key("ANTHROPIC_KEY")
        if not judge_key:
            raise ExampleError("JUDGE_UNAVAILABLE", "LLM fields differ but ANTHROPIC_API_KEY isn't set:\n  " + "\n  ".join(format_diff(d) for d in diffs))
        claims = [
            {
                "path": format_path(d[0]),
                "prompt": route[1],
                "documented": d[1],
                "observed": None if d[2] is MISSING else d[2],
            }
            for d, route in judged
        ]
        try:
            judge_model, results = llm_judge.judge(judge_key, claims, judge_model_override)
        except llm_judge.JudgeError as e:
            raise ExampleError("JUDGE_ERROR", str(e))
        for (d, route), r in zip(judged, results):
            verdict = llm_judge.classify(r)
            judged_results.append((d, judge_model, r, verdict))
            fallback_note = " (fallback chain: a layout field shares this ID)" if route[2] else ""
            line = (
                f"{format_diff(d)}\n    judge ({judge_model}){fallback_note}: "
                f"{r['match']}, confidence {r['confidence']:.2f}. {r['reasoning']}"
            )
            if verdict == "fail":
                failures.append(line)
                fixable.append(d)
            elif verdict == "warn":
                warnings.append(line)

    print_comparison(test_id, expected, result.get("parsed_document") or {}, index, exact, judged_results)
    if failures:
        message = "docs output doesn't match the extraction:\n  " + "\n  ".join(failures)
        if fix_path and propose_fix(fix_path, example, apply_fixes(expected, fixable)):
            message += f"\n  Proposed fix written to {fix_path}"
        raise ExampleError("OUTPUT_DRIFT" if exact else "LLM_DRIFT", message)
    return warnings


def load_key(var):
    """Read a key from .env (wins, as with Doc Detective's loadVariables) or the environment."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
    if os.path.exists(env_path):
        for line in open(env_path, encoding="utf-8"):
            name, _, value = line.strip().partition("=")
            if name == var and value:
                return value
    return os.environ.get(var)


def load_api_key():
    return load_key("SENSIBLE_TEST_API_KEY")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", required=True, help="Markdown file with annotated examples")
    parser.add_argument("--test", action="append", help="testId to run (repeatable). Default: all in the file")
    parser.add_argument("--list", action="store_true", help="List annotated examples and exit")
    parser.add_argument("--check-syntax", action="store_true", help="Only check config and output syntax. No API key or network needed")
    parser.add_argument(
        "--propose-fixes",
        action="store_true",
        default=os.environ.get("DOC_EXAMPLES_PROPOSE_FIXES") == "1",
        help="On OUTPUT_DRIFT, rewrite the doc's output block with the actual values (default: DOC_EXAMPLES_PROPOSE_FIXES=1)",
    )
    parser.add_argument("--judge-model", help=f"Judge model ID (default: DOC_EXAMPLES_JUDGE_MODEL or {llm_judge.DEFAULT_JUDGE_MODEL})")
    parser.add_argument("--keep", action="store_true", help=f"Don't delete {DOC_TYPE} after the run (for debugging in the app)")
    args = parser.parse_args()

    examples = parse_examples(args.file)
    if args.list:
        for test_id, example in examples.items():
            print(f"{test_id}  {example['document_url']}")
        return 0
    if args.check_syntax:
        failed = 0
        for test_id in args.test or list(examples):
            try:
                check_syntax(test_id, examples[test_id])
                print(f"PASS {test_id}  syntax")
            except ExampleError as e:
                print(f"FAIL {test_id}  {e}")
                failed += 1
        return 1 if failed else 0

    key = load_api_key()
    if not key:
        print("SENSIBLE_TEST_API_KEY isn't set in .env or the environment", file=sys.stderr)
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
                warnings = run_example(key, test_id, examples[test_id], args.file if args.propose_fixes else None, args.judge_model)
                print(f"PASS {test_id}" + (f" with {len(warnings)} warning(s) from the LLM judge" if warnings else ""))
            except ExampleError as e:
                print(f"FAIL {test_id}  {e}")
                failed += 1
    finally:
        if not args.keep and delete_doc_type(key):
            print(f"Deleted document type {DOC_TYPE}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
