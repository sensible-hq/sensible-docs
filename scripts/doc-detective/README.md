# Docs tests

Tests that run inside a docs page and check the page still tells the truth. There are two kinds:

- **UI tests** walk through the Sensible app the way the page tells a reader to, for example signing in and opening the Document Types tab. [Doc Detective](https://docs.doc-detective.com) runs them.
- **Code tests** run a documented SenseML config on its example document with the Sensible API, and check Sensible's output against the output the page shows. `code_tests.py` runs them.

Both are written as HTML comments in the page, so readers never see them. Today they cover `docs/document extraction/getting-started.md`.

## Run the tests

1. Install the dependencies once:

   ```bash
   npm install --global doc-detective@4.38.1
   pip install --target scripts/doc-detective/.deps -r scripts/doc-detective/requirements.txt
   ```

   `.doc-detective.json` turns off two Doc Detective defaults: **`autoUpdate`** (it would otherwise download and run a newer version from npm on startup, so only the pinned version runs) and **`telemetry`** (it would otherwise send anonymous usage data, versions and pass/fail counts, to PostHog). Doc Detective is AGPL-3.0; it's used only as an unmodified, separately run test tool, not distributed or hosted.

2. Put the keys in `.env` at the repo root (it's git-ignored):

   ```
   SENSIBLE_TEST_EMAIL=...       # the docs test account
   SENSIBLE_TEST_PASSWORD=...
   SENSIBLE_TEST_API_KEY=...     # the docs test account's API key
   ANTHROPIC_API_KEY=...         # for the LLM judge; ANTHROPIC_KEY also works
   ```

3. Run a page:

   ```bash
   scripts/doc-detective/run.sh "docs/document extraction/getting-started.md"
   ```

   It runs the UI tests, checks every UI test and step actually ran, runs the code tests, writes `scripts/doc-detective/output/report.html`, scrubs secret values from every report file, then checks that none are left (`check_secrets.py`). It exits 1 if anything failed, including a leak.

Other commands:

| Command | What it does |
| --- | --- |
| `code_tests.py --file PAGE --check-syntax` | Checks the markup and code blocks. No keys or network. |
| `code_tests.py --file PAGE --list` | Lists the page's tests. |
| `code_tests.py --file PAGE --check-fixtures` | Reports fixtures that differ from the test account, without changing anything. |
| `code_tests.py --file PAGE --test ID` | Runs one code test. |
| `code_tests.py --file PAGE --build-envelope 10` | Builds each code test's regression baseline from 10 runs. |
| `code_tests.py --file PAGE --extend-envelope 10` | Adds 10 runs to each saved baseline. |
| `python3 -m unittest discover -s scripts/doc-detective/tests -t scripts/doc-detective` | Runs the offline tests of this tooling. No keys or network. |

## Markup

### UI tests

Doc Detective's own syntax. Each step is one action, with a `description` the report shows:

```markdown
<!-- test {"testId": "app_document_types_page", "description": "Sign in with the test account, then open the Document Types tab"} -->
<!-- step {"description": "Log into account: open the sign-in page", "goTo": {"url": "https://app.sensible.so/signin/"}} -->
<!-- step {"description": "Log into account: enter the email", "type": {"keys": "$SENSIBLE_TEST_EMAIL", "selector": "input[name=\"email\"]"}} -->
<!-- test end -->
```

`$NAME` takes a value from the environment. Doc Detective's automatic step detection is off (`.doc-detective.json`), so only these comments run.

### Code tests

Markers inside a code test say where each part comes from: **`inline`** parts are published on the page (what readers see and copy), a **`fixture`** is private and committed (a doc type, its SenseML config, and a reference document in the test account), and **`expect`** is an expectation written in the test itself, for claims the page makes in prose or a table. "Config" always means a SenseML config; a test's own JSON is its **options**.

````markdown
<!-- code test {"testId": "extract_auto_insurance_anyco", "description": "Run the tutorial config against the example document and check the documented output"} -->

   <!-- inline document -->

   | Example document | [Download link](https://raw.githubusercontent.com/.../auto_insurance_anyco.pdf) |

<!-- inline config -->
```json
{ "fields": [ ... ] }
```

<!-- inline output -->
```json
{ "policy_number": { ... } }
```
<!-- code test end -->
````

| Marker | Points at |
| --- | --- |
| `<!-- inline document -->` | The first link on the next line: the page's own download link, so there's one copy of the URL. |
| `<!-- inline document {"from": "ID"} -->` | Another code test's document, for a section without its own link. |
| `<!-- inline config -->` | The next code block: the config, uploaded exactly as written, comments included. |
| `<!-- inline config {"fragment": "field"} -->` | The next code block is a one-field excerpt (`{ ... },`). It runs wrapped in `{"fields": [ ... ]}`. |
| `<!-- inline output -->` | The next code block: the output the page claims. |

### Fingerprint claims (portfolio segments)

For a claim about how fingerprints segment a portfolio, a code test runs a private **fixture** instead of a code block on the page, and checks an **expect** written in the test, comparing the extraction's documents (configs and page ranges) instead of `parsed_document`:

```markdown
<!-- code test {"testId": "last_test_fails", "description": "...", "segment_documents_with": "fingerprints"} -->
<!-- inline document -->
| Example document | [Download link](https://raw.githubusercontent.com/.../portfolio_bank_paystub_tax.pdf) |
<!-- fixture {"name": "fixture_fp_demo_last_fails"} -->
<!-- expect {"compare": "documents", "documents": [["fixture_last_fails", 1, 8]]} -->
<!-- code test end -->
```

| Marker or option | Meaning |
| --- | --- |
| `code test {"segment_documents_with": "fingerprints"}` | A portfolio extraction, segmented with fingerprints. Named after the public API's parameter, which it sets. Without it, a code test runs a single-document extraction. |
| `<!-- fixture {"name": "<doc type name>"} -->` | A fixture: the doc type with that name in the test account, as committed under `scripts/test/probe_endpoints/contract/fixtures/` (`<name>.doctype.json`, `<name>.<config>.config.json`, and a reference document in the folder's `manifest.json`). The name is exactly what the app shows; the runner finds its folder. Repeatable: each fixture is its own doc type, and all are requested together. Doc type, config, and reference document names must start with `fixture_`, so nobody deletes them in the app by accident. Fixture doc types are persistent: the runner creates or republishes them (to production) when they're missing or differ, and never deletes them. |
| `<!-- expect {"compare": "documents", "documents": [...]} -->` | The documents the page claims, as `[config, firstPage, lastPage]` with **printed (1-based)** page numbers, to match the prose. `[]` means no documents. |

These comparisons are exact: fingerprinting uses no LLM, so there's no judge and no envelope. A mismatch fails as `SEGMENTS_DRIFT`.

### Fingerprint samples (the page's own code blocks)

To test a fingerprint sample as the page shows it, mark the sample itself instead of using a fixture. The runner uploads it as written (comments and all) to a **sample doc type** named `docs_ci_sample_<page>__<testId>…`, published to development. Sensible validates each config on upload, so a sample with invalid syntax fails as `CONFIG_INVALID`. If the example document is in this repo (a `raw.githubusercontent.com/.../v0/assets/pdfs/` link), the runner also uploads it as the doc type's reference document, so the editor opens on it.

**Sample doc types are replaced, not kept:**

- **Replaced on each run.** Every run of a test deletes its sample doc types and recreates them from the page's current samples, so they always match the page.
- **Kept until then,** so the report can link each config to the SenseML editor. Because the names don't change between runs, an older report's editor links show the latest run's configs. For exactly what a run ran, use its extraction link (extraction history is permanent), or the page at the run's commit.
- **Orphans are deleted.** After each page run, `code_tests.py` deletes that page's sample doc types that no test on the page uses any more, for example after you rename or remove a test. It only touches names with that page's prefix (`docs_ci_sample_<page>__`), and `--keep` skips it.

**Portfolio samples:** give each sample's `inline config` a `doc_type` and a `config` name. Samples with the same `doc_type` share a doc type. All the doc types run together as one fingerprint-segmented portfolio:

````markdown
<!-- code test {"testId": "fingerprint_example_portfolio", "segment_documents_with": "fingerprints"} -->
<!-- inline config {"fragment": "fingerprint", "doc_type": "auto_insurance_quotes", "config": "anyco"} -->
```json
"fingerprint": { ... },
```
<!-- inline config {"fragment": "fingerprint", "doc_type": "loss_run_reports", "config": "acme"} -->
...
<!-- inline document -->
| Example document | [Download link](https://raw.githubusercontent.com/.../portfolio.pdf) |
<!-- inline output -->
```json
{ ..., "documents": [{"configuration": "anyco", "startPage": 0, "endPage": 0, ...}, ...] }
```
<!-- expect {"compare": "documents"} -->
<!-- code test end -->
````

`expect`'s `documents` work as for fixtures, with the samples' `config` names. Leave `documents` out to check the documents in the page's example response instead (an `inline output` with a `documents` list: each item's `configuration`, `startPage`, and `endPage`, 0-based as the API returns them).

**Standalone samples:** `expect {"compare": "fingerprint"}` runs one `inline config` (a whole config, or a `"fingerprint"` fragment) as a standalone extraction in a doc type with strict [fingerprint mode](https://docs.sensible.so/docs/fingerprint-mode), where Sensible runs a config only if its fingerprint passes. `passes` is the page's claim. Each of `variants` reruns the config with the listed tests (0-based indexes into `fingerprint.tests`) replaced by a match no document has, so you can test a scoring claim, such as "if 2 out of 3 pass, the config passes":

```markdown
<!-- expect {"compare": "fingerprint", "passes": true, "variants": [{"break": [0], "passes": true}, {"break": [0, 1], "passes": false}]} -->
```

The config as written and each variant is one extraction. A mismatch fails as `FINGERPRINT_DRIFT`.

| Marker or option | Meaning |
| --- | --- |
| `<!-- inline config {"fragment": "fingerprint"} -->` | The next code block is a `"fingerprint": { ... },` excerpt. It runs wrapped in `{ "fingerprint": { ... }, "fields": [] }`. |
| `<!-- inline config {..., "doc_type": "...", "config": "..."} -->` | One of a portfolio test's samples: the doc type and config name it runs as (lowercase letters, digits, underscores). Repeatable. |

**Tables of claims:** tag the table with one comment, and check it with one table test that has a row entry for each table row, in order (like a Doc Detective test and its steps). The table itself has no other markers, so readers see it unchanged:

```markdown
<!-- table test {"testId": "portfolio_failures_tests", "table": "portfolio_failures", "segment_documents_with": "fingerprints", "description": "..."} -->
<!-- inline document -->
| Example document | [Download link](https://raw.githubusercontent.com/.../portfolio_bank_paystub_tax.pdf) |

<!-- table {"tableId": "portfolio_failures"} -->
| document | failing test | ... | result |
| -------- | ------------ | --- | ------ |
| tax return, pages 1–2 | ... | ... | Sensible doesn't return a tax return. |
| tax return, pages 1–2 | ... | ... | Sensible returns the tax return as pages 1–8, ... |

<!-- row {"rowId": "first_test_fails", "fixture": {"name": "fixture_fp_demo_first_fails"}, "expect": {"compare": "documents", "documents": []}} -->
<!-- row {"rowId": "last_test_fails", "fixture": {"name": "fixture_fp_demo_last_fails"}, "expect": {"compare": "documents", "documents": [["fixture_last_fails", 1, 8]]}} -->
<!-- table test end -->
```

A row's keys are marker names with the same options (`fixture`, `expect`), so a row converts to a code test and back mechanically: `rowId` becomes `testId`, each key becomes its marker, and the table test's `inline document` and `segment_documents_with` move onto the code test. The runner checks the structure, not the prose: the tag and the test must name each other, and the test needs exactly one row entry per table row. Adding or deleting a row (or losing a comment in an editor) without updating the test fails with `DOCS_MALFORMED`. It doesn't compare a row's text with its `expect`. The tag is the hint that the table and its test change together. Each row runs as its own test, `<testId>__<rowId>`, and the report says which table row it checks.

**Renamed markup:** `<!-- example config/document/output -->` are now `<!-- inline ... -->`; `example config {"fixture": ...}` is `<!-- fixture {"name": ...} -->`; `example output {"expect": ...}` is `<!-- expect {"compare": ..., "documents": ...} -->`; and `"segment"` is `"segment_documents_with"`. The old forms fail with `DOCS_MALFORMED`, naming the new markup.

**If someone edits a fixture in the app:** before each run, the runner compares the fixture's doc type settings and its published config with the committed files. It also checks the reference documents (missing, or linked to another config). It restores anything that differs, checks the restore took (the test fails if it didn't), and the test passes **with a `[fixture]` warning** that names each difference. CI lists these warnings on the run's summary page, for example `config …: $.fingerprint.tests[1].match[1].text: committed "Form 1040-SR", test account "Form 1040"`. An unpublished draft in the app doesn't affect tests. To check fixtures without changing anything, run `code_tests.py --file PAGE --check-fixtures`. It lists each fixture as `OK` or `DRIFT` (with the differences) and exits 1 if any differ.

### Rules

- Test IDs are lowercase letters, digits, and underscores, and unique across all tests on a page. Name them for what they check, prefixed by surface: `app_...` for UI tests, `extract_...` for code tests.
- `inline`, `fixture`, and `expect` markers go inside a `<!-- code test -->` (a table test takes only `inline document`; its rows hold `fixture` and `expect`), never a Doc Detective `<!-- test -->`. A code test has at most one `expect`, and `fixture` or `segment_documents_with` needs one.
- A fixture's `.doctype.json` file name and its `"name"` must match, both prefixed `fixture_`. Its reference document PDFs must be under `assets/pdfs/`.
- Put comments between list items, not inside a numbered list, so ReadMe's numbering doesn't break. A comment indented inside a list item (like the document marker above) is fine.
- Configs may use `/* */` comments and trailing commas: Sensible accepts both. Output blocks may use comments and `...`, but no trailing commas: Sensible never outputs them. Neither may have duplicate keys or `NaN`.

## What a code test checks

1. **Syntax**, before any network call. Errors name the line in the page.
2. **The example document link resolves.**
3. **Extraction.** The config is uploaded to a temporary document type (`docs_ci_examples`) in the docs test account, published to development, and extracted. Only one config is in the document type at a time, and the runner checks Sensible used it: in development, Sensible runs every config in a document type and picks the best fit.
4. **Comparison** with Sensible's `parsed_document`:
   - Every key and value the page shows must match. Keys the page leaves out are ignored.
   - `...` means "don't check": a value (`"created": "..."`), an object member, or the rest of an array (`[a, b, ...]`, `[a, ..., z]`). An array without `...` must match in full.
   - Values are compared exactly: `true` doesn't match `1`; `1` matches `1.0`.
5. **The LLM judge**, for values that differ and that an LLM method produced (Query Group, List, NLP Table, at any depth in the config, including sections, conditionals, and fallback chains). The judge sees each value, the field's declared type with that type's example from `types.md`, and the whole field. It answers pass, partial, or fail with a confidence. Layout values are never sent to the judge.
6. **The regression envelope**, for every LLM field, whatever happened above.
7. **The record**: everything above, saved as `output/code-tests/<testId>.json` (shape: `schemas/record.schema.json`). Every report reads records.

| Result | Meaning |
| --- | --- |
| Pass | Everything matched, or the judge passed it with confidence of at least 0.7. |
| Pass with warnings | The judge was unsure (partial, or a low-confidence pass), or the output is outside its envelope. |
| Fail | See the category below. |

| Failure category | Meaning |
| --- | --- |
| `DOCS_MALFORMED` | The markup or a code block is broken. |
| `DOCUMENT_UNREACHABLE` | The example document link doesn't resolve. |
| `CONFIG_INVALID` | Sensible rejected the config. |
| `EXTRACTION_ERROR` | The extraction didn't complete, or used the wrong config. |
| `OUTPUT_DRIFT` | A layout value in the documented output doesn't match. |
| `SEGMENTS_DRIFT` | A portfolio extraction's documents don't match the ones the page claims. |
| `FINGERPRINT_DRIFT` | A standalone fingerprint sample passed when the page claims it fails, or the reverse. |
| `LLM_DRIFT` | The judge failed an LLM value. |
| `JUDGE_UNAVAILABLE` | LLM values differ and there's no Anthropic key. |
| `JUDGE_ERROR` | The judge couldn't decide. It fails closed: an undecided value is never a pass. |
| `ENVELOPE_INVALID` | A saved baseline doesn't match `schemas/envelope.schema.json`. |
| `RUNNER_ERROR` | The test couldn't run: an unexpected error in the runner or its setup, such as a key with stray whitespace. The message is recorded with keys redacted, and the traceback is in the log. |

Everything is deterministic except what's labeled **judge**: an LLM decided it, and the same input can get a different verdict on another run.

## Regression envelopes

An envelope is a baseline of what each LLM field's output normally looks like across several runs: null rate, output type, JSON type, value and source-text formats (digits become `9`, letters `a`), length and value ranges, unit, confidence signal, and item counts of lists and tables. A run outside the baseline is a **warning**, never a failure: the judge asks whether the docs are still right; the envelope asks whether the product's behavior shifted.

| Judge | Envelope | What it suggests |
| --- | --- | --- |
| pass | outside | The docs hold, but the feature's behavior changed. |
| fail | outside | Something new. Likely a regression: report it to engineering. |
| fail | within | The product varies this way normally, so the page claims something it doesn't reliably deliver. Fix the docs. |
| couldn't decide | either | Fix the judge problem; the envelope says whether the product shifted. |

Baselines live in `envelopes/<testId>.json`; commit them. A baseline records its config's SHA-256, so changing the config makes it stale. To accept new behavior, rebuild (`--build-envelope 10`); to record rare variants, extend (`--extend-envelope 10`). Neither runs on a fixture page unless `DOC_EXAMPLES_ENVELOPES_DIR` points elsewhere, so a fixture can't overwrite the real baselines. Tuning is in `config/envelope.json`.

## Reports

**In CI:** each run's page (Actions > the run) shows a summary: each test's result, what it checked, any warnings, and the details of any failure (`report.py summary`). It links to the full HTML report, which is uploaded unzipped, so it opens in the browser (you need to be signed in to GitHub). The failure issue links to it too. The zipped artifact still has the raw records and Doc Detective's results; `gh run download` can't fetch the unzipped report yet ([cli/cli#13012](https://github.com/cli/cli/issues/13012)), so download it from the run page.

**Usage line:** each report's header shows the docs test account's Sensible usage, so testing costs stay visible:
- **This run:** extractions, and API requests (a lower bound: the SDK's own polling isn't counted). `code_tests.py` writes these to `output/run.json`.
- **Month to date:** fetched from Sensible (`GET /extractions`, since the 1st, UTC) **after the tests run**, when the report is built. It shows extractions, total `charged`, and how many came from test runs (document names starting `ci__`). Sensible is the source of truth: local runs, CI, and app use all count, and there's nothing to persist between runs.
- **Budget (optional):** set `DOC_TESTS_MONTHLY_BUDGET` to a monthly extraction budget (in charged extractions; Sensible doesn't report a month's API requests, only extractions). The line shows usage against it: a warning at 80%, a failure chip at 100%. It's informational: it never stops a run. What does stop a run is a hard cap of 20 extractions per run (`DOC_TESTS_MAX_EXTRACTIONS` overrides it): an extraction past the cap fails its test with `RUNNER_ERROR`, so a page that grows, or a bug, can't spend the test account's budget.


- **`output/report.html`**: every test in page order, sections collapsed unless they need attention, judge verdicts with the full prompt and output, envelope results with the baseline. Test sections are labeled UI test or Code test.
- **Text summary**: printed per code test; the failure issue quotes it.
- **Failure issue** (CI): one standing issue labeled `doc-detective`, with failed UI steps, failed code tests, and a triage table pairing each judge failure with its envelope state.
- **Envelope issue** (CI): one standing issue labeled `doc-detective-envelope`. It comments only when the breaches change, and closes when a run is back within the envelope.
- **Proposed fix** (CI): for a documented-output mismatch, a draft PR from `doc-detective/getting-started-fixes` that rewrites the mismatched values. Review it: the difference can be a product regression, which the fix would codify.

`sample-reports/` has two example reports from the fixtures.

## CI

`.github/workflows/doc-detective-getting-started.yml` runs on pushes to `v0` that change the page or this tooling, monthly (the 1st, 15:00 UTC), and on demand. Never on pull requests. It needs repo secrets `SENSIBLE_TEST_EMAIL`, `SENSIBLE_TEST_PASSWORD`, `SENSIBLE_TEST_API_KEY`, and `ANTHROPIC_API_KEY`; keep them in step with `config/secrets.txt`, which `scrub.sh` scrubs from reports. `run.sh` runs it last, and the workflow runs it again as its own step before uploading reports, so a cancelled or timed-out run never uploads Doc Detective's plain-text password.

**Secrets fail closed.** Doc Detective writes typed text, including the test account password, into its reports in plain text ([doc-detective#204](https://github.com/doc-detective/doc-detective/issues/204)), and a scrub alone fails open. So `check_secrets.py` runs after every scrub:

- **Leak scan:** every file under `output/`, any type, is searched for each secret in `config/secrets.txt`, as written and JSON-, HTML-, URL-, and base64-encoded, and for credential-shaped strings nobody registered (Anthropic keys, bearer tokens, GitHub tokens, AWS keys). Any hit fails the run. In CI, nothing is published (docs-fix PR, issues, artifact) unless the "Check for leaked secrets" step passes. It never prints a value.
- **Coverage**, so a future secret can't be missed: the run fails if a `${{ secrets.X }}` in the workflow, a `$VAR` in a page's test markup, or a variable in `.env` is in neither `config/secrets.txt` nor `config/public-vars.txt`, or if the "Check for leaked secrets" step doesn't receive every secret the workflow uses. CI runs this first (`--coverage-only`, no secrets needed).

**To add a secret:** add its variable name to `config/secrets.txt`, pass it to the steps that need it **and** to "Scrub reports" and "Check for leaked secrets". If you miss one, the coverage check fails and says which. A variable that's safe to publish goes in `config/public-vars.txt` instead. The workflow pins its actions to commit SHAs and its Python dependencies to hashes (`requirements.txt`, compiled from `requirements.in`), since the job holds these secrets.

`.github/workflows/doc-tests-fingerprint.yml` runs the Fingerprint page's code tests the same way: on pushes to `v0` that change the page's tests, its fixtures (`fixtures/fingerprint_portfolio/`), or this tooling, monthly (the 1st, 15:30 UTC), and on demand. A push that changes only `fingerprint.md`'s prose, such as a ReadMe save, skips the tests: `should_run.py` compares what the page's tests run (markup, configs, documents, expectations, and each tagged table's row count) before and after the push. It needs only `SENSIBLE_TEST_API_KEY` (no Doc Detective: `run.sh` skips it on pages without UI tests). It runs the same secret steps as the getting-started workflow (classification check, scrub, leak check) and publishes nothing unless the leak check passes; `check_secrets.py` covers `doc-tests-*.yml` workflows as well as `doc-detective*.yml`. Failures go to a standing issue labeled `doc-tests-fingerprint`; every run uploads `doc-tests-fingerprint-reports`. An optional repo variable `DOC_TESTS_MONTHLY_BUDGET` shows usage against a monthly extraction budget in the report. It runs 12 extractions: 5 table rows, 4 portfolio samples, and 3 strict-mode runs of the standalone sample.

`.github/workflows/doc-tests-portfolio.yml` runs the Portfolios page's fingerprint example the same way (1 portfolio extraction; monthly on the 1st, 15:45 UTC). Its failures go to a standing issue labeled `doc-tests-portfolio`. `code_tests.py` only deletes the temporary `docs_ci_examples` doc type if its own run used it, so the two workflows don't interfere.

## Fixtures

`fixtures/` has copies of the getting started page whose example document link points at an altered PDF: one with a wrong premium (fails), one with a reformatted phone number (passes, envelope warning). `fixtures/build_fixtures.py` regenerates the copies from the real page. Their links point at this branch's raw URLs; repoint `BRANCH` after it merges.

## Code layout

| Path | Contents |
| --- | --- |
| `run.sh`, `code_tests.py`, `report.py` | Commands. `report.py` has `html`, `verify-ui`, `issue`, `summary`, and `envelope-issue`. `should_run.py` decides whether a push needs the fingerprint run. |
| `codetests/markup.py` | Reads a page's tests and checks the markup rules. |
| `codetests/jsonish.py` | Parses code blocks: comments, trailing commas, `...`. |
| `codetests/compare.py` | The comparison, coverage notes, and proposed fixes. |
| `codetests/fields.py` | Which output keys LLM methods produce, and their declared types. |
| `codetests/judge.py` | The LLM judge. Prompts and model: `config/judge/`. |
| `codetests/envelope.py` | Regression envelopes. |
| `codetests/sensible.py` | The Sensible API calls. |
| `codetests/record.py` | The record each code test produces. |
| `codetests/runner.py` | Runs a code test, builds envelopes. |
| `codetests/reports/` | Text summary, failure issue, envelope issue, report.html, and their shared wording. |
| `config/`, `schemas/` | Judge prompts and model, envelope tuning, the secrets list; record and envelope schemas. |

## Known limits

- The envelope measures top-level LLM fields; LLM fields nested in sections aren't measured.
- A list property or nested key with the same name as a layout field ID elsewhere in the config is routed by that layout field.
- A rare legitimate variant missing from a baseline's runs warns until the baseline is extended.
- The fixtures' "likely regression" is really a changed PDF. Recording each example document's hash in its baseline would make that read as a stale baseline instead.
