# google-ocr decisions

Claude Code session ID: bc2d327b-1002-40d8-9161-f39ecf5a8273

## Lazarus
- **Keep Lazarus in the OCR engine table, marked deprecated.** Frances's call in sensible#3468. Existing configs that specify it still work (rerouted to Microsoft), so users need to find out what happens to them.
- **Remove `lazarus` from the OpenAPI enum, explain in `x-internal-note`.** Frances's call. The backend still accepts it; the spec shouldn't advertise it.
- **Changelog entry stays an uncommitted draft** in `drafts/`, like Frances's other entry drafts.
- **Use "Lazarus" (display name), not `` `lazarus` ``, in the table.** Frances's edit; matches Amazon/Microsoft/Google in the same table.
- **Excerpt:** "Choose an OCR engine for extracting text from images: …". Frances rejected "OCRing images of text" after review: "extract" is the SEO term and "OCRing" is jargon.

## Default OCR engine
- **Amazon is the default for new doc types.** The engine's `DEFAULT_OCR_SERVICE_TYPE = "microsoft"` applies only when no `ocr_engine` is stored (older doc types, or API-created ones without it). Recorded in the `ocr_engine` `x-internal-note` so agents don't misread the engine again.
- **Never edit API reference markdown** (`reference/**/*.md`); it's generated. Only the `reference/*.json` specs.

## Google OCR
- **Test instead of asking an engineer.** Frances's call: a 72-page scanned PDF settles it.
- **Prove the engine with `prevent_default_merge_lines: true`.** The API response doesn't name the engine that ran. Google returns words; Amazon/Microsoft return lines even with merging off.
- **Drop the page limit entirely** rather than change 5 to 25: no cap exists in code, and the test OCRed page 72.
- **Rewrite, don't delete, the Merge Lines advice.** Built-in merging handles Google output; Merge Lines stays as an option for handwriting.
- **Leave the Merge Lines page's handwriting example alone** until someone reruns it.
- **Fixture config has no comments.** The runner parses the published config with `json.loads`; comments would cause permanent drift and the runner would overwrite them. The explanation lives in `manifest.json`'s description.
- **Rename the fixture in place** (PUT doc type, config, reference) to keep Frances's version history.
- **Test-only PDFs go in `scripts/test/assets/`, not `assets/pdfs/`** (rule written in `internal-doc-guidelines.md` and `assets/pdfs/README.md`). Frances's rule: `assets/pdfs/` is only for PDFs that appear in the docs. The runner only allowed `assets/pdfs/`, so `FIXTURE_PDF_DIRS` in `codetests/settings.py` now allows both folders.
- **No code test on a page yet.** Fixture tests only compare `documents` segmentation, not extracted values.
- **Stack app #1906 on #1905** to avoid conflicts on the same paragraphs.
- **Drop "Amazon is an alternative to experiment with"** from the settings tab: it contradicts "Amazon is the default engine".
