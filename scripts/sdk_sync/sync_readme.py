#!/usr/bin/env python3
"""Check that a sensible-docs SDK guide matches the corresponding GitHub README.

Usage:
    sync_readme.py <raw-readme-url> <source_doc_path>

The README is split by a marker comment:

    <!-- SENSIBLE-DOCS-SYNC-START -->

Everything after that line must match the source doc (YAML frontmatter stripped).
Exits 1 with a diff if they are out of sync, 0 if they match.

One-time setup: add the marker to each SDK repo's README just before the synced
section. No authentication required — the README URL must be publicly accessible.
"""

import sys
import re
import urllib.request
import urllib.error

SYNC_MARKER = "<!-- SENSIBLE-DOCS-SYNC-START -->"


def fetch(url):
    try:
        with urllib.request.urlopen(url) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: could not fetch {url}: {e}")


def strip_frontmatter(content):
    if content.startswith("---"):
        m = re.match(r"^---\n.*?\n---\n?", content, re.DOTALL)
        if m:
            return content[m.end():].lstrip("\n")
    return content


def split_on_marker(text, source):
    marker_line = SYNC_MARKER + "\n"
    idx = text.find(marker_line)
    if idx == -1:
        sys.exit(
            f"ERROR: sync marker not found in {source}.\n"
            f"Add this line just before the synced section:\n\n"
            f"  {SYNC_MARKER}\n"
        )
    return text[idx + len(marker_line):]


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: sync_readme.py <raw-readme-url> <source_doc_path>")

    readme_url, source_path = sys.argv[1], sys.argv[2]

    readme = fetch(readme_url)
    readme_body = split_on_marker(readme, readme_url)

    with open(source_path) as f:
        source_body = strip_frontmatter(f.read())

    if readme_body.rstrip("\n") == source_body.rstrip("\n"):
        print(f"✓ {source_path} matches {readme_url}")
        return

    # Derive a human-readable repo URL from the raw URL
    # https://raw.githubusercontent.com/org/repo/branch/README.md
    #   -> https://github.com/org/repo
    parts = readme_url.replace("https://raw.githubusercontent.com/", "").split("/")
    repo_url = f"https://github.com/{parts[0]}/{parts[1]}" if len(parts) >= 2 else readme_url

    readme_lines = readme_body.splitlines()
    source_lines = source_body.splitlines()

    print(f"✗ Out of sync: {source_path}")
    print()
    print("To fix:")
    print(f"  1. Open {repo_url}/edit/main/README.md")
    print(f"  2. Replace everything after '{SYNC_MARKER}'")
    print(f"     with the content of {source_path} (minus its YAML frontmatter)")
    print(f"  3. Open a PR in that repo and merge it")
    print()
    print(f"  README body after marker: {len(readme_lines)} lines")
    print(f"  sensible-docs source:     {len(source_lines)} lines")

    sys.exit(1)


if __name__ == "__main__":
    main()
