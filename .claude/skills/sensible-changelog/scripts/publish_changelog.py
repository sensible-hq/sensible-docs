#!/usr/bin/env python3
"""
Publishes a changelog to readme.com as a hidden draft.

Usage:
    echo "$BODY" | python publish_changelog.py "March 2026"

Reads the changelog body from stdin, title from argv[1].
Requires README_API_KEY env var (sources ~/.bashrc if not set).

Prints the draft URL on success, full error response on failure.
"""

import sys
import os
import base64
import json
import subprocess
import urllib.request
import urllib.error


def get_api_key():
    key = os.environ.get("README_API_KEY")
    if key:
        return key
    # Try sourcing ~/.bashrc
    result = subprocess.run(
        ["bash", "-c", "source ~/.bashrc 2>/dev/null && echo $README_API_KEY"],
        capture_output=True, text=True
    )
    key = result.stdout.strip()
    if not key:
        print("ERROR: README_API_KEY not set. Set it in ~/.bashrc and re-run.", file=sys.stderr)
        sys.exit(1)
    return key


def main():
    if len(sys.argv) < 2:
        print("Usage: echo \"$BODY\" | python publish_changelog.py \"March 2026\"", file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1]
    body = sys.stdin.read().strip()

    if not body:
        print("ERROR: changelog body is empty (nothing on stdin)", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    auth = base64.b64encode(f"{api_key}:".encode()).decode()

    payload = json.dumps({
        "title": title,
        "body": body,
        "hidden": True
    }).encode()

    req = urllib.request.Request(
        "https://dash.readme.com/api/v1/changelogs",
        data=payload,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            slug = result.get("slug", "")
            print(f"Published (hidden draft): https://dash.readme.com/project/sensible/v2.0/changelog/{slug}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"ERROR {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
