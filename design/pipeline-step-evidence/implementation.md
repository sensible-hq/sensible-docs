# Implementation: step evidence for pipeline-for-pr

The design is in `design.md` beside this file.

## Files

| File | What it does |
|---|---|
| `.claude/skills/pipeline-for-pr/evidence.yaml` | The checks for each step. Edit it when a step's skill changes what it reads, runs, or produces. |
| `scripts/pipeline/step_evidence.py` | The checker. Prints the evidence block for the current step, or `--json`. Exits 0 when every check passes, 1 otherwise. |
| `.claude/hooks/pipeline_evidence_gate.py` | The `Stop` hook. Imports the checker, and blocks a pipeline session's stop until the current block has been shown. |
| `.claude/settings.json` | Registers the hook under `Stop`. |
| `.claude/skills/pipeline-for-pr/SKILL.md` | Tells the agent to end each report with the block, to mark skipped steps with `Skipped:`, and to list every session's ID. |
| `.claude/skills/pipeline-for-pr/checklist-template.md` | The same conventions, in the checklist the checker reads. |
| `scripts/pipeline/test/test_step_evidence.py` | Tests for the checker and the hook. Runs in the `Test scripts` workflow. |

## Running it by hand

```
python3 scripts/pipeline/step_evidence.py --checklist .claude/sessions/<session>/checklist.md
python3 scripts/pipeline/step_evidence.py --checklist <checklist> --step 3 --json
```

## Adding a check

Add an entry under the step in `evidence.yaml`. The kinds are `read`, `bash`, `file`, `commit`, `pr_body`, and `checklist`, described in `design.md`. Patterns are Python regular expressions; `{engine_pr}`, `{docs_pr}`, and `{branch}` fill in from the checklist header, escaped. A kind that doesn't exist yet needs a branch in `check()` in `step_evidence.py` and a test.

## Testing

```
cd scripts/pipeline/test && python3 -m pytest -q
```

The tests build a throwaway git repo, a checklist from the real template, and a fake transcript, then run the script and the hook as subprocesses. `gh` is a stub on `PATH`. Each test covers a way a step could be skipped and still look done: a read from an earlier step reused, a partial read, a commit from before the step, an edited evidence block, a different PR number.
