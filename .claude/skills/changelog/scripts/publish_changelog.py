#!/usr/bin/env python3
"""
Publishes or updates a changelog on readme.com as a hidden draft.

Usage:
    echo "$BODY" | python publish_changelog.py "March 2026"           # create new
    echo "$BODY" | python publish_changelog.py "March 2026" --append  # append to existing

Reads the changelog body from stdin, title from argv[1].
Requires README_API_KEY env var (sources ~/.bashrc if not set).

Create mode: automatically avoids slug conflicts — if "march-2026" already exists,
uses "march-2026-2", "march-2026-3", etc.

Append mode: fetches the existing draft by slug, appends stdin content, and PUTs it back.

Prints the draft URL on success, full error response on failure.
"""

import sys
import os
import re
import base64
import json
import subprocess
import urllib.request
import urllib.error


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
        print("ERROR: README_API_KEY not set. Set it in ~/.bashrc and re-run.", file=sys.stderr)
        sys.exit(1)
    return key


HEADERS = {
    "User-Agent": "sensible-changelog/1.0",
}


def make_auth_header(api_key):
    return base64.b64encode(f"{api_key}:".encode()).decode()


def title_to_slug(title):
    """'March 2026' -> 'march-2026'"""
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def fetch_existing_slugs(auth):
    """Fetch all existing changelog slugs (handles pagination)."""
    slugs = set()
    page = 1
    while True:
        req = urllib.request.Request(
            f"https://dash.readme.com/api/v1/changelogs?perPage=100&page={page}",
            headers={**HEADERS, "Authorization": f"Basic {auth}"},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                entries = json.loads(resp.read())
                if not entries:
                    break
                for entry in entries:
                    slugs.add(entry["slug"])
                if len(entries) < 100:
                    break
                page += 1
        except urllib.error.HTTPError as e:
            print(f"ERROR fetching existing changelogs: {e.code} {e.read().decode()}", file=sys.stderr)
            sys.exit(1)
    return slugs


def find_available_slug(base_slug, existing_slugs):
    """Return base_slug if free, otherwise base_slug-2, -3, etc."""
    if base_slug not in existing_slugs:
        return base_slug
    n = 2
    while True:
        candidate = f"{base_slug}-{n}"
        if candidate not in existing_slugs:
            return candidate
        n += 1


def fetch_changelog(slug, auth):
    """Fetch an existing changelog by slug. Returns the parsed JSON or exits on error."""
    req = urllib.request.Request(
        f"https://dash.readme.com/api/v1/changelogs/{slug}",
        headers={**HEADERS, "Authorization": f"Basic {auth}"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"ERROR {e.code} fetching '{slug}': {error_body}", file=sys.stderr)
        sys.exit(1)


def update_changelog(slug, title, body, auth):
    """PUT updated body to an existing changelog slug."""
    payload = json.dumps({
        "title": title,
        "slug": slug,
        "body": body,
        "hidden": True,
    }).encode()
    req = urllib.request.Request(
        f"https://dash.readme.com/api/v1/changelogs/{slug}",
        data=payload,
        headers={**HEADERS, "Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            updated_slug = result.get("slug", slug)
            print(f"Updated (hidden draft): https://docs.sensible.so/update/changelog/{updated_slug}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"ERROR {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: echo \"$BODY\" | python publish_changelog.py \"March 2026\" [--append]", file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1]
    append_mode = "--append" in sys.argv
    new_content = sys.stdin.read().strip()

    if not new_content:
        print("ERROR: changelog body is empty (nothing on stdin)", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    auth = make_auth_header(api_key)
    base_slug = title_to_slug(title)

    update_mode = "--update" in sys.argv

    if append_mode:
        existing = fetch_changelog(base_slug, auth)
        existing_body = existing.get("body", "").rstrip()
        updated_body = existing_body + "\n\n" + new_content
        update_changelog(base_slug, title, updated_body, auth)
        return

    if update_mode:
        update_changelog(base_slug, title, new_content, auth)
        return

    existing_slugs = fetch_existing_slugs(auth)
    slug = find_available_slug(base_slug, existing_slugs)

    if slug != base_slug:
        print(f"Note: '{base_slug}' already exists — using '{slug}' to avoid conflict.")

    payload = json.dumps({
        "title": title,
        "slug": slug,
        "body": new_content,
        "hidden": True,
    }).encode()

    req = urllib.request.Request(
        "https://dash.readme.com/api/v1/changelogs",
        data=payload,
        headers={**HEADERS, "Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            published_slug = result.get("slug", slug)
            print(f"Published (hidden draft): https://docs.sensible.so/update/changelog/{published_slug}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"ERROR {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
