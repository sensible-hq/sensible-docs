"""Tests for scripts/pipeline/step_evidence.py and the Stop hook .claude/hooks/pipeline_evidence_gate.py.

Each test builds a throwaway git repo with a pipeline checklist and a fake session transcript, then runs the
script or the hook the way Claude Code does. `gh` is replaced by a stub on PATH.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "scripts/pipeline/step_evidence.py"
HOOK = REPO / ".claude/hooks/pipeline_evidence_gate.py"
SESSION = "11111111-2222-3333-4444-555555555555"
TEMPLATE = (REPO / ".claude/skills/pipeline-for-pr/checklist-template.md").read_text()
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def git(repo, *args, env=None):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True,
                          env={**os.environ, **GIT_ENV, **(env or {})}).stdout


class World:
    def __init__(self, tmp: Path):
        self.repo = tmp / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "v0")
        (self.repo / "README.md").write_text("base\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "base")
        git(self.repo, "branch", "base-ref")
        self.checklist = self.repo / ".claude/sessions/run/checklist.md"
        self.checklist.parent.mkdir(parents=True)
        self.transcript = tmp / "projects" / f"{SESSION}.jsonl"
        self.transcript.parent.mkdir()
        self.records: list[dict] = []
        self.bin = tmp / "bin"
        self.bin.mkdir()
        self.gh_body("")
        self.write_checklist()

    def write_checklist(self, ticked=(), fields=None, header=None):
        text = TEMPLATE.replace("<engine-pr>", "4321").replace("<session-id>", SESSION)
        text = text.replace("<session-name>", "run")
        for k, v in (header or {}).items():
            text = text.replace(f"{k}: <", f"{k}: {v} <!--", 1).replace(f"{k}: {v} <!--", f"{k}: {v}\n<!--", 1)
            text = "\n".join(l for l in text.splitlines() if not l.startswith("<!--"))
        for n in ticked:
            text = text.replace(f"- [ ] **{n}.", f"- [x] **{n}.")
        for name, value in (fields or {}).items():
            text = text.replace(f"  - {name}:", f"  - {name}: {value}", 1)
        self.checklist.write_text(text)

    def say(self, ts: str, *items):
        content = []
        for kind, value in items:
            if kind == "text":
                content.append({"type": "text", "text": value})
            else:
                key = {"Read": "file_path", "Bash": "command", "Skill": "skill"}[kind]
                content.append({"type": "tool_use", "name": kind, "input": {key: value}})
        self.records.append({"type": "assistant", "timestamp": ts, "message": {"content": content}})
        self.transcript.write_text("".join(json.dumps(r) + "\n" for r in self.records))

    def gh_body(self, body: str):
        gh = self.bin / "gh"
        gh.write_text("#!/bin/sh\ncat <<'EOF'\n" + json.dumps({"body": body, "url": "https://example/pr/9"}) + "\nEOF\n")
        gh.chmod(0o755)

    def env(self):
        return {**os.environ, **GIT_ENV, "PATH": f"{self.bin}:{os.environ['PATH']}", "PIPELINE_BASE_REF": "base-ref"}

    def script(self, *extra):
        out = subprocess.run([sys.executable, str(SCRIPT), "--checklist", str(self.checklist), "--transcript",
                              str(self.transcript), "--json", *extra], capture_output=True, text=True, env=self.env())
        return out.returncode, json.loads(out.stdout) if out.stdout.startswith("{") else out.stdout

    def hook(self, **event):
        payload = {"session_id": SESSION, "transcript_path": str(self.transcript), "cwd": str(self.repo), **event}
        out = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True,
                             env=self.env())
        assert out.returncode == 0, out.stderr
        return json.loads(out.stdout) if out.stdout.strip() else None


@pytest.fixture
def world(tmp_path):
    return World(tmp_path)


def statuses(outcome):
    return [(r["label"], r["status"]) for r in outcome["results"]]


STEP1_FIELDS = {"Merged into the engine's default branch, or still in an open PR": "merged",
                "Affected pages": "docs/a.md", "Existing docs PR, if any": "none", "Extractor directories": "none"}


def test_step1_passes_with_links_to_the_transcript(world):
    world.say("2026-11-24T10:00:00Z", ("Read", "/x/repo/.claude/skills/update-docs-from-pr/SKILL.md"))
    world.say("2026-11-24T10:01:00Z", ("Bash", "gh pr view 4321 --repo sensible-hq/sensible --json state"))
    world.say("2026-11-24T10:02:00Z", ("Bash", 'gh pr list --repo x --state all --search "sensible#4321"'))
    world.write_checklist(fields=STEP1_FIELDS)
    code, out = world.script()
    assert code == 0, out
    assert out["step"] == 1
    links = [r["link"] for r in out["results"]]
    assert links[:3] == [f"{world.transcript}:1", f"{world.transcript}:2", f"{world.transcript}:3"]


def test_missing_evidence_is_reported_with_the_empty_checklist_field(world):
    world.say("2026-11-24T10:00:00Z", ("Bash", "gh pr view 9999"))
    code, out = world.script()
    assert code == 1
    result = dict(statuses(out))
    assert result["Read `.claude/skills/update-docs-from-pr/SKILL.md`"] == "missing"
    assert result["Fetched the engine PR's state"] == "missing"  # a different PR number doesn't count
    checklist = out["results"][-1]
    assert "Affected pages" in checklist["detail"]
    assert checklist["link"].startswith(f"{world.checklist}:")


def test_a_reread_is_needed_for_a_later_step_using_the_same_skill(world):
    # Step 5 follows update-docs-from-pr like step 1 does; step 1's read must not satisfy step 5.
    world.say("2026-11-24T10:00:00Z", ("Read", "/r/.claude/skills/update-docs-from-pr/SKILL.md"))
    world.say("2026-11-24T10:10:00Z", ("Skill", "upload-pr-extractor"))
    world.say("2026-11-24T10:20:00Z", ("Bash", "cat .claude/skills/json5-commenter/SKILL.md"))
    world.say("2026-11-24T10:30:00Z", ("Read", "/r/.claude/skills/create-docs-example/SKILL.md"))
    world.write_checklist(ticked=(1, 2, 3, 4))
    _, out = world.script()
    assert out["step"] == 5
    assert out["results"][0]["status"] == "missing"
    world.say("2026-11-24T10:40:00Z", ("Read", "/r/.claude/skills/update-docs-from-pr/SKILL.md"))
    _, out = world.script()
    assert out["results"][0]["status"] == "pass"
    assert out["results"][0]["link"] == f"{world.transcript}:5"


@pytest.mark.parametrize("kind,value,counts", [
    ("Read", "/r/.claude/skills/update-docs-from-pr/SKILL.md", True),
    ("Bash", "cat .claude/skills/update-docs-from-pr/SKILL.md", True),
    ("Bash", "cat -n /r/.claude/skills/update-docs-from-pr/SKILL.md | less", True),
    ("Skill", "update-docs-from-pr", True),
    ("Bash", "sed -n 100,125p .claude/skills/update-docs-from-pr/SKILL.md", False),
    ("Bash", "grep -n Step .claude/skills/update-docs-from-pr/SKILL.md; cat notes.txt", False),
    ("Read", "/r/.claude/skills/update-docs-from-pr/SKILL.md.bak", False),
    ("Bash", "python3 - <<'X'\nrun('cat .claude/skills/update-docs-from-pr/SKILL.md')\nX", False),
    ("Bash", "cd /r && cat .claude/skills/update-docs-from-pr/SKILL.md", True),
])
def test_only_a_whole_file_read_of_the_skill_counts(world, kind, value, counts):
    world.say("2026-11-24T10:00:00Z", (kind, value))
    _, out = world.script()
    assert (out["results"][0]["status"] == "pass") is counts


def test_a_partial_read_tool_call_doesnt_count(world):
    world.records.append({"type": "assistant", "timestamp": "2026-11-24T10:00:00Z", "message": {"content": [
        {"type": "tool_use", "name": "Read",
         "input": {"file_path": "/r/.claude/skills/update-docs-from-pr/SKILL.md", "offset": 100, "limit": 20}}]}})
    world.say("2026-11-24T10:00:01Z", ("text", "ok"))
    _, out = world.script()
    assert out["results"][0]["status"] == "missing"


def test_transcripts_are_found_by_session_id_without_a_path(world):
    world.say("2026-11-24T10:00:00Z", ("Read", "/r/.claude/skills/update-docs-from-pr/SKILL.md"))
    out = subprocess.run([sys.executable, str(SCRIPT), "--checklist", str(world.checklist), "--json"],
                         capture_output=True, text=True,
                         env={**world.env(), "CLAUDE_PROJECTS_DIR": str(world.transcript.parent.parent)})
    assert json.loads(out.stdout)["results"][0]["status"] == "pass"


def test_a_skipped_step_moves_the_current_step_on(world):
    world.write_checklist(ticked=(1,))
    world.checklist.write_text(world.checklist.read_text().replace(
        "  - Sensible app URLs:", "  - Skipped: the PR has no extractor\n  - Sensible app URLs:"))
    _, out = world.script()
    assert out["step"] == 3


def test_file_check_links_the_matching_line(world):
    draft = world.repo / "drafts/4321-example.md"
    draft.parent.mkdir()
    draft.write_text("# Example\n\n```json\n{\n  // the anchor\n}\n```\n")
    world.write_checklist(ticked=(1, 2))
    _, out = world.script()
    result = {r["label"]: r for r in out["results"]}
    assert result["Example draft has a JSON block"]["link"] == f"{draft}:3"
    assert result["Example draft has comments"]["link"] == f"{draft}:5"


def test_docs_pr_checks_are_unverified_before_step_4_fills_the_header(world):
    world.write_checklist(ticked=(1, 2, 3))
    _, out = world.script()
    result = dict(statuses(out))
    assert result["Committed a docs change on the docs branch"] == "unverified"
    assert result["Docs PR body lists the engine PR"] == "unverified"


def test_commit_and_pr_body_checks(world):
    world.say("2026-01-01T00:00:00Z", ("Read", "/r/.claude/skills/create-docs-example/SKILL.md"))
    git(world.repo, "checkout", "-qb", "feature")
    (world.repo / "docs").mkdir()
    (world.repo / "docs/page.md").write_text("page\n")
    git(world.repo, "add", "docs")
    git(world.repo, "commit", "-qm", "Add the example page")
    world.gh_body("Docs for sensible-hq/sensible#4321.")
    world.write_checklist(ticked=(1, 2, 3), header={"Docs branch": "feature", "Docs PR": "sensible-docs#9"})
    _, out = world.script()
    result = {r["label"]: r for r in out["results"]}
    assert result["Committed a docs change on the docs branch"]["status"] == "pass"
    assert "Add the example page" in result["Committed a docs change on the docs branch"]["detail"]
    assert result["Docs PR body lists the engine PR"]["status"] == "pass"
    world.gh_body("Docs for sensible-hq/sensible#43210.")
    _, out = world.script()
    assert dict(statuses(out))["Docs PR body lists the engine PR"] == "missing"


def test_commits_from_before_the_step_started_dont_count(world):
    git(world.repo, "checkout", "-qb", "feature")
    (world.repo / "docs").mkdir()
    (world.repo / "docs/page.md").write_text("page\n")
    git(world.repo, "add", "docs")
    git(world.repo, "commit", "-qm", "Example page", env={"GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"})
    world.say("2026-01-02T00:00:00Z", ("Read", "/r/.claude/skills/create-docs-example/SKILL.md"))
    world.write_checklist(ticked=(1, 2, 3), header={"Docs branch": "feature", "Docs PR": "sensible-docs#9"})
    _, out = world.script()
    assert dict(statuses(out))["Committed a docs change on the docs branch"] == "missing"


# --- hook ---------------------------------------------------------------------------------------------------

def test_hook_ignores_sessions_without_a_pipeline_checklist(world):
    world.checklist.unlink()
    assert world.hook() is None


def test_hook_ignores_another_sessions_checklist(world):
    assert world.hook(session_id="someone-else") is None


def test_hook_blocks_until_the_block_is_shown_verbatim(world):
    decision = world.hook()
    assert decision["decision"] == "block"
    block = decision["reason"].split("\n\n", 1)[1]
    assert "Step 1 evidence" in block and "evidence-id: step 1 ·" in block

    world.say("2026-11-24T11:00:00Z", ("text", "Step 1 report.\n\n" + block.replace("❌", "✅")))
    assert world.hook()["decision"] == "block"  # an edited block doesn't count

    world.say("2026-11-24T11:01:00Z", ("text", "Step 1 report.\n\n" + block + "\n\nThe read is missing because…"))
    assert world.hook() is None
    assert world.hook() is None  # a side question later doesn't need it again

    world.say("2026-11-24T11:02:00Z", ("Read", "/r/.claude/skills/update-docs-from-pr/SKILL.md"))
    assert world.hook()["decision"] == "block"  # new evidence, new block


def test_hook_accepts_the_block_in_last_assistant_message(world):
    block = world.hook()["reason"].split("\n\n", 1)[1]
    assert world.hook(last_assistant_message="Report\n" + block) is None


def test_hook_lets_the_stop_through_when_already_continuing(world):
    assert world.hook(stop_hook_active=True) is None


def test_hook_finds_the_checklist_in_a_worktree(world, tmp_path):
    wt = tmp_path / "wt"
    git(world.repo, "worktree", "add", "-q", str(wt), "-b", "feature")
    moved = wt / ".claude/sessions/run/checklist.md"
    moved.parent.mkdir(parents=True)
    moved.write_text(world.checklist.read_text())
    world.checklist.unlink()
    assert world.hook()["decision"] == "block"


def test_spec_matches_the_skill_steps():
    import yaml
    spec = yaml.safe_load((REPO / ".claude/skills/pipeline-for-pr/evidence.yaml").read_text())
    skill = (REPO / ".claude/skills/pipeline-for-pr/SKILL.md").read_text()
    for n, checks in spec.items():
        assert f"## Step {n} " in skill
        for c in checks:
            if c["kind"] == "read":
                assert (REPO / c["path"]).exists(), c["path"]
