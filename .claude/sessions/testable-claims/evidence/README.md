# Evidence from the 2026-11-19 claim tests

Raw material for the first evidence records (see `../design.md`). Everything ran on **production** (`https://api.sensible.so/v0`) in **Frances's own account** (`SENSIBLE_API_KEY`), not the docs test account. The parameter was still deployed as `omit`; sensible-hq/sensible#3533 renamed it `ocrIfMissing` with identical logic but hadn't deployed. Each config ran in its own doc type, named like the config file, with config name `all`.

- `configs/`: the config each doc type ran (`all_user.json` is the quote example with `omit`; `all_renamed.json` is the same with `ocrIfMissing`, which production and dev both rejected on publish).
- `results/`: the extraction responses, with the `actor` field (API key name) removed.
- `documents/`: the test PDFs. All names, companies, and addresses are fictional.
- `scripts/`: `build_quote.py` builds `cgl_quote_digital.pdf` and `cgl_quote_screenshot.pdf` (`python3 build_quote.py <out dir>`); `add_page1_image.py` builds `two_images.pdf` from the screenshot quote.
- `claims/`: the dry run of `extract-testable-claims` on sensible-hq/sensible-docs#825: the claims split from the page, and Jev's scores.

Links: run = `https://app.sensible.so/extraction?e=<id>`, config = `https://app.sensible.so/editor/?d=<doc type>&c=all&g=<document stem>`. The editor link shows the doc type's config **now**, not necessarily what ran; the config files here are what ran.

## Claim: `ocrIfMissing` accepts a Match array

Document: `cgl_quote_screenshot.pdf`. "Premium Summary" and "Premium shown is annual" are consecutive embedded lines on page 2. A match array matches consecutive lines in order.

| doc type / config | array | total_premium | extraction ID |
| --- | --- | --- | --- |
| `ocr_array_in_order` / `array_in_order.json` | in document order: matches, so no OCR | null | 89b9d561-2ec7-4599-9950-51f4c93fb18e |
| `ocr_array_reversed` / `array_reversed.json` | reversed: no match, so OCR | $6,109.00 | 13537dfc-76af-453d-8513-5068a57085cb |

Result: supported, and evaluated as a sequence. Code: `types.ts` `ocrIfMissing: AnchorMatch`; `AnchorMatch` includes `(Matcher | RepeatMatcher)[]`; `ocr.ts` passes it to `standardizeMatch`, which handles arrays.

## Claim: `ocrIfMissing` checks the document's embedded text

Document: `two_images.pdf` (text images on page 1, "Agency Reference: HIA-REF-4417", and page 2, the premium table).

| doc type / config | preprocessors | agency_ref (p1 image) | total_premium (p2 image) | extraction ID |
| --- | --- | --- | --- | --- |
| `claims_t1_none` | none | null | null | 82caa28b-4833-43ea-b000-51a900ef811f |
| `claims_t1_omit_only` | `omit` "Total Premium" | extracted | extracted | 64cbaa10-8273-4362-87e2-ab05d0ec33fa |
| `claims_t1b_match_only` | OCR `match` "Premium shown is annual" (page 2) | null | extracted | c7dda447-382c-4834-a015-47ddbf06c248 |
| `claims_t1b_test` | that `match` OCR, then `omit` "Total Premium" | **null** | extracted | 64cbc7b6-34f9-4ef8-bc19-043e6cada4fb |

Result: **contradicted**. `omit` found "Total Premium" in page 2's OCR text from the earlier preprocessor and skipped OCR. It searches the text as earlier preprocessors left it. Frances changed the row to "If Sensible doesn't find the matched text in the document, it OCRs every page" (#825, `c8c5ede36`).

Invalid first attempt, kept for the record: `claims_t1_test` / `claims_t1_match_only` matched "Premium Summary", which also appears (lowercase) in page 1's cover letter, so the first preprocessor OCR'd page 1 (8fae3a3b-47df-4ba8-be94-8e21a577fb00, 93302e76-d1d0-4241-833e-b6dfbc27e978).

## Claim: `ocrIfMissing` OCRs every page

| doc type / config | document | preprocessors | total_premium (p2) | extraction ID |
| --- | --- | --- | --- | --- |
| `claims_t2_digital_ok` | digital | none | extracted | f44159ff-c077-4071-b337-429115ce4c14 |
| `claims_t2_range_only` | digital | pageRange `endPage: 1` | null | e2fb6bc2-134c-4b2d-938a-45b24a6a33e2 |
| `claims_t2_test` | screenshot | pageRange `endPage: 1`, then `omit` | **extracted** | a2c51a98-98cc-457e-b42e-ce4331199c04 |
| `claims_t2_ctrl` | screenshot | pageRange `endPage: 2`, then `omit` | extracted | d8b4234c-8c77-4fb3-9dac-f75ed53909c3 |

Result: **likely engine bug**. `omit` OCR'd page 2, which Page Range had excluded, and its text came back. Code: `page-range.ts` empties out-of-range pages without setting `startPage`; `ocr.ts` returns every page index when the match is missing and filters only by `startPage`. Not tested: whether `match`-based OCR does the same. Draft report for eng: `../eng-page-range-bug.md` (not sent).

## Earlier runs (same session, before these tests)

Doc types `ocr_omit_quote` (the example; config now `all_user.json` with `omit`; screenshot and digital both extract $6,109.00 / $6,477.72), `ocr_omit_quote_control` (`control.json`, no preprocessor: both fields null on the screenshot quote), `ocr_omit_present` and `ocr_omit_absent` (the engine's synthetic tests from sensible-hq/sensible#3519). In the dev account, `ocr_if_missing_quote` holds `all_renamed.json` as an unpublished draft with both quote PDFs, for checking the rename deploy.
