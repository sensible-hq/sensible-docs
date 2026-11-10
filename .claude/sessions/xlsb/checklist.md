# xlsb docs checklist

Claude Code session name: xlsb
Claude Code session ID: 1e71441a-3c84-48a0-baa5-c36aac379bbb
Source PR: sensible-hq/sensible#3474 (Accept xlsb workbooks as a spreadsheet input)
Frontend PR: sensible-hq/sensible-app#1882 (Frontend side of xlsb support)
Docs PR: sensible-hq/sensible-docs#741, ready for review (branch `fe_xlsb_docs`, worktree `~/GitHub/sensible-docs-xlsb`)

## Status (2026-11-10)

Engineering decided to keep the failing cases as known limitations (comment on #741). Docs,
specs, and the smoke test now describe them. Ready for Frances's review; then mark #741 ready
and merge.

History: on 2026-10-12, production testing found that sync API requests with raw XLS, XLSM, and
XLSB bodies fail (gateway `binaryMediaTypes`), `/classify` rejects CSV, and content types are
case-sensitive. Reported on sensible#3474.

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

## Known limitations (2026-11-10)

- [x] Bugs reported on sensible#3474 (2026-10-12); engineering: keep as known limitations
- [x] Merge v0 into the branch (kept this branch's session pointer files)
- [x] file-types.md: footnote 1 (XLS/XLSM/XLSB extraction: async endpoints or base64 JSON for sync; lowercase content types), footnote 3 (classification: XLSX only); renumbered existing footnotes 1–3 to 2, 4, 5 without changing their text
- [x] Specs: removed XLS/XLSM/XLSB from extraction `SupportedFileTypes`, and those plus CSV from classification `SupportedFileTypes`; added a sentence to the sync extract and both classify descriptions; kept `ContentTypeParameter` and `PostGolden`
- [x] Style pass: writing-rules, glossary, friction log, style overview, sentence guidance, concept template, editorial preferences, revise-doc-style (skipped blog, changelog, integration, config-library templates and JSON5 reference: not applicable)
- [x] Smoke test: SENSIBLE_TEST_API_KEY (was SENSIBLE_API_KEY), test account doc types (layout_basics, 1040s, auto_insurance_quotes), limitation framing; run on the test account: 6 pass, 7 fail, 0 changed
- [x] Bug report: resolution section
- Not documented: the unverified `.xls` → XLSX mapping for email attachments (never tested)

## Classification is a workaround, not a limitation (2026-11-10)

- [x] Positive-control tests (temporary doc type with a matching description): XLS, XLSM, XLSB classify when sent as XLSX or as `application/pdf` (what the Python SDK sends); they fail only with their own content types. CSV never classifies. Footnote 3 and the classify descriptions had overstated it
- [x] Footnote 3 rewritten (Frances chose "CSV only + workaround"); classify descriptions updated
- [x] `x-internal-note` on `ContentTypeParameter`: without a content type, Sensible detects XLSB as XLSX
- [x] Embedded tests under footnote 3: `classify_excel_formats_as_xlsx` (7 requests), `classify_csv_not_supported` (2); both pass on the test account
- [x] Runner extension: `expect {"compare": "classification"}`, `CLASSIFICATION_DRIFT`, record schema, HTML/text/summary reports, 10 unit tests (209 total pass), README
- [x] `run.sh` saves the scrubbed report with `DOC_TESTS_SAVE_REPORT=1`: `scripts/doc-detective/reports/docs-senseml-reference-concepts-file-types.html`
- [x] Test samples in `scripts/test/assets/`: `xls_sample.xls`, `xlsm_sample.xlsm` (engine test data, metadata name shortened to "Ben K"), `csv_sample.csv`
- [x] `add-doc-tests` skill written on #749 (depends on this PR's markup)
- [x] Report: classification runs against a persistent fixture, `fixture_spreadsheet_classify` (linked to the SenseML editor, with the XLSB as its reference document); each request shows its curl command; files link relative to the report. Fixture reference documents can be spreadsheets now
- Not run in CI: no workflow covers file-types.md yet

## Next steps

- [ ] Frances: review the docs, spec, and tooling diff on #741, and the saved report
- [ ] Merge #741
- [ ] After merge: run close-docs-pr (swaps labels on sensible#3474 and sensible-app#1882, removes the worktree)
- [ ] If engineering enables any of these later: the smoke test shows CHANGED rows; update file-types.md and the specs
