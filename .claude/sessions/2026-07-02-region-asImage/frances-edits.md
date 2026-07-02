# Frances's edits — region/asImage session (2026-07-02)

Consolidated diff: `aacc76421..bd7a671a4` (4 commits)

Files touched: `document-range.md`, `region.md`, `query-group.md`, new `concepts/images.md`

---

## Frances's stated reasons

1. Query Group and Document Range both have image-related parameters — they were siloed from each other and from the new `asImage` Region parameter.
2. Three methods now support image-related capabilities. That's enough to warrant surfacing image processing as a concept topic. Previously only Document Range supported it.

---

## Changes by file

### NEW: `docs/Senseml reference/concepts/images.md`

Created from scratch. A 2-column lookup table (Use case | Method) with three rows:

| Use case | Method |
|---|---|
| Use an LLM to extract structured data from an image. For example, extract facts about a photo of a building, such as its color and whether it's multistory-story or single-story. | use the [Query Group](doc:query-group) method with the Multimodal Engine parameter configured |
| Extract an image from a known region as an encoded string. For example, use this option when your documents contain complex charts, from which neither LLM-based nor layout-based methods can reliably extract structured data. Extract the chart as an image and show it to human to interpret. | use the [Region](doc:region) method with the As Image parameter configured |
| Search for non-labeled, non-text images in a range. For example, search for unlabeled photos of houses in a real estate document, and extract the images' coordinates. This option returns images' coordinates, which you can then use to render the images yourself. | use the [Document Range](doc:document-range) method with the Include Images parameter configured |

Plus a Notes section with:
- Coordinate conventions (top-left origin, not bottom-left as in PDF.js; in inches; ordered clockwise from top-left)
- "This topic is about processing non-text images. For information about processing text images, see [OCR](doc:ocr)."

Title of page: "Image processing"

---

### `document-range.md`

**`includeImages` parameter description** — from:
> "Returns the zero-indexed page number and coordinates of regions containing images in the document range. **Notes**: If you set `true`, also set`"type": "images"` in the `field` object (see Examples section for an example). Returns image region coordinates, not image bytes or text lines. To extract structured data from images, see the [Query Group](doc:query-group) method and configure the Multimodal Engine parameter."

To:
> "If true, Sensible searches for images in the document range and returns the zero-indexed page number and coordinates of regions containing images in the range. **Notes**: If you set `true`, also set `"type": "images"` in the `field` object (see Examples section for an example). Returns image region coordinates, not image bytes or text lines. Sensible doesn't support this parameter for scanned documents. For rendering the image coordinates returned by this parameter, see [Notes](doc:document-range#notes). For alternatives to this parameter, see [Image processing](doc:images)."

**Notes section heading** — from `## Extracting images` to `## Extracting images from Document Range coordinates`

**Notes section body** — from:
> "The Document Range supports extracting non-text images that you can then render. For example, extract photos of buildings embedded in an inspection report and save them to a backend. It doesn't support extracting structured data from the images.
>
> **Note:** To extract structured data from an image, use the [Query Group](doc:query-group) method with the Multimodal Engine parameter configured. For example, extract facts about the building, such as whether it's multistory-story or single-story.
>
> To extract images, set `"includeImages":true` for the Document Range method. Sensible returns the image region coordinates rather than the actual encoded bytes of images. If you want to extract the images themselves, you can use a PDF library in your chosen programming language to follow these general steps:
> * Render the page containing the image to a bitmap. Page numbers are zero-indexed in the Sensible output.
> * Convert Sensible's coordinates for the image region to pixel per inch (PPI) coordinates. Sensible's region coordinates follow these conventions:
>   * they're in reference to a 0.0 origin at the top left corner of the page (not the bottom left origin, as is for example the convention with the popular PDF.js library)
>   * they're in inches (to convert inches to pixels, multiply the inches coordinates by your PPI setting...)
>   * they're ordered clockwise from top left: (top left), (top right), (bottom right), (bottom left)"

To:
> "When you use the Document Range's Include Images parameter to search for images in a range, the Document Range returns the coordinates of images it finds rather than the encoded bytes of the image. If you want to extract the images themselves, use a PDF library in your chosen programming language to follow these general steps:
> * Render the page containing the image to a bitmap. Page numbers are zero-indexed in the Sensible output.
> * Convert Sensible's [coordinates](doc:image#coordinate-conventions) for the image region to pixel per inch (PPI) coordinates.
> * Extract a partial bitmap defined by the PPI coordinates of the image from the rendered page.
> * Encode the bitmap to bytes in the image format of your choice."

(Coordinate conventions bullets removed — now live in `images.md` and linked via `doc:image#coordinate-conventions`.)

**Parameter table** — column widths normalized (no content changes to other rows).

---

### `region.md`

**`asImage` parameter description** — from:
> "When true, Sensible renders the region's bounding rectangle from the PDF page and returns it as a `data:image/png;base64,...` string. Use this to capture visual content — such as signatures, stamps, or checkboxes — instead of extracting text."

To:
> "When true, Sensible returns the region as an image. Sensible returns the image's [coordinates](doc:images#notes) and its base64-encoded string, for example, `data:image/png;base64data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABMgAAABaCAYAAA....` Use this option to capture visual content instead of extracting text. For example, use this option when your documents contain complex charts, from which neither LLM-based nor layout-based methods can reliably extract structured data. Extract the chart as an image and show it to human to interpret. For alternatives to this parameter, see [Image processing](doc:images)."

---

### `query-group.md`

**Parameter table** — column widths normalized (no content changes to existing rows).

**`multimodalEngine` description** — added at end:
> "For alternatives to the Multimodal parameter, see [Image processing](doc:images)."

---

## Speculated reasons (beyond stated)

**Coordinate conventions consolidated into `images.md`** — previously lived only in `document-range.md`. Now that Region's `asImage` also returns coordinates, a single canonical home that both methods can link to was needed. The concept topic created that home.

**`asImage` description rewrite: mechanism-first → scenario-first** — Claude's original description led with the implementation ("renders the bounding rectangle... returns it as a data:image/png;base64,... string"). Frances rewrote to lead with what Sensible does from the user's perspective, consistent with her stated editorial preference for scenario-first framing. She also replaced the specific use-case list (signatures, stamps, checkboxes) with the chart-interpretation example, which better distinguishes `asImage` from the Signature method (which also deals with visual content in bounded regions).

**"show it to an end-user to review" → "show it to human to interpret"** — "end-user" and "review" imply a UI display context. "Human to interpret" is broader and makes the use case more legible: the point is that automated extraction failed and a human judgment is required.

**Scanned-doc limitation added to `includeImages`** — either always true and previously undocumented, or noticed while reviewing `includeImages` in the context of the broader image processing topic.

**`query-group.md` table reformat** — triggered by opening the file to add the `[Image processing]` cross-ref; the very wide column widths were inconsistent with other tables and were normalized while editing.
