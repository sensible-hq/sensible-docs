---
name: add-doc-tests
description: Add embedded tests for a docs page's testable claims, using the repo's docs-test markup (Doc Detective UI tests and code tests in HTML comments). Finds the claims a page makes, triages which to test, writes the markup, proves each test can fail, runs it on the docs test account, and saves the HTML report. Invoke when Frances asks to add, write, or update embedded tests or doc tests for a page or claim, or when a doc-writing skill (create-new-doc, update-existing-doc, update-docs-from-pr, create-concept-doc, create-docs-example) reaches its testing step.
argument-hint: <path/to/page.md> [the claims or section to test]
allowed-tools: Bash(python3:*), Bash(scripts/doc-detective/run.sh:*), Bash(bash -ic:*), Bash(git diff:*), Bash(curl:*), Bash(jq:*), Read, Glob, Grep, Edit, Write
---

You add tests that run inside a docs page and check the page still tells the truth. The tests are HTML comments, so readers never see them. The design and its reasoning are in `design/docs-test-skill/CONCEPT.md`; the markup, commands, and failure categories are in `scripts/doc-detective/README.md`. **Read the README before writing any markup**: it's the source of truth, and this skill only says how to use it.

Parse **$ARGUMENTS**: the first token is the page; any remaining text names the claims or section to test. With no claims named, test what changed on the branch (`git diff origin/v0 -- <page>`), or the whole page if it's new.

## Rules that always apply

- **Test account only.** Use `SENSIBLE_TEST_API_KEY` (and `SENSIBLE_TEST_EMAIL`, `SENSIBLE_TEST_PASSWORD` for UI tests), never `SENSIBLE_API_KEY`. Never print a key. If the key isn't in the environment, try `bash -ic '...'` (it's exported in `~/.bashrc`); if it's still missing, stop and ask.
- **Never change what readers see to make a claim testable.** If a claim can't be tested as written, say so; don't edit the visible text, code block, or example to suit the test.
- **Never "fix" a doc claim to make a test pass** without telling Frances. A failing test means the doc or the product is wrong, and she decides which.
- **Licensing:** Doc Detective (AGPL-3.0) only as the pinned, unmodified CLI that `run.sh` calls. Don't install or copy Doc Detective's agent-tools, LSP, hooks, or MCP server. Check the license of any new tool or dependency before adding it, and flag GPL, AGPL, or SSPL.
- **Cost:** a run is capped at 20 extractions (`DOC_TESTS_MAX_EXTRACTIONS`). Each code test that extracts costs one extraction per run; classification requests and config uploads aren't extractions. Say what a new test costs.

## Step 1: List the claims

Read the page (or the diff) and list each concrete claim a reader would act on: a button or tab name, a config's output, a parameter's allowed values or default, a status code, a supported file type, what an endpoint accepts. Quote each one with its line number.

## Step 2: Triage each claim

Test a claim only if **all** of these hold (CONCEPT.md, "Triage rubric"):

| Question | Why |
|---|---|
| Is it concrete and checkable (a value, a label, a status, an output)? | Vague claims can't fail |
| Would a reader act on it, so being wrong costs them? | Procedures, examples, parameter values first |
| Can it be checked with the test account and the public API or app? | No customer data, no private systems |
| Is the result stable, or can its variation be described (`[...]`, the judge, envelopes)? | Flaky tests get ignored |
| Is the cost acceptable? | About one extraction per code test per run |

Mark each claim **test**, **test later** (name the blocker), or **don't test** (give the reason). Don't test marketing or comparative claims, timing, screenshots, paid-plan or admin-only features, third-party accounts, or anything destructive.

## Step 3: Pick the markup

Match the claim to the markup the README defines. Don't invent a new format; if nothing fits, stop and propose a runner extension to Frances first (see "Extending the runner" below).

