# Review: sensible-hq/sensible-docs PR #803

Branch `fe_doc_test_priorities`. Reviewed at `f2933c834`; fixes in `c59d7f3da`, `e3951d1d3`, `95bca2562`, `c0e63672d`, `f4af6e78d`, and `82bead504`; head `82bead504`.

## Verdict

Mergeable. No P0 or P1. Three P2s were real and are fixed: a "not classified" claim could pass when `/classify` was rate-limited or down, a docs push could silently cancel a waiting test run, and a failed plan stopped every page without opening an issue. The classify fix has unit tests. The concurrency fix (`queue: max` on a job) and the `plan-failed` job are documented GitHub features that haven't run on GitHub yet; the first manual run after merge confirms them (Question 1).

## Findings

### P2-1. A "not classified" claim passed when /classify was rate-limited or down

**What**: `classify()` treated every non-2xx response, and a 200 whose body wasn't JSON, as "not classified". A 429 or 5xx from `/classify` then passed every `"classified": false` claim. The runner restores the fixture through the API first, so a full outage or a bad key fails earlier; the exposure is `/classify` failing on its own, for example a rate limit during the back-to-back requests. A block whose claims are all `false`, like #741's CSV test, would then go green with a pass chip next to the error. No page uses classification until #741 merges.

**Where** (at `f2933c834`): `scripts/doc-detective/codetests/sensible.py:166-172`
```python
name = ""
if response.ok:
    try:
        name = (response.json().get("document_type") or {}).get("name", "")
    except ValueError:
        pass
return response.status_code, response.text, name
```

**Fix** (`c59d7f3da`, `f4af6e78d`, `82bead504`): only 400 and 415 mean "not classified"; anything else raises `RUNNER_ERROR`, including a 200 that doesn't name the requested doc type (each request allows only the fixture's). `sensible.py:40` and `:175-187` at `82bead504`:
```python
CLASSIFY_REJECTED = {400, 415}
...
if response.status_code in CLASSIFY_REJECTED:
    return response.status_code, response.text, ""
if not response.ok:
    raise CodeTestError(RUNNER_ERROR, f"classify returned HTTP {response.status_code}, which says nothing about the file: {settings.redact(response.text)[:200]}")
try:
    name = response.json()["document_type"]["name"]
except (ValueError, TypeError, KeyError):
    name = None
# Sensible answers "no match" with a 400, and the request allows only doc_type, so a 200 names doc_type
if name != doc_type:
    raise CodeTestError(RUNNER_ERROR, f"classify returned HTTP {response.status_code} without classifying the file as {doc_type}, "
                        f"the only doc type requested: {settings.redact(response.text)[:200]}")
return response.status_code, response.text, name
```

**Why 400 and 415**: those are the rejections observed for this kind of request, recorded on #741 (`fe_xlsb_docs`) and listed in `.claude/sessions/doc-test-priorities/decisions.md` ("Evidence: how /classify says it didn't classify a file"):
- 400 "Missing request body" and 400 "Could not determine the content type of the document": `scripts/doc-detective/reports/docs-senseml-reference-concepts-file-types.html` (commit `16f5a3aa1`, docs test account, 2026-11-10).
- 400 "No match found for document" and a 415 for an uppercase `macroEnabled` content type: `scripts/test/file_types/smoke_test_xlsb.sh:190` and `:32` at commit `b7409da17`. They were observed on production on 2026-10-12 and rerun on the docs test account on 2026-11-10 with no change (`.claude/sessions/xlsb/checklist.md:18` and `:53` on `fe_xlsb_docs`).

The spec (`reference/openapi_classification.json`) lists 200, 400, 401, 415, 429, and 500, but doesn't say which mean "rejected the file".

**Tests**: `ClassifyResponseTest` (`tests/test_classification.py`) covers 400, 415, 401, 429, 500, 502, an HTML body, a JSON array, `{}`, `{"document_type": null}`, and a 200 whose name is null, empty, or another doc type.

### P2-2. A docs push could silently cancel a waiting test run

**What**: one workflow-level concurrency group, plus a push trigger on all of `docs/**`, put every ReadMe save in the queue. GitHub keeps one pending run per group by default and cancels it when a newer one arrives:

