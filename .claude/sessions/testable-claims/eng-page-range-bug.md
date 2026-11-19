# Draft for eng (not sent)

To: horacio-penya (author of sensible-hq/sensible#3519). Frances asked for it to be super concise, with code evidence, and with branch links rather than commit permalinks. The run used `omit`, the deployed name; the rename (#3533) changed no logic.

---

@horacio-penya possible bug in `ocrIfMissing` (#3519): it OCRs pages a Page Range preprocessor excluded, and their text comes back.

`[{ "type": "pageRange", "endPage": 1 }, { "type": "ocr", "ocrIfMissing": "Total Premium" }]` on a 2-page PDF extracts a field from page 2.
• Repro: https://app.sensible.so/extraction?e=a2c51a98-98cc-457e-b42e-ce4331199c04
• Control, Page Range alone (page 2 excluded): https://app.sensible.so/extraction?e=e2fb6bc2-134c-4b2d-938a-45b24a6a33e2

Code:
• Page Range only empties out-of-range pages and leaves `startPage` unset: https://github.com/sensible-hq/sensible/blob/main/src/engine/standardized-text/preprocessors/configuration/page-range.ts#L22-L26
• `ocrIfMissing` returns every page index: https://github.com/sensible-hq/sensible/blob/main/src/engine/standardized-text/preprocessors/configuration/ocr.ts#L69
• …and the OCR filter only checks `startPage`, so the emptied pages get OCR'd: https://github.com/sensible-hq/sensible/blob/main/src/engine/standardized-text/preprocessors/configuration/ocr.ts#L30-L34

Probably affects `match`-based OCR too (same filter), but I haven't tested that. Intended?

---

Line numbers were right on `main` at `02eb7dd1c` (2026-11-19); check them before sending.
