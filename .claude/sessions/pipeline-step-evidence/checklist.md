# Checklist: step evidence for pipeline-for-pr

Claude Code session name: Orchestration skill for PR responses
Claude Code session ID: 3c110100-6543-4507-8dcd-b3e7e1dcf7e3
Branch: `pipeline-step-evidence`, worktree `../sensible-docs-pipeline-step-evidence`

Frances (2026-11-24): every pipeline handoff should carry evidence that the step ran, with links she can verify. Agreed approach: a script checks the evidence, not the agent, and a Stop hook enforces it. Make the design calls, test as you go, open a PR when done.

- [x] Design (`design/pipeline-step-evidence/design.md`)
- [x] Evidence spec for steps 1–8 (`.claude/skills/pipeline-for-pr/evidence.yaml`)
- [x] Checker `scripts/pipeline/step_evidence.py`
- [x] Stop hook `.claude/hooks/pipeline_evidence_gate.py`, registered in `.claude/settings.json`
- [x] Tests: 26 pass in `scripts/pipeline/test/`; the suite is added to the `Test scripts` workflow
- [x] Mutation check: breaking the read ordering, the commit window, the verbatim match, or the `stop_hook_active` guard each fails a test
- [x] Live run against this session's transcript. It found two false positives, fixed: a partial `sed -n` read and a `cat` inside a heredoc string both counted as reading the skill
- [x] Skill and checklist template: evidence block in every report, the `Skipped:` field, session IDs separated by commas, and step 7 no longer says `add-doc-tests` is unmerged
- [x] Implementation notes (`design/pipeline-step-evidence/implementation.md`)
- [x] PR opened: sensible-docs#849
- [ ] First real pipeline run with the hook on: confirm the transcript already holds the final message when `Stop` fires. Until that's confirmed, `last_assistant_message` from the hook input is the fallback
