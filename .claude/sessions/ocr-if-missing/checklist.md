# ocr-if-missing checklist

Claude Code session name: ocrIfMissing
Claude Code session ID: 0ded2aae-03f7-4ca1-bf75-b37050ab318e
Resume: `cd /home/franc/GitHub/sensible-docs-private && claude --resume 0ded2aae-03f7-4ca1-bf75-b37050ab318e`
Docs PR: sensible-hq/sensible-docs#825 (draft), branch `ocr-omit-quote-example`, worktree `~/GitHub/sensible-docs-ocr-omit-quote`
Engine: sensible-hq/sensible#3519 (adds `omit`), sensible-hq/sensible#3533 (renames it `ocrIfMissing`, no alias)
Notes: fscelliott/sensible-docs-private#1 · Test evidence (configs, results, PDFs, and the narrative README): `scripts/doc-detective/testable-claims/pr-825-ocr-if-missing/`

## Status (2026-11-19)

The page documents `ocrIfMissing` with the insurance-quote example. **Don't merge until #3533 deploys**: as of 2026-11-19, production and dev both reject `ocrIfMissing` on publish (schema still requires `omit`).

## Tested claims

All runs are in Frances's own **production** account and use `omit` (the deployed name; #3533 changed no logic). Run links show what ran; config links show the doc type's config now. Configs and responses are saved in the evidence folder above.

