# testable-claims checklist

Claude Code session name: ocrIfMissing
Claude Code session ID: 0ded2aae-03f7-4ca1-bf75-b37050ab318e
Resumed in session ID: 182a711b-cc3c-4499-b338-54f7a8efa58c
PR: sensible-hq/sensible-docs#834 (draft), branch `testable-claims-skill`, worktree `~/GitHub/sensible-docs-testable-claims`
Decisions and progress: `decisions.md` · Design proposal: `design.md` · Evidence: `scripts/doc-detective/testable-claims/pr-825-ocr-if-missing/` on #825

## Status (2026-11-19)

Frances answered `design.md`'s open questions. The record-only path is built: evidence schema and checks, per-section pointer comment, matrix rows, stale warning, SQLite load, and the skill's review step. The three #825 records are approved and committed on #825 in `scripts/doc-detective/testable-claims/pr-825-ocr-if-missing/`, with the test material that produced them.

## Done

- [x] `extract-testable-claims` skill: criteria, Jev noul scorer, calibration cases, steps for evidence and proposed tests
- [x] Calibrated (14 cases, Claude-labeled)
- [x] Dry run on #825; tests for two claims run with controls; results and configs saved in `scripts/doc-detective/testable-claims/pr-825-ocr-if-missing/` on #825
- [x] Design proposal with reasons, conflicts, and open questions (`design.md`)

## To do

- [ ] Frances reviews `cases.yaml` labels; add real sentences from docs pages
- [x] Frances answers `design.md`'s open questions
- [x] Review step in `extract-testable-claims/SKILL.md`; skill now names `SENSIBLE_TEST_API_KEY`
- [x] Evidence schema (`schemas/evidence.schema.json`) and checks (`codetests/evidence.py check`, unit test on committed records)
- [x] Runners ignore the pointer comment (unit test)
- [x] `test_matrix.py` lists records in a Record-only claims section (links the record JSON)
- [x] CI stale warning (183 days, annotation only)
- [x] SQLite load (`evidence.py sqlite`), shaped for Frances's future database
- [x] Unit tests; README section and Extending it row
- [x] Frances approved the three #825 records (2026-11-19); records and the Parameters comment are committed on #825, which must merge after this PR
- [ ] After #3533 deploys: rerun the three claims in the docs test account with `ocrIfMissing`, as new records
- [ ] `schema` code-test kind (next), then `contrast`
- [ ] Report generated from an evidence record (HTML), if the JSON link isn't enough
- [ ] Mark the skill PR ready for review

## Elsewhere, from the same session (for context)

- #825 (OCR page, `ocrIfMissing`): draft; don't merge until sensible-hq/sensible#3533 deploys. Its own checklist: `.claude/sessions/ocr-if-missing/checklist.md` on branch `ocr-omit-quote-example`.
- #831 (`update-schema-descriptions` skill and a sandbox guard fix): draft. Frances questioned whether schema descriptions come from `/** */` comments; Claude traced every published description to doc comments in `types.ts`. Unresolved whether she agrees.
- `eng-page-range-bug.md`: draft message for horacio-penya, not sent.
- Port `example-claims` (style rule and Jev noul support) in `fscelliott/sensible-docs-private`, `ports/example-claims/`: applies cleanly to `v0`; not applied.
- Test doc types in Frances's production account: `ocr_omit_*` (4), `ocr_array_*` (2), `claims_*` (10). In dev: `ocr_if_missing_quote`. Delete when no longer needed as proof.
