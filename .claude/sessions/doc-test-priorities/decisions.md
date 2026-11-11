# doc-test-priorities: progress and decisions

Session: xlsb (`1e71441a-3c84-48a0-baa5-c36aac379bbb`). Checklist: `.claude/sessions/doc-test-priorities/checklist.md`.
Related: #741 (XLSB docs; depends on this PR), #749 (`add-doc-tests` skill).

## Progress log

### 2026-11-11
- Frances asked for priority levels 1-3 so GitHub Actions can run sets of tests at different cadences; the getting started guide is priority 1, the file-types classification tests priority 3.
- Frances asked to separate the test infrastructure from the XLSB docs: moved the runner changes from #741 into this branch as a patch from #741's last `v0` merge (`v0` hadn't changed those files since), and removed them from #741.
- Wrote `test-pages.json`, `plan_runs.py`, and `doc-tests.yml`, deleted the three per-page workflows, updated the README and secret-coverage glob. 229 unit tests pass.

- Review of f2933c834 (six reviewers): two P1s (classify false pass on API errors; a docs push could cancel a waiting scheduled run), two P2s (plan failure stops all pages silently; saved-report commits rerun every page), and P3s. All fixed in four commits; 247 unit tests pass.
- Added saved-evidence provenance and a generated test matrix (Frances: keep track of which claims are tested, where, and where their reports are).

## Decisions

| Decision | Why | Who |
| --- | --- | --- |
| Priority 1 weekly, 2 monthly, 3 on demand only | Frances's cadences | Frances |
| Priority per page, not per test | `run.sh` and CI run a page at a time; Doc Detective's UI test syntax can't carry or filter by our own key. Per-test priority for code tests can come later if a page needs it | Claude, Frances agreed |
| One committed list of tested pages (`test-pages.json`) and one workflow, replacing three | One place to set priority; adding a page is an entry, not a copied workflow | Claude, Frances agreed |
| Pushes to `v0` still run priority 1 and 2 pages whose tests, watched files, or tooling changed; never priority 3 | Keeps today's on-push behavior for the pages that had it; priority 3 is on demand only | Claude |
| Fail if a page has test markup but isn't listed | A new tested page can't be left out of CI by accident | Claude, Frances agreed |
| Pages run one at a time (`max-parallel: 1`, one concurrency group) | They share doc types in the test account | Claude |
| Keep each page's issue label (`doc-detective`, `doc-tests-fingerprint`, `doc-tests-portfolio`) | Open issues keep receiving comments | Claude |
| Every page's job receives all four secrets | Simpler, and the leak check must receive every secret the workflow passes; a conditional expression would hide secrets from the coverage check | Claude |
| Test infrastructure in its own PR, merged before #741 | Frances: separate infra from the XLSB docs | Frances |

| Only 400 and 415 from /classify mean "not classified"; anything else fails the test | An outage or rate limit says nothing about the file | Review finding, Claude |
| Concurrency on the test job with queue: max, not on the workflow | A docs push could cancel a waiting scheduled run; plan-only runs shouldn't queue | Review finding, Claude |
| A failed plan opens one doc-tests-plan issue | Otherwise a bad test-pages.json stops every page with only a red X | Review finding, Claude |
| Generate the test matrix from markup + test-pages.json + saved results, never hand-edit; a unit test checks it's current | A hand-kept list drifts from the pages | Frances asked for the matrix; Claude chose generated |
| Saved evidence = report.html + results JSON with commit, uncommitted flag, UTC time, environment | Reports are long-term traceability for future writers (Frances's testing philosophy) | Frances |
| Persist what can't be rebuilt from the repo; delete what can | Frances's philosophy, stated as a rule in the README | Frances, Claude |
| Claim-kind registry, common result shape, per-test persistent doc types go in a separate refactor PR | Behavior and structure changes; this PR is already large | Claude (proposed) |

## Evidence: how /classify says it didn't classify a file

`CLASSIFY_REJECTED = {400, 415}` in `codetests/sensible.py` rests on these observed responses (all committed on sensible-docs#741, branch `fe_xlsb_docs`):

| Response | Where it's recorded | When, which account |
| --- | --- | --- |
| HTTP 400 "Missing request body" (4 requests) | `scripts/doc-detective/reports/docs-senseml-reference-concepts-file-types.html`, commit 16f5a3aa1 | 2026-11-10, docs test account |
| HTTP 400 "Could not determine the content type of the document" (CSV sent as `application/pdf`) | Same report | 2026-11-10, docs test account |
| HTTP 400 "No match found for document" | `scripts/test/file_types/smoke_test_xlsb.sh:190` (expected and observed result, checks 5 and 7) | 2026-10-12, production; rerun 2026-11-10 on the docs test account, 0 changed |
| HTTP 415 for `...macroEnabled.12` (capital E) | `scripts/test/file_types/smoke_test_xlsb.sh:32` (check 9) | Same runs |

The API spec (`reference/openapi_classification.json`) lists 200, 400, 401, 415, 429, and 500 for /classify; it doesn't say which mean "rejected the file".

## Open questions

- Should priority 2 pages still run on push, or only monthly? Kept on push (today's behavior); easy to drop in `plan_runs.py`.
