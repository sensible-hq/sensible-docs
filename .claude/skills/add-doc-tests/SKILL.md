---
name: add-doc-tests
description: Turn the claims approved in extract-testable-claims into runnable tests in a docs page, using the repo's docs-test markup (Doc Detective UI tests and code tests in MDX comments). Writes the markup, proves each test can fail, runs it on the docs test account, saves the HTML report, and registers the page for CI. Doesn't find or triage claims; extract-testable-claims does that first. Invoke when Frances approves claims at priority 1 to 3 in extract-testable-claims, or asks to add, write, or update embedded tests or doc tests for claims she has already approved.
argument-hint: <path/to/page.md> [claim IDs, or the approved claims table]
allowed-tools: Bash(python3:*), Bash(scripts/doc-detective/run.sh:*), Bash(bash -ic:*), Bash(git diff:*), Bash(curl:*), Bash(jq:*), Read, Glob, Grep, Edit, Write
---

You turn approved claims into tests that run inside a docs page and check the page still tells the truth. The tests are MDX comments, so readers never see them. The markup, commands, failure categories, and how to extend the runner are in `scripts/doc-detective/README.md`. **Read the README before writing any markup**: it's the source of truth, and this skill only says how to use it. The design and its reasoning are in `design/docs-test-skill/CONCEPT.md`.

Parse **$ARGUMENTS**: the first token is the page; the rest names the claims to test, by claim ID or as the approved table.

## What this skill doesn't do

The two skills split at Frances's approval, so neither repeats the other:

| Step | Skill |
|---|---|
| Find the claims, score them, find evidence, propose and hand-run tests | `extract-testable-claims`, Steps 1 to 6 |
| Review: verdict and priority for each tested claim, approved by Frances | `extract-testable-claims`, Step 7 |
| Record-only claims: evidence records and the `tested claims` comment | `extract-testable-claims`, Step 7 |
| Approved claims at priority 1 to 3: markup, fail-proof, run, saved report, CI entry | this skill |

If there's no approved table for the page in this session or on the PR, stop and run `extract-testable-claims` first. Don't list or triage claims here.

## Input

From `extract-testable-claims` Step 7, for each claim approved at priority 1, 2, or 3: the claim ID, the claim as tested, its kind, the hand-run test and control (config, document, expected and actual result), the verdict, and the priority. The hand-run test is the starting point for the markup: it already showed which document, config, and result separate a true claim from a false one.

A claim with verdict `contradicted` gets no markup until the page is fixed; tell Frances and skip it.

## Rules that always apply

- **Test account only.** Use `SENSIBLE_TEST_API_KEY` (and `SENSIBLE_TEST_EMAIL`, `SENSIBLE_TEST_PASSWORD` for UI tests), never `SENSIBLE_API_KEY`. Never print a key. If the key isn't in the environment, try `bash -ic '...'` (it's exported in `~/.bashrc`); if it's still missing, stop and ask.
- **Never change what readers see to make a claim testable.** If a claim can't be tested as written, say so; don't edit the visible text, code block, or example to suit the test.
- **Never "fix" a doc claim to make a test pass** without telling Frances. A failing test means the doc or the product is wrong, and she decides which.
- **Licensing:** Doc Detective (AGPL-3.0) only as the pinned, unmodified CLI that `run.sh` calls. Don't install or copy Doc Detective's agent-tools, LSP, hooks, or MCP server. Check the license of any new tool or dependency before adding it, and flag GPL, AGPL, or SSPL.
- **Cost:** a run is capped at 20 extractions (`DOC_TESTS_MAX_EXTRACTIONS`). Each code test that extracts costs one extraction per run; classification requests and config uploads aren't extractions. Say what a new test costs, multiplied by how often its priority runs in CI.

## Step 1: Pick the markup

Match each claim to the markup the README defines. Don't invent a new format; if nothing fits, stop and propose a new claim kind to Frances first (see "Adding a claim kind" below).

