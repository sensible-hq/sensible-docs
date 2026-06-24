#!/usr/bin/env python3
"""
Verify a blog post draft's "Putting it all together" output block matches
a live Sensible API extraction.

Extracts the config from the CONFIG:START/CONFIG:END block, uploads it, runs
a live extraction against the golden PDF, then diffs the result against the
json output block that follows CONFIG:END in the same section.

Usage:
    python .claude/skills/blog-how-to-parse-x/test_blog_output.py \
        --draft drafts/blog-oocl-delivery-orders-20260622.md \
        --doc-type oocl_delivery_orders \
        --pdf path/to/golden.pdf \
        [--config-name oocl_post]

Tests: .claude/skills/blog-how-to-parse-x/tests/test_blog_output_checker.py

Environment:
    SENSIBLE_API_KEY: Sensible API key (required)
"""

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

_SKILL = Path(__file__).parent
_REPO_ROOT = _SKILL.parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "scripts"))
sys.path.insert(0, str(_SKILL))

from extract_config_from_draft import extract_config
from upload_and_extract import extract_document
from upload_pr_extractor import get_or_create_doc_type, publish_config, upload_golden


def extract_output_block(draft_path: Path) -> dict:
    """Extract the JSON output block from the 'Putting it all together' section.

    Looks for the first ```json block (not ```json5) that appears after
    the <!-- CONFIG:END --> marker in the 'Putting it all together' section.
    """
    content = draft_path.read_text(encoding="utf-8")

    section_match = re.search(
        r"## Putting it all together\b.*?(?=\n## |\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if not section_match:
        print("Error: no 'Putting it all together' section found in draft", file=sys.stderr)
        sys.exit(1)

    section = section_match.group(0)
    parts = section.split("<!-- CONFIG:END -->", maxsplit=1)
    if len(parts) < 2:
        print("Error: no CONFIG:END marker in 'Putting it all together' section", file=sys.stderr)
        sys.exit(1)

    post_config = parts[1]
    # Match ```json but not ```json5
    json_match = re.search(r"```json\n(.*?)\n```", post_config, re.DOTALL)
    if not json_match:
        print("Error: no JSON output block found after CONFIG:END in draft", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(json_match.group(1))
    except json.JSONDecodeError as e:
        print(f"Error: output block is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def diff_outputs(expected: dict | list, actual: dict | list, path: str = "") -> list[str]:
    """Recursively diff expected vs actual parsed_document values.

    Returns a list of human-readable mismatch descriptions.
    """
    mismatches = []

    if type(expected) != type(actual):
        mismatches.append(
            f"  TYPE MISMATCH at {path or 'root'}:\n"
            f"    draft : {type(expected).__name__} {json.dumps(expected)}\n"
            f"    api   : {type(actual).__name__} {json.dumps(actual)}"
        )
        return mismatches

    if isinstance(expected, list):
        if len(expected) != len(actual):
            mismatches.append(
                f"  LENGTH MISMATCH at {path or 'root'}[]: draft has {len(expected)}, api has {len(actual)}"
            )
        for i, (e, a) in enumerate(zip(expected, actual)):
            mismatches.extend(diff_outputs(e, a, path=f"{path}[{i}]"))
        return mismatches

    if isinstance(expected, dict):
        all_keys = set(expected) | set(actual)
        for key in sorted(all_keys):
            child_path = f"{path}.{key}" if path else key
            if key not in actual:
                mismatches.append(f"  MISSING in api response : {child_path}")
            elif key not in expected:
                mismatches.append(f"  EXTRA in api response   : {child_path} = {json.dumps(actual[key])}")
            else:
                mismatches.extend(diff_outputs(expected[key], actual[key], path=child_path))
        return mismatches

    # Scalar comparison
    if expected != actual:
        mismatches.append(
            f"  MISMATCH : {path}\n"
            f"    draft  : {json.dumps(expected)}\n"
            f"    api    : {json.dumps(actual)}"
        )
    return mismatches


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify a blog post draft's output block matches a live Sensible extraction."
    )
    parser.add_argument("--draft", required=True, type=Path, help="Path to blog post draft")
    parser.add_argument("--doc-type", required=True, help="Sensible document type name")
    parser.add_argument("--pdf", required=True, type=Path, help="Path to golden PDF")
    parser.add_argument("--config-name", help="Config name (defaults to doc-type)")
    args = parser.parse_args()

    config_name = args.config_name or args.doc_type

    if not args.draft.exists():
        print(f"Error: draft not found: {args.draft}", file=sys.stderr)
        sys.exit(1)
    if not args.pdf.exists():
        print(f"Error: PDF not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    print(f"Draft         : {args.draft}")
    print(f"Document type : {args.doc_type}")
    print(f"Config name   : {config_name}")
    print(f"PDF           : {args.pdf}")
    print()

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        config_path = Path(tmp.name)

    try:
        extract_config(args.draft, config_path)
        print(f"Extracted config from draft ({config_path.stat().st_size} bytes)")

        doc_type_id = get_or_create_doc_type(args.doc_type)
        publish_config(doc_type_id, config_name, config_path)
        upload_golden(doc_type_id, args.pdf, config_name)

        print()
        print("Running extraction...")
        response = extract_document(args.doc_type, config_name, args.pdf)
        api_output = response.get("parsed_document", response)
    finally:
        config_path.unlink(missing_ok=True)

    print("Extracting expected output from draft...")
    draft_output = extract_output_block(args.draft)

    mismatches = diff_outputs(draft_output, api_output)

    print()
    total = len(draft_output)
    if not mismatches:
        print(f"OK  all {total} top-level field(s) match")
        sys.exit(0)
    else:
        print(f"FAIL  {len(mismatches)} mismatch(es) across {total} top-level field(s):")
        for m in mismatches:
            print(m)
        sys.exit(1)


if __name__ == "__main__":
    main()
