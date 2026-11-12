# claim-kinds session checklist

- Session: xlsb (1e71441a-3c84-48a0-baa5-c36aac379bbb), continued from #803's review follow-ups O1 to O4
- Worktree: `~/GitHub/sensible-docs-claim-kinds`, branch `fe_doc_test_claim_kinds`
- Stacked on #760 (`sample-editor-links`), which is stacked on #803 (`fe_doc_test_priorities`). Merge order: #803, #760, this PR.
- `.claude-session` and `.claude/active-session` are deliberately unchanged from the base: every stacked PR that rewrites them conflicts with every other one.

## Done (2026-11-11)

- [x] O1: claim-kind registry, `codetests/kinds/`: `output`, `documents`, `fingerprint`, `classification`, plus `common.py`. `kinds/__init__.py` documents the interface a kind module defines
- [x] `markup.py`, `runner.py`, `record.py`, the reports (`html.py`, `text.py`, `summary.py`), `test_matrix.py`, and `code_tests.py` dispatch through the registry; no more branching on `compare`
- [x] Records name their kind (`"kind"`); each kind's record section has its own schema in `schemas/kinds/<kind>.schema.json`, and `record.schema()` assembles the full schema, with the allowed kinds from the registry
- [x] Shared HTML parts in `reports/parts.py`; sample doc type helpers in `codetests/samples.py`
- [x] O4: report links to repo files are relative to where the report is written (`html.Links`)
- [x] `tests/test_kinds.py`: every kind defines the interface; the schema matches the registry, with no orphan schema files; a made-up `page_count` kind, registered only in `KINDS`, parses, runs, validates, and reports with no other change
- [x] README: the pieces, "Extending it", and the code layout describe the registry
- [x] Found and fixed on #760 (5329fde03): `add_reference` still passed `"pdf"` after #803 changed `_upload_reference` to read `"path"`, so every sample doc type failed with `KeyError: 'path'`. A merge bug from reconciling #760 with #803; the fake client hid it
- [x] Unit tests: 269 pass
- [x] Live runs on the test account, this branch: Fingerprint (10 tests), Portfolios (1), Getting started (2 code tests), and Supported file types via a throwaway merge with #741 (2 classification tests, before #741 removed them from the page): all pass

## Not done

- [x] (#811) O2: one record shape for every runner (UI tests, parameter-table checks from #749, API contract tests from #744). Not started: it's a design question about what those runners record, not a refactor of this one
- [x] (#811) O3, the rest: #760 already keeps sample doc types until the next run. The documented-output tests still share `docs_ci_examples`, one config at a time, deleted after each run; a doc type per test would make those openable too
- [ ] Update the `add-doc-tests` skill (#749) after this merges (exact replacement text in #811's checklist): its "add a new claim kind" step lists the dozen files this PR replaces with one module (`.claude/skills/add-doc-tests/SKILL.md`, line 100 on #749)
- [ ] Getting started's UI test fails locally only: `SENSIBLE_TEST_PASSWORD` isn't set in this shell, so sign-in can't finish. CI has the secret
