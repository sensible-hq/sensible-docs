# Revisions after the AI draft, by kind

Model: `jev-1.14.0`. 755 revision hunks; code settled 170 and Jev 585. Answers replayed from recordings.
PRs: 16 before, 5 after. Doc lines changed: 3387 before, 174 after.

## Revision lines per 100 doc lines, pooled

| Kind | Before | After | Hunks before | Hunks after |
|---|---|---|---|---|
| factual | 14.97 | 5.75 | 36 | 3 |
| copy edit | 8.06 | 19.54 | 91 | 13 |
| typo | 0.86 | 0.0 | 14 | 0 |
| elaboration | 40.33 | 9.2 | 152 | 8 |
| rewrite | 56.19 | 5.75 | 65 | 5 |
| addition | 29.02 | 2.3 | 84 | 2 |
| deletion | 24.03 | 3.45 | 77 | 3 |
| formatting | 3.63 | 0.0 | 35 | 0 |
| unsettled | 28.11 | 10.34 | 158 | 9 |

**Factual** is the closest proxy for a factual error corrected: after the edit, the page contradicts what the draft told a reader about the product. It also catches a fact that changed because the PR's scope changed, so check the list below. **Rewrite** replaced content without contradicting it.

## Per PR

| PR | Period | Doc lines | factual | copy edit | typo | elaboration | rewrite | addition | deletion | formatting | unsettled |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #508 | before | 191 | 0 | 0 | 0 | 0 | 2 | 122 | 31 | 0 | 13 |
| #515 | before | 382 | 241 | 0 | 2 | 141 | 188 | 194 | 11 | 6 | 53 |
| #586 | before | 485 | 6 | 0 | 0 | 2 | 0 | 4 | 44 | 0 | 35 |
| #589 | before | 44 | 0 | 4 | 3 | 6 | 0 | 0 | 3 | 0 | 0 |
| #590 | before | 59 | 4 | 63 | 0 | 6 | 0 | 2 | 6 | 0 | 62 |
| #612 | before | 341 | 117 | 66 | 12 | 60 | 62 | 102 | 44 | 14 | 122 |
| #622 | before | 541 | 12 | 19 | 0 | 527 | 1336 | 51 | 74 | 63 | 396 |
| #626 | before | 22 | 18 | 4 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| #637 | before | 110 | 0 | 6 | 2 | 63 | 20 | 22 | 10 | 2 | 17 |
| #641 | before | 19 | 0 | 6 | 0 | 0 | 2 | 17 | 3 | 2 | 0 |
| #642 | before | 41 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 6 | 0 |
| #715 | before | 849 | 27 | 64 | 8 | 424 | 100 | 323 | 413 | 30 | 135 |
| #718 | before | 179 | 46 | 2 | 0 | 34 | 183 | 77 | 59 | 0 | 87 |
| #729 | before | 43 | 18 | 25 | 2 | 75 | 8 | 32 | 107 | 0 | 22 |
| #730 | before | 14 | 14 | 2 | 0 | 2 | 0 | 0 | 2 | 0 | 0 |
| #742 | before | 67 | 4 | 12 | 0 | 24 | 0 | 37 | 4 | 0 | 10 |
| #798 | after | 10 | 8 | 12 | 0 | 2 | 0 | 0 | 2 | 0 | 0 |
| #800 | after | 16 | 0 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| #801 | after | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| #809 | after | 56 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| #825 | after | 90 | 0 | 10 | 0 | 14 | 10 | 4 | 4 | 0 | 14 |

## Factual changes

Each hunk Jev called factual, for a reader to confirm.

