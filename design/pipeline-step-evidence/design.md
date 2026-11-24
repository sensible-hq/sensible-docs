# Design: step evidence for pipeline-for-pr

## Problem

`pipeline-for-pr` stops after each step for Frances to review. Its steps run other skills, and an agent can skip a step, or skip reading the skill it was told to follow, and still write a confident report. Frances can't tell from the report alone.

## Decision

A script, not the agent, checks each step's evidence and writes it into the handoff report. A `Stop` hook makes the report carry that evidence before the turn can end.

Asking the agent to inspect its own logs was rejected. The agent that skipped a step is the same one that would skip or misread the check, so its account of the log proves nothing new.

## What counts as evidence

Each step lists its checks in `.claude/skills/pipeline-for-pr/evidence.yaml`. A check is one of these kinds:

| Kind | Passes when | Link it gives |
|---|---|---|
| `read` | The session transcript shows the step's skill file read in full: a `Read` of the path with no `offset` or `limit`, a `cat`, `less`, `more`, or `bat` of it as a shell command, or a `Skill` call naming it. A `sed -n`, `head`, `grep`, or partial `Read` doesn't count, because it saw only part of the instructions. | Transcript `file:line`, with the time |
| `bash` | A `Bash` command matching a pattern ran during the step. | Transcript `file:line`, with the start of the command |
| `file` | A file matching a glob exists, and contains a pattern if one is given. | The file's `path:line` at the first match |
| `commit` | The docs branch has a commit touching a path, made during the step. | The commit hash and subject |
| `pr_body` | The docs PR body matches a pattern. Needs `gh` and the network. | The PR URL |
| `checklist` | Every field under the step in the checklist has a value. | The checklist `path:line` of each empty field |

A check passes, fails, or is **unverified**: its inputs don't exist yet (no docs PR number before step 4) or `gh` failed. Unverified is shown, never counted as a pass.

## Order

Transcript checks only count entries from the step's own window. The window opens at the first `read` of the step's skill that comes after the previous step's window opened. So step 5's read of `update-docs-from-pr/SKILL.md` can't be satisfied by step 1's read of the same file, and step 5's commits must come after step 5 started.

## The hook

`.claude/hooks/pipeline_evidence_gate.py` runs on `Stop`:

1. Finds this session's pipeline checklist: a `.claude/sessions/*/checklist.md` in the main checkout or any worktree, headed `# Checklist: pipeline for sensible#…`, whose `Claude Code session ID:` line lists this session. No checklist means this isn't a pipeline session, and the hook does nothing.
2. Takes the current step: the first step that isn't ticked and has no `Skipped:` reason.
3. Runs the checker and builds the evidence block, which ends with an `evidence-id: step N · <hash>` line. The hash covers the results, so it changes when the evidence changes.
4. Passes if an assistant message in the transcript, or the hook input's `last_assistant_message`, already contains the whole block, with whitespace normalized. Otherwise it blocks the stop and hands the agent the block to paste verbatim. A block with any line changed doesn't match, so an edited ❌ still blocks.

Requiring the block once per evidence state, rather than on every stop, keeps side questions cheap: once Frances has seen the evidence, a reply about something else isn't blocked. When the evidence changes, the next stop shows it again.

Following Claude Code's guidance for `Stop` hooks, the hook lets the turn end when `stop_hook_active` is set, so a turn that can't comply doesn't loop. By then the agent has been told once, and a report without the block is easy to spot.

## Limits

- The checks prove a step's skill was opened and its outputs exist. They don't prove each instruction inside the skill was followed. Add checks inside a skill only where skips actually happen.
- A pipeline that spans sessions needs each session ID on the checklist's `Claude Code session ID:` line, separated by commas, or earlier steps show as missing.
- The `read` check matches shell commands by pattern. A command that only mentions `cat <skill path>` inside a string, after a `;`, `&&`, `|`, or `(`, still counts as a read. Writing such a string is rare outside work on this checker itself.
- The checker finds transcripts by session ID under `~/.claude/projects/`. Claude Code's transcript format isn't a published contract, so a format change shows every transcript check as ❌. That fails safe: the report shows missing evidence, never false evidence.
- The `pr_body` check needs `gh` and the network. Without them it's ⚠️ unverified.
