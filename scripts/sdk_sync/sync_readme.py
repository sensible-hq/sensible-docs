#!/usr/bin/env python3
"""Sync a sensible-docs SDK guide to a GitHub SDK repo's README.

Usage:
    sync_readme.py <owner/repo> <source_doc_path>

The README in the SDK repo is split by a marker comment:

    <!-- SENSIBLE-DOCS-SYNC-START -->

Everything before (and including) that line is the "intro" — language-specific
content that lives in the SDK repo. Everything after is replaced by the content
of the sensible-docs source file (YAML frontmatter stripped).

One-time setup: add the marker to each SDK repo's README before running this.

Always exits 0. Sets GITHUB_OUTPUT: pr_opened=true/false, pr_url=<url>.
The calling workflow owns the failure step.
"""

import base64
import json
import os
import re
import subprocess
import sys
import tempfile

SYNC_MARKER = "<!-- SENSIBLE-DOCS-SYNC-START -->"
SYNC_BRANCH = "auto/sync-readme-from-sensible-docs"
SYNC_TITLE = "Sync README from sensible-docs"
GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT", "")


def set_output(name, value):
    if GITHUB_OUTPUT:
        with open(GITHUB_OUTPUT, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"OUTPUT {name}={value}")


def run(cmd, check=True):
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def gh_json(path, method=None, input_data=None):
    cmd = ["gh", "api", path]
    if method:
        cmd += ["--method", method]
    if input_data is not None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(input_data, f)
            fname = f.name
        cmd += ["--input", fname]
        try:
            result = run(cmd)
        finally:
            os.unlink(fname)
    else:
        result = run(cmd)
    return json.loads(result.stdout)


def get_readme(repo, ref=None):
    path = f"repos/{repo}/contents/README.md"
    if ref:
        path += f"?ref={ref}"
    data = gh_json(path)
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data["sha"]


def strip_frontmatter(content):
    if content.startswith("---"):
        m = re.match(r"^---\n.*?\n---\n?", content, re.DOTALL)
        if m:
            return content[m.end():].lstrip("\n")
    return content


def split_readme(readme):
    """Return (intro, body) split on the sync marker line (inclusive in intro)."""
    marker_line = SYNC_MARKER + "\n"
    idx = readme.find(marker_line)
    if idx == -1:
        sys.exit(
            f"ERROR: sync marker not found in README.\n"
            f"Add this line to the README just before the synced section:\n\n"
            f"  {SYNC_MARKER}\n"
        )
    split = idx + len(marker_line)
    return readme[:split], readme[split:]


def get_default_branch(repo):
    return gh_json(f"repos/{repo}")["default_branch"]


def branch_exists(repo, branch):
    return run(["gh", "api", f"repos/{repo}/git/refs/heads/{branch}"], check=False).returncode == 0


def create_branch(repo, branch, from_sha):
    gh_json(
        f"repos/{repo}/git/refs",
        method="POST",
        input_data={"ref": f"refs/heads/{branch}", "sha": from_sha},
    )


def get_branch_head_sha(repo, branch):
    return gh_json(f"repos/{repo}/git/refs/heads/{branch}")["object"]["sha"]


def update_readme_on_branch(repo, branch, content, file_sha, message):
    gh_json(
        f"repos/{repo}/contents/README.md",
        method="PUT",
        input_data={
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "sha": file_sha,
            "branch": branch,
        },
    )


def find_open_pr(repo):
    result = run([
        "gh", "pr", "list",
        "--repo", repo,
        "--state", "open",
        "--head", SYNC_BRANCH,
        "--json", "number,url",
        "--jq", ".[0] // empty",
    ])
    s = result.stdout.strip()
    return json.loads(s) if s else None


def create_pr(repo, default_branch):
    result = run([
        "gh", "pr", "create",
        "--repo", repo,
        "--title", SYNC_TITLE,
        "--body", (
            "Auto-generated: syncs the README body from the "
            "[sensible-docs](https://github.com/sensible-hq/sensible-docs) "
            "repository, which is the source of truth for SDK guide content.\n\n"
            "Merge to apply the latest documentation update."
        ),
        "--head", SYNC_BRANCH,
        "--base", default_branch,
    ])
    return result.stdout.strip()


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: sync_readme.py <owner/repo> <source_doc_path>")

    repo, source_path = sys.argv[1], sys.argv[2]

    with open(source_path) as f:
        body = strip_frontmatter(f.read())

    current_readme, _ = get_readme(repo)
    intro, _ = split_readme(current_readme)
    expected_readme = intro + body

    if current_readme.rstrip("\n") == expected_readme.rstrip("\n"):
        print(f"✓ {repo} README is up to date")
        set_output("pr_opened", "false")
        set_output("pr_url", "")
        return

    print(f"→ {repo} README needs updating")
    default_branch = get_default_branch(repo)
    existing_pr = find_open_pr(repo)

    if existing_pr:
        _, branch_file_sha = get_readme(repo, ref=SYNC_BRANCH)
        update_readme_on_branch(repo, SYNC_BRANCH, expected_readme, branch_file_sha, SYNC_TITLE)
        pr_url = existing_pr["url"]
        print(f"→ Updated existing PR #{existing_pr['number']}: {pr_url}")
    else:
        if branch_exists(repo, SYNC_BRANCH):
            _, branch_file_sha = get_readme(repo, ref=SYNC_BRANCH)
        else:
            head_sha = get_branch_head_sha(repo, default_branch)
            create_branch(repo, SYNC_BRANCH, head_sha)
            _, branch_file_sha = get_readme(repo, ref=SYNC_BRANCH)

        update_readme_on_branch(repo, SYNC_BRANCH, expected_readme, branch_file_sha, SYNC_TITLE)
        pr_url = create_pr(repo, default_branch)
        print(f"→ Created PR: {pr_url}")

    set_output("pr_opened", "true")
    set_output("pr_url", pr_url)


if __name__ == "__main__":
    main()
