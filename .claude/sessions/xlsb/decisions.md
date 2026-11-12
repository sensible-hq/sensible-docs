# xlsb session: progress and decisions

Claude Code session name: xlsb
Claude Code session ID: 1e71441a-3c84-48a0-baa5-c36aac379bbb
Resume: `cd /home/franc/GitHub/sensible-docs && claude --resume 1e71441a-3c84-48a0-baa5-c36aac379bbb`
Checklist: `.claude/sessions/xlsb/checklist.md` · Bug report: `.claude/sessions/xlsb/eng-bug-report.md`
PRs: sensible-docs#741 (this branch, `fe_xlsb_docs`), sensible-docs#749 (`add-doc-tests` skill, branch `doc-test-skill`)
Sources: sensible-hq/sensible#3474 (engine), sensible-hq/sensible-app#1882 (app upload pickers)

## Where things stand (2026-11-10)

- #741 is ready for review: docs, specs, a smoke test, two embedded tests, a docs-test runner extension, and a saved HTML report.
- Open: Frances reviews #741 and the saved report, then merges; then `close-docs-pr`. #749's skill depends on #741's markup, so #741 merges first.
- Not covered by CI: no workflow runs the file-types.md tests. They run by hand with `run.sh`.

## Progress log

### 2026-10-12
- Read sensible#3474: XLSB (`application/vnd.ms-excel.sheet.binary.macroenabled.12`) added as a spreadsheet input.
- Added XLSB to `file-types.md` and to every spec list that had XLSM. Opened #741.
- sensible-app#1882 (merged) adds XLSB to the app's upload pickers, so the Extract tab claim holds.
- Renamed sensible-app's doc labels to match sensible's, labeled #3474 and #1882 `doc_changes_needed`, and taught `close-docs-pr` to swap labels on app PRs.
- Tested production: raw XLSB, XLSM, and XLS bodies to `/extract`, `/classify`, and `/classify/async` fail with "Missing request body". The engine reads XLSB fine (XLSB bytes sent as XLSX work), and upload-URL and base64 JSON routes work.
- Found the cause in the engine repo: API Gateway `binaryMediaTypes` (`packages/infra-stage-ephemeral/infra/gatewayV1.ts`) omits XLS, XLSM, and XLSB. Also: `/classify` rejects CSV (its handler reads only binary bodies), and content types are case-sensitive (`macroEnabled` gets 415).
- Checked specs, docs, and the XLS (#2739) and XLSM (#3100) PRs: nothing frames these as known limitations.
- Wrote the smoke test (`scripts/test/file_types/smoke_test_xlsb.sh`) and the bug report; Frances posted the report on #3474. Converted #741 to draft.

### 2026-10-13 to 2026-11-10
- Engineering's reply (relayed in a comment on #741): "not sure if it's worth to fix it. Let's keep it as a known limitation, and we can enable it when/if needed." No gateway change landed.

### 2026-11-10
- Merged v0 into the branch (70 commits behind; kept this branch's session pointer files).
- Documented the limitations: footnotes on `file-types.md`, spec request bodies trimmed to what works, endpoint descriptions updated.
- Switched the smoke test to `SENSIBLE_TEST_API_KEY` and the test account's doc types; it now flags CHANGED when the API stops matching the docs.
- Marked #741 ready for review.
- Positive-control classification tests (a doc type whose description matches the samples) showed XLS, XLSM, and XLSB **do** classify when sent as XLSX or as `application/pdf` (what the Python SDK sends). Only CSV never classifies. Rewrote footnote 3 and the classify descriptions.
- Added an `x-internal-note`: without a content type, Sensible detects XLSB as XLSX.
- Extended the docs-test runner with classification claims, wrote two embedded tests under footnote 3, and saved the HTML report. Moved them from a temporary doc type to a persistent fixture, `fixture_spreadsheet_classify`, and added curl commands and file links to the report.
- Wrote the `add-doc-tests` skill on #749.

### 2026-11-11
- Split the work: test infrastructure moved to #803 (with CI by priority: 1 weekly, 2 monthly, 3 on demand); this PR is the XLSB docs. #803 merges first; then file-types.md goes into `test-pages.json` as priority 3.
- Started replacing the abstract test spreadsheets with a commission statement (Frances rejected invoice and rent roll examples): CSV written and uploaded to the test account as `fixture_commission_statements`; XLS, XLSM, XLSB need SheetJS (install blocked by the auto-mode classifier) or Excel.

## Decisions

| Date | Decision | Why | Who |
| --- | --- | --- | --- |
| 2026-10-12 | Worktree `~/GitHub/sensible-docs-xlsb`, branch `fe_xlsb_docs` | update-docs-from-pr convention | Claude |
| 2026-10-12 | Rename sensible-app doc labels to sensible's names and colors; keep the app's richer descriptions | One label set across repos, so `close-docs-pr` handles both | Frances |
| 2026-10-12 | `close-docs-pr` swaps labels on sensible-app PRs too; the change ships in #741 | Frances asked; PR #741 is where it came up | Frances |
| 2026-10-12 | Read the API specs with `jq` to build test requests, not the sensible-docs MCP or `scripts/test` | The branch's specs are the source of truth; the MCP serves the published (older) reference | Claude, Frances agreed |
| 2026-10-12 | Smoke test in `scripts/test/file_types/`, rewritten to print full curl commands with a summary table | Frances wanted readable requests and results at a glance | Frances |
| 2026-10-12 | Shorten "Ben Kogan" to "Ben K" in test sample metadata | The repo is public | Frances |
| 2026-10-12 | Hold #741 as a draft until engineering answers | The spec claimed XLSB works on routes where it fails | Frances |
| 2026-11-10 | Treat the failures as known limitations, not bugs to fix | Engineering: "keep it as a known limitation, and we can enable it when/if needed" | Engineering, via Frances |
| 2026-11-10 | Spec: remove request body types that never work (XLS, XLSM, XLSB from sync extract; those plus CSV from classify); keep them in `ContentTypeParameter` and `PostGolden` | The spec should list only what works; base64 JSON, upload URLs, and reference uploads do work | Frances ("Remove broken types") |
| 2026-11-10 | Smoke test uses `SENSIBLE_TEST_API_KEY` only | Test runs must touch only the test account | Frances (standing rule) |
| 2026-11-10 | No public docs about XLSB being detected as XLSX; record it in an `x-internal-note` | Nothing a reader does depends on it | Frances |
| 2026-11-10 | Footnote 3: Sensible doesn't classify CSV; XLS, XLSM, XLSB classify when sent with the XLSX content type; the Python SDK works as is | Positive-control tests; documents a format-detection behavior engineering hasn't explicitly endorsed | Frances ("CSV only + workaround") |
| 2026-11-10 | Test the classification claim with embedded code tests in the existing report, not pytest or a contract test | Frances wanted a committed HTML report from the existing tooling | Frances |
| 2026-11-10 | Extend the runner with `expect {"compare": "classification"}` and `CLASSIFICATION_DRIFT` | The runner only extracted; no existing markup could send a file to `/classify` | Claude, Frances agreed |
| 2026-11-10 | Save scrubbed reports to `scripts/doc-detective/reports/` with `DOC_TESTS_SAVE_REPORT=1`, only after a clean leak check | Frances wanted a committed report that changes only on rerun | Frances |
| 2026-11-10 | Classify against a persistent fixture (`fixture_spreadsheet_classify`) with the XLSB as its reference document; allow spreadsheet reference documents | Frances wanted to open the doc type in the app | Frances |
| 2026-11-10 | Report shows each request's curl command (key as `$SENSIBLE_TEST_API_KEY`) and links test files relative to the report | Frances wanted to see the requests and the documents | Frances |
| 2026-11-11 | Test infrastructure in its own PR (#803), merged before this one | Frances: separate infra from the XLSB docs | Frances |
| 2026-11-11 | Test spreadsheets show a realistic business document: an insurance commission statement (not an invoice or rent roll), with a fixture named for it | Frances wanted realistic, new examples; based on the configuration library's commission statement | Frances |
| 2026-11-10 | `add-doc-tests` skill goes on #749 with its concept; runner change, fixture, and tests go on #741 | The docs claim and its test ship together; the skill builds on the concept | Claude (Frances didn't object) |
| 2026-11-11 | Embedded code tests removed from `file-types.md`, and the page dropped from `test-pages.json`; the fixture, test files, and saved report stay | Frances wants #741 free of docs changes, with the docs shipped clean in #809; the tests get reimplemented later in the new approach (lines saved in checklist.md) | Frances, via the google-ocr session |
| 2026-11-11 | Swap the classification fixture to the commission statement now, with `xlsb_sample.xlsb` as a placeholder; every "not classified" request gets a same-file control that classifies | Frances deferred the XLSB; the live check showed a 400 can mean a content mismatch, not an unsupported format | Frances (defer), Claude (control) |

## Things that turned out wrong along the way

- The first bug report called #741 merged when it wasn't; fixed the same day.
- The first footnote 3 said Sensible doesn't classify XLS, XLSM, or XLSB. Positive-control tests showed they classify when not declared with their own content types.
- Every test run before 2026-11-10 used `SENSIBLE_API_KEY` (the production account), against Frances's test-key rule. All runs since use `SENSIBLE_TEST_API_KEY`.
- The first fixture run failed: Sensible adds `ocr_engine: "amazon"` to new doc types, so the committed file now includes it, as the other fixtures do.

## Open questions

- Node SDK: does its `classify` work for XLS, XLSM, XLSB like the Python SDK? Not checked.
- Unverified: `.xls` maps to the XLSX content type in the engine's `DOCUMENT_CONTENT_TYPE_FOR_EXTENSIONS`, used for email attachments. Not tested; not documented.
- Should a CI workflow run the file-types.md tests (about 9 classify calls, no extractions)?
