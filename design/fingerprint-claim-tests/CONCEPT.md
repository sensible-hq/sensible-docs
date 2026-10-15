# Concept: code tests for fingerprint claims

> **Superseded markup (2026-10-15):** the markup sketched below was replaced during implementation. Current syntax: `inline` / `fixture` / `expect` markers, `segment_documents_with`, fixtures named by doc type name, and tables of claims as one `<!-- table -->` tag plus one `<!-- table test -->` with `<!-- row -->` entries. See `scripts/doc-detective/README.md`. The claim inventory, contrast pairs, and cleanup sections below are still current.


Status: draft · 2026-10-15 (revised: code-test options, not a new test type) · PR #727 · builds on #737 (inline code tests), #744 (fixtures, seed.py), #749 (claim triage)

## The idea

`fingerprint.md` and `portfolio.md` make claims about how Sensible behaves: "this config passes", "Sensible returns the tax return as pages 1–8", "a `[[ ]]` element in Tests is invalid". Each claim gets an inline test next to it.

These are **#737 code tests**, not a new test type: run a config on a document, and compare the response with what the page claims. Two things differ from today's code tests, and both are options on #737's existing markers:

1. **Where the config comes from:** often a committed **fixture** rather than the next code block. Many of the page's examples are illustrative (`"NARS"`, `"wording A from revision 1"`) and can't run as written.
2. **What part of the response is compared:** page ranges (`documents`), which configs ran (`classification_summary`), or whether the config publishes, instead of `parsed_document`.

Fingerprinting uses no LLM, so these comparisons are **deterministic**: #737's judge and envelopes don't apply. Per the #749 research, that makes them eligible to gate CI.

## Markup: extensions to #737's markers

```markdown
<!-- code test {"testId": "extract_portfolio_last_fails", "description": "A failing last test makes the document absorb the following pages", "segment": "fingerprints"} -->
<!-- example document {"from": "portfolio_contents"} -->
<!-- example config {"fixture": "fingerprint_portfolio/fp_demo_last_fails"} -->
<!-- example output {"compare": "documents", "expect": [["last_fails", 1, 8]]} -->
<!-- example contrast {"config": {"fixture": "fingerprint_portfolio/fp_demo_any_alternate"}, "expect": [["any_alternate", 1, 2]]} -->
<!-- code test end -->
```

