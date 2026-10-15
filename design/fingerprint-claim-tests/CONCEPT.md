# Concept: inline tests for fingerprint claims

Status: draft · 2026-10-15 · PR #727 · builds on #737 (inline code tests), #744 (fixtures, seed.py), #749 (claim triage)

## The idea

`fingerprint.md` and `portfolio.md` make claims about how Sensible behaves: "this config passes", "Sensible returns the tax return as pages 1–8", "a `[[ ]]` element in Tests is invalid". Each claim gets an inline test next to it, in the same HTML-comment style as #737's code tests. A runner checks the claim against the docs test account.

Unlike #737's code tests, these checks are **deterministic**. Fingerprinting uses no LLM, so the tests need no judge and no regression envelope, and can compare results exactly. Per the #749 research, that makes them eligible to gate CI.

## What's different from #737's code tests

| | #737 code test | fingerprint claim test |
| --- | --- | --- |
| What's checked | a config's `parsed_document` against the page's output block | which configs pass (standalone), page ranges (portfolio), or config validity |
| Configs | the page's code block, uploaded to a temp doc type | the page's code block, **or** a committed fixture when the page's example is illustrative |
| Doc types | one temp doc type, one config | often **several** doc types, one config each (isolation), and sometimes several configs on purpose (claims about how configs interact) |
| Extraction | single document | single document, or **portfolio** (`types` + `segment_documents_with: fingerprints`) |
| Nondeterminism | LLM judge + envelopes | none. Pin the OCR engine, and prefer PDFs with a text layer. |

## Markup

One new block, `<!-- fingerprint test -->`, with the same rules as #737 (single-line JSON, unique `testId`, comments between list items):

```markdown
<!-- fingerprint test {"testId": "portfolio_last_fails", "claim": "A failing last test makes the document absorb the following pages", "mode": "portfolio", "document": {"from": "portfolio_contents"}, "configs": [{"fixture": "fp_demo_last_fails"}], "expect": {"documents": [["last_fails", 1, 8]]}} -->
```

