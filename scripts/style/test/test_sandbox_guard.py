"""Tests for .claude/hooks/sandbox_guard.py."""
import json
import os
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parents[3] / ".claude/hooks/sandbox_guard.py"


def run(cmd, docs_repo="fscelliott/sensible-docs-private-test", cwd=None, **env_vars):
    env = {**os.environ, "DOCS_REPO": docs_repo, **env_vars}
    event = {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(cwd or Path.cwd())}
    r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event), capture_output=True, text=True, env=env)
    return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] if r.stdout else "allow"


def test_blocks_writes_to_sensible_hq():
    assert run("gh api -X POST repos/sensible-hq/sensible/issues/3374/labels -f 'labels[]=docs_done'") == "deny"
    assert run("gh api -X DELETE repos/sensible-hq/sensible/issues/3374/labels/doc_changes_needed") == "deny"
    assert run("gh api repos/sensible-hq/sensible-docs/issues/9/comments -f body=x") == "deny"
    assert run("gh pr create --repo sensible-hq/sensible-docs --title t --body b") == "deny"
    assert run("gh issue create --repo sensible-hq/sensible-docs --title t") == "deny"
    assert run("git push git@github.com:sensible-hq/sensible-docs.git HEAD:v0") == "deny"
    assert run("cd x && gh pr merge 5 --repo sensible-hq/sensible-docs --squash") == "deny"


def clone(tmp_path, name, url):
    d = tmp_path / name
    subprocess.run(["git", "init", "-q", str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "remote", "add", "origin", url], check=True)
    return d


def test_push_checks_the_remote_url(tmp_path):
    copy = clone(tmp_path, "copy", "git@github.com:fscelliott/sensible-docs-private-test.git")
    engine = clone(tmp_path, "engine", "https://github.com/sensible-hq/sensible.git")
    assert run("git push -u origin fe_today_docs", cwd=copy) == "allow"
    assert run("git push -u origin fe_today_docs", cwd=engine) == "deny"
    assert run(f'git -C "{engine}" push -u origin fe_x', cwd=copy) == "deny"
    assert run('git -C "$ENGINE_DIR" push -u origin fe_x', cwd=copy, ENGINE_DIR=str(engine)) == "deny"
    assert run(f'git -C "{copy}" push -u origin fe_x', cwd=engine) == "allow"


def test_expands_variables():
    assert run('gh pr create --repo "$ENGINE_REPO" --draft --title t', ENGINE_REPO="sensible-hq/sensible") == "deny"
    assert run('gh pr view 1 --repo "$ENGINE_REPO"', ENGINE_REPO="sensible-hq/sensible") == "allow"


def test_allows_reads_and_copy_writes(tmp_path):
    assert run("gh pr view 3374 --repo sensible-hq/sensible --json title,body,files") == "allow"
    assert run("gh pr diff 3351 --repo sensible-hq/sensible") == "allow"
    assert run("gh api repos/sensible-hq/sensible/pulls/3374/files --paginate") == "allow"
    assert run('gh api -X GET search/issues -f q="repo:sensible-hq/sensible-docs is:issue"') == "allow"
    assert run("gh pr create --repo fscelliott/sensible-docs-private-test --title t --body b") == "allow"
    copy = clone(tmp_path, "copy", "git@github.com:fscelliott/sensible-docs-private-test.git")
    assert run("git push -u origin fe_today_docs", cwd=copy) == "allow"


def test_off_when_docs_repo_is_upstream():
    assert run("gh pr create --repo sensible-hq/sensible-docs --title t", docs_repo="sensible-hq/sensible-docs") == "allow"
