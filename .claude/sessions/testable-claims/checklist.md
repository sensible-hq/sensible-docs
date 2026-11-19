# testable-claims checklist

Claude Code session name: ocrIfMissing
Claude Code session ID: 0ded2aae-03f7-4ca1-bf75-b37050ab318e
PR: sensible-hq/sensible-docs#834 (draft), branch `testable-claims-skill`, worktree `~/GitHub/sensible-docs-testable-claims`
Decisions and progress: `decisions.md` · Design proposal: `design.md` · Evidence: `evidence/README.md`

## Status (2026-11-19)

The `extract-testable-claims` skill is built and was tried on #825. The durable-evidence design (record-only priority, pointer comment, evidence records, review step) is a proposal with open questions; nothing of it is built. Start with `design.md`'s open questions.

## Done

- [x] `extract-testable-claims` skill: criteria, Jev noul scorer, calibration cases, steps for evidence and proposed tests
- [x] Calibrated (14 cases, Claude-labeled)
- [x] Dry run on #825; tests for two claims run with controls; results and configs saved in `evidence/`
- [x] Design proposal with reasons, conflicts, and open questions (`design.md`)

## To do

- [ ] Frances reviews `cases.yaml` labels; add real sentences from docs pages
- [ ] Frances answers `design.md`'s open questions
- [ ] Add the review step to `extract-testable-claims/SKILL.md` (Frances approves matrix entries and the pointer comment before anything is written)
- [ ] Evidence record schema and folder (`scripts/doc-detective/evidence/`)
- [ ] Runner reads the pointer comment as a pointer, not a test (so it doesn't count as "not run")
- [ ] `test_matrix.py` reads evidence records; a record-only row shows evidence date and report link
- [ ] Report generated from an evidence record, saved in `reports/`
- [ ] First evidence records: the three #825 claims in `evidence/README.md`, then the pointer comment on the OCR page (after Frances approves)
- [ ] Optional, per open question 4: `contrast` and `schema` code-test kinds
- [ ] Unit tests for each piece; README "Extending it" updated
- [ ] Mark the skill PR ready for review once the review step exists

## Elsewhere, from the same session (for context)

- #825 (OCR page, `ocrIfMissing`): draft; don't merge until sensible-hq/sensible#3533 deploys. Its own checklist: `.claude/sessions/ocr-if-missing/checklist.md` on branch `ocr-omit-quote-example`.
- #831 (`update-schema-descriptions` skill and a sandbox guard fix): draft. Frances questioned whether schema descriptions come from `/** */` comments; Claude traced every published description to doc comments in `types.ts`. Unresolved whether she agrees.
- `eng-page-range-bug.md`: draft message for horacio-penya, not sent.
- Port `example-claims` (style rule and Jev noul support) in `fscelliott/sensible-docs-private`, `ports/example-claims/`: applies cleanly to `v0`; not applied.
- Test doc types in Frances's production account: `ocr_omit_*` (4), `ocr_array_*` (2), `claims_*` (10). In dev: `ocr_if_missing_quote`. Delete when no longer needed as proof.
