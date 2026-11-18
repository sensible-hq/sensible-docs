#!/usr/bin/env python3
"""PreToolUse guard for test copies of the docs repo: no writes to sensible-hq repos.

While DOCS_REPO (set in .claude/settings.json) names a repo outside the sensible-hq org, this hook denies
Bash commands that would change something in a sensible-hq repo: GitHub API calls with a write method
or fields, gh commands that create, edit, comment on, close, merge, or label PRs and issues there, and
git pushes to a sensible-hq remote. Reads (gh pr view, gh pr diff, GET API calls) pass.
When DOCS_REPO is a sensible-hq repo, the hook does nothing.

It expands $VARIABLES before matching, so `--repo "$ENGINE_REPO"` counts as sensible-hq/sensible. For a
push, it asks git for the URL of the remote being pushed to (in the -C directory when there is one), so
`git -C "$ENGINE_DIR-x" push origin b` is caught even though the command never names the org.
"""
import json
import os
import re
import shlex
import subprocess
import sys

ORG = "sensible-hq/"
GH_WRITE = re.compile(r"\bgh\s+(?:pr|issue|label|release|workflow|run)\s+(?:create|edit|comment|close|reopen|merge|"
                      r"delete|review|ready|lock|unlock|transfer|pin|unpin|develop|rerun|cancel|run)\b")
API = re.compile(r"\bgh\s+api\b")
API_WRITE = re.compile(r"(?:-X|--method)\s*['\"]?(?:POST|PUT|PATCH|DELETE)\b|(?:^|\s)(?:-f|-F|--field|--raw-field|--input)\s", re.I)
API_GET = re.compile(r"(?:-X|--method)\s*['\"]?GET\b", re.I)


def push_target(part: str, cwd: str) -> str | None:
    """The URL a `git [-C dir] push [remote]` would push to, or None if this part isn't a push."""
    try:
        words = shlex.split(part)
    except ValueError:
        return None
    if "git" not in words:
        return None
    i, where = words.index("git") + 1, cwd
    while i + 1 < len(words) and words[i] == "-C":
        where = os.path.join(where, words[i + 1])
        i += 2
    if i >= len(words) or words[i] != "push":
        return None
    args = [w for w in words[i + 1:] if not w.startswith("-")]
    remote = args[0] if args else "origin"
    if "://" in remote or "@" in remote:
        return remote
    r = subprocess.run(["git", "-C", where, "remote", "get-url", "--push", remote], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def blocked(cmd: str, cwd: str = ".") -> str | None:
    for part in re.split(r"&&|\|\||;|\|", os.path.expandvars(cmd)):
        url = push_target(part, cwd)
        if url is not None and ORG in url.replace(":", "/"):
            return "a git push to a sensible-hq remote"
        if ORG not in part:
            continue
        if GH_WRITE.search(part):
            return "a gh command that changes a sensible-hq PR, issue, label, or workflow"
        if API.search(part) and API_WRITE.search(part) and not API_GET.search(part):
            return "a GitHub API write to a sensible-hq repo"
    return None


def main() -> int:
    docs_repo = os.environ.get("DOCS_REPO", "")
    if not docs_repo or docs_repo.startswith(ORG):
        return 0
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if event.get("tool_name") != "Bash":
        return 0
    why = blocked((event.get("tool_input") or {}).get("command", ""), event.get("cwd") or os.getcwd())
    if not why:
        return 0
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
          "permissionDecisionReason": f"Sandbox guard: DOCS_REPO is {docs_repo}, a test copy, so {why} isn't "
          "allowed. Use $DOCS_REPO for docs work. Report what you would have changed instead."}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