| Claim | Markup (README section) |
|---|---|
| A procedure in the Sensible app | UI test: `<!-- test -->` and `<!-- step -->` (Doc Detective) |
| A config, its example document, and its output, all on the page | Code test with `inline document`, `inline config`, `inline output` |
| A one-field excerpt | `inline config {"fragment": "field"}` |
| An example that doesn't read its document | Code test with no `inline document` (runs on a blank page) |
| How fingerprints segment a portfolio, claimed in prose | Code test with `segment_documents_with`, `fixture`, and `expect {"compare": "documents"}` |
| The page's own fingerprint samples | `inline config {"fragment": "fingerprint", ...}` with `expect {"compare": "documents"}` or `{"compare": "fingerprint"}` |
| A table where each row is a claim | `<!-- table {"tableId"} -->` tag and a `<!-- table test -->` with one `row` per table row |
| Which files Sensible classifies, with which content type | Code test with `expect {"compare": "classification"}` and test files in `scripts/test/assets/` |
| A parameter table's names, required flags, types, values | No markup: `scripts/param-tables/check_param_tables.py` reads the table (prototype) |
| An API spec claim (`reference/*.json`) | Not page markup: a contract test in the API contract suite (PR #744), per CONCEPT.md "API changes" |

Placement and syntax:
- Test IDs: lowercase letters, digits, and underscores, unique on the page, prefixed by surface (`app_`, `extract_`, `classify_`).
- Every comment on one line, in the `<!-- name {json} -->` shape.
- Inside a numbered list, indent the comments under the item they test. Never put a comment between numbered items: it breaks ReadMe's numbering.
- Put the test next to the claim it checks, so whoever edits the claim sees the test.
- Test files and fixture documents are committed. Check spreadsheet and Office metadata for personal names before committing (`docProps/core.xml` in ZIP formats, the summary stream in XLS), and shorten them.

## Step 4: Preview the markup

Show Frances the markup you'll add and where, as a diff, before writing it into the page.

## Step 5: Validate, then prove each test can fail

1. `python3 scripts/doc-detective/code_tests.py --file "<page>" --check-syntax` (no keys, no network) and `--list`.
2. Make each new test fail once on purpose: change one expected value, label, or `classified` flag in a scratch copy of the page, or point a step at a misspelled label, and run that test (`--test ID`). It must fail with the expected category (`OUTPUT_DRIFT`, `CLASSIFICATION_DRIFT`, and so on). A test that's never been seen to fail isn't kept. Don't leave the broken copy in the repo.

## Step 6: Run and save the report

```bash
bash -ic 'DOC_TESTS_SAVE_REPORT=1 scripts/doc-detective/run.sh "<page>"'
```

`run.sh` runs the UI tests (only if the page has some), the code tests, writes `scripts/doc-detective/output/report.html`, scrubs secrets, and fails if any are left. With `DOC_TESTS_SAVE_REPORT=1` it also saves the scrubbed report to `scripts/doc-detective/reports/<page slug>.html`; commit that file, so the report stays viewable until the next saved run.

## Step 7: Fix loop, capped at 3

If a new test fails on the real page, decide whether the doc, the test, or the product is wrong. Fix the test at most 3 times. After that, leave it marked "needs manual review" in the checklist and tell Frances. If the doc looks wrong, report it with the evidence; don't change it.

## Step 8: Report

Add a claims table to the PR description and the session checklist:

| Claim (line) | Decision | Test | Result |
|---|---|---|---|
| "Sensible doesn't classify CSV files" (47) | test | `classify_csv_not_supported` | pass |
| "Easy to set up" (3) | don't test | marketing claim | |

Give Frances the saved report's path. Unit tests for the tooling: `python3 -m unittest discover -s scripts/doc-detective/tests -t scripts/doc-detective` (run from the repo root).

## Extending the runner

When a claim needs a check the markup can't express (as classification did, PR #741), propose the extension before writing it: the new markup in the existing `<!-- name {json} -->` shape, what the runner calls, the record fields, and the failure category. Then:
- keep it Doc Detective-compatible in shape (CONCEPT.md, "Licensing rule"), written from Doc Detective's documented syntax, never its code;
- update `markup.py` (parse and validate), `runner.py`, `sensible.py`, `schemas/record.schema.json`, the reports (`reports/html.py`, `text.py`, `summary.py`), and `errors.py`;
- add offline unit tests under `scripts/doc-detective/tests/`, including one that proves a mismatch fails;
- document it in `scripts/doc-detective/README.md` (markup, options table, failure category).