| marker / option | new behavior | existing behavior kept |
| --- | --- | --- |
| `code test {"segment": "fingerprints"}` | portfolio extraction: `types` + `segment_documents_with` | omitted = single-document extraction |
| `example config {"fixture": "<dir>/<doctype>"}` | load the config and its doc type from `scripts/test/probe_endpoints/contract/fixtures/` (seeded by #744's `seed.py`). Several `example config` markers = several doc types, one config each, requested together. | no options = the next code block, uploaded as written |
| `example config {"substitute": {"NARS": "August 11, 2021"}}` | apply text replacements to the next code block before upload, so an illustrative example runs with real text while keeping the page's exact structure | |
| `example output {"compare": "documents", "expect": [[config, first, last], ...]}` | compare portfolio page ranges. Printed (1-based) pages match the prose. `[]` = no documents. | no options = compare the next code block with `parsed_document` |
| `example output {"compare": "classification", "expect": {"ran": [...], "skipped": [...]}}` | standalone: a config **ran** if its `classification_summary` entry has `score` (never `fingerprints_present`, which counts matching lines) | |
| `example output {"compare": "publish", "expect": {"publish": "rejected", "error_contains": "tests/0 must be"}}` | publish only, no extraction | |
| `example contrast {...}` | a control run that must give a **different** result (see below) | |

The expected value goes in the marker, next to the claim, because these claims live in prose and table cells, not in output code blocks. `fixtures/fingerprint_portfolio/` keeps only configs and doc types (`manifest.json`). `expected.json` was deleted: the markers hold the expected results.

## Compared with today's code tests

| | today | with these options |
| --- | --- | --- |
| Config source | next code block | code block, code block with `substitute`, or fixture |
| Doc types | one temp doc type, one config | one or several (one config each, for isolation), or a fixture doc type |
| Extraction | single document | single document or portfolio |
| Compared | `parsed_document` | also `documents`, `classification`, `publish` |
| Judge / envelopes | for LLM fields | skipped: no LLM fields |

## Every test must be able to fail

Following #749 step 4, a test is only kept after it's been seen to fail. For fingerprint claims, the natural form is a **contrast pair**: the claim's run and a control run that differs in exactly one thing, with different expected results.

| claim | run | contrast |
| --- | --- | --- |
| a failing `last` test absorbs later pages | `last_fails`: pages 1–8 | `any_alternate`: pages 1–2 |
| separate tests are looser than one test | `separate_tests`: pages 3–7 | `flat_array`: pages 4–7 |
| chained matches need order | in order: passes | same matches reversed: fails |

If the contrast ever gives the same result as the claim, the test reports `NOT_DISCRIMINATING`. The claim may still be true, but the test no longer proves it.

## Claim inventory (fingerprint.md, portfolio.md)

| # | claim | mode | fixture | status |
| - | ----- | ---- | ------- | ------ |
| 1 | Troubleshooting row `first`: no tax return | portfolio | `fixture_fp_demo_first_fails` | fixture exists |
| 2 | row `last`: pages 1–8 | portfolio | `fixture_fp_demo_last_fails` (+ contrast `any_alternate`) | exists |
| 3 | row `every`: pages 4–7 | portfolio | `fixture_fp_demo_every_fails` | exists |
| 4 | row `any`: pages 4–8 | portfolio | `fixture_fp_demo_any_fails` | exists |
| 5 | Alternate wordings: `any` match in one test | portfolio | `fixture_fp_demo_any_alternate`; better: the page's block with `substitute` | exists |
| 6 | Prefer tip: separate tests looser than one test; ALT ONE / ALT TWO | portfolio | `fixture_fp_portfolio_*`; better: the page's three blocks with `substitute` | exists |
| 7 | flat array: no partial credit across pages | portfolio | `fixture_fp_portfolio_flat_array` | exists |
| 8 | portfolio.md fingerprint example: quotes on pp. 1, 2; loss run p. 3 | portfolio | the page's two blocks as written | exists (`fixture_fp_pmd_*`) |
| 9 | standalone: config passes at ≥50% of matches | standalone | new: 1 doc type, configs at 2/4 (ran) and 1/4 (skipped) | **new fixture** |
| 10 | standalone: a chained match counts as one, in order, can span pages | standalone | new | **new fixture** |
| 11 | `[[ ]]` as a Tests element is rejected; `[ ]` publishes | validate | page's table syntax | **new**, no extraction |
| 12 | a string is a case-insensitive `includes` match | standalone | new | **new fixture** |
| 13 | standalone ignores Page and Offset | standalone | portfolio-syntax config on a single doc | **new fixture** |
| 14 | `offset` example (match on page 5, offset −1 → page 4) | portfolio | new | **new fixture**, needs a suitable PDF |
| 15 | Wells Fargo standalone example | standalone | needs an example PDF | **test later** (no document) |
| 16 | validator UI ("chained matchers", 5/6) | UI (Doc Detective) | — | **test later** (#737 UI tests) |

**Don't test:** page-type pairing (a CSE best practice, not behavior), "preferentially runs" wording, the use-case table, and the preprocessor tip (a workflow recommendation).

## Runner changes (#737's `code_tests.py`)

All additive. No new test type and no new runner module:
- `codetests/markup.py`: parse the new options and the `example contrast` marker; check them in `--check-syntax`.
- `codetests/sensible.py`: portfolio extraction (`types`, `segment_documents_with`), a publish-only call, and fixture doc types (seeded via #744's `seed.py`, or created per run as `docs_ci_examples_<n>`).
- `codetests/compare.py`: `documents`, `classification`, and `publish` comparisons. These are exact, so they never route to the judge.
- `codetests/record.py` and `reports/`: new failure categories `SEGMENTS_DRIFT`, `CONFIG_SELECTION_DRIFT`, `VALIDATION_DRIFT`, `NOT_DISCRIMINATING`.

Cost: one extraction per test, plus one per contrast. That's about 20 small extractions per full run of both pages. Schedule: like #737 (pushes to v0 that touch the pages or fixtures, plus monthly). Because they're deterministic, they could optionally gate PRs.

## Test account cleanup

| resource | cleanup |
| --- | --- |
| configs uploaded from page blocks | deleted right after their extraction, in a `finally` (as #737 does today) |
| temporary doc types (`docs_ci_examples_<n>`, one config each) | deleted at the end of **each test**, in a `finally`, not just at the end of the run. A startup sweep deletes leftover `docs_ci_examples_*` doc types from crashed runs. `--keep` skips deletion for debugging, as in #737. |
| fixture doc types (`fixture_fp_demo_*`, `fixture_fp_portfolio_*`, `fixture_fp_pmd_*`) | never deleted. They're persistent, and `seed.py` restores or republishes them when they're missing or differ. |
| extractions | **can't be deleted**: the public API has no DELETE for documents or extractions (its only DELETEs are doc types, configs, config versions, reference documents, and email processors). Name them `ci__<testId>` so they're easy to filter, and accept the build-up in the dedicated test account. |

## Dependencies and order

1. #744 merges (seed.py, fixtures layout). Then fold `fingerprint_portfolio/manifest.json` into it.
2. #737 merges (runner, markup, reports).
3. Add the code-test options + new fixtures (#9–14).
4. Add the comments to fingerprint.md and portfolio.md, proving each can fail (contrast or a deliberate mutation) before keeping it.
5. Optional: the #749 `add-doc-tests` skill learns this test kind.

## Open questions

1. **Where expectations live:** in the page comment (proposed), or in `expected.json` with the comment holding only an ID? The comment keeps claim and assertion together. A JSON file keeps the page lighter.
2. **`substitute` vs fixtures:** substitution tests the page's real code shape, but adds a mapping a reviewer must check. Fixtures are simpler but can drift from the page's example.
3. **Test account hygiene:** the temp doc types created per run need deleting. The persistent fixture doc types (`fixture_fp_demo_*`, `fixture_fp_portfolio_*`, `fixture_fp_pmd_*`) stay.
4. **OCR:** pin `ocr_engine` in fixture doc types. Avoid scanned PDFs (the senior 1040-SR) for gating tests.
