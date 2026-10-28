"""Acceptance tests for agent_lines.py, as specified in scripts/style_sync/README.md
("Agent-only rules > Spec"), plus one test of .claude/hooks/vale-check.sh that uses it.

Each test builds a small git repo in a temp dir with the real Sensible styles and
registry, commits a "human" version of a page, then makes an "agent" edit.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
REAL_ROOT = HERE.parents[4]
SCRIPT = REAL_ROOT / "scripts/style_sync/agent_lines.py"
HOOK = REAL_ROOT / ".claude/hooks/vale-check.sh"
VALE = os.environ.get("VALE_BIN") or shutil.which("vale") or (
    str(Path.home() / ".local/bin/vale") if (Path.home() / ".local/bin/vale").exists() else None
)
needs_vale = pytest.mark.skipif(VALE is None, reason="vale binary not installed")

HUMAN_DASH = "Sensible skips the page — a person wrote this dash."
AGENT_DASH = "Configure portfolio mode — Sensible segments the file."
PLAIN = "This line has no dash."


def git(root, *args, who="Human"):
    # Fixed identity, no signing: the tests mustn't depend on the user's git config
    ident = ["-c", f"user.name={who}", "-c", f"user.email={who.lower()}@example.com",
             "-c", "commit.gpgsign=false"]
    subprocess.run(["git", *ident, *args], cwd=root, check=True, capture_output=True, text=True)


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def page(*lines):
    return "# Page\n\n" + "\n\n".join(lines) + "\n"


def line_of(path: Path, text: str) -> int:
    return path.read_text(encoding="utf-8").splitlines().index(text) + 1


@pytest.fixture
def repo(tmp_path):
    """A git repo with the real styles, the real registry, a .vale.ini with
    Sensible.EmDash off, and one committed page holding a human em dash."""
    root = tmp_path / "repo"
    shutil.copytree(REAL_ROOT / ".github/styles", root / ".github/styles")
    write(root / "scripts/style_sync/registry.yaml",
          (REAL_ROOT / "scripts/style_sync/registry.yaml").read_text(encoding="utf-8"))
    write(root / ".vale.ini", (REAL_ROOT / ".vale.ini").read_text(encoding="utf-8"))
    write(root / "docs/page.md", page(HUMAN_DASH, PLAIN))
    git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "human")
    return root


def run(root, *args, vale=VALE):
    cmd = [sys.executable, str(SCRIPT), *args]
    if vale is not None:
        cmd += ["--vale", vale]
    return subprocess.run(cmd, cwd=root, capture_output=True, text=True)


def flagged(result):
    """The (path, line, rule) of each output line."""
    out = []
    for ln in result.stdout.splitlines():
        path, line, _col, rule, _msg = ln.split(":", 4)
        out.append((path, int(line), rule))
    return out


@needs_vale
def test_only_the_agent_added_line_is_flagged(repo):
    f = repo / "docs/page.md"
    write(f, page(HUMAN_DASH, PLAIN, AGENT_DASH))  # the agent appends a line
    r = run(repo, "--base", "HEAD", "docs/page.md")
    assert r.returncode == 1, r.stderr
    assert flagged(r) == [("docs/page.md", line_of(f, AGENT_DASH), "Sensible.EmDash")]


@needs_vale
def test_human_dash_alone_is_clean(repo):
    r = run(repo, "--base", "HEAD", "docs/page.md")
    assert (r.returncode, r.stdout) == (0, ""), r.stderr


@needs_vale
def test_normal_vale_run_ignores_the_human_dash(repo):
    """.vale.ini turns Sensible.EmDash off, so CI lint and plain Vale runs don't flag it."""
    r = subprocess.run([VALE, "--output=JSON", "--no-exit", "docs/page.md"],
                       cwd=repo, capture_output=True, text=True)
    checks = [a["Check"] for alerts in json.loads(r.stdout or "{}").values() for a in alerts]
    assert "Sensible.EmDash" not in checks


