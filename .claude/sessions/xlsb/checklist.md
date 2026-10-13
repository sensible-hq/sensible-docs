# xlsb docs checklist

Claude Code session name: xlsb
Claude Code session ID: 1e71441a-3c84-48a0-baa5-c36aac379bbb
Source PR: sensible-hq/sensible#3474 (Accept xlsb workbooks as a spreadsheet input)
Frontend PR: sensible-hq/sensible-app#1882 (Frontend side of xlsb support)
Docs PR: sensible-hq/sensible-docs#741, draft until the #741 decision (branch `fe_xlsb_docs`, worktree `~/GitHub/sensible-docs-xlsb`)

## Status (2026-10-12)

Docs changes are done. On hold: production testing found that sync API requests with raw XLS,
XLSM, and XLSB bodies fail (gateway bug), so the API reference now claims XLSB works on routes
where it doesn't. Waiting on a decision about whether to hold #741 until engineering fixes it.

## Docs changes

- [x] Read engine PR and diff
- [x] Search docs/ and reference/ for xlsm, xlsx, and spreadsheet MIME types
- [x] Add XLSB to the spreadsheet formats list in concepts/file-types.md
- [x] Add `application/vnd.ms-excel.sheet.binary.macroenabled.12` to request bodies and content-type enums in openapi_extraction.json, openapi_classification.json, openapi_configuration.json (`PostGolden`)
- [x] Vale: PostToolUse hook ran on file-types.md. The only new alert is Google.Acronyms on "XLSB", same as XLSX/XLS/XLSM beside it; left as is
- [x] Confirm the Extract tab accepts .xlsb: yes, sensible-app#1882 (merged) adds it to the upload pickers
- [x] Open docs PR #741

## Labels and skills

- [x] Rename sensible-app doc labels to match sensible (`doc_changes_needed`, `docs_done`, `docs_dont_publicly_doc`), add `docs_future_not_yet_blocked`
- [x] Add `doc_changes_needed` to sensible#3474 and sensible-app#1882
- [x] Update `close-docs-pr` (and `update-docs-from-pr`) to swap labels on sensible-app PRs too

## Production API testing

- [x] Smoke test: `scripts/test/file_types/smoke_test_xlsb.sh`, 13 checks, prints full curl commands and a PASS/FAIL summary table flagging changes from the 2026-10-12 baseline
- [x] Sample: `scripts/test/assets/xlsb_sample.xlsb` (from sensible#3474 `tests/data/test.xlsb`; metadata name shortened to "Ben K")
- [x] Results, confirmed in 3 runs (2 by Claude, 1 by Frances): 6 pass, 7 fail
- [x] Checked specs, docs, and engine PR history for known limitations: none; all three bugs look like oversights
- [x] Bug report with TL;DR and results table: `.claude/sessions/xlsb/eng-bug-report.md`

## Next steps

- [ ] Frances: file the bugs with engineering (bug report TL;DR works as the summary)
  - Bug 1 (high): gateway `binaryMediaTypes` omits XLS, XLSM, XLSB → sync /extract, /classify, /classify/async drop the body
  - Bug 2 (medium): /classify rejects CSV (handler reads only binary bodies)
  - Bug 3 (low–medium): content type check is case-sensitive (`macroEnabled` → 415)
  - Unverified: `.xls` maps to the XLSX content type in `DOCUMENT_CONTENT_TYPE_FOR_EXTENSIONS`
- [ ] Frances: decide on #741
  - Option A: hold until Bug 1 is fixed, re-run the smoke test, then merge
  - Option B: merge now with a known-issue note on file-types.md (extraction: use upload URLs or base64 JSON; classification of XLS/XLSM/XLSB/CSV not available)
- [ ] After a fix ships: re-run the smoke test; expect checks 1, 2, 3, 6, 8 to flip to PASS (marked CHANGED)
- [ ] After merge: run close-docs-pr (swaps labels on sensible#3474 and sensible-app#1882, removes the worktree)
