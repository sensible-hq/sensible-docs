# Fingerprints: verified behavior

Last verified: 2026-10-14 (PR #727). Backend: `sensible-hq/sensible` @ `242e382fd`.

Sources:

- **code**: `src/engine/fingerprints.ts`, `src/engine/configurations/standardize.ts`, `src/engine/anchor.ts`, `src/engine/multi-extract.ts`.
- **run**: a fingerprint-mode extraction in the test account (`SENSIBLE_TEST_API_KEY`). Review at `https://app.sensible.so/extraction?e=<id>` while logged in to the test account.
- **fixture**: `scripts/test/probe_endpoints/contract/fixtures/fingerprint_portfolio/` (configs, `manifest.json`, and `expected.json` with each verifying run).
- **validator**: SenseML editor > Options > Validate fingerprints. It runs in single-document mode only, so it can't show portfolio behavior.

## Verified rules

### Syntax

| rule | source |
| ---- | ------ |
| Standalone (simple) syntax: `tests` is an array whose elements are strings, Match objects, Boolean matches, or arrays of Match objects. | code, schema |
| In standalone syntax, an array element of `tests` (`"tests": [ [A, B], ... ]`) is a **chained match**. | code; validator labels it "2 chained matchers" |
| `[[A, B]]` as an element of `tests` is **invalid**: "the supplied configuration cannot be published … tests/0 must be string / object". | API probe |
| Portfolio syntax: each test is `{page, offset?, match}`. In `match`, `[A, B]` is independent matches (any order, can share a line), and `[[A, B]]` is a chained match. | code (`standardize.ts` maps `[A, B]` to `[[A], [B]]`) |
| A string is a case-insensitive `includes` match. | code (`standardizeMatch`), anchor docs |
| All Match types work in fingerprints, including Boolean (`any`/`all`/`not`), `first`, and `repeat`. `page` and `firstInSection` matchers don't. | schema, code (`getMatchResult`) |

### Chained match

An array of Match objects that Sensible scores as **one** match, however many Match objects it contains. It succeeds only if Sensible finds every Match object **in order, on separate lines** (each one searches from the line after the previous match). Source: code (`matchArrayInner`).

### Standalone scoring

| rule | source |
| ---- | ------ |
| Sensible flattens all tests into a list of matches, searches the whole document, ignores `page` and `offset`, and passes the config if found / total ≥ 0.5. | code (`FINGERPRINT_SUCCESS_RATE_THRESHOLD = 0.5`) |
| Counting: each element of `tests` is one match (a chained match counts as one). For a portfolio-syntax config, each element of a flat `match` array counts as one, and a `[[ ]]` chained match counts as one. | code; validator counts ("6 matchers", "5/6") |
| Fingerprint Mode (normal/strict) doesn't change the 50% threshold. It only changes what happens when every config fails. | fingerprint-mode.md, code |
| The threshold isn't configurable. | Frances |

### Portfolio segmentation

| rule | source |
| ---- | ------ |
| Sensible checks **each test separately, on each page**. A test passes on a page only if all its matches are found on that page (threshold 1). | code (`matchPages`) |
| A passing test labels the page with its page type. Sensible derives document boundaries from the labels. | code (`identifyDocuments`) |
| Tests are **not** AND-ed together. With two separate single-match `every` tests, one passing test starts a document even if the other fails on that page. One test with both matches doesn't. | run: separate tests returned pages 3–7, flat and chained returned 4–7 (fixtures `fp_portfolio_*`) |
| A failing match fails **its test on that page**, not the whole fingerprint. Segmentation still happens but can be wrong. | runs (below) |
| Fingerprint Mode doesn't apply to portfolios. There's no 50% threshold. | fingerprint-mode.md, code |

Effect of a failing test, by page type (portfolio_bank_paystub_tax.pdf, one doc type per run, printed page numbers):

| failing test | effect | verified result | run |
| ------------ | ------ | --------------- | --- |
| `first` | no start signal; the document isn't found unless another test starts it | no tax return | `3340f5b6-0947-48b2-8d19-cc3a428e5cc5` |
| `last` | no end signal; the document absorbs the following pages | tax return pages 1–8 | `11c0f301-8983-4ce0-bcfa-0ad6215b64d4` |
| `every` | the page is left out; mid-document, the document splits | statement pages 4–7 (first page left out); split case: pages 3–4 and 6–7 | `f621c1c2-b504-4643-ab37-101c8ab02b2c`, `6444973d-fa33-423c-bce8-e9f41e2f27db` |
| `any` | the document starts on the first passing page and never ends from this test | statement pages 4–8 | `d68045b1-0e30-4271-9719-08370f345d04` |

Another document type's tests can hide these errors. For example, the next document's `first` test ends a document whose `last` test failed.

### Alternate wordings

An `any` Boolean match in a single test handles alternate wordings. Run `bdf09121-9e59-4b92-ae8e-29087978f724`: a `last` test with `any` of an absent and a present wording returned pages 1–2 (pages 1–8 without it). Separate `last` tests per wording probably also work, because tests are independent, but that's **untested**. The docs use `any` only.

## Misconceptions that came up, and what corrected them

| # | wrong belief | actually | corrected by |
| - | ------------ | -------- | ------------ |
| 1 | "In a portfolio, 100% of tests must pass." (fingerprint.md line 108 was even changed from "matches" to "tests") | Tests are independent per-page signals. Only the matches within one test must all succeed on a page. | code, then runs |
| 2 | "Two single-match tests behave the same as one test with a flat array in a portfolio." | Separate tests are looser: pages 3–7 vs 4–7. | Frances's challenge, then run |
| 3 | "The test is the smallest scored unit, so matches can't be counted." | Standalone scoring counts matches. A flat portfolio `match` array counts once per element on a standalone document. | code, validator |
| 4 | "The nested `[[ ]]` in the original PREFER example is a typo" (it was removed). | In a portfolio `match`, `[[ ]]` is a chained match. | code; restored |
| 5 | "Flat vs nested also matters in standalone syntax." | `[[ ]]` as a `tests` element is invalid. A flat `[ ]` element is already chained. | API probe, validator |
| 6 | "Order matters in a flat portfolio `match` array." | Only chained matches are ordered. | code |
| 7 | "Simple syntax expands to one `any` test per element." | It expands to **one** `any` test holding all the matches. | code |
| 8 | "Any failing match fails the whole portfolio fingerprint" (Frances's verified-in-the-validator belief, briefly adopted; it led to dropping the fallbacks tip). | A failing match fails its test on that page. The document is still segmented, possibly wrong. | run (senior 1040-SR test 2: pages 1–9) |
| 9 | "`Preparer's name` isn't on the 1040." | It's there with a curly apostrophe (U+2019). The `pdftotext` search used `'`. | Frances's screenshot |
| 10 | "`Wells Fargo` only appears on the statement's first page." | Elsewhere it's image text, invisible to `pdftotext`. | Frances |
| 11 | "The validator can screenshot portfolio behavior." | It's single-document mode only. | validator UI |

## Lessons for verifying fingerprint claims

- **Run it, don't reason it.** Items 1, 2, 7 and 8 came from reading docs or partial code. Each was settled in minutes by a run with one doc type per config, so configs can't interact.
- **`pdftotext` is a weak oracle.** It misses image text and is literal about punctuation. Use Sensible's own runs or the validator to confirm a match succeeds or fails.
- **Isolate configs.** Configs in one doc type, or doc types in one request, affect each other's segmentation. Use one config per doc type, and request only that doc type, unless the interaction is what's being tested.
- **Pull before reviewing.** One "still broken" report was against a copy three commits behind.