@needs_vale
def test_untracked_file_counts_every_line(repo):
    write(repo / "docs/new.md", page(HUMAN_DASH, AGENT_DASH))
    r = run(repo, "--base", "HEAD", "docs/new.md")
    assert r.returncode == 1, r.stderr
    assert [line for _, line, _ in flagged(r)] == [3, 5]


@needs_vale
def test_changed_line_that_keeps_its_dash_counts(repo):
    f = repo / "docs/page.md"
    edited = HUMAN_DASH.replace("skips", "ignores")
    write(f, page(edited, PLAIN))
    r = run(repo, "--base", "HEAD", "docs/page.md")
    assert r.returncode == 1, r.stderr
    assert flagged(r) == [("docs/page.md", line_of(f, edited), "Sensible.EmDash")]


@needs_vale
def test_staged_and_committed_since_base_both_count(repo):
    """--base is a branch point: lines committed after it are still added lines."""
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True,
                          text=True, check=True).stdout.strip()
    write(repo / "docs/page.md", page(HUMAN_DASH, PLAIN, AGENT_DASH))
    git(repo, "commit", "-qam", "agent", who="Agent")
    r = run(repo, "--base", base)  # no FILE: finds changed docs itself
    assert r.returncode == 1, r.stderr
    assert flagged(r) == [("docs/page.md", 7, "Sensible.EmDash")]


@needs_vale
def test_dash_in_a_code_block_follows_vale_default(repo):
    """Vale skips fenced code by default, and so does the script."""
    write(repo / "docs/page.md", page(HUMAN_DASH, PLAIN, "```txt\n" + AGENT_DASH + "\n```"))
    r = run(repo, "--base", "HEAD", "docs/page.md")
    assert (r.returncode, r.stdout) == (0, ""), r.stderr


def test_no_vale_exits_2(repo):
    write(repo / "docs/page.md", page(HUMAN_DASH, PLAIN, AGENT_DASH))
    r = run(repo, "--base", "HEAD", "docs/page.md", vale=str(repo / "no-such-vale"))
    assert r.returncode == 2
    assert r.stderr.strip()


def test_unknown_base_exits_2(repo):
    r = run(repo, "--base", "no-such-ref", "docs/page.md", vale=VALE or "vale")
    assert r.returncode == 2


def test_outside_a_git_repo_exits_2(tmp_path):
    write(tmp_path / "docs/page.md", page(AGENT_DASH))
    r = run(tmp_path, "--base", "HEAD", "docs/page.md", vale=VALE or "vale")
    assert r.returncode == 2


# --- The edit hook ------------------------------------------------------------


def run_hook(repo, file: Path):
    """Run the hook the way Claude Code does: the PostToolUse JSON event on stdin."""
    event = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(file)}})
    hooks = repo / ".claude/hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    shutil.copy(HOOK, hooks / "vale-check.sh")
    write(repo / "scripts/style_sync/agent_lines.py", SCRIPT.read_text(encoding="utf-8"))
    env = dict(os.environ, PATH=f"{Path(VALE).parent}:{os.environ.get('PATH', '')}")
    return subprocess.run(["bash", str(hooks / "vale-check.sh")], input=event,
                           capture_output=True, text=True, env=env)


@needs_vale
@pytest.mark.skipif(shutil.which("jq") is None, reason="jq not installed")
def test_hook_hands_the_agent_dash_to_claude(repo):
    f = repo / "docs/page.md"
    write(f, page(HUMAN_DASH, PLAIN, AGENT_DASH))
    r = run_hook(repo, f)
    assert r.returncode == 2, r.stderr  # 2 = alerts, stderr goes to Claude
    dash_alerts = [ln for ln in r.stderr.splitlines() if "Sensible.EmDash" in ln]
    assert len(dash_alerts) == 1
    assert f":{line_of(f, AGENT_DASH)}:" in dash_alerts[0]


@needs_vale
@pytest.mark.skipif(shutil.which("jq") is None, reason="jq not installed")
def test_hook_is_quiet_about_the_human_dash(repo):
    r = run_hook(repo, repo / "docs/page.md")
    assert r.returncode == 0, r.stderr
