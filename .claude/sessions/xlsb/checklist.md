# xlsb docs checklist

Claude Code session name: xlsb
Claude Code session ID: 1e71441a-3c84-48a0-baa5-c36aac379bbb
Source PR: sensible-hq/sensible#3474 (Accept xlsb workbooks as a spreadsheet input)
Frontend PR: sensible-hq/sensible-app#1882 (Frontend side of xlsb support)
Docs PR: sensible-hq/sensible-docs#741, ready for review (branch `fe_xlsb_docs`, worktree `~/GitHub/sensible-docs-xlsb`)

Decisions and progress log: `.claude/sessions/xlsb/decisions.md`

## Status (2026-11-10)

#741 is ready for review. Engineering decided to keep the failing API cases as known limitations
(comment on #741), and the docs, specs, smoke test, and embedded tests now describe them.
Classification turned out to be a workaround, not a limitation, for XLS, XLSM, and XLSB; only CSV
can't be classified.

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
- [x] file-types.md: footnote 1 (XLS/XLSM/XLSB extraction: async endpoints or base64 JSON for sync; lowercase content types), footnote 3 (classification: XLSX only; superseded below); renumbered existing footnotes 1–3 to 2, 4, 5 without changing their text
- [x] Specs: removed XLS/XLSM/XLSB from extraction `SupportedFileTypes`, and those plus CSV from classification `SupportedFileTypes`; added a sentence to the sync extract and both classify descriptions (classify sentence superseded below); kept `ContentTypeParameter` and `PostGolden`
- [x] Style pass: writing-rules, glossary, friction log, style overview, sentence guidance, concept template, editorial preferences, revise-doc-style (skipped blog, changelog, integration, config-library templates and JSON5 reference: not applicable)
- [x] Smoke test: SENSIBLE_TEST_API_KEY (was SENSIBLE_API_KEY), test account doc types (layout_basics, 1040s, auto_insurance_quotes), limitation framing; run on the test account: 6 pass, 7 fail, 0 changed
- [x] Bug report: resolution section
- Not documented: the unverified `.xls` → XLSX mapping for email attachments (never tested)

## Classification is a workaround, not a limitation (2026-11-10)

- [x] Positive-control tests (temporary doc type with a matching description): XLS, XLSM, XLSB classify when sent as XLSX or as `application/pdf` (what the Python SDK sends); they fail only with their own content types. CSV never classifies. Footnote 3 and the classify descriptions had overstated it
- [x] Footnote 3 rewritten (Frances chose "CSV only + workaround"); classify descriptions updated
- [x] `x-internal-note` on `ContentTypeParameter`: without a content type, Sensible detects XLSB as XLSX
- [x] Embedded tests under footnote 3: `classify_excel_formats_as_xlsx` (7 requests), `classify_csv_not_supported` (2); both pass on the test account
- [x] Runner extension: `expect {"compare": "classification"}`, `CLASSIFICATION_DRIFT`, record schema, HTML/text/summary reports, unit tests (214 total pass), README
- [x] `run.sh` saves the scrubbed report with `DOC_TESTS_SAVE_REPORT=1`: `scripts/doc-detective/reports/docs-senseml-reference-concepts-file-types.html`
- [x] Test samples in `scripts/test/assets/`: `xls_sample.xls`, `xlsm_sample.xlsm` (engine test data, metadata name shortened to "Ben K"), `csv_sample.csv`
- [x] `add-doc-tests` skill written on #749 (depends on this PR's markup)
- [x] Report: classification runs against a persistent fixture, `fixture_spreadsheet_classify` (linked to the SenseML editor, with the XLSB as its reference document); each request shows its curl command; files link relative to the report. Fixture reference documents can be spreadsheets now
- Not run in CI: no workflow covers file-types.md yet

## Split into two PRs (2026-11-11)

- [x] Runner changes (classification markup, spreadsheet fixtures, curl commands and file links, saved reports) moved to #803 with priority-based CI; this PR keeps the XLSB docs, file-types tests, fixture, samples, smoke test, and saved report
- Commission statement samples: CSV in the worktree (uncommitted) and `fixture_commission_statements` in the test account; waiting on a way to make XLS, XLSM, XLSB (SheetJS install or Excel)

## Restructured (2026-11-11)

- [x] Frances moved the XLSB docs to #809 (no tests, no embedded comments); this PR is now the XLSB tests, stacked on #803 with #809 merged in
- [x] Fixture and test spreadsheets moved to `scripts/doc-detective/fixtures/spreadsheet_classification/`; requests name bare files in that folder
- [x] file-types.md added to `test-pages.json` at priority 3; TEST-MATRIX.md regenerated
- [x] Saved evidence rerun on a clean commit (eb0d6704b): both classification tests pass
- [x] Draft commission statement CSV untracked (committed by mistake)

## Embedded tests removed from file-types.md (2026-11-11)

Frances wants #741 free of docs changes, with the XLSB docs shipped clean in #809, and is rewriting the test approach in another session. So `file-types.md` here now matches #809 exactly, and the page's entry is out of `test-pages.json` (a listed page with no tests would run an empty job).

Still in this PR, for when the tests come back: the fixture and test spreadsheets (`scripts/doc-detective/fixtures/spreadsheet_classification/`), and the saved report and results from the last run (`reports/docs-senseml-reference-concepts-file-types.{html,json}`, both tests passing at commit eb0d6704b). That report is the evidence that the claims held on 2026-11-11. `TEST-MATRIX.md` no longer lists the page.

The removed lines, verbatim. They went under footnote 3, indented three spaces:

```markdown
   <!-- code test {"testId": "classify_excel_formats_as_xlsx", "description": "XLS, XLSM, and XLSB classify when sent as XLSX or by the Python SDK, but not with their own content types"} -->
   <!-- fixture {"name": "fixture_spreadsheet_classify"} -->
   <!-- expect {"compare": "classification", "requests": [{"file": "xls_sample.xls", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": true, "label": "XLS sent as XLSX"}, {"file": "xlsm_sample.xlsm", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": true, "label": "XLSM sent as XLSX"}, {"file": "xlsb_sample.xlsb", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": true, "label": "XLSB sent as XLSX"}, {"file": "xlsb_sample.xlsb", "content_type": "application/pdf", "classified": true, "label": "Python SDK (sends application/pdf)"}, {"file": "xls_sample.xls", "content_type": "application/vnd.ms-excel", "classified": false, "label": "XLS with its own content type"}, {"file": "xlsm_sample.xlsm", "content_type": "application/vnd.ms-excel.sheet.macroenabled.12", "classified": false, "label": "XLSM with its own content type"}, {"file": "xlsb_sample.xlsb", "content_type": "application/vnd.ms-excel.sheet.binary.macroenabled.12", "classified": false, "label": "XLSB with its own content type"}]} -->
   <!-- code test end -->
   <!-- code test {"testId": "classify_csv_not_supported", "description": "Sensible doesn't classify CSV files"} -->
   <!-- fixture {"name": "fixture_spreadsheet_classify"} -->
   <!-- expect {"compare": "classification", "requests": [{"file": "csv_sample.csv", "content_type": "text/csv", "classified": false, "label": "CSV"}, {"file": "csv_sample.csv", "content_type": "application/pdf", "classified": false, "label": "Python SDK (sends application/pdf)"}]} -->
   <!-- code test end -->
```

- [x] (2026-11-12, `fe_file_types_tests`) Restored the updated tests below to `file-types.md`, with the XLSX control, and added `file-types.md` back to `test-pages.json`; both pass, saved report at commit e3057fb48. Originally: reimplement these tests in the new test approach, then add `file-types.md` back to `test-pages.json` (it was priority 3, name `file-types`, issue label `doc-tests-file-types`, timeout 10)

## Commission statement spreadsheets (decided 2026-11-11)

Frances chose LibreOffice for XLSX, XLS, and XLSM, and Excel by hand for XLSB (LibreOffice can only import XLSB). No SheetJS. The XLSM is the macro-enabled container only, with no macros. Source: `scripts/test/assets/commission_statement.csv` (untracked).

- [x] Frances: `sudo apt install libreoffice-calc`
- [x] Converted with `fixtures/spreadsheet_classification/make_spreadsheets.py` (2026-11-11), not plain `soffice --convert-to`: that dropped the number formats, so money showed as `4200` instead of `4,200.00`. The script sets `#,##0.00` and `0%`; all three files now display exactly like the CSV (checked by exporting each back to CSV as shown). The XLSM is macro-enabled with no VBA parts. The files are in `scripts/test/assets/` (untracked) until the XLSB is ready
- [x] ~~Frances: save `commission_statement.xlsb` from Excel next to the CSV~~ (Excel expired; converted with SheetJS instead, below)
- [x] Moved the CSV, XLSX, XLS, and XLSM into the fixture folder, replacing `csv_sample.csv`, `xls_sample.xls`, and `xlsm_sample.xlsm`. The doc type's description now describes a commission statement; the reference document is `commission_statement.xlsx`. `xlsb_sample.xlsb` stays as a placeholder (the smoke test uses it too)
- [x] XLSB (2026-11-11): Frances's Excel license had expired, so it was converted from the XLSX once with SheetJS CE 0.20.3 (Apache-2.0), installed outside the repo (commands in `make_spreadsheets.py`). It's a real binary workbook and displays exactly like the CSV. It's now the fixture's reference document; `xlsb_sample.xlsb` is deleted, and the smoke test uses the new file
- [x] Live check with the saved test lines below: all 12 requests behave as documented, including the XLSB rows that failed with the placeholder. Smoke test: 13 of 13 checks match the documented behavior

**Finding from the live check (2026-11-11):** a 400 "No match found" from `/classify` doesn't separate "unsupported format" from "the contents don't match the doc type's description". With the commission statement description, `xlsb_sample.xlsb` (the engine's "hello" sheet) isn't classified even as XLSX, so its two "classified" rows failed, and its "not classified" row passed for the wrong reason (fixed once the commission statement XLSB replaced it). So **every "not classified" request needs a control: the same file classified with a supported content type.** The XLSX row in the block below is that control for the commission statement; keep one when reimplementing. Every other request passed: XLSX, and XLS and XLSM sent as XLSX, classify; XLS and XLSM with their own content types, and CSV, don't.