> "By default, any existing `pending` job or workflow in the same concurrency group will be canceled" … "the new queued job or workflow will take its place."
> — https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency

The likely case is one push replacing another: while a run is in progress, push A changes a page's tests and waits; push B, a ReadMe save, arrives and cancels it. B's plan compares only B's own commits, so A's change goes untested until the page's next scheduled run. Less often, a scheduled run is the one cancelled: it waits while another run is in progress (a push's run, or, when the 1st is a Monday, a weekly run still going at 15:30, usually because the scheduler started it late), and a push that arrives during the wait cancels it. A cancelled run shows grey and opens no issue (the issue step is inside the `test` job, which it never runs). The old per-page workflows had separate groups and page-specific paths, so a docs push for one page couldn't cancel another page's run.

**Where** (at `f2933c834`): `.github/workflows/doc-tests.yml:53-55` and the `docs/**` path at `:28`.

**Fix** (`e3951d1d3`): the group moves to the `test` job with `queue: max` (`doc-tests.yml:140-143` at `82bead504`); the plan job is outside it, so a push that tests nothing never queues.
```yaml
  test:
    concurrency:
      group: doc-tests
      cancel-in-progress: false
      queue: max
```
> "`max`: Up to 100 jobs or workflow runs can be `pending` in the concurrency group."
> — https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax (documented for `jobs.<job_id>.concurrency`; the only example is workflow-level)

### P2-3. A failed plan stopped every page, and opened no issue

**What**: `plan_runs.py` fails when a page with test markup isn't listed, or a listed page was renamed or deleted. The plan job then exited 1, the `test` job was skipped, and its issue step never ran: one bad entry stopped every page's schedule with only a red X. #741 would trigger this on merge unless it adds its `test-pages.json` entry, and no check runs on pull requests to catch it first.

**Fix** (`e3951d1d3`): a `plan-failed` job (`doc-tests.yml:104-124`, no secrets, `issues: write` only) opens or comments on one issue labeled `doc-tests-plan` for push and scheduled runs. A schedule whose priority has no pages now fails instead of passing while testing nothing (`test_a_schedule_with_no_pages_fails`).

### P3-1. Committing a saved report reran every priority 1 and 2 page

