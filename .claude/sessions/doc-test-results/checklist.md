# doc-test-results session checklist

- Session: xlsb (1e71441a-3c84-48a0-baa5-c36aac379bbb), the "not done" items from #810
- Worktree: `~/GitHub/sensible-docs-doc-test-results`, branch `fe_doc_test_results`
- Stacked on #810 (`fe_doc_test_claim_kinds`) → #760 → #803. Merge order: #803, #760, #810, then this PR.
- `.claude-session` and `.claude/active-session` deliberately unchanged from the base, so stacked PRs don't conflict.

## Done (2026-11-11)

- [x] O3: each output test runs in its own sample doc type, `docs_ci_sample_<page>__<testId>`, recreated each run and kept until the next, so records and report.html link to the config in the SenseML editor. Envelope builds and blank-page probes use it too
- [x] The shared `docs_ci_examples` doc type is gone: `settings.DOC_TYPE`, the client's `ensure_doc_type`, `upload_config`, `delete_config`, `delete_doc_type`, and `code_tests.cleanup`. Pages no longer share a doc type, so concurrent page runs can't collide in it. `--keep` now only skips deleting orphaned sample doc types
- [x] O2: one result per test, whatever ran it (`codetests/results.py`, `schemas/result.schema.json`). report.html, the CI summary, the failure issue, saved results, and the matrix read it; the four copies of the status logic are gone
- [x] Other runners join by writing `output/results/<runner>.json` during `run.sh`; their results reach every report and the matrix, and a failure fails the run (`report.py html` exits 1)
- [x] Behavior change: a marked-up test with no result is saved and shown as "not run" everywhere (saved results used to say "fail"); the page still fails
- [x] Unit tests: 274 pass (`tests/test_results.py` runs a made-up `param-tables` result through every consumer)
- [x] Live, test account: Getting started (2 code tests, each in its own doc type, editor links in the output) and Portfolios (1): pass. `docs_ci_examples` no longer exists in the account

## Next

- [ ] #749 (parameter-table checks): add a `run.sh` step, or an adapter in `check_param_tables.py`, that writes `output/results/param-tables.json` for the page. Each table becomes one result: kind "parameter table", claim "the <method> parameter table matches the SenseML schema", errors as the message, warnings as warnings, the schema URL as evidence
- [ ] #744 (API contract tests): same, as `output/results/contract.json`, from pytest's results (one per test function, the spec as evidence)
- [ ] `add-doc-tests` skill (#749), after #810 merges: replace the "add a new claim kind" step (SKILL.md line 100 on #749), which lists about a dozen files, with: "write a module in `codetests/kinds/` (see `kinds/__init__.py` for what it defines; copy `classification.py`), its record section's schema in `schemas/kinds/<kind>.schema.json`, and add it to `kinds.KINDS`; `tests/test_kinds.py` checks the rest"
- [ ] After this merges: dispatch priority 1 and 2 by hand, and check each job's summary and report
