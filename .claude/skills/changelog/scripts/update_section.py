#!/usr/bin/env python3
"""
Replaces a single section in a readme.io changelog draft without touching the rest.

Usage:
    echo "$NEW_SECTION_BODY" | python update_section.py <slug> <heading>

    <slug>    — changelog slug, e.g. "july-2026"
    <heading> — full heading line to match, e.g. "## Improvement: Advanced configurability for the Region method"
                Can be a unique prefix — the script matches the first heading that starts with this string.

The new section content is read from stdin. It should include the heading line itself.

Example:
    cat << 'EOF' | python update_section.py july-2026 "## Improvement: Advanced configurability"
    ## Improvement: Advanced configurability for the Region method

    For the [Region](doc:region) method, you can now relax the criteria ...
    EOF

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


HEADERS = {"User-Agent": "sensible-changelog/1.0"}


def make_auth(api_key):
    return base64.b64encode(f"{api_key}:".encode()).decode()


def fetch_changelog(slug, auth):
    req = urllib.request.Request(
        f"https://dash.readme.com/api/v1/changelogs/{slug}",
        headers={**HEADERS, "Authorization": f"Basic {auth}"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code} fetching '{slug}': {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def find_section_bounds(body, heading_prefix):
    """
    Returns (start, end) character indices for the section whose heading line
    starts with heading_prefix. end points to the start of the next ## heading
    (or end of string). Returns (None, None) if not found.
    """
    lines = body.splitlines(keepends=True)
    section_start = None
    char_pos = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if section_start is None:
            if stripped.startswith(heading_prefix):
                section_start = char_pos
        else:
            # Next ## heading ends the section
            if re.match(r'^#{1,6}\s', stripped) and not stripped.startswith(heading_prefix):
                return section_start, char_pos
        char_pos += len(line)

    if section_start is not None:
        return section_start, char_pos  # section runs to end of body

    return None, None


def put_changelog(slug, title, body, auth):
    payload = json.dumps({"title": title, "slug": slug, "body": body, "hidden": True}).encode()
    req = urllib.request.Request(
        f"https://dash.readme.com/api/v1/changelogs/{slug}",
        data=payload,
        headers={**HEADERS, "Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            updated_slug = result.get("slug", slug)
            print(f"Updated (hidden draft): https://docs.sensible.so/update/changelog/{updated_slug}")
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: echo \"$NEW_SECTION\" | python update_section.py <slug> <heading-prefix>", file=sys.stderr)
        sys.exit(1)

    slug = sys.argv[1]
    heading_prefix = sys.argv[2]
    new_section = sys.stdin.read().rstrip("\n")

    if not new_section:
        print("ERROR: new section content is empty (nothing on stdin)", file=sys.stderr)
        sys.exit(1)

    auth = make_auth(get_api_key())
    data = fetch_changelog(slug, auth)
    body = data.get("body", "")
    title = data.get("title", slug)

    start, end = find_section_bounds(body, heading_prefix)

    if start is None:
        print(f"ERROR: no section found matching heading prefix: {heading_prefix!r}", file=sys.stderr)
        print("Headings in this changelog:", file=sys.stderr)
        for line in body.splitlines():
            if re.match(r'^#{1,6}\s', line):
                print(f"  {line}", file=sys.stderr)
        sys.exit(1)

    old_section = body[start:end].rstrip("\n")
    print(f"Replacing:\n  {old_section.splitlines()[0]}")
    print(f"With:\n  {new_section.splitlines()[0]}")

    # Preserve trailing whitespace/newlines of the replaced region
    new_body = body[:start] + new_section + "\n\n" + body[end:].lstrip("\n")
    put_changelog(slug, title, new_body, auth)


if __name__ == "__main__":
    main()
