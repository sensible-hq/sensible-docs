# google-ocr progress log

Claude Code session ID: bc2d327b-1002-40d8-9161-f39ecf5a8273. Newest entries last. All dates 2026-11-10.

## Lazarus deprecation
- Read sensible-hq/sensible#3468 and its thread. Frances's call (comment 6774748323): changelog item, deprecate Lazarus in the OCR engine table, remove it from the intro, drop it from the OpenAPI enum with an `x-internal-note`.
- Opened docs PR #798. Frances tightened the Lazarus row and changed the excerpt; Claude restored "extracting text from images" wording on request.
- Claude wrongly "corrected" the doc type default to Microsoft based on the engine's unset-value fallback and the app's help text. Frances pointed out Amazon is the default for new doc types. Confirmed in sensible-app: `DocumentType.ts:219` and `QuickStartFullModal.tsx:102` store `ocr_engine: "amazon"`. Reverted, and recorded the rule in the `ocr_engine` `x-internal-note`.
- Opened sensible-app#1905 to fix the "Microsoft is the default engine" help text.
- Ran Vale, JSON, frontmatter YAML, Redocly (same 1 warning as v0), CI. Squash-merged #798 as 457c445be.
- close-docs-pr: local cleanup done; issue creation and the engine label swap were blocked by the permission classifier.

## Google OCR page limit
- Docs said "5 pages or fewer"; app said 25 pages.
- Code history of `readers/google.ts`: sensible#1120 (2022-05-26) added 5-page chunks, 5 concurrent, looping over all chunks. `batchAsyncCalls` (then `src/common.ts`, now `src/common-node.ts`) never truncates. No later commit added a cap.
- Grepped a sparse clone of the engine `src/`: no document page cap; only user-configured `maxPages` (Page Filter), `pageLinesLimit` (OCR preprocessor), Amazon's 5 MB sync threshold, a response-size 413, and the Google rate limiter (~120 pages/min).
- Slack: #engineering 2022-06-03 thread (Josh's release notes "Google OCR support for up to 25 pages"); Frances filed sensible-app#541 to update the UI text to 25.
- Test in the test account (doc type later renamed to the fixture): 72-page Beazley quote rasterized at 150 DPI with Ghostscript (0 extractable words).
  - Google, default merging: all 7 markers through page 72, ~23 s.
  - Google, `prevent_default_merge_lines: true`: single-word values, so the output is Google's.
  - Amazon control, same setting: whole lines.
- Frances edited the test config (Merge Lines preprocessor, phrase anchors, 4 fields) and asked to make it a fixture.
- Renamed in place: doc type `fixture_ocr_google_page_limit`, config `fixture_page_markers`, reference `fixture_beazley_scanned_72_pages`. Published comment-free config to production. Rerun: 4/4 fields, p72 = "Page 22 of 22".
- Docs PR #801: Google row fix, fixture files under `scripts/test/probe_endpoints/contract/fixtures/ocr_engine/`, PDF. Runner `fixture_drift`: no drift.
- App PR #1906 (stacked on #1905): Google help text fix in both components.

## 2026-11-11
- Moved the fixture PDF from `assets/pdfs/` to `scripts/test/assets/` (Frances: `assets/pdfs/` is only for docs PDFs). Runner now accepts fixture PDFs from either folder (`FIXTURE_PDF_DIRS`); updated `test_markup.py` and the README. `tests.test_markup` passes; fixture drift check still clean. 6 unrelated test failures also happen without this change (missing `anthropic` and `sensibleapi` modules locally).
- Frances: keep fixture PDFs fully separate from `assets/pdfs/`, and name the folder so it's clearly for fixtures. Fixture PDFs now live only in `scripts/test/fixture_pdfs/` (runner `FIXTURE_PDFS_DIR`); `portfolio.pdf` and `portfolio_bank_paystub_tax.pdf` copied there from `assets/pdfs/` for the fingerprint fixtures; fingerprint workflow watches the copies. Blank page stays in `assets/pdfs/` (docs code tests use its v0 URL).
