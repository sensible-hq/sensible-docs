# doc-test-priorities: progress and decisions

Session: xlsb (`1e71441a-3c84-48a0-baa5-c36aac379bbb`). Checklist: `.claude/sessions/doc-test-priorities/checklist.md`.
Related: #741 (XLSB docs; depends on this PR), #749 (`add-doc-tests` skill).

## Progress log

### 2026-11-11
- Frances asked for priority levels 1-3 so GitHub Actions can run sets of tests at different cadences; the getting started guide is priority 1, the file-types classification tests priority 3.
- Frances asked to separate the test infrastructure from the XLSB docs: moved the runner changes from #741 into this branch as a patch from #741's last `v0` merge (`v0` hadn't changed those files since), and removed them from #741.
- Wrote `test-pages.json`, `plan_runs.py`, and `doc-tests.yml`, deleted the three per-page workflows, updated the README and secret-coverage glob. 229 unit tests pass.

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

## Open questions

- Should priority 2 pages still run on push, or only monthly? Kept on push (today's behavior); easy to drop in `plan_runs.py`.
