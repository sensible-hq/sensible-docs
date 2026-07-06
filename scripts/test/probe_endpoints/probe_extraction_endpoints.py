#!/usr/bin/env python3
"""
probe_extraction_endpoints.py — Snapshot tests for all extraction API endpoints.

Usage:
  python3 probe_extraction_endpoints.py           # compare responses against snapshots
  python3 probe_extraction_endpoints.py --update  # run all endpoints and refresh snapshots

Requires: SENSIBLE_API_KEY env var.

Each run saves raw responses to outputs/<timestamp>_extraction/.
Snapshots in snapshots/ are normalized — volatile fields (IDs, timestamps,
pre-signed URLs) are replaced with "<omitted>" so diffs only show structural changes.
Diffs are saved to the same run directory as diff.txt.

Async endpoints produce two snapshots each: _initial (the immediate POST response)
and _retrieve (the GET /documents/{id} result after polling to COMPLETE or FAILED).
"""

import json
import os
import sys
import time
import difflib
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.error

# ── Config ────────────────────────────────────────────────────────────────────

API_BASE = "https://api.sensible.so/v0"
ASSET_BASE = "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs"

SINGLE_DOC_TYPE = "w2s"
SINGLE_DOC_URL = f"{ASSET_BASE}/postprocessor.pdf"

PORTFOLIO_TYPES = ["bank_statements", "pay_stubs", "1040s"]
PORTFOLIO_DOC_URL = f"{ASSET_BASE}/portfolio_bank_paystub_tax.pdf"

POLL_INTERVAL = 5    # seconds between status checks
POLL_TIMEOUT  = 180  # give up after this many seconds

REPO_ROOT    = Path(__file__).parent.parent.parent.parent  # sensible-docs-actor/
SCRIPT_DIR   = Path(__file__).parent                        # probe_endpoints/
SNAPSHOT_DIR = SCRIPT_DIR / "snapshots"
OUTPUT_DIR   = SCRIPT_DIR / "outputs"

SINGLE_DOC_LOCAL    = REPO_ROOT / "assets/pdfs/postprocessor.pdf"
PORTFOLIO_DOC_LOCAL = REPO_ROOT / "assets/pdfs/portfolio_bank_paystub_tax.pdf"

# Keys whose values are replaced with "<omitted>" before saving or diffing.
VOLATILE_KEYS = {
    "id", "created", "completed", "upload_url", "download_url",
    "version_id", "charged", "taskId", "batchId", "batch_id",
    "cutoff_date", "continuation_token", "last_evaluated_creation_date",
}

# ── HTTP helpers ──────────────────────────────────────────────────────────────

API_KEY: str = ""


def _request(method: str, url: str, body=None, content_type="application/json", auth=True):
    headers: dict = {}
    if auth:
        headers["Authorization"] = f"Bearer {API_KEY}"

    data = None
    if body is not None:
        if isinstance(body, bytes):
            data = body
            headers["Content-Type"] = content_type
        else:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else {})


def api(method: str, path: str, body=None, content_type="application/json"):
    return _request(method, f"{API_BASE}{path}", body, content_type)


def put_to_s3(upload_url: str, file_bytes: bytes):
    """PUT document bytes to a pre-signed S3 URL — no Authorization header."""
    return _request("PUT", upload_url, body=file_bytes, content_type="application/pdf", auth=False)


# ── Polling ───────────────────────────────────────────────────────────────────

def poll_until_done(extraction_id: str) -> dict:
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        _, body = api("GET", f"/documents/{extraction_id}")
        status = body.get("status")
        if status in ("COMPLETE", "FAILED"):
            return body
        print(f"    polling {extraction_id[:8]}…  status={status}")
        time.sleep(POLL_INTERVAL)
    raise TimeoutError(f"{extraction_id} did not finish within {POLL_TIMEOUT}s")


# ── Normalize & snapshot ──────────────────────────────────────────────────────

