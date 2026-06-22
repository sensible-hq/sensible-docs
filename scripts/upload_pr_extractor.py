#!/usr/bin/env python3
"""
Upload a Sensible extractor config and golden PDF to a Sensible account.

Creates the document type if it doesn't exist, publishes the config to
production, and uploads the golden PDF as a reference document.

Usage:
    python scripts/upload_pr_extractor.py \\
        --doc-type <name> \\
        --config <path/to/config.json> \\
        --golden <path/to/golden.pdf> \\
        [--config-name <name>]

Environment:
    SENSIBLE_API_KEY: Sensible API key (required)
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = "https://api.sensible.so/v0"


def get_api_key() -> str:
    key = os.environ.get("SENSIBLE_API_KEY")
    if not key:
        print("Error: SENSIBLE_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return key


def api_request(method: str, path: str, body: dict | None = None) -> dict | list | None:
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"  HTTP {e.code} {method} {url}: {error_body}", file=sys.stderr)
        return None


def get_or_create_doc_type(name: str) -> str:
    """Return the UUID of the named document type, creating it if needed."""
    doc_types = api_request("GET", "/document_types") or []
    for dt in doc_types:
        if dt["name"] == name:
            print(f"  Found existing document type '{name}' ({dt['id']})")
            return dt["id"]

    result = api_request("POST", "/document_types", {"name": name, "schema": {}})
    if not result:
        print(f"Error: could not create document type '{name}'", file=sys.stderr)
        sys.exit(1)

    print(f"  Created document type '{name}' ({result['id']})")
    return result["id"]


def publish_config(doc_type_id: str, config_name: str, config_path: Path) -> None:
    """Create or update a configuration, publishing to production."""
    config_text = config_path.read_text(encoding="utf-8")
    # Note: configs may use relaxed JSON (trailing commas, comments) accepted by
    # the Sensible engine, so we skip strict local validation and let the API validate.

    body = {
        "name": config_name,
        "configuration": config_text,
        "publish_as": "production",
    }

    result = api_request("POST", f"/document_types/{doc_type_id}/configurations", body)
    if result:
        print(f"  Created and published configuration '{config_name}'")
        return

    # Config may already exist — try updating via PUT
    result = api_request("PUT", f"/document_types/{doc_type_id}/configurations/{config_name}", body)
    if result:
        print(f"  Updated and published configuration '{config_name}'")
        return

    print(f"Error: could not create or update configuration '{config_name}'", file=sys.stderr)
    sys.exit(1)


def upload_golden(doc_type_id: str, golden_path: Path, config_name: str) -> None:
    """Upload a golden PDF as a reference document associated with a config."""
    # API requires name with only lowercase letters, numbers, and underscores.
    # Replace dots and other disallowed chars with underscores so that
    # e.g. "cells.xlsm" → "cells_xlsm" and "cells.xlsx" → "cells_xlsx".
    import re
    golden_name = re.sub(r"[^a-z0-9_]", "_", golden_path.name.lower())

    body = {"name": golden_name, "configuration": config_name}
    result = api_request("POST", f"/document_types/{doc_type_id}/goldens", body)
    if not result or "upload_url" not in result:
        # Golden may already exist — try regenerating the upload URL via PUT
        result = api_request("PUT", f"/document_types/{doc_type_id}/goldens/{golden_name}", body)
    if not result or "upload_url" not in result:
        # Golden already exists on this document type (uploaded in a prior run for a different
        # config). The existing file is still accessible in the app — skip re-upload.
        print(f"  Note: golden '{golden_name}' already exists — skipping re-upload")
        return

    upload_url = result["upload_url"]
    pdf_data = golden_path.read_bytes()
    req = urllib.request.Request(upload_url, data=pdf_data, method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                print(f"  Uploaded golden '{golden_name}'")
            else:
                print(f"  Warning: upload returned status {resp.status}", file=sys.stderr)
    except urllib.error.HTTPError as e:
        print(f"Error uploading golden: HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload a Sensible extractor config and golden PDF to a Sensible account."
    )
    parser.add_argument("--doc-type", required=True, help="Document type name (created if not exists)")
    parser.add_argument("--config", required=True, type=Path, help="Path to config JSON file")
    parser.add_argument("--golden", required=True, type=Path, help="Path to golden PDF file")
    parser.add_argument(
        "--config-name",
        help="Configuration name (defaults to config filename stem, e.g. 'all' for all.json)",
    )
    args = parser.parse_args()

    config_name = args.config_name or args.config.stem

    if not args.config.exists():
        print(f"Error: config file not found: {args.config}", file=sys.stderr)
        sys.exit(1)
    if not args.golden.exists():
        print(f"Error: golden PDF not found: {args.golden}", file=sys.stderr)
        sys.exit(1)

    print(f"Document type : {args.doc_type}")
    print(f"Config        : {args.config} (name: '{config_name}')")
    print(f"Golden        : {args.golden}")
    print()

    doc_type_id = get_or_create_doc_type(args.doc_type)
    publish_config(doc_type_id, config_name, args.config)
    upload_golden(doc_type_id, args.golden, config_name)

    print()
    print(
        f"Done! View in Sensible app: "
        f"https://app.sensible.so/editor/?d={args.doc_type}&c={config_name}&g={args.golden.stem}"
    )


if __name__ == "__main__":
    main()
