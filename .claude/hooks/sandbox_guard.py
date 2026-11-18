#!/usr/bin/env python3
"""PreToolUse guard for test copies of the docs repo: no writes to sensible-hq repos.

While DOCS_REPO (set in .claude/settings.json) names a repo outside the sensible-hq org, this hook denies
Bash commands that would change something in a sensible-hq repo: GitHub API calls with a write method
or fields, gh commands that create, edit, comment on, close, merge, or label PRs and issues there, and
git pushes to a sensible-hq remote URL. Reads (gh pr view, gh pr diff, GET API calls) pass.
When DOCS_REPO is a sensible-hq repo, the hook does nothing.
"""
import json
import os
import re
import sys

ORG = "sensible-hq/"
GH_WRITE = re.compile(r"\bgh\s+(?:pr|issue|label|release|workflow|run)\s+(?:create|edit|comment|close|reopen|merge|"
                      r"delete|review|ready|lock|unlock|transfer|pin|unpin|develop|rerun|cancel|run)\b")
API = re.compile(r"\bgh\s+api\b")
API_WRITE = re.compile(r"(?:-X|--method)\s*['\"]?(?:POST|PUT|PATCH|DELETE)\b|(?:^|\s)(?:-f|-F|--field|--raw-field|--input)\s", re.I)
API_GET = re.compile(r"(?:-X|--method)\s*['\"]?GET\b", re.I)


def blocked(cmd: str) -> str | None:
    for part in re.split(r"&&|\|\||;|\|", cmd):
        if ORG not in part:
            continue
        if GH_WRITE.search(part):
            return "a gh command that changes a sensible-hq PR, issue, label, or workflow"
        if API.search(part) and API_WRITE.search(part) and not API_GET.search(part):
            return "a GitHub API write to a sensible-hq repo"
        if re.search(r"\bgit\s+push\b", part):
            return "a git push to a sensible-hq remote"
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
    why = blocked((event.get("tool_input") or {}).get("command", ""))
    if not why:
        return 0
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
          "permissionDecisionReason": f"Sandbox guard: DOCS_REPO is {docs_repo}, a test copy, so {why} isn't "
          "allowed. Use $DOCS_REPO for docs work. Report what you would have changed instead."}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
