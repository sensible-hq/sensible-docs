#!/usr/bin/env python3
"""Check that sensible-docs SDK guides match the SDK repo READMEs.

Checks both SDK repos. If any README is out of sync, opens or updates
a PR in sensible-docs with copy-paste instructions for fixing them,
then exits 1. Exits 0 if everything is in sync.

Requires GH_TOKEN with contents: write and pull-requests: write on
this repo (the default GITHUB_TOKEN in GitHub Actions is sufficient).
"""

import json
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import date

SYNC_MARKER = "<!-- SENSIBLE-DOCS-SYNC-START -->"
PR_BRANCH = "auto/sdk-readme-sync-needed"
PR_TITLE = "SDK READMEs need updating"
PENDING_FILE = "scripts/sdk_check/sdk-docs-sync-pending.md"

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


def find_open_pr():
    result = run([
        "gh", "pr", "list",
        "--state", "open",
        "--head", PR_BRANCH,
        "--json", "number,url",
        "--jq", ".[0] // empty",
    ])
    s = result.stdout.strip()
    return json.loads(s) if s else None


def build_pending_file(drifted_sdks):
    lines = [
        "# SDK READMEs need updating\n",
        f"\nChecked: {date.today()}\n",
        f"\nFor each SDK below, open the edit link and replace everything after "
        f"`{SYNC_MARKER}` with the content shown.\n",
    ]
    for sdk in drifted_sdks:
        with open(sdk["source_path"]) as f:
            body = strip_frontmatter(f.read()).rstrip("\n")
        lines += [
            f"\n## {sdk['name']}\n",
            f"\nEdit: {sdk['edit_url']}\n",
            f"\nReplace everything after `{SYNC_MARKER}` with:\n",
            "\n````markdown\n",
            body,
            "\n````\n",
        ]
    lines.append("\n---\nMerge or close this PR after updating the SDK READMEs.\n")
    return "".join(lines)


def open_tracking_pr(drifted_sdks):
    pending_content = build_pending_file(drifted_sdks)

    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])

    existing_pr = find_open_pr()

    if existing_pr:
        run(["git", "fetch", "origin", PR_BRANCH])
        run(["git", "checkout", PR_BRANCH])
    else:
        run(["git", "checkout", "-b", PR_BRANCH])

    with open(PENDING_FILE, "w") as f:
        f.write(pending_content)

    run(["git", "add", PENDING_FILE])

    dirty = run(["git", "diff", "--cached", "--quiet"], check=False).returncode != 0
    if dirty:
        run(["git", "commit", "-m", f"Update SDK README sync instructions ({date.today()})"])

    run(["git", "push", "origin", PR_BRANCH, "--force"])

    if existing_pr:
        pr_url = existing_pr["url"]
        print(f"→ Updated existing PR: {pr_url}")
    else:
        names = ", ".join(sdk["name"] for sdk in drifted_sdks)
        result = run([
            "gh", "pr", "create",
            "--title", PR_TITLE,
            "--body", (
                f"**{names}** {'are' if len(drifted_sdks) > 1 else 'is'} out of sync "
                f"with the sensible-docs source files.\n\n"
                f"See `{PENDING_FILE}` in this PR for copy-paste content and edit links.\n\n"
                f"After updating the SDK READMEs, merge or close this PR."
            ),
            "--head", PR_BRANCH,
            "--base", "v0",
        ])
        pr_url = result.stdout.strip()
        print(f"→ Created PR: {pr_url}")

    return pr_url


def main():
    drifted = []

    for sdk in SDKS:
        readme = fetch(sdk["readme_url"])
        readme_body = split_on_marker(readme, sdk["readme_url"])

        with open(sdk["source_path"]) as f:
            source_body = strip_frontmatter(f.read())

        if readme_body.rstrip("\n") == source_body.rstrip("\n"):
            print(f"✓ {sdk['name']} README is up to date")
        else:
            print(f"✗ {sdk['name']} README is out of sync")
            drifted.append(sdk)

    if not drifted:
        return

    pr_url = open_tracking_pr(drifted)
    print(f"\n::error::SDK READMEs are out of sync. See PR for copy-paste instructions: {pr_url}")
    sys.exit(1)


if __name__ == "__main__":
    main()
