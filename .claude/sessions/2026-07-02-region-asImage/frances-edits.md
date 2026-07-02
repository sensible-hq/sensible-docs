# Frances's edits — region/asImage session (2026-07-02)

Four commits: `59edcc102`, `501d9c847`, `9487b8684`, `bd7a671a4`

Files touched: `document-range.md`, `region.md`, `query-group.md`, new `concepts/images.md`

---

## Frances's stated reasons

1. Query Group and Document Range both have image-related parameters — they were siloed from each other and from the new `asImage` Region parameter.
2. Three methods now support image-related capabilities. That's enough to warrant surfacing image processing as a concept topic. Previously only Document Range supported it.

---

## Edit-by-edit log

### Commit 1 — `document-range.md` (59edcc102)

**`includeImages` description** — rewrote from:
> "Returns the zero-indexed page number and coordinates of regions containing images in the document range. **Notes**: If you set `true`, also set `"type": "images"` in the `field` object... Returns image region coordinates, not image bytes or text lines. To extract structured data from images, see the Query Group method and configure the Multimodal Engine parameter."

To:
> "If true, Sensible searches for images in the document range and returns the zero-indexed page number and coordinates of regions containing images in the range. **Notes**: If you set `true`, also set `"type": "images"` in the `field` object... Returns image region coordinates, not image bytes or text lines. Sensible doesn't support this parameter for scanned documents. For alternatives to this parameter, see [Notes](doc:document-range#notes)."

Changes: active subject ("Sensible searches"), added scanned-doc limitation, changed cross-ref from inline link to [Notes] anchor.

**Notes section heading** — changed "Extracting images" → "Options for processing images"

**Notes section body** — replaced a 2-sentence paragraph + Note callout with a 3-bullet list:
- LLM structured extraction → Query Group + Multimodal Engine
- Image from known region as encoded string → Region + As Image
- Search for non-labeled images in a range → Document Range (this option)

Also left draft text at the bottom (italic, clearly in-progress, cleaned up in commit 2):
> *extract image coordinates from Document Range supports extracting the coordinates of non-text images that you can then render...*

---

### Commit 2 — new `concepts/images.md` + `document-range.md` cleanup (501d9c847)

**New file `docs/Senseml reference/concepts/images.md`** — created with:
- Frontmatter title: "Extracting from images" (note: in this commit the YAML block was accidentally wrapped in backticks instead of being proper frontmatter — fixed in commit 3)
- Same 3-bullet list moved from document-range.md Notes

**`document-range.md` `includeImages`** — updated cross-ref to add:
> "For alternatives to this parameter, see [Processing Images](doc:images)."

**`document-range.md` Notes** — heading changed back to "Extracting images from Document Range coordinates" (more specific than "Options for processing images"). The 3-bullet list removed (now lives in images.md). Updated the opening sentence of the coordinate instructions to use "When you use the Document Range's Include Images parameter to search for images in a range, the Document Range returns the coordinates..."

---

### Commit 3 — `images.md`, `document-range.md`, `region.md`, `query-group.md` (9487b8684)

**`images.md`** — substantial revision:
- Title changed: "Extracting from images" → "Image processing"
- Converted 3-bullet list to a 2-column table (Use case | Method):

| Use case | Method |
|---|---|
| LLM extracts structured data from an image | Query Group + Multimodal Engine |
| Extract image from known region as encoded string | Region + As Image |
| Search for non-labeled non-text images in a range | Document Range + Include Images |

- Added Notes section with coordinate conventions:
  - Origin at top-left of page (not bottom-left as in PDF.js)
  - In inches; conversion example given (72 PPI × 3.156 inches ≈ 227 pixels)
  - Ordered clockwise from top-left
- Added: "This topic is about processing non-text images. For information about processing text images, see [OCR](doc:ocr)."

**`document-range.md` `includeImages`** — cross-ref updated: "Processing Images" → "Image processing" (matching renamed title)

**`document-range.md` Notes** — removed coordinate conventions bullets (now in images.md), replaced with single link: `doc:image#coordinate-conventions`

**`region.md` `asImage`** — rewrote description from:
> "When true, Sensible renders the region's bounding rectangle from the PDF page and returns it as a `data:image/png;base64,...` string. Use this to capture visual content — such as signatures, stamps, or checkboxes — instead of extracting text."

To:
> "When true, Sensible returns the region as an image. Sensible returns the image's coordinates and its base64-encoded string, for example, `data:image/png;base64data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABMgAAABaCAYAAA....` Use this option to capture visual content instead of extracting text. For alternatives to this parameter, see [Image processing](doc:images)."

**`query-group.md`** — reformatted the entire parameter table: narrowed column widths (no content changes). Added to `multimodalEngine` description:
> "For alternatives to the Multimodal parameter, see [Image processing](doc:images)."

---

### Commit 4 — `images.md`, `region.md` tweaks (bd7a671a4)

**`images.md`** — Region row example: "show it to an end-user to review" → "show it to human to interpret"

**`region.md` `asImage`** — two changes:
1. Added `[coordinates](doc:images#notes)` link to "Sensible returns the image's coordinates"
2. Added example sentence: "For example, use this option when your documents contain complex charts, from which neither LLM-based nor layout-based methods can reliably extract structured data. Extract the chart as an image and show it to human to interpret."

---

## Speculated reasons (beyond stated)

**Coordinate conventions moved to images.md** — the coordinate notes (top-left origin, inches, clockwise) were previously only in document-range.md. Now that Region's `asImage` also returns coordinates, the information needs to live in one canonical place that both methods can link to. Creating the concept topic gave her a natural home for it.

**query-group.md table reformatting** — no content change, just column width normalization. Likely triggered by the need to add the `[Image processing]` cross-ref and noticing the table was formatted with very wide columns inconsistent with the rest of the docs.

**"Extracting from images" → "Image processing"** — the initial title "Extracting from images" implies getting bytes out. But Document Range's use case (extracting coordinates) and Query Group's use case (LLM extraction) don't fit that framing cleanly. "Image processing" is broader and neutral.

**Region `asImage` description rewrite** — Claude's original description was mechanism-first ("renders the bounding rectangle... returns it as a data:image/png;base64,... string"). Frances rewrote to be user-facing and scenario-grounded, consistent with her stated editorial preference for scenario-first framing. She also dropped the specific use-case examples (signatures, stamps, checkboxes) in favor of the chart-interpretation example, which better distinguishes `asImage` from the Signature method.

**Scanned-doc limitation added** — "Sensible doesn't support this parameter for scanned documents" added to `includeImages`. This was either always true and previously undocumented, or Frances noticed it while reviewing the includeImages behavior in context of the broader image processing topic.

**"show it to an end-user to review" → "show it to human to interpret"** — subtle framing shift. "End-user" and "review" suggest a UI display context. "Human to interpret" is broader — covers human review in any context, including an analyst receiving the base64 string. The change also makes the use case more legible: the point is that a human is needed because automated extraction failed.