| Claim | Markup (README section) |
|---|---|
| A procedure in the Sensible app | UI test: `test` and `step` (Doc Detective) |
| A config, its example document, and its output, all on the page | Code test with `inline document`, `inline config`, `inline output` |
| A one-field excerpt | `inline config {"fragment": "field"}` |
| An example that doesn't read its document | Code test with no `inline document` (runs on a blank page) |
| How fingerprints segment a portfolio, claimed in prose | Code test with `segment_documents_with`, `fixture`, and `expect {"compare": "documents"}` |
| The page's own fingerprint samples | `inline config {"fragment": "fingerprint", ...}` with `expect {"compare": "documents"}` or `{"compare": "fingerprint"}` |
| A table where each row is a claim | `table {"tableId"}` tag and a `table test` with one `row` per table row |
| Which files Sensible classifies, with which content type | Code test with one `fixture` (the doc type to classify as; its description is what Sensible classifies by) and `expect {"compare": "classification"}`, with the test files in the fixture's own folder |
| A parameter table's names, required flags, types, values | No markup: `scripts/param-tables/check_param_tables.py` reads the table (prototype; not yet a `run.sh` runner) |
| An API spec claim (`reference/*.json`) | Not page markup: a contract test in the API contract suite (PR #744), per CONCEPT.md "API changes" |

Placement and syntax:
- Write every comment as an MDX comment on one line, in the `{/* name {json} */}` shape. The runner still reads `<!-- ... -->`, but ReadMe's editor converts it, so new markup is MDX.
- Use the claim ID from the review as the test ID when it fits the README's rules (lowercase letters, digits, and underscores, unique on the page), so the report, `TEST-MATRIX.md`, and the review table name the same claim the same way.
- Inside a numbered list, indent the comments under the item they test. Never put a comment between numbered items: it breaks ReadMe's numbering.
- Put the test next to the claim it checks, so whoever edits the claim sees the test.
- Keep markup short (README, "Keep markup short"): leave out optional keys a report doesn't need.
- Test documents, doc types, and configs look like real business documents, never abstract placeholders. Pick a document type a Sensible customer would process (an insurance commission statement, a bank statement, a quote) and name everything after it: `fixture_commission_statements` and `commission_statement.csv`, not `fixture_spreadsheet_classify` and `csv_sample.csv`. The document can be sparse, a header and two rows, as long as each value is plausible for that business. Keep the values invented: no real customers, people, or account numbers.
- Fixtures live in `scripts/doc-detective/fixtures/<group>/`, one self-contained folder each (doc type, config, `manifest.json`, and the fixture's own files). Name a file with `file` (in the fixture's folder) or `docs_pdf` (a file name in `assets/pdfs/`, used in place); never copy a docs PDF into a fixture.
- Check spreadsheet and Office metadata for personal names before committing (`docProps/core.xml` in ZIP formats, the summary stream in XLS), and shorten them.

## Step 2: Preview the markup

Show Frances the markup you'll add and where, as a diff, before writing it into the page.

## Step 3: Validate, then prove each test can fail

1. `python3 scripts/doc-detective/code_tests.py --file "<page>" --check-syntax` (no keys, no network) and `--list`.
2. Make each new test fail once on purpose: change one expected value, label, or `classified` flag in a scratch copy of the page, or point a step at a misspelled label, and run that test (`--test ID`). It must fail with the expected category (`OUTPUT_DRIFT`, `CLASSIFICATION_DRIFT`, and so on). The review's control run usually tells you which change makes it fail. A test that's never been seen to fail isn't kept. Don't leave the broken copy in the repo.

## Step 4: Run, save the report, and register the page

```bash
bash -ic 'DOC_TESTS_SAVE_REPORT=1 scripts/doc-detective/run.sh "<page>"'
```

`run.sh` runs the UI tests (only if the page has some) and the code tests, writes `output/report.html`, scrubs secrets, and fails if any are left. With `DOC_TESTS_SAVE_REPORT=1` it also saves the report and results to `scripts/doc-detective/reports/` and regenerates `TEST-MATRIX.md`; commit both.

If the page is new to testing, add it to `scripts/doc-detective/test-pages.json` at the approved priority. CI fails if a page has tests but no entry.

## Step 5: Fix loop, capped at 3

If a new test fails on the real page while the hand-run test passed, the markup is the likeliest cause. Fix the test at most 3 times. After that, leave it marked "needs manual review" in the checklist and tell Frances. If the doc looks wrong, report it with the evidence; don't change it.

## Step 6: Report

Add a table to the PR description and the session checklist, one row per approved claim:

| Claim ID | Priority | Test | Seen to fail | Result |
|---|---|---|---|---|
| `classify_csv_not_supported` | 1 | code test, classification | `CLASSIFICATION_DRIFT` | pass |

Give Frances the saved report's path. Unit tests for the tooling: `python3 -m unittest discover -s scripts/doc-detective/tests -t scripts/doc-detective` (run from the repo root).

## Adding a claim kind

When a claim needs a check the markup can't express, propose the new kind before writing it: its markup in the existing `{/* name {json} */}` shape, what it calls, its record section, and its failure category. Keep the shape Doc Detective-compatible (CONCEPT.md, "Licensing rule"), written from Doc Detective's documented syntax, never its code. Then follow the README's "Extending it" table: a module in `codetests/kinds/` (copy `classification.py`), its record schema in `schemas/kinds/`, one line in `kinds.KINDS`, and unit tests that include one proving a mismatch fails. A check that isn't page markup, such as the parameter-table checks, is a runner instead: a `run.sh` step that writes `output/results/<runner>.json`.
