#!/usr/bin/env python3
"""Claude Code Stop hook: a pipeline-for-pr handoff has to carry the script-checked evidence for its step.

Does nothing unless this session has a pipeline checklist: a .claude/sessions/*/checklist.md, in the main
checkout or any worktree, headed "# Checklist: pipeline for sensible#..." whose "Claude Code session ID:" line
lists this session.

For the current step (the first that's neither ticked nor skipped), runs scripts/pipeline/step_evidence.py and
looks for its evidence block, verbatim, in an assistant message from this session. If no message has it yet,
blocks the stop and hands the block to the agent to paste. Once a block has been shown, later stops pass until
the evidence changes. Lets the stop through when stop_hook_active is set, so a turn can't loop.

Design: design/pipeline-step-evidence/design.md.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/pipeline"))
import step_evidence as se  # noqa: E402


def find_checklist(cwd: Path, session_id: str) -> Path | None:
    out = subprocess.run(["git", "-C", str(cwd), "worktree", "list", "--porcelain"], capture_output=True, text=True)
    roots = [Path(l.removeprefix("worktree ")) for l in out.stdout.splitlines() if l.startswith("worktree ")]
    for root in roots or [cwd]:
        for path in sorted((root / ".claude/sessions").glob("*/checklist.md")):
            try:
                text = path.read_text()
            except OSError:
                continue
            if se.HEADER_RE.search(text) and session_id in (se.header_value(text, "Claude Code session ID") or ""):
                return path
    return None


def normalize(text: str) -> str:
    return " ".join(text.split())


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    session_id, transcript = event.get("session_id"), event.get("transcript_path")
    if not session_id or not transcript or event.get("stop_hook_active"):
        return 0
    checklist = find_checklist(Path(event.get("cwd") or "."), session_id)
    if checklist is None:
        return 0
    try:
        outcome = se.evaluate(checklist, Path(transcript))
    except (OSError, ValueError) as e:
        print(f"pipeline evidence check failed: {e}", file=sys.stderr)
        return 0
    if outcome["step"] is None:
        return 0
    block = se.render(outcome)
    wanted = normalize(block)
    shown = [e.value for e in se.load_events(se.transcripts(se.parse_checklist(checklist), Path(transcript)))
             if e.kind == "text"] + [event.get("last_assistant_message") or ""]
    if any(wanted in normalize(text) for text in shown):
        return 0
    reason = ("This is a pipeline-for-pr session, and the reply doesn't carry the evidence for step "
              f"{outcome['step']}. End the handoff report with this block, verbatim and unedited, so Frances can "
              "check the step. If a line is ❌ or ⚠️, say why after the block in your own words; don't change the block.\n\n"
              + block)
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