- #515 `491e56a44` docs/Senseml reference/concepts/file-types.md (0.93): `| Email bodies | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ |` → `| Email bodies | ✅ | ✅ | ❌ | ✅ | | ✅ | ✅ | ✅ | | Email attachments | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ |`
- #515 `31f24d28d` docs/Email extraction/getting-started-email.md (0.96): `3. Optionally, Sensible can treat an attachment as a [portfolio](doc:portfolio) — a single file containing mu…` → `3. Alternatively, if attachments may contain multiple documents combined in a single file — for example, a PD…`
- #515 `b902edd88` docs/Senseml reference/cell-rows.md (0.79): `"value": ">200 million", "type": "string" } }, { "book_title": { "value": "The Little Prince (Le Petit Prince…` → `"value": "200",`
- #515 `b902edd88` docs/Senseml reference/cell-rows.md (0.78): `"value": "150 million", "type": "string" } }, { "book_title": { "value": "Harry Potter and the Philosopher's …` → `"value": "150",`
- #515 `c71ff5165` docs/Senseml reference/cell-rows.md (0.89): `"source_ids": ["_sales_raw"]` → `"source_ids": ["_language_raw"]`
- #586 `ac1378b4f` reference/openapi_email.json (0.79): `"tika", "ocrmypdf", "amazon-textract",` → `"amazon", "google", "lazarus",`
- #590 `42c32fc98` docs/Senseml reference/concepts/file-types.md (0.96): `| Multi-page image formats<sup>1</sup><br/> (TIFF) | ❌ | ✅ | ✅ | ✅ | | ❌ | ❌ | ✅ |` → `| Multi-page image formats<sup>1</sup><br/> (TIFF) | ❌ | ✅ | ❌ | ✅ | | ❌ | ❌ | ✅ |`
- #590 `fb486d213` docs/Senseml reference/concepts/file-types.md (0.9): `4. Since JPEG and PNG are single-page formats, portfolio extraction returns one document.` → `4. Most JPEG or PNG files are single-document files. Rarely, a JPEG or PNG file is a portfolio file, in which…`
- #612 `662217425` reference/openapi_extraction.json (0.7): `"$ref": "#/components/schemas/ExtractionSingleResponse"` → `"$ref": "#/components/schemas/ExtractionSyncResponse"`
- #612 `662217425` reference/openapi_extraction.json (0.7): `"$ref": "#/components/schemas/ExtractionSingleResponse"` → `"$ref": "#/components/schemas/ExtractionSyncResponse"`
- #612 `a7814eb4a` docs/Senseml reference/advanced-computed-field-methods/extra-data.md (0.91): `"collision_deductible": { "value": 500, "type": "currency", "unit": "$", "source": "$500" }, "comprehensive_d…` → `"collision_deductible": { "source": "$500", "value": 500, "unit": "$", "type": "currency" }, "comprehensive_d…`
- #612 `5ee5a3d41` docs/Senseml reference/advanced-computed-field-methods/extra-data.md (0.86): `"collision_deductible": { "source": "$500", "value": 500, "unit": "$", "type": "currency" }, "comprehensive_d…` → `"collision_deductible": { "source": "$500", "value": 500, "unit": "$", "type": "currency" }, "comprehensive_d…`
- #612 `0fc326f75` docs/Senseml reference/advanced-computed-field-methods/extra-data.md (0.97): `hidden: true` → `hidden: false`
- #622 `724849c28` docs/Senseml reference/preprocessors/split-lines.md (0.71): `"anchor": { "match": { "text": "cover circumference", "type": "includes" } }, "stop": { "text": "cover shape"…` → `"anchor": { "match": { "text": "circumference", "type": "includes" } }, "stop": { "text": "cover shape", "typ…`
- #626 `48931ca5b` docs/Senseml reference/concepts/llm-models.md (0.93): `| LLM Engine parameter:<br/> mode: **fast** | GPT-4o mini | Claude 4.5 Haiku | Gemini 2.5 Flash-Lite | | LLM …` → `| LLM Engine parameter:<br/> mode: **fast** | GPT-4o mini | Claude 4.5 Haiku | Gemini 3.1 Flash-Lite | | LLM …`
- #626 `48931ca5b` docs/Senseml reference/concepts/llm-models.md (0.94): `| default | GPT-4o mini | Claude 4.5 Haiku | Gemini 2.5 Flash-Lite | | Multimodal Engine parameter: **true** …` → `| default | GPT-4o mini | Claude 4.5 Haiku | Gemini 3.1 Flash-Lite | | Multimodal Engine parameter: **true** …`
- #626 `48931ca5b` docs/Senseml reference/concepts/llm-models.md (0.93): `| default | GPT-4o (fine-tuned) | Claude 4.5 Haiku | Gemini 2.5 Flash-Lite |` → `| default | GPT-4o (fine-tuned) | Claude 4.5 Haiku | Gemini 3.1 Flash-Lite |`
- #626 `48931ca5b` docs/Senseml reference/concepts/llm-models.md (0.91): `| default | GPT-4o | Claude 4.5 Haiku | Gemini 2.5 Flash-Lite |` → `| default | GPT-4o | Claude 4.5 Haiku | Gemini 3.1 Flash-Lite |`
- #626 `48931ca5b` docs/Senseml reference/llm-based-methods/query-group.md (0.98): `| confidenceSignals | boolean<br/>or<br/>'"strict"'<br/>or<br/>object<br/>default: 'true' | If true, Sensible…` → `| confidenceSignals | boolean<br/>or<br/>'"strict"'<br/>or<br/>object<br/>default: 'true' | If true, Sensible…`
- #715 `0b364b5c6` docs/Senseml reference/postprocessors/xml-postprocessor.md (0.79): `Use the XML postprocessor to transform Sensible's 'parsed_document' output into an XML document. For example,…` → `Define your own XML output with a [JsonLogic](doc:jsonlogic)-based postprocessor. For example, use a postproc…`
- #715 `a3bfb90d5` docs/Senseml reference/postprocessors/xml-postprocessor.md (0.8): `"content": "CH Robinson Rate Confirmation"` → `"content": "AU Tax Invoice Precise"`
- #715 `a3bfb90d5` docs/Senseml reference/postprocessors/xml-postprocessor.md (0.76): `"type": "string", "value": "328298459" }, "rate": { "source": "$4,500.00", "type": "currency", "unit": "$", "…` → `"source": "328298459", "value": 328298459, "type": "number"`
- #715 `d09e997b7` docs/Senseml reference/postprocessors/xml-postprocessor.md (0.7): `"postprocessorOutput": "<load_id>328298459</load_id>\n<rate>4500</rate>"` → `"postprocessorOutput": "<document><load_id>328298459</load_id><rate>4500</rate></document>"`
- #715 `8eb4225fc` docs/Senseml reference/postprocessors/xml-postprocessor.md (0.8): `"content": "AU Tax Invoice Precise" /* hardcoded text content */` → `"content": "Rate Confirmation" /* hardcoded text content */`
- #715 `8eb4225fc` docs/Senseml reference/postprocessors/xml-postprocessor.md (0.79): `<FORM>AU Tax Invoice Precise</FORM>` → `<FORM>Rate Confirmation</FORM>`
- #715 `e3621d418` docs/Senseml reference/postprocessors/xml-postprocessor.md (0.72): `To generate one XML element per extracted field without naming each field individually in the rule, use the […` → `To generate one XML element per extracted field without naming each field individually in the rule, use the […`
- #718 `b82357528` docs/Senseml reference/concepts/jsonlogic.md (0.94): `"type": "jsonLogic",` → `"type": "xml",`
- #718 `d2c30e238` docs/Senseml reference/concepts/jsonlogic.md (0.7): `"type": "jsonLogic", "rule": { "is_array": { "preserve": ["a", "b", "c"] } }` → `"type": "xml", "rule": { "eachKey": { "tag": "document", /* root XML element */ "content": { "mapObject": [ /…`
- #718 `c03464256` docs/Senseml reference/concepts/jsonlogic.md (0.72): `"line_items": ["item_1", "item_2"]` → `"line_items": [ { "value": "item_1", "type": "string" }, { "value": "item_2", "type": "string" } ]`
- #729 `2507319e4` docs/Senseml reference/layout-based-methods/column.md (0.82): `By default, the method extracts to the edge of the page. To stop extracting at a specific line, such as the n…` → `By default, the method extracts to the end of the page. To stop extracting at a specific line, such as the ne…`
- #729 `d3aee0265` docs/Senseml reference/layout-based-methods/column.md (0.7): `| stop | [Match object](doc:match). default: 'none' | Stops extraction at the top boundary of the matched lin…` → `| stop | limited support for [Match](doc:match) object (doesn't support Match arrays or strings as values). d…`
- #729 `779801e8c` docs/Senseml reference/layout-based-methods/column.md (0.82): `| key | value | description | | :---------------- | :--------------------------------- | :-------------------…` → `| key | value | description | | :---------------- | :--------------------------------------------------------…`
- #730 `c110dedc7` docs/Senseml reference/layout-based-methods/region.md (0.76): `"width": 2.15, /* region width in inches */ "height": 0.25, /* region height in inches */ "offsetX": -0.55, /…` → `"width": 2.55, /* region width in inches */ "height": 0.6, /* region height in inches */ "offsetX": -0.65, /*…`
- #730 `c110dedc7` docs/Senseml reference/layout-based-methods/region.md (0.82): `"value": "1 2 3 4 5 7 8 9 3 – –"` → `"value": "1 2 3 – 4 5 – 7 8 9 3"`
- #730 `ee65625fb` docs/Senseml reference/layout-based-methods/region.md (0.7): `"value": "1 2 3 – 4 5 – 7 8 9 3"` → `"value": "111 – 22 – 3333"`
- #742 `f0c314d6f` docs/Senseml reference/concepts/color.md (0.7): `To manage reference documents and to change which symbols the SenseML editor displays, click **Options** in t…` → `Click the **Options** dropdown in the middle pane of the SenseML editor. The dropdown contains the following …`
- #798 `7bfcee065` docs/Senseml reference/document-type-settings/ocr-engine.md (0.79): `| Amazon | Default engine for the OCR preprocessor.<br/>Default engine for document types. | | Microsoft | Su…` → `| Amazon | Default engine for the OCR preprocessor. | | Microsoft | Default engine for document types.<br/>Su…`
- #798 `65fdfbede` docs/Senseml reference/document-type-settings/ocr-engine.md (0.75): `| Amazon | Default engine for the OCR preprocessor. | | Microsoft | Default engine for document types.<br/>Su…` → `| Amazon | Default engine for the OCR preprocessor.<br/>Default engine for document types. | | Microsoft | Su…`
- #801 `406dc8310` docs/Senseml reference/document-type-settings/ocr-engine.md (0.95): `| Google | Faster than Microsoft and suited to handwriting. Sensible merges the words that Google OCR returns…` → `| Google | Faster than Microsoft and suited to handwriting. The Google engine doesn't merge words into lines …`
