"""Tests for .claude/hooks/vale_gate.py, run as Claude Code runs it: JSON on stdin.

Builds a throwaway git repo that links to this repo's Vale styles, registry, and scripts, so the hook
sees the real rules. Needs Vale installed.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import uuid

REPO = Path(__file__).resolve().parents[3]
HOOK = REPO / ".claude/hooks/vale_gate.py"
RUN = uuid.uuid4().hex[:8]  # loop-guard state is per session; a fresh id per run keeps runs independent
pytestmark = pytest.mark.skipif(not (shutil.which("vale") or (Path.home() / ".local/bin/vale").exists()),
                                reason="Vale isn't installed")


@pytest.fixture
def repo(tmp_path):
    for name in (".github", "style-rules", "scripts"):
        (tmp_path / name).symlink_to(REPO / name)
    shutil.copy(REPO / ".vale.ini", tmp_path / ".vale.ini")
    (tmp_path / "docs").mkdir()
    (tmp_path / "reference").mkdir()
    page = tmp_path / "docs/page.md"
    page.write_text("# Page\n\nWe will utilize this feature — it works.\n\nSensible extracts the value.\n")
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t"}
    for cmd in (["init", "-q"], ["add", "docs/page.md"], ["commit", "-qm", "base"]):
        subprocess.run(["git", "-C", str(tmp_path), *cmd], check=True, env=env)
    return tmp_path


def run(event: dict) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event), capture_output=True, text=True,
                          env={**os.environ, "TMPDIR": os.environ.get("TMPDIR", "/tmp")})


def edit(repo, old, new, event="PreToolUse", session="s1", path="docs/page.md"):
    return run({"hook_event_name": event, "session_id": f"{session}-{RUN}", "tool_name": "Edit",
                "tool_input": {"file_path": str(repo / path), "old_string": old, "new_string": new}})


def test_pre_denies_a_blocking_rule_on_a_changed_line(repo):
    r = edit(repo, "Sensible extracts the value.", "Sensible extracts the value — fast.", session="deny")
    out = json.loads(r.stdout)["hookSpecificOutput"]
    assert out["permissionDecision"] == "deny"
    assert "Sensible.EmDash" in out["permissionDecisionReason"]
    assert "line 5" in out["permissionDecisionReason"]


def test_pre_ignores_unchanged_lines_and_warn_rules(repo):
    # Line 3 already has an em dash, and "utilize" is a warn rule; neither is in the changed line.
    r = edit(repo, "Sensible extracts the value.", "Sensible returns the value.", session="clean")
    assert r.returncode == 0 and r.stdout == ""


def test_pre_blocks_json5_fences(repo):
    r = edit(repo, "Sensible extracts the value.", "Sensible extracts the value.\n\n```json5\n{}\n```",
             session="fence")
    assert "sensible-code-fences" in json.loads(r.stdout)["hookSpecificOutput"]["permissionDecisionReason"]


def test_pre_loop_guard_releases_after_three_denials(repo):
    args = (repo, "Sensible extracts the value.", "Sensible extracts the value — fast.")
    for _ in range(3):
        assert json.loads(edit(*args, session="guard").stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"
    out = json.loads(edit(*args, session="guard").stdout)["hookSpecificOutput"]
    assert "permissionDecision" not in out and "Sensible.EmDash" in out["additionalContext"]


def test_post_reports_only_changed_lines(repo):
    page = repo / "docs/page.md"
    page.write_text(page.read_text().replace("Sensible extracts the value.", "Please note that Sensible extracts it."))
    r = edit(repo, "", "", event="PostToolUse")
    assert r.returncode == 2
    assert "Sensible.Filler" in r.stderr
    assert "line 3" not in r.stderr  # the old em dash on an untouched line


def test_reference_markdown_is_skipped(repo):
    (repo / "reference/api.md").write_text("# API\n\nPlease note that — this.\n")
    r = edit(repo, "", "", event="PostToolUse", path="reference/api.md")
    assert r.returncode == 0 and r.stderr == ""


def test_post_lists_judge_gated_alerts_as_candidates(repo):
    page = repo / "docs/page.md"
    page.write_text(page.read_text().replace("Sensible extracts the value.", "Sensible extracts data against a document type."))
    r = edit(repo, "", "", event="PostToolUse")
    assert r.returncode == 2
    assert "Possible problems for Jev to judge" in r.stderr
    assert "Sensible.AgainstPhrasing" in r.stderr.split("Possible problems for Jev to judge")[1]


def test_post_reports_each_alert_once_per_session(repo):
    page = repo / "docs/page.md"
    page.write_text(page.read_text().replace("Sensible extracts the value.", "Please note that Sensible extracts it."))
    first = edit(repo, "", "", event="PostToolUse", session="once")
    assert first.returncode == 2 and "Sensible.Filler" in first.stderr
    # Another edit elsewhere moves the line down; the same alert isn't repeated
    page.write_text("Intro line.\n\n" + page.read_text())
    second = edit(repo, "", "", event="PostToolUse", session="once")
    assert "Sensible.Filler" not in second.stderr
    # A new problem is reported, with a count of the open ones
    page.write_text(page.read_text().replace("Intro line.", "It is worth mentioning the intro."))
    third = edit(repo, "", "", event="PostToolUse", session="once")
    assert third.returncode == 2 and "Sensible.Filler" in third.stderr and "still on lines you changed" in third.stderr
    # Another session hears about it again
    assert "Please note" in page.read_text() and "Sensible.Filler" in edit(repo, "", "", event="PostToolUse", session="other").stderr
