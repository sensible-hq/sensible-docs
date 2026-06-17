#!/usr/bin/env python3
"""
Downloads all published changelogs from readme.com and saves them locally.

Usage:
    python download_changelogs.py

Saves each changelog as:
    references/changelogs/<slug>.md

with a frontmatter header containing title and date, so files are
self-describing and easy to grep.

Run this script whenever you want to refresh the local cache.
Requires README_API_KEY env var (sources ~/.bashrc if not set).
"""

import sys
import os
import re
import base64
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR.parent / "references" / "changelogs"
HEADERS = {"User-Agent": "sensible-changelog/1.0"}


def get_api_key():
    key = os.environ.get("README_API_KEY")
    if key:
        return key
    result = subprocess.run(
        ["bash", "-c", "source ~/.bashrc 2>/dev/null && echo $README_API_KEY"],
        capture_output=True, text=True
    )
    key = result.stdout.strip()
    if not key:
        print("ERROR: README_API_KEY not set.", file=sys.stderr)
        sys.exit(1)
    return key


def make_auth(api_key):
    return base64.b64encode(f"{api_key}:".encode()).decode()


def fetch_json(url, auth):
    req = urllib.request.Request(
        url,
        headers={**HEADERS, "Authorization": f"Basic {auth}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def fetch_all_changelogs(auth):
    entries = []
    page = 1
    while True:
        batch = fetch_json(
            f"https://dash.readme.com/api/v1/changelogs?perPage=100&page={page}",
            auth
        )
        if not batch:
            break
        entries.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return entries


def main():
    api_key = get_api_key()
    auth = make_auth(api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Fetching changelog list...")
    entries = fetch_all_changelogs(auth)
    print(f"Found {len(entries)} changelogs")

    saved = 0
    skipped = 0
    for entry in entries:
        slug = entry["slug"]
        title = entry["title"]
        hidden = entry.get("hidden", False)
        created_at = entry.get("createdAt", "")[:10]  # YYYY-MM-DD

        # Skip hidden drafts — only save published changelogs as reference
        if hidden:
            skipped += 1
            continue

        # Fetch full body
        try:
            detail = fetch_json(
                f"https://dash.readme.com/api/v1/changelogs/{slug}",
                auth
            )
        except urllib.error.HTTPError as e:
            print(f"  ERROR fetching {slug}: {e.code}", file=sys.stderr)
            continue

        body = detail.get("body", "").strip()
        if not body:
            skipped += 1
            continue

        # Write with frontmatter so files are self-describing
        content = f"---\ntitle: {title}\nslug: {slug}\ndate: {created_at}\n---\n\n{body}\n"
        out_path = OUTPUT_DIR / f"{slug}.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"  Saved: {slug}.md ({title})")
        saved += 1

    print(f"\nDone. {saved} saved, {skipped} skipped (hidden or empty).")


if __name__ == "__main__":
    main()
