# Frances's edits — July 2026 changelog draft (2026-07-09)

Diffs between Claude's draft (published to readme.io as `july-2026`) and Frances's edited version.

---

## Intro paragraph

**Claude:**
> In the last month, Sensible attributed extractions to the user or credential that initiated them, released new configuration options for the Region method and confidence signals, added a Today operator for JsonLogic, and updated Gemini models to the 3.x line. This month's release also includes several UX improvements to the Sensible app.

**Frances:**
> In the last month, Sensible updated Gemini models to 3.x, released new configuration options for confidence signals for LLM models, added a new extended JsonLogic operation, and added advanced configuration options for the Region method. Sensible also made several UX improvements to the Sensible app.

---

## Entry order

**Claude:** New features first (Actor, Region image, JsonLogic), then Improvements (LLM models, Confidence signals, Region configurability), then UX improvements (Selective import, Bulk actions, Word wrap, Cmd+click) — 10 entries total.

**Frances:** LLM model updates first, then Actor, Region image, JsonLogic, Confidence signals, Region configurability, then 2 combined UX entries — 8 entries total (Actor attribution moved into New features; two UX pairs merged).

---

## LLM model version updates

**Claude:**
> ## Improvement: LLM model version updates
>
> Sensible updated the Gemini models used across LLM-based methods to the 3.x line: `gemini-2.5-flash-lite` becomes `gemini-3.1-flash-lite`, and `gemini-2.5-pro` becomes `gemini-3.1-pro-preview`. Default LLM providers are unchanged. For more information, see [LLM models](doc:llm-models).

**Frances:**
> ## Improvement: LLM model version updates
>
> Sensible updated the Gemini models used for LLM-based methods to 3.x from 2.x. For more information, see [LLM models](doc:llm-models).

---

## Actor attribution

**Claude:**
> ## New feature: Actor attribution on extractions
>
> Sensible now records which user or API credential initiated each extraction. The `actor` field appears on every extraction response: for extractions you initiate in the Sensible app, `actor` is your account email address; for API key extractions, it's `api_key: <key name>`, or `api_key` if the key is unnamed; for auth token extractions, it's `auth_token: <creator>`. Sensible omits `actor` for system-initiated extractions that lack authentication context, such as email processor extractions. For more information, see [Extraction](doc:extraction).

**Frances:**
> ## New feature: Trace who initiated an extraction
>
> You can now view which user or named API key initiated an extraction. API extraction responses now include a new Actor parameter that shows either your account email address (for extractions you initiate in the Sensible app), or the name of your API key (for extractions you initiate through the API or SDK). For more information, see [Extraction endpoints](ref:choosing-an-endpoint).

---

## Region as image

**Claude:**
> ## New feature: Region method returns image output
>
> You can now return a [Region](doc:region) field as a PNG image instead of extracted text. Set the new As Image parameter to `true`, and Sensible returns the region as a `data:image/png;base64,...` URI. Use this option to capture visual content — such as charts or diagrams — that neither LLM-based nor layout-based text extraction can reliably handle. For a comparison of image extraction options, see [Image processing](doc:images).

**Frances:**
> ## New feature: Extract document region as PNG
>
> You can now return a region of a document as a PNG. Use this option to capture visual content for a human to review, such as charts or diagrams. This option is useful when neither LLM-based nor layout-based methods can reliably extract data from complex images. When you set the [Region](doc:region) method's new As Image parameter to `true`, Sensible returns the region as a PNG data URI, for example, `data:image/png;base64,`,iVBORw0KGgoAA`...` . For a comparison of image extraction options, see [Image processing](doc:images).

---

## JsonLogic Today operator

**Claude:**
> ## New feature: Today operator for JsonLogic
>
> Sensible released the new Today operator for [JsonLogic](doc:jsonlogic). The operator returns the current UTC date as a `YYYY-MM-DD` string and takes no arguments. Combine it with the existing Date Shift operator to compute dates relative to today — for example, a contract expiration date one year from the current date — without hardcoding a date in your config. For more information, see [JsonLogic](doc:jsonlogic).