| key | meaning |
| --- | --- |
| `mode` | `portfolio`, `standalone`, or `validate` (publish only) |
| `document` | `{"link": true}` = the next download link on the page (like #737's `example document`); `{"from": "<testId>"}` = reuse another test's document |
| `configs` | each item is `{"fixture": "<doctype>"}` (from `fixtures/fingerprint_portfolio/`), or `{"block": "next"}` = the next `json` code block on the page, uploaded as written |
| `substitute` | optional. Text replacements applied to a page block before upload, so an **illustrative** example (`"NARS"`, `"wording A from revision 1"`) runs with real text from the test PDF while keeping the page's exact structure. Example: `{"NARS": "August 11, 2021", "Name of Insured": "Transaction history"}` |
| `expect` | what the claim says will happen (below) |
| `contrast` | optional. A second run that must give a **different** result (see "Every test must be able to fail") |

`expect` shapes, all exact:

| mode | expect | checked against |
| --- | --- | --- |
| `portfolio` | `{"documents": [[config, firstPage, lastPage], ...]}`, with **printed** (1-based) page numbers to match the prose; `[]` = no documents | `documents[].configuration/startPage/endPage` (0-based) |
| `standalone` | `{"ran": ["cfgA", ...], "skipped": ["cfgB"]}` | `classification_summary`: a config **ran** if it has `score`. Don't use `fingerprints_present`: it counts matching lines, not matches. |
| `validate` | `{"publish": "rejected", "error_contains": "tests/0 must be"}` or `{"publish": "ok"}` | the configuration API's response |

Expectations live **in the page comment**, next to the claim, so a reviewer sees the prose and its assertion together. `fixtures/fingerprint_portfolio/` keeps only configs and doc types (`manifest.json`, seeded by #744's `seed.py`). `expected.json` is retired, or generated from the page comments for the contract tests.

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
| 1 | Troubleshooting row `first`: no tax return | portfolio | `fp_demo_first_fails` | fixture exists |
| 2 | row `last`: pages 1–8 | portfolio | `fp_demo_last_fails` (+ contrast `any_alternate`) | exists |
| 3 | row `every`: pages 4–7 | portfolio | `fp_demo_every_fails` | exists |
| 4 | row `any`: pages 4–8 | portfolio | `fp_demo_any_fails` | exists |
| 5 | Alternate wordings: `any` match in one test | portfolio | `fp_demo_any_alternate`; better: the page's block with `substitute` | exists |
| 6 | Prefer tip: separate tests looser than one test; ALT ONE / ALT TWO | portfolio | `fp_portfolio_*`; better: the page's three blocks with `substitute` | exists |
| 7 | flat array: no partial credit across pages | portfolio | `fp_portfolio_flat_array` | exists |
| 8 | portfolio.md fingerprint example: quotes on pp. 1, 2; loss run p. 3 | portfolio | the page's two blocks as written | exists (`fp_pmd_*`) |
| 9 | standalone: config passes at ≥50% of matches | standalone | new: 1 doc type, configs at 2/4 (ran) and 1/4 (skipped) | **new fixture** |
| 10 | standalone: a chained match counts as one, in order, can span pages | standalone | new | **new fixture** |
| 11 | `[[ ]]` as a Tests element is rejected; `[ ]` publishes | validate | page's table syntax | **new**, no extraction |
| 12 | a string is a case-insensitive `includes` match | standalone | new | **new fixture** |
| 13 | standalone ignores Page and Offset | standalone | portfolio-syntax config on a single doc | **new fixture** |
| 14 | `offset` example (match on page 5, offset −1 → page 4) | portfolio | new | **new fixture**, needs a suitable PDF |
| 15 | Wells Fargo standalone example | standalone | needs an example PDF | **test later** (no document) |
| 16 | validator UI ("chained matchers", 5/6) | UI (Doc Detective) | — | **test later** (#737 UI tests) |

**Don't test:** page-type pairing (a CSE best practice, not behavior), "preferentially runs" wording, the use-case table, and the preprocessor tip (a workflow recommendation).

## Runner

Extend #737's `code_tests.py` rather than adding a second tool:
- `codetests/markup.py`: parse `fingerprint test`, check its keys, resolve `document` / `configs` / `substitute`.
- `codetests/sensible.py`: add portfolio extraction (`types`, `segment_documents_with`), a publish-only validate call, and `classification_summary` reads.
- new `codetests/fingerprint.py`: seed fixtures (#744's `seed.py`), create temp doc types for page blocks (`docs_ci_fp_<testId>_<n>`), run, compare, and run the contrast.
- `codetests/record.py` and `reports/`: one record per test. New failure categories: `SEGMENTS_DRIFT`, `CONFIG_SELECTION_DRIFT`, `VALIDATION_DRIFT`, `NOT_DISCRIMINATING`.

Cost: one extraction per run, plus one per contrast. That's about 20 small extractions per full run of both pages. Schedule: like #737 (pushes to v0 that touch the pages or fixtures, plus monthly), and because it's deterministic, optionally a PR gate.

## Dependencies and order

1. #744 merges (seed.py, fixtures layout). Then fold `fingerprint_portfolio/manifest.json` into it.
2. #737 merges (runner, markup, reports).
3. Add `fingerprint test` support + new fixtures (#9–14).
4. Add the comments to fingerprint.md and portfolio.md, proving each can fail (contrast or a deliberate mutation) before keeping it.
5. Optional: the #749 `add-doc-tests` skill learns this test kind.

## Open questions

1. **Where expectations live:** in the page comment (proposed), or in `expected.json` with the comment holding only an ID? The comment keeps claim and assertion together. A JSON file keeps the page lighter.
2. **`substitute` vs fixtures:** substitution tests the page's real code shape, but adds a mapping a reviewer must check. Fixtures are simpler but can drift from the page's example.
3. **Test account hygiene:** the temp doc types created per run need deleting. The persistent fixture doc types (`fp_demo_*`, `fp_portfolio_*`, `fp_pmd_*`) stay.
4. **OCR:** pin `ocr_engine` in fixture doc types. Avoid scanned PDFs (the senior 1040-SR) for gating tests.
