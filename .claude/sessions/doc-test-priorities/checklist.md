# doc-test-priorities checklist

Claude Code session name: xlsb (this branch was split off the xlsb session)
Claude Code session ID: 1e71441a-3c84-48a0-baa5-c36aac379bbb
Branch: `fe_doc_test_priorities` · worktree `~/GitHub/sensible-docs-doc-test-priorities` · started 2026-11-11 from `v0`
Decisions and progress: `.claude/sessions/doc-test-priorities/decisions.md`

Goal: docs-test infrastructure in its own PR, separate from the XLSB docs (#741): the runner changes the XLSB tests need, and CI that runs pages by priority.

## Runner changes (moved from #741)

- [x] Classification claims: `expect {"compare": "classification"}` with one fixture, `CLASSIFICATION_DRIFT`, record schema, HTML/text/summary reports with curl commands and file links
- [x] Fixture reference documents can be spreadsheets (`.xlsx`, `.xls`, `.xlsm`, `.xlsb`, `.csv`), under `assets/pdfs/` or `scripts/test/assets/`
- [x] `DOC_TESTS_SAVE_REPORT=1`: `run.sh` keeps the scrubbed report in `scripts/doc-detective/reports/`
- [x] Unit tests build their own temporary repo and fixture (no dependency on #741's files)
- [x] Removed the same changes from #741 (it keeps the docs, file-types tests, fixture, samples, saved report)

## Priority-based CI

- [x] `scripts/doc-detective/test-pages.json`: each tested page with priority 1 (weekly), 2 (monthly), or 3 (on demand only)
- [x] `plan_runs.py`: which pages a run tests (push, schedule, on demand); fails if a page with test markup isn't listed
- [x] `.github/workflows/doc-tests.yml` replaces `doc-detective-getting-started.yml`, `doc-tests-fingerprint.yml`, `doc-tests-portfolio.yml`; same steps per page, pages one at a time, same issue labels
- [x] `check_secrets.py` covers `doc-tests.yml` (glob `doc-tests*.yml`); coverage check passes
- [x] Unit tests for the planner, including that the workflow's crons match the planner's (229 pass)
- [x] README CI section rewritten
- [x] `.gitignore`: `scripts/doc-detective/.deps` ignored as a folder or a symlink

## Review fixes (2026-11-11, review of f2933c834)

- [x] Classification: only 400/415 mean "not classified"; other responses fail as RUNNER_ERROR; request files limited to the test folders (symlinks resolved); curl commands shell-quoted
- [x] CI: test-job concurrency with queue: max; plan-failed issue; empty schedule fails; saved reports/README/matrix don't trigger runs; read-only by default; per-page envelope labels; bare titles; timeout bound; single run.sh call
- [x] Reference uploads: unknown extension fails; spreadsheet upload tested; stale comments, secrets.txt, schema, README fixed
- [x] Saved evidence: provenance in reports and reports/<name>.json; generated TEST-MATRIX.md with a freshness test (247 unit tests pass)
- [x] Rest of the review on the fixed branch: report (`review-803.md`), three rounds of report checks, devil's-advocate pass on every finding (two P1s recalibrated to P2; two non-defects dropped); the last round found and fixed a 200-with-no-name gap (82bead504)
- Deferred to a refactor PR: claim-kind registry, common result shape across runners, `claim: {kind}` record field, per-test persistent doc types (Frances's persist-until-next-run model)

## Fixture PDF sync (2026-11-11)

- [x] `sync_fixture_pdfs.py`: copies each `assets/pdfs/` file over its namesake in `scripts/test/fixture_pdfs/` when the bytes differ; `--check` reports only. No-op until the folder exists
- [x] `.github/workflows/sync-fixture-pdfs.yml`: on pushes to v0 that change `assets/pdfs/**`, syncs and opens or updates a PR on `auto/sync-fixture-pdfs` (same pattern as sync-llmstxt.yml); no secrets
- [x] Checked against #801's folder: `portfolio.pdf` and `portfolio_bank_paystub_tax.pdf` match `assets/pdfs/` today; `beazley_scanned_72_pages.pdf` has no namesake (fixture only)
- [x] ~~Conflict with #801 over FIXTURE_PDFS_DIR~~ superseded by the fixture move below

## Fixtures move under scripts/doc-detective (2026-11-11, Frances: Option A)

- [x] Test-account fixtures: `scripts/test/probe_endpoints/contract/fixtures/fingerprint_portfolio/` → `scripts/doc-detective/fixtures/fingerprint_portfolio/` (#744's contract-test fixtures stay where they are)
- [x] Self-test pages: `scripts/doc-detective/fixtures/` → `scripts/doc-detective/tests/pages/`; regenerated with build_fixtures.py
- [x] Manifest references: `file` (in the fixture's folder) or `docs_pdf` (a file name in assets/pdfs, used in place); the old `pdf` key fails with a message naming the new keys. Classification requests use the same keys
- [x] Removed the fixture-PDF sync (script, workflow, tests): nothing is copied, so nothing can drift
- [x] Each page watches its own fixtures' folders automatically (from its markup); a fixture change no longer reruns every page
- [x] `--check-fixtures` on fingerprint.md against the test account: all fixtures OK in the new location; 257 unit tests pass
- [ ] #741 after this merges: move `scripts/test/probe_endpoints/contract/fixtures/spreadsheet_classification/` and the test spreadsheets (`scripts/test/assets/{xls,xlsm,xlsb}_sample.*`, `csv_sample.csv`) into `scripts/doc-detective/fixtures/spreadsheet_classification/`; manifest `"pdf"` → `"file"`; requests' `file` → bare file names; add the `test-pages.json` entry; regenerate TEST-MATRIX.md and the saved report
- [ ] #801 after this merges: move its `ocr_engine` fixture folder to `scripts/doc-detective/fixtures/ocr_engine/` with `beazley_scanned_72_pages.pdf` inside it (`"file"`); reference `portfolio.pdf` and `portfolio_bank_paystub_tax.pdf` with `"docs_pdf"` instead of copies; drop `scripts/test/fixture_pdfs/` and #801's FIXTURE_PDFS_DIR change (this PR replaces it with DOCS_PDFS_DIR)
- The superseded #801 conflict note above no longer applies: after this PR, #801 drops its settings change instead of merging it

## Next steps

- [x] Open the PR: #803
- [ ] Frances: review
- [ ] After merge: run the workflow on demand once per priority (1, 2) to confirm it works on GitHub; schedules only run from `v0`
- [ ] After this merges: #741 adds `docs/Senseml reference/concepts/file-types.md` to `test-pages.json` with priority 3 (its tests need this PR's runner)
- [ ] #749's `add-doc-tests` skill: add a step to add new pages to `test-pages.json` with a priority
