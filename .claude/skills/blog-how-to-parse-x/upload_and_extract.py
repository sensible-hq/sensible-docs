#!/usr/bin/env python3
"""
Upload a Sensible config and golden PDF, then run a live extraction.

Combines upload_pr_extractor.py with a live extraction against the golden PDF
so Step 4 of the blog-how-to-parse-x skill is a single command.

Usage:
    python .claude/skills/blog-how-to-parse-x/upload_and_extract.py \
        --doc-type <name> \
        --config <path/to/config.json> \
        --pdf <path/to/golden.pdf> \
        [--config-name <name>] \
        [--output <path/to/output.json>]

Environment:
    SENSIBLE_API_KEY: Sensible API key (required)

Tests: .claude/skills/blog-how-to-parse-x/tests/test_upload_and_extract.py
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

# scripts/ sits at the repo root, four levels above this file's directory
_SCRIPTS = Path(__file__).parent.parent.parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS))

from upload_pr_extractor import (
    API_BASE,
    get_api_key,
    get_or_create_doc_type,
    publish_config,
    upload_golden,
)


def extract_document(doc_type: str, config_name: str, pdf_path: Path) -> dict:
    """POST a PDF to the Sensible extract endpoint and return the full response."""
    url = f"{API_BASE}/extract/{doc_type}?configuration_name={config_name}"
    pdf_data = pdf_path.read_bytes()
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/pdf",
    }
    req = urllib.request.Request(url, data=pdf_data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"  HTTP {e.code} POST {url}: {error_body}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload a Sensible config + golden PDF, then run a live extraction."
    )
    parser.add_argument("--doc-type", required=True, help="Document type name (created if not exists)")
    parser.add_argument("--config", required=True, type=Path, help="Path to config JSON file")
    parser.add_argument("--pdf", required=True, type=Path, help="Path to golden PDF file")
    parser.add_argument(
        "--config-name",
        help="Configuration name (defaults to config filename stem)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Save parsed_document to this file (defaults to stdout)",
    )
    args = parser.parse_args()

    config_name = args.config_name or args.config.stem

    if not args.config.exists():
        print(f"Error: config file not found: {args.config}", file=sys.stderr)
        sys.exit(1)
    if not args.pdf.exists():
        print(f"Error: PDF not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    print(f"Document type : {args.doc_type}")
    print(f"Config        : {args.config} (name: '{config_name}')")
    print(f"PDF           : {args.pdf}")
    print()

    doc_type_id = get_or_create_doc_type(args.doc_type)
    publish_config(doc_type_id, config_name, args.config)
    upload_golden(doc_type_id, args.pdf, config_name)

    print()
    print("Running extraction...")
    response = extract_document(args.doc_type, config_name, args.pdf)
    parsed_document = response.get("parsed_document", response)

    if args.output:
        args.output.write_text(json.dumps(parsed_document, indent=2), encoding="utf-8")
        print(f"  Saved parsed_document → {args.output}")
    else:
        print(json.dumps(parsed_document, indent=2))

    print()
    print(
        f"View in Sensible app: "
        f"https://app.sensible.so/editor/?d={args.doc_type}&c={config_name}&g={args.pdf.stem}"
    )


if __name__ == "__main__":
    main()
