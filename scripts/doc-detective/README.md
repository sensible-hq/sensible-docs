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

   It runs the UI tests, checks every UI test and step actually ran, runs the code tests, writes `scripts/doc-detective/output/report.html`, and scrubs secret values from every report file. It exits 1 if anything failed.

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

````markdown
<!-- code test {"testId": "extract_auto_insurance_anyco", "description": "Run the tutorial config against the example document and check the documented output"} -->

   <!-- example document -->

   | Example document | [Download link](https://raw.githubusercontent.com/.../auto_insurance_anyco.pdf) |

<!-- example config -->
```json
{ "fields": [ ... ] }
```

<!-- example output -->
```json
{ "policy_number": { ... } }
```
<!-- code test end -->
````

| Marker | Points at |
| --- | --- |
| `<!-- example document -->` | The first link on the next line: the page's own download link, so there's one copy of the URL. |
| `<!-- example document {"from": "ID"} -->` | Another code test's document, for a section without its own link. |
| `<!-- example config -->` | The next code block: the config, uploaded exactly as written, comments included. |
| `<!-- example config {"fragment": "field"} -->` | The next code block is a one-field excerpt (`{ ... },`). It runs wrapped in `{"fields": [ ... ]}`. |
| `<!-- example output -->` | The next code block: the output the page claims. |

### Fingerprint claims (portfolio segments)

For a claim about how fingerprints segment a portfolio, a code test runs committed **fixtures** instead of a code block on the page, and compares the extraction's documents (configs and page ranges) instead of `parsed_document`:

```markdown
<!-- code test {"testId": "segment_last_test_fails", "description": "...", "segment": "fingerprints"} -->
<!-- example document -->
| Example document | [Download link](https://raw.githubusercontent.com/.../portfolio_bank_paystub_tax.pdf) |
<!-- example config {"fixture": "fingerprint_portfolio/fixture_fp_demo_last_fails"} -->
<!-- example output {"compare": "documents", "expect": [["fixture_last_fails", 1, 8]]} -->
<!-- code test end -->
```

| Marker | Meaning |
| --- | --- |
| `code test {"segment": "fingerprints"}` | A portfolio extraction that segments with fingerprints. |
| `example config {"fixture": "<dir>/<doctype>"}` | A doc type and its one config from `scripts/test/probe_endpoints/contract/fixtures/<dir>/` (`<doctype>.doctype.json`, `<doctype>.<config>.config.json`). Repeatable: each fixture is its own doc type, and all are requested together. Fixture doc type and config names must start with `fixture_`, so nobody deletes them in the app by accident; the runner rejects a fixture without the prefix. Every fixture doc type also needs at least one reference document, listed under `references` in its folder's `manifest.json` (`name`, also prefixed `fixture_`; `pdf`, repo-relative; `configuration`), so you can open it in the SenseML editor. The report links each fixture to the editor: `https://app.sensible.so/editor/?d=<doctype>&c=<config>&g=<reference>`. Fixture doc types are persistent: the runner creates or republishes them (to production) when they're missing or differ, and never deletes them. |
| `example output {"compare": "documents", "expect": [...]}` | The documents the page claims, as `[config, firstPage, lastPage]` with **printed (1-based)** page numbers, to match the prose. `[]` means no documents. |

These comparisons are exact: fingerprinting uses no LLM, so there's no judge and no envelope. A mismatch fails as `SEGMENTS_DRIFT`.

**Tables of claims:** tag the table with one comment, and check it with one table test that has a row entry for each table row, in order (like a Doc Detective test and its steps). The table itself has no other markers, so readers see it unchanged:

```markdown
<!-- table test {"testId": "portfolio_failures_tests", "table": "portfolio_failures", "segment": "fingerprints", "description": "..."} -->
<!-- example document -->
| Example document | [Download link](https://raw.githubusercontent.com/.../portfolio_bank_paystub_tax.pdf) |

<!-- table {"tableId": "portfolio_failures"} -->
| document | failing test | ... | result |
| -------- | ------------ | --- | ------ |
| tax return, pages 1–2 | ... | ... | Sensible doesn't return a tax return. |
| tax return, pages 1–2 | ... | ... | Sensible returns the tax return as pages 1–8, ... |

<!-- row {"rowId": "first_test_fails", "config": {"fixture": "fingerprint_portfolio/fixture_fp_demo_first_fails"}, "expect": []} -->
<!-- row {"rowId": "last_test_fails", "config": {"fixture": "fingerprint_portfolio/fixture_fp_demo_last_fails"}, "expect": [["fixture_last_fails", 1, 8]]} -->
<!-- table test end -->
```

The runner checks the structure, not the prose: the tag and the test must name each other, and the test needs exactly one row entry per table row. Adding or deleting a row (or losing a comment in an editor) without updating the test fails with `DOCS_MALFORMED`. It doesn't compare a row's text with its `expect`. The tag is the hint that the table and its test change together. Each row runs as its own test, `<testId>__<rowId>`, and the report says which table row it checks.

**If someone edits a fixture in the app:** before each run, the runner compares the fixture's doc type settings and its published config with the committed files. It also checks the reference documents (missing, or linked to another config). It restores anything that differs, and the test passes **with a `[fixture]` warning** that names each difference, for example `config …: $.fingerprint.tests[1].match[1].text: committed "Form 1040-SR", test account "Form 1040"`. An unpublished draft in the app doesn't affect tests. To check fixtures without changing anything, run `code_tests.py --file PAGE --check-fixtures`. It lists each fixture as `OK` or `DRIFT` (with the differences) and exits 1 if any differ.

### Rules

- Test IDs are lowercase letters, digits, and underscores, and unique across all tests on a page. Name them for what they check, prefixed by surface: `app_...` for UI tests, `extract_...` for code tests.
- `example` markers go inside a `<!-- code test -->`, never a Doc Detective `<!-- test -->`.
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

- **`output/report.html`**: every test in page order, sections collapsed unless they need attention, judge verdicts with the full prompt and output, envelope results with the baseline. Test sections are labeled UI test or Code test.
- **Text summary**: printed per code test; the failure issue quotes it.
- **Failure issue** (CI): one standing issue labeled `doc-detective`, with failed UI steps, failed code tests, and a triage table pairing each judge failure with its envelope state.
- **Envelope issue** (CI): one standing issue labeled `doc-detective-envelope`. It comments only when the breaches change, and closes when a run is back within the envelope.
- **Proposed fix** (CI): for a documented-output mismatch, a draft PR from `doc-detective/getting-started-fixes` that rewrites the mismatched values. Review it: the difference can be a product regression, which the fix would codify.

`sample-reports/` has two example reports from the fixtures.

## CI

`.github/workflows/doc-detective-getting-started.yml` runs on pushes to `v0` that change the page or this tooling, monthly (the 1st, 15:00 UTC), and on demand. Never on pull requests. It needs repo secrets `SENSIBLE_TEST_EMAIL`, `SENSIBLE_TEST_PASSWORD`, `SENSIBLE_TEST_API_KEY`, and `ANTHROPIC_API_KEY`; keep them in step with `config/secrets.txt`, which `run.sh` scrubs from reports.

## Fixtures

`fixtures/` has copies of the getting started page whose example document link points at an altered PDF: one with a wrong premium (fails), one with a reformatted phone number (passes, envelope warning). `fixtures/build_fixtures.py` regenerates the copies from the real page. Their links point at this branch's raw URLs; repoint `BRANCH` after it merges.

## Code layout

| Path | Contents |
| --- | --- |
| `run.sh`, `code_tests.py`, `report.py` | Commands. `report.py` has `html`, `verify-ui`, `issue`, and `envelope-issue`. |
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