def normalize(obj):
    """Recursively replace volatile field values with '<omitted>'."""
    if isinstance(obj, dict):
        return {k: ("<omitted>" if k in VOLATILE_KEYS else normalize(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(item) for item in obj]
    return obj


RUN_DIR: Path = Path()   # set once in main(); all raw outputs for this run go here
_diff_lines: list = []   # accumulates diffs across all compare calls


def save_raw(name: str, data: dict):
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    (RUN_DIR / f"{name}.json").write_text(json.dumps(data, indent=2))


def save_snapshot(name: str, data: dict):
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{name}.json"
    path.write_text(json.dumps(normalize(data), indent=2))
    print(f"  saved  {name}.json")


def compare_snapshot(name: str, data: dict):
    path = SNAPSHOT_DIR / f"{name}.json"
    new_text = json.dumps(normalize(data), indent=2)

    if not path.exists():
        print(f"  {name}: NO SNAPSHOT — run --update to create one")
        return

    old_text = path.read_text()
    if old_text.strip() == new_text.strip():
        print(f"  {name}: OK")
        return

    print(f"  {name}: CHANGED")
    diff = list(difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=f"{name}.json (snapshot)",
        tofile=f"{name}.json (current)",
        n=3,
    ))
    sys.stdout.writelines(diff)
    _diff_lines.append(f"\n### {name}\n")
    _diff_lines.extend(diff)


def write_diff_summary():
    if not _diff_lines:
        return
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    path = RUN_DIR / "diff.txt"
    path.write_text("".join(_diff_lines))
    print(f"\n  diff saved to: {path.relative_to(REPO_ROOT)}")


# ── Endpoint runners ──────────────────────────────────────────────────────────

def run_extract_sync():
    """POST /extract/{document_type}  — synchronous single-doc extraction."""
    print("\n[1/6] POST /extract/{document_type}  (sync)")
    doc_bytes = SINGLE_DOC_LOCAL.read_bytes()
    http, body = api("POST", f"/extract/{SINGLE_DOC_TYPE}?environment=development",
                     body=doc_bytes, content_type="application/pdf")
    print(f"    HTTP {http}")
    save_raw("extract_sync", body)
    return {"extract_sync": body}


def run_generate_upload_url():
    """POST /generate_upload_url/{document_type}  — async upload flow."""
    print("\n[2/6] POST /generate_upload_url/{document_type}  (async — upload)")
    http, initial = api("POST", f"/generate_upload_url/{SINGLE_DOC_TYPE}",
                        body={"content_type": "application/pdf"})
    print(f"    HTTP {http}")
    save_raw("generate_upload_url_initial", initial)

    put_http, _ = put_to_s3(initial["upload_url"], SINGLE_DOC_LOCAL.read_bytes())
    print(f"    PUT to S3: HTTP {put_http}")

    retrieve = poll_until_done(initial["id"])
    save_raw("generate_upload_url_retrieve", retrieve)

    return {
        "generate_upload_url_initial": initial,
        "generate_upload_url_retrieve": retrieve,
    }


def run_extract_from_url():
    """POST /extract_from_url/{document_type}  — async extract-from-URL flow."""
    print("\n[3/6] POST /extract_from_url/{document_type}  (async — from URL)")
    http, initial = api("POST", f"/extract_from_url/{SINGLE_DOC_TYPE}",
                        body={"document_url": SINGLE_DOC_URL, "content_type": "application/pdf"})
    print(f"    HTTP {http}")
    save_raw("extract_from_url_initial", initial)

    retrieve = poll_until_done(initial["id"])
    save_raw("extract_from_url_retrieve", retrieve)

    return {
        "extract_from_url_initial": initial,
        "extract_from_url_retrieve": retrieve,
    }


def run_generate_upload_url_portfolio():
    """POST /generate_upload_url  — async portfolio upload flow."""
    print("\n[4/6] POST /generate_upload_url  (async portfolio — upload)")
    http, initial = api("POST", "/generate_upload_url",
                        body={"types": PORTFOLIO_TYPES, "content_type": "application/pdf"})
    print(f"    HTTP {http}")
    save_raw("generate_upload_url_portfolio_initial", initial)

    put_http, _ = put_to_s3(initial["upload_url"], PORTFOLIO_DOC_LOCAL.read_bytes())
    print(f"    PUT to S3: HTTP {put_http}")

    retrieve = poll_until_done(initial["id"])
    save_raw("generate_upload_url_portfolio_retrieve", retrieve)

    return {
        "generate_upload_url_portfolio_initial": initial,
        "generate_upload_url_portfolio_retrieve": retrieve,
    }


def run_extract_from_url_portfolio():
    """POST /extract_from_url  — async portfolio extract-from-URL flow."""
    print("\n[5/6] POST /extract_from_url  (async portfolio — from URL)")
    http, initial = api("POST", "/extract_from_url",
                        body={
                            "document_url": PORTFOLIO_DOC_URL,
                            "types": PORTFOLIO_TYPES,
                            "content_type": "application/pdf",
                            "segment_documents_with": "llm",
                        })
    print(f"    HTTP {http}")
    save_raw("extract_from_url_portfolio_initial", initial)

    retrieve = poll_until_done(initial["id"])
    save_raw("extract_from_url_portfolio_retrieve", retrieve)

    return {
        "extract_from_url_portfolio_initial": initial,
        "extract_from_url_portfolio_retrieve": retrieve,
    }


def run_list_extractions():
    """GET /extractions  — list recent extractions (first page, limit 5)."""
    print("\n[6/6] GET /extractions  (list, limit=5)")
    http, body = api("GET", "/extractions?limit=5")
    print(f"    HTTP {http}")
    save_raw("list_extractions", body)
    return {"list_extractions": body}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    global API_KEY, RUN_DIR
    API_KEY = os.environ.get("SENSIBLE_API_KEY", "")
    if not API_KEY:
        sys.exit("Error: SENSIBLE_API_KEY environment variable not set.")

    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    RUN_DIR = OUTPUT_DIR / f"{run_ts}_extraction"

    update_mode = "--update" in sys.argv
    action = save_snapshot if update_mode else compare_snapshot
    label = "UPDATE" if update_mode else "COMPARE"
    print(f"=== probe_extraction_endpoints.py  mode={label} ===")
    print(f"    run dir: {RUN_DIR.relative_to(REPO_ROOT)}")

    results: dict = {}
    results.update(run_extract_sync())
    results.update(run_generate_upload_url())
    results.update(run_extract_from_url())
    results.update(run_generate_upload_url_portfolio())
    results.update(run_extract_from_url_portfolio())
    results.update(run_list_extractions())

    print(f"\n=== {label} results ===")
    for name, data in results.items():
        action(name, data)

    if not update_mode:
        write_diff_summary()


if __name__ == "__main__":
    main()