*(Then updated by Claude to:)*
> ## New feature: Advanced JsonLogic date operation
>
> In addition to the existing [JsonLogic](doc:jsonlogic) operators for transforming extracted data, Sensible released the new Today operator. The operator returns the current UTC date as a `YYYY-MM-DD` string and takes no arguments. Combine it with the existing Date Shift operator to compute dates relative to today — for example, a contract expiration date one year from the current date — without hardcoding a date in your config. For more information, see [JsonLogic](doc:jsonlogic#today).

**Frances:**
> ## New feature: Advanced JsonLogic date operation
>
> In addition to the existing [JsonLogic](doc:jsonlogic) operators for transforming extracted data,<br />Sensible released the new Today operator. The operator returns the current UTC date as a `YYYY-MM-DD` string and takes no arguments. Combine it with the existing Date Shift operator to compute dates relative to today without specifying a hardcoded date in your config. For more information, see [JsonLogic](doc:jsonlogic#today).

---

## Confidence signals engine

**Claude:**
> ## Improvement: Configurable engine for confidence signals
>
> You can now configure which LLM provider evaluates [confidence signals](doc:query-group) for your configs. Previously, confidence signals always ran on OpenAI. Set the `engine` option on the Confidence Signals parameter to route to `anthropic`, `google`, or `open-ai`. For more information, see [LLM models](doc:llm-models).

**Frances:**
> ## Improvement: Configure which LLM qualifies accuracy
>
> You can now configure which LLM provider qualifies the accuracy of your LLM-based extractions. Previously, Sensible used OpenAI to qualify accuracy with [confidence signals](doc:confidence). Now, you can set the Confidence Signals parameter's new Engine parameter to `anthropic`, `google`, or `open-ai`. For more information, see <Anchor target="_blank" href="doc:llm-models">LLM models</Anchor>.

---

## Region overlap thresholds

**Claude (after update):**
> ## Improvement: Advanced configurability for the Region method
>
> For the [Region](doc:region) method, you can now relax the criteria by which Sensible determines that a region "contains" lines. For example, use the new Percent Overlap X and Percent Overlap Y parameters to extract lines that partially extend outside the region boundary. For more information, see [Region](doc:region).

**Frances:**
> ## Improvement: Advanced configurability for the Region method
>
> For the Region method, you can now relax the criteria by which Sensible determines that a region "contains" lines. Use the new Percent Overlap X and Percent Overlap Y parameters to extract lines that partially extend outside the region boundary. For more information, see [Region](doc:region).

---

## UX: Selective config import + Bulk actions for Reference Documents

Claude wrote these as two separate entries. Frances merged them into one.

**Claude (two entries):**
> ## UX improvement: Selective config import from the library
>
> When importing from the [config library](doc:config-library), you can now choose individual configurations instead of importing the entire package. Each configuration is selected by default; deselect any you don't need before cloning.
>
> <!-- SCREENSHOT NEEDED: source PR #1831 ... -->
> <!-- DOC LINK NEEDED: no public page for selective config import -->

> ## UX improvement: Bulk actions for Reference Documents
>
> In the **Reference Documents** tab of the Sensible app, you can now select multiple documents and act on them at once. Supported bulk actions are **Delete**, **Assign** (to a document type), and **Unassociate**.
>
> <!-- SCREENSHOT NEEDED: source PR #1830 ... -->
> <!-- DOC LINK NEEDED: no public page for Reference Documents bulk actions -->

**Frances (one merged entry, with screenshots):**
> ## UX improvement: Bulk actions
>
> In the Sensible, app, you now have more selection control over reference documents in document types and over templates in the config library.
>
> When importing from the [config library](doc:library-quickstart) in the **Template library** tab, you can now choose individual configurations instead of importing the entire package. Deselect any configs you don't need before cloning, and Sensible omits the unwanted configs and their reference documents.
>
> ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_july2026_clone.png)
>
> In a document type's **Reference Documents** tab, you can now select multiple documents and act on them in bulk, including deleting them, assigning them all to one config, or unassociating each from its config.
>
> ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_july2026_ref.png)

---

## UX: Word wrap + Cmd+click

Claude wrote these as two separate entries. Frances merged them into one.

**Claude (two entries):**
> ## UX improvement: Word wrap in the config editor
>
> You can now toggle word wrap in the SenseML config editor. Use the **Toggle word wrap** option to wrap long lines instead of scrolling horizontally.
>
> <!-- SCREENSHOT NEEDED: source https://github.com/user-attachments/assets/3a3c366b-5c4c-4de1-9804-8c39689f58d6 ... -->
> <!-- DOC LINK NEEDED: no public page for word wrap in config editor -->

> ## UX improvement: Cmd+click to insert text on macOS
>
> In the extraction viewer, you can now use **Cmd+click** on a bounding box to insert that line's text at the editor cursor. Previously, **Ctrl+click** was the shortcut on all platforms, but macOS intercepts Ctrl+click as a right-click. On Windows and Linux, **Ctrl+click** continues to work as before.
>
> <!-- DOC LINK NEEDED: no public page for Cmd+click shortcut -->

**Frances (one merged entry, with screenshots):**
> ## UX improvement: SenseML editor
>
> Sensible has improved the SenseML editor's viewing and copying features.
>
> You can now toggle word wrap in the SenseML editor. Right click anywhere in the left pane of the SenseML editor with JSON view selected, then select **Toggle word wrap** option to wrap long lines of SenseML, instead of scrolling horizontally.
>
> ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_july2026wordwrap.png)
>
> In the SenseML editor in MacOS, you can now hold **Command** and click on a line in the rendered PDF to insert that line's text at the editor cursor in the left pane. Previously, holding **Control** and clicking was the shortcut on all platforms, but macOS intercepts that shortcut as a right click. On Windows and Linux, holding **Control** and clicking continues to work.
>
> ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelist_july2026copy.png)
