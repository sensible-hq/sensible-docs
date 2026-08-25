#!/usr/bin/env python3
"""Check that sensible-docs SDK guides match the SDK repo READMEs.

Checks both SDK repos. If any README is out of sync, opens or updates
a GitHub Issue in sensible-docs with copy-paste instructions and edit
links, then exits 1. Exits 0 if everything is in sync.

Requires GH_TOKEN with issues: write on this repo
(the default GITHUB_TOKEN in GitHub Actions is sufficient).
"""

import difflib
import json
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import date

SYNC_MARKER = "<!-- SENSIBLE-DOCS-SYNC-START -->"
ISSUE_TITLE = "SDK READMEs need updating"

SDKS = [
    {
        "name": "sensible-api-py",
        "readme_url": "https://raw.githubusercontent.com/sensible-hq/sensible-api-py/main/README.md",
        "source_path": "docs/integrations/sdk-guides/python-sdk-quickstart.md",
        "edit_url": "https://github.com/sensible-hq/sensible-api-py/edit/main/README.md",
    },
    {
        "name": "sensible-api-js",
        "readme_url": "https://raw.githubusercontent.com/sensible-hq/sensible-api-js/main/README.md",
        "source_path": "docs/integrations/sdk-guides/node-sdk-quickstart.md",
        "edit_url": "https://github.com/sensible-hq/sensible-api-js/edit/main/README.md",
    },
]


def fetch(url):
    try:
        with urllib.request.urlopen(url) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: could not fetch {url}: {e}")


def normalize(text):
    lines = []
    for line in text.splitlines():
        line = line.rstrip()
        if line.startswith("|") and line.endswith("|"):
            cells = line.split("|")
            normalized = []
            for c in cells[1:-1]:
                c = c.strip()
                if re.match(r"^-+$", c):
                    c = "---"
                normalized.append(c)
            line = "| " + " | ".join(normalized) + " |"
        lines.append(line)
    return "\n".join(lines)


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


def run(cmd, check=True):
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def find_open_issue():
    result = run([
        "gh", "issue", "list",
        "--state", "open",
        "--search", ISSUE_TITLE,
        "--json", "number,url",
        "--jq", ".[0] // empty",
    ])
    s = result.stdout.strip()
    return json.loads(s) if s else None


def make_diff(readme_body, source_body, sdk_name, source_path):
    diff = difflib.unified_diff(
        readme_body.splitlines(keepends=True),
        source_body.splitlines(keepends=True),
        fromfile=f"{sdk_name}/README.md (current)",
        tofile=f"{source_path} (sensible-docs)",
        n=2,
    )
    return "".join(diff)


def build_issue_body(drifted_sdks):
    lines = [f"Checked: {date.today()}\n"]

    for sdk in drifted_sdks:
        with open(sdk["source_path"]) as f:
            source_body = strip_frontmatter(f.read())
        readme_body = sdk["readme_body"]

        diff = make_diff(readme_body, source_body, sdk["name"], sdk["source_path"])
        source_raw_url = (
            "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/"
            + sdk["source_path"]
        )
        lines += [
            f"\n## {sdk['name']}\n",
            f"\n[Edit README]({sdk['edit_url']})\n",
            f"\nReplace everything after `{SYNC_MARKER}` with the contents of: {source_raw_url}\n",
            f"\n````diff\n{diff}````\n",
        ]
    lines.append("\nClose this issue after updating the SDK READMEs.\n")
    return "".join(lines)


def open_or_update_issue(drifted_sdks):
    body = build_issue_body(drifted_sdks)
    existing = find_open_issue()

    if existing:
        run([
            "gh", "issue", "edit", str(existing["number"]),
            "--title", ISSUE_TITLE,
            "--body", body,
        ])
        url = existing["url"]
        print(f"→ Updated existing issue: {url}")
    else:
        result = run([
            "gh", "issue", "create",
            "--title", ISSUE_TITLE,
            "--body", body,
        ])
        url = result.stdout.strip()
        print(f"→ Created issue: {url}")

    return url


def main():
    drifted = []

    for sdk in SDKS:
        readme = fetch(sdk["readme_url"])
        readme_body = split_on_marker(readme, sdk["readme_url"])

        with open(sdk["source_path"]) as f:
            source_body = strip_frontmatter(f.read())

        if normalize(readme_body) == normalize(source_body):
            print(f"✓ {sdk['name']} README is up to date")
        else:
            print(f"✗ {sdk['name']} README is out of sync")
            drifted.append({**sdk, "readme_body": readme_body})

    if not drifted:
        return

    url = open_or_update_issue(drifted)
    print(f"\n::error::SDK READMEs are out of sync. See issue for copy-paste instructions: {url}")
    sys.exit(1)


if __name__ == "__main__":
    main()