| claim on the page | result | proof |
| --- | --- | --- |
| Accepts a Match object | holds | example doc type: [screenshot](https://app.sensible.so/editor/?d=ocr_omit_quote&c=all&g=cgl_quote_screenshot), [digital](https://app.sensible.so/editor/?d=ocr_omit_quote&c=all&g=cgl_quote_digital) |
| Accepts a Match array (evaluated as consecutive lines) | holds | in order, no OCR: [run](https://app.sensible.so/extraction?e=89b9d561-2ec7-4599-9950-51f4c93fb18e) · [config](https://app.sensible.so/editor/?d=ocr_array_in_order&c=all&g=cgl_quote_screenshot); reversed, OCR: [run](https://app.sensible.so/extraction?e=13537dfc-76af-453d-8513-5068a57085cb) · [config](https://app.sensible.so/editor/?d=ocr_array_reversed&c=all&g=cgl_quote_screenshot) |
| If it finds the text, it OCRs nothing | holds | the in-order array run above (`total_premium` null, so no OCR) |
| If it doesn't find the text, it OCRs every page | holds; after Page Range it also OCRs removed pages, eng will fix this for Page Range (2026-11-20); the same effect after Remove Page or Page Filter stays a known limitation, covered by the note after the parameter table | `ocrIfMissing` alone OCRs both pages: [run](https://app.sensible.so/extraction?e=64cbaa10-8273-4362-87e2-ab05d0ec33fa) · [config](https://app.sensible.so/editor/?d=claims_t1_omit_only&c=all&g=two_images). Bug: it also OCRs pages Page Range excluded: [run](https://app.sensible.so/extraction?e=a2c51a98-98cc-457e-b42e-ce4331199c04) · [config](https://app.sensible.so/editor/?d=claims_t2_test&c=all&g=cgl_quote_screenshot); control, Page Range alone: [run](https://app.sensible.so/extraction?e=e2fb6bc2-134c-4b2d-938a-45b24a6a33e2) · [config](https://app.sensible.so/editor/?d=claims_t2_range_only&c=all&g=cgl_quote_digital). Not reported to eng yet. |
| ~~It searches the document's embedded text~~ | **contradicted**; row reworded to "in the document" (`c8c5ede36`) | after an earlier OCR preprocessor, it searched OCR text and skipped OCR: [run](https://app.sensible.so/extraction?e=64cbc7b6-34f9-4ef8-bc19-043e6cada4fb) · [config](https://app.sensible.so/editor/?d=claims_t1b_test&c=all&g=two_images); control, the earlier OCR alone: [run](https://app.sensible.so/extraction?e=c7dda447-382c-4834-a015-47ddbf06c248) · [config](https://app.sensible.so/editor/?d=claims_t1b_match_only&c=all&g=two_images) |
| A document with enough embedded text isn't OCR'd by default, even with a text image | holds for the example document | no preprocessors, both image fields null: [run](https://app.sensible.so/extraction?e=82caa28b-4833-43ea-b000-51a900ef811f) · [config](https://app.sensible.so/editor/?d=claims_t1_none&c=all&g=two_images); the example's control: [config](https://app.sensible.so/editor/?d=ocr_omit_quote_control&c=all&g=cgl_quote_screenshot) |
| The example's Output block | holds with `omit` | [config](https://app.sensible.so/editor/?d=ocr_omit_quote&c=all&g=cgl_quote_screenshot) (run IDs not saved). **Rerun with `ocrIfMissing` after the deploy.** |

## Not tested yet (scored worth testing)

Evidence is engine code only (engine `main`, 2026-11-19):

- [ ] **Empty array OCRs nothing.** `ocr.ts` returns no pages when `standardizeMatch` gives none. Test: `"ocrIfMissing": []` on the screenshot quote; expect `total_premium` null.
- [ ] **Can be combined only with Engine.** `types.ts` union variant and the schema's `additionalProperties: false`. Test: publish with `match` added (expect rejection) and with `engine` (expect success).
- [ ] **Match is required unless Page Lines Limit or OCR If Missing is set.** Schema `required` lists. Test: publish `{"type": "ocr"}` alone; expect rejection.

## For Frances to judge: worth testing or not

Jev scored these between 0.30 and 0.70 (unsure). Wording is from the 2026-11-19 dry run; the page has changed since.

- [ ] "Use the OCR If Missing parameter for documents with enough embedded text that Sensible doesn't OCR them by default." (0.65) Advice, but it implies the default-OCR behavior tested above.
- [ ] "Choose OCR If Missing text that's in every document of this type, but that can variably need OCR." (0.52) Advice.
- [ ] "Because the rest of the example quote is embedded text, Sensible doesn't OCR it by default." (0.52) Already backed by the control run above.
- [ ] Not on the page, so not scored: `ocrIfMissing` also accepts a plain string (`AnchorMatch` includes `string`), but the value column says "Match object or Match array". Document the string form, or leave it out like the Match row does?

## Evidence records (approved 2026-11-19)

The three tested claims above are recorded as record-only claims in `scripts/doc-detective/testable-claims/pr-825-ocr-if-missing/`, listed by a `tested claims` comment after the Parameters table. The tooling that validates them (`codetests/evidence.py`) is on sensible-hq/sensible-docs#834, so merge #834 first.

## Before merging
- [ ] #834 merged; rebase this branch on `v0`, then run `python3 scripts/doc-detective/codetests/evidence.py check` and `python3 scripts/doc-detective/test_matrix.py` and commit the regenerated matrix

- [x] #3533 deployed to production: on 2026-11-20 publishing `ocrIfMissing` succeeded and `omit` was rejected (docs test account)
- [x] Reran the example with `ocrIfMissing` in the docs test account (2026-11-20): output matches the Output block (extraction 94c3ccf2-cfb1-489b-aa8f-a619bdaa4af6); the control without the preprocessor returns both fields null (7b3a5d2c-3a4d-4aae-b8b6-c5383afbec49)
- [x] Page Range finding: eng (2026-11-20) described the same effect for `pageLinesLimit` after Remove Page or Page Filter, Decided 2026-11-20: eng will fix Page Range; Remove Page and Page Filter stay known limitations. Frances's note after the parameter table recommends specifying the OCR preprocessor first. The draft bug report (`.claude/sessions/testable-claims/eng-page-range-bug.md` on #834) is no longer needed.
- [x] Note scope (2026-11-20): eng will fix Page Range; Remove Page and Page Filter stay known limitations (arbitrary pages are harder). The note names only Remove Page: Page Range will be fixed, and Page Filter's only page is the hidden, deprecated `deprecated-page-filter`. The note's first sentence (specify the OCR preprocessor first) covers both until then.
- [ ] When eng's Page Range fix deploys, nothing on the page needs to change; optionally rerun `claims_t2_test` to confirm the fix
- [x] Independent rerun of the page's example, config and PDF taken from the page (docs test account, 2026-11-20): example PDF matches the Output block (32f7f3ab-857d-4350-b509-c8ffef84f158); digital version matches with no OCR (166 ms, 3bdbcc87-a8fd-491e-8f0b-c1054ae35d49); control without the preprocessor returns both fields null (7b3f59fd-2b35-483e-bb96-a9da79d9764c). Doc types `rerun_ocr_if_missing` and `rerun_ocr_if_missing_control`.
- [ ] Update the test doc types in Frances's account to `ocrIfMissing`, or delete them: production `ocr_omit_*` (4), `ocr_array_*` (2), `claims_*` (10); dev `ocr_if_missing_quote` (unpublished draft)
- [ ] Remaining Vale errors are on unchanged rows (`matchAll`, `pageOffset`, "Addendums"); fix or leave