**What**: `TOOLING = ["scripts/doc-detective/**", ...]` matched `scripts/doc-detective/reports/*.html`, which the README tells you to commit. Each saved report would rerun Getting started (UI tests and LLM judge), Fingerprint (12 extractions, per the README's CI section), and Portfolios: wasted extractions, not wrong results.

**Fix** (`e3951d1d3`; test in `f4af6e78d`): `NOT_TOOLING` (`plan_runs.py:41-46`: reports, sample reports, README, `TEST-MATRIX.md`) is filtered in `plan_runs.py` and passed to `should_run.decide(ignore=...)`, and mirrored as `!` paths in the workflow (`doc-tests.yml:39-42`). `test_workflow_paths_ignore_the_same_files` keeps the two lists equal; `test_ignored_files_dont_count_as_changes` covers `decide(ignore=...)` on a real git history.

### P3-2. Classification request files could be any repo file

**What**: the check used `normpath` and allowed anything in the checkout, so a request could send `.env` or unscrubbed output to Sensible, and an in-repo symlink could point outside. Fixture reference documents already had a stricter rule.

**Fix** (`c59d7f3da`): `markup.request_path()` resolves symlinks and requires `fixture_document_dirs()`, the fixture rule; the runner opens the resolved path. Tests cover `.env` and a symlink out of the folder.

### P3-3. The report's curl commands weren't shell-quoted

**What**: `--data-binary @{file}` broke on paths with spaces (`assets/pdfs/types test.pdf` exists), and a `content_type` from merged markup could inject a command into a line readers are told to paste.

**Fix** (`c59d7f3da`): `shlex.quote` on the URL, the Content-Type header, and the file; the query is URL-encoded. `CurlCommandTest` checks a hostile content type stays one argument.

### P3-4. Write permissions covered every job

**What**: the workflow-level block gave `contents: write` and `pull-requests: write` to the plan job and to the fingerprint and portfolio jobs. Their old workflows had only `contents: read` and `issues: write` (`git show 39ff57219:.github/workflows/doc-tests-fingerprint.yml`, and the portfolio workflow at the same commit). Any code those jobs run, including their hash-pinned pip dependencies, could push to the repo or open PRs with the job token.

**Fix** (`e3951d1d3`): `contents: read` at workflow level (`doc-tests.yml:61`); the `test` job writes (`:133-136`); `plan-failed` has `issues: write` only. Fingerprint and portfolio still get write access, because permissions are per job, not per matrix entry; splitting the fix-PR step into its own job would remove it.

### P3-5. Smaller correctness and accuracy fixes

- Envelope issues (`e3951d1d3`): the label was hardcoded, so a second page with `envelope_issue` would share the first's issue and could close it. Latent: only Getting started has one. Now `${{ matrix.issue_label }}-envelope` (`doc-tests.yml:319`), unchanged for Getting started (`doc-detective-envelope`).
- `timeout_minutes` (`e3951d1d3`): bounded to 1–40 (`plan_runs.py:49`), below the job's 45, so the job timeout can't cut off the scrub and issue steps.
- Stale text: `secrets.txt` named a deleted workflow, a `settings.py` comment said reference documents are PDFs, and the schema said "temporary doc type" (`95bca2562`); a comment said "as before" (`c59d7f3da`); the README claimed `file-types.md` already used classification and left out the `classify_` prefix (`c0e63672d`).

## Open observations

**OOS but good**

- **O1. A claim-kind registry.** A kind of claim touches about 13 places, for example `markup._expect` (`markup.py:177`), `markup._code_test` (`:205`), `markup.check_syntax` (`:353`), `COMPARES` (`:85`), `runner._run` (`runner.py:252`), the record schema, `html.render_code_test` (`reports/html.py:186`), `html.details_label` (`:357`), `summary.test_rows` (`reports/summary.py:10`), `text.summary` (`reports/text.py:8`), `code_tests.probe_blank` (`code_tests.py:126`), and `test_matrix.KINDS` (`test_matrix.py:31`). One module per kind (parse, check, run, schema fragment, HTML, text, label), with a `claim: {kind, ...}` record field, makes a new kind one file.
- **O2. One result shape for every runner.** Code tests, UI tests, parameter-table checks (#749), and API contract tests (#744) each report differently. A shared record (page, test, kind, claim, status, category, evidence) lets one report, one matrix, and one CI flow cover all of them.
- **O3. Persist each test's doc type until the next run.** Temporary doc types are deleted at the end of a test. Keeping them, and cleaning up at the start of the next run, lets a reader open exactly what ran. The shared `docs_ci_examples` doc type would become one per test.
- **O4. Compute report links from the output path** instead of `../../../`, so a report saved elsewhere keeps working.

## Questions

1. Is `queue: max` on a job accepted as the docs describe? Confirm on the first dispatch run: no validation error, and a second dispatch while one runs shows as pending, not cancelled.
2. Should Getting started run on prose-only pushes? Its old workflow did; it now skips them like the other pages and waits for the weekly run.

## In person

The load-bearing idea in this PR is that a saved report is evidence. With P2-1 and P2-2 fixed, what's left is structural: every new claim kind costs about a dozen edits, and every runner reports in its own format. O1 and O2 are the next PR; they turn "add a kind of test" into one file and put every claim, from every runner, in the same matrix.

**Opinions on the fixes**: the classify fix fails closed, which is right, but its allowlist rests on four observed responses rather than the spec, so a new rejection status from Sensible will show up as a runner error until someone adds it. The permissions fix stops at the job boundary; splitting the fix-PR step out (P3-4) would finish it. `TEST-MATRIX.md` is generated and checked, so it can't drift, but it's only as good as each test's description, which belongs in the add-doc-tests skill.

**Pipeline completeness**: all review phases ran end to end.

**Ranked ask**: (1) after merge, dispatch priority 1, then priority 2, by hand: confirm Question 1, and check each job's summary and report; (2) before #741 merges, add `file-types.md` to `test-pages.json` and regenerate `TEST-MATRIX.md` there.
