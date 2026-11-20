# Draft for eng (not sent)

To: horacio-penya (author of sensible-hq/sensible#3519). Frances asked for it to be super concise, with code evidence, and with branch links rather than commit permalinks. The links are the 2026-11-20 reruns in the docs test account with `ocrIfMissing`; the 2026-11-19 runs with `omit` gave the same results.

---

@horacio-penya possible bug in `ocrIfMissing` (#3519): it OCRs pages a Page Range preprocessor excluded, and their text comes back.

`[{ "type": "pageRange", "endPage": 1 }, { "type": "ocr", "ocrIfMissing": "Total Premium" }]` on a 2-page PDF extracts a field from page 2.
• Repro: https://app.sensible.so/extraction?e=824ede31-9eae-468e-8bbd-4eebbad0f58c
• Control, Page Range alone (page 2 excluded): https://app.sensible.so/extraction?e=8ecf74f3-7605-4f30-9950-8337cb3872bb

Code:
• Page Range only empties out-of-range pages and leaves `startPage` unset: https://github.com/sensible-hq/sensible/blob/main/src/engine/standardized-text/preprocessors/configuration/page-range.ts#L22-L26
• `ocrIfMissing` returns every page index: https://github.com/sensible-hq/sensible/blob/main/src/engine/standardized-text/preprocessors/configuration/ocr.ts#L69
• …and the OCR filter only checks `startPage`, so the emptied pages get OCR'd: https://github.com/sensible-hq/sensible/blob/main/src/engine/standardized-text/preprocessors/configuration/ocr.ts#L30-L34

Probably affects `match`-based OCR too (same filter), but I haven't tested that. Intended?

---

Line numbers were right on `main` at `02eb7dd1c` (2026-11-19); check them before sending.