The saved test lines, updated for the commission statement files, with the XLSX control added (the original version is in the section above):

```markdown
   <!-- code test {"testId": "classify_excel_formats_as_xlsx", "description": "XLS, XLSM, and XLSB classify when sent as XLSX or by the Python SDK, but not with their own content types"} -->
   <!-- fixture {"name": "fixture_spreadsheet_classify"} -->
   <!-- expect {"compare": "classification", "requests": [{"file": "commission_statement.xlsx", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": true, "label": "XLSX (control)"}, {"file": "commission_statement.xls", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": true, "label": "XLS sent as XLSX"}, {"file": "commission_statement.xlsm", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": true, "label": "XLSM sent as XLSX"}, {"file": "commission_statement.xlsb", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": true, "label": "XLSB sent as XLSX"}, {"file": "commission_statement.xlsb", "content_type": "application/pdf", "classified": true, "label": "Python SDK (sends application/pdf)"}, {"file": "commission_statement.xls", "content_type": "application/vnd.ms-excel", "classified": false, "label": "XLS with its own content type"}, {"file": "commission_statement.xlsm", "content_type": "application/vnd.ms-excel.sheet.macroenabled.12", "classified": false, "label": "XLSM with its own content type"}, {"file": "commission_statement.xlsb", "content_type": "application/vnd.ms-excel.sheet.binary.macroenabled.12", "classified": false, "label": "XLSB with its own content type"}]} -->
   <!-- code test end -->
   <!-- code test {"testId": "classify_csv_not_supported", "description": "Sensible doesn't classify CSV files"} -->
   <!-- fixture {"name": "fixture_spreadsheet_classify"} -->
   <!-- expect {"compare": "classification", "requests": [{"file": "commission_statement.csv", "content_type": "text/csv", "classified": false, "label": "CSV"}, {"file": "commission_statement.csv", "content_type": "application/pdf", "classified": false, "label": "Python SDK (sends application/pdf)"}]} -->
   <!-- code test end -->
```

## Next steps
- [ ] Merge #803, then #809, then this PR
- [ ] Then add `docs/Senseml reference/concepts/file-types.md` to `scripts/doc-detective/test-pages.json` with priority 3
- [x] (Done 2026-11-11, on this branch, before #803 merged) Move `scripts/test/probe_endpoints/contract/fixtures/spreadsheet_classification/` and the test spreadsheets (`scripts/test/assets/{xls,xlsm,xlsb}_sample.*`, `csv_sample.csv`) into `scripts/doc-detective/fixtures/spreadsheet_classification/`; manifest `"pdf"` → `"file"`; requests' `file` → bare file names; regenerate TEST-MATRIX.md and rerun with DOC_TESTS_SAVE_REPORT=1 (the smoke test keeps reading `scripts/test/assets/xlsb_sample.xlsb`, or points at the moved file)

- [ ] Frances: review the docs, spec, and tooling diff on #741, and the saved report
- [ ] Merge #741
- [ ] After merge: run close-docs-pr (swaps labels on sensible#3474 and sensible-app#1882, removes the worktree)
- [ ] If engineering enables any of these later: the smoke test shows CHANGED rows; update file-types.md and the specs
