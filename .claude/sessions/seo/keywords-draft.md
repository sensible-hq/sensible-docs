# SEO/GEO phrases draft

> **Status 2026-10-20:** Proposed excerpts for #1–41 are applied to the pages (`apply_excerpts.py`).
> #42 is pending (OpenAPI spec). First-~150-words rewrites are still to do.

- **Decision (2026-10-20): no `metadata.keywords`.** ReadMe stores the field but strips it from the rendered
  page, `.md`, and `llms.txt`, so it isn't worth filling in. Phrases only count where people and crawlers
  read them: title, excerpt (-> meta description and llms.txt description), and body text.
- **Candidate phrases**: the pool of synonyms and search phrases for the page. `*` = phrase does not
  appear anywhere in the page body today. Candidates not promoted to Best phrases aren't used.
- **Excerpt = source of truth.** You edit `excerpt`; `sync_description.py` (docs/ only, via the
  `generate-descriptions` workflow) copies it to `metadata.description`, which renders as the meta
  description and feeds `llms.txt` (`scripts/llms_txt/generate.py`). reference/ pages aren't auto-synced.
- **Proposed excerpt**: a new excerpt (target <= 150 chars, hard cap 160), drafted by subagents per topic
  group and checked at fan-in for length, parse-words, and phrase collisions. *Why:* explains the change.
- Research notes behind the phrase choices are kept privately (not in this repo).
- **Best phrases**: the 2–4 phrases to work into the excerpt and first ~150 words. Each phrase is assigned
  to one primary page to avoid pages competing for the same term.
- **Excerpt rule (2026-10-20): no self-naming.** An excerpt never names its own method, object, or
  preprocessor (the slug already does). Overview pages that list several methods (#12, #32) may name them.
- **Terminology rule (2026-10-20): "extract," not "parse."** Docs use "extract" consistently. Parse-words
  appear in body text only once: the defined alias on the Overview ("...extracts structured data from
  documents (also called document parsing)"). (An email-page alias was tried and removed per review.)

Pages are grouped by topic. Page numbers are stable IDs (other notes refer to them, e.g. "#27"), so they aren't sequential within groups.

## Overview and getting started

### 1. Overview
File: `welcome/overview.md`
#### Current excerpt (146 chars)
Sensible is a developer-first document data extraction platform using SenseML to pull structured JSON from PDFs, emails, spreadsheets, and images.
#### Proposed excerpt (149 chars)
Sensible is a developer-first platform for PDF data extraction and intelligent document processing. Get JSON from PDFs, emails, spreadsheets, images.
*Why:* Current is accurate but leads with a generic category; puts two Best phrases in the first 100 chars and keeps the PDF-to-JSON outcome; drops 'SenseML' (not a search term). Edited at fan-in (length or wording).
#### Candidate phrases
document parser *, PDF parser *, document parsing API *, document data extraction API *, PDF data extraction *, PDF to JSON *, structured data from PDFs *, unstructured to structured data *, document AI *
#### Best phrases
document parsing (as the one defined alias: "also called document parsing"); intelligent document processing; PDF data extraction; PDF to JSON

### 2. Getting started
File: `welcome/getting-started-ai.md`
#### Current excerpt (155 chars)
Learn how to extract document data using Sensible's LLM-powered tools, from setting up your account to authoring prompts and publishing extraction configs.
#### Proposed excerpt (150 chars)
Extract data from PDFs with an LLM in minutes. Write natural-language prompts for AI data extraction, then publish and test them as a Sensible config.
*Why:* Drops the 'Learn how to' opener and account-setup filler; leads with the LLM-extraction search phrase and adds 'AI data extraction'.
#### Candidate phrases
tutorial *, AI document extraction *, extract data from PDF with LLM *, LLM PDF parsing *, GPT document extraction *, prompt-based extraction *, no-code document extraction *
#### Best phrases
AI data extraction; extract data from PDF with LLM

### 3. Getting started with layout-based extractions
File: `document extraction/getting-started.md`
#### Current excerpt (150 chars)
Extract structured data from documents using Sensible's layout-based SenseML query language, including configs, anchors, methods, and API integration.
#### Proposed excerpt (128 chars)
Write deterministic, template-based extraction rules in SenseML to extract data from forms by layout, using anchors and methods.
*Why:* Current is a feature list; new version front-loads the deterministic/template-based terms reviewers asked for and keeps the tutorial's scope (anchors, methods, test, API). Edited at fan-in (length or wording).
#### Candidate phrases
SenseML tutorial *, template-based extraction *, rule-based extraction *, deterministic extraction *, coordinate-based extraction *, zonal OCR *, extract data from forms *, PDF parsing tutorial *
#### Best phrases
deterministic extraction; template-based extraction; rule-based extraction; extract data from forms

### 4. Intelligent document processing
File: `Senseml reference/concepts/idp.md`
#### Current excerpt (158 chars)
Learn how intelligent document processing automates structured data extraction from documents to handle variability across real-world business document types.
#### Proposed excerpt (145 chars)
Intelligent document processing (IDP) automates data extraction. Use probabilistic or deterministic techniques depending on document variability.
*Why:* Drops 'Learn how'; states the definition directly with 'automated data extraction'. 'document automation' and 'document data capture' left out to avoid stuffing. Edited at fan-in (length or wording). *Revised per PR review: your wording for sentence 2; trimmed sentence 1 to fit your sentence 2.*
#### Candidate phrases
document processing automation *, document automation *, automated data extraction *, AI document processing *, document AI *
#### Best phrases
document automation; automated data extraction; document data capture

### 25. Out-of-the-box extractions
File: `document extraction/library-quickstart.md`
#### Current excerpt (152 chars)
Use Sensible's pre-built configuration library to extract data from common business documents like bank statements, tax forms, and pay stubs in minutes.
#### Proposed excerpt (145 chars)
Import pre-built templates from Sensible's configuration library to extract data from bank statements, tax forms, pay stubs, and more in minutes.
*Why:* Light tweak: swaps 'pre-built configuration library' for 'pre-built templates' (matches the app's Template library tab); 'prebuilt models' omitted as inaccurate.
#### Candidate phrases
prebuilt models *, pre-built templates *, document templates *, bank statement extraction *, pay stub extraction *, tax form extraction *, configuration library, cookbook *
#### Best phrases
prebuilt models; pre-built templates; bank statement extraction

## Files, OCR, and preprocessing

### 5. Supported file types
File: `Senseml reference/concepts/file-types.md`
#### Current excerpt (122 chars)
Sensible supports PDF, Word, Excel, CSV, JPEG, PNG, and TIFF files for extraction and classification. Support has nuances.
#### Proposed excerpt (117 chars)
Extract data from PDF, Word, Excel, CSV, JPEG, PNG, and TIFF files. Support for each file format varies by operation.
*Why:* Replaces vague 'Support has nuances' with what the page actually contains (support tables, size limits, conversions) and adds 'file format' and 'file size limits'. *Revised per PR review: your wording for sentence 2.*
#### Candidate phrases
supported formats *, file formats *, file size limits *, extract data from Excel *, extract data from Word *, scanned documents *, image to text *, email extraction *
#### Best phrases
file formats; extract data from Excel; extract data from Word; file size limits

### 6. OCR
File: `Senseml reference/concepts/ocr.md`
#### Current excerpt (157 chars)
How Sensible handles OCR for document extraction, including configurable options for OCR level, preprocessor, and engine settings by document type or config.
#### Proposed excerpt (133 chars)
Sensible OCRs scanned PDFs and images automatically. Configure OCR level, per-page OCR, and the engine: Amazon, Google, or Microsoft.
*Why:* Drops 'How Sensible handles' opener; leads with scanned PDFs/images-to-text and names the three engines (searchable). 'OCR API' not used: page isn't about an API. Edited at fan-in (length or wording). *Revised per PR review: cut 'to text'.*
#### Candidate phrases
OCR API *, scanned PDF *, image to text *, text recognition *, Amazon Textract *, Google Document AI *, Microsoft Azure *
#### Best phrases
OCR API; scanned PDF; image to text

### 28. OCR preprocessor
File: `Senseml reference/preprocessors/ocr-preprocessor.md`
#### Current excerpt (148 chars)
Use Sensible's OCR preprocessor to selectively OCR specific pages in documents containing both embedded text and scanned or handwritten text images.
#### Proposed excerpt (136 chars)
Force OCR on specific pages, such as scanned or handwritten pages in a PDF with embedded text. Select pages by text match or line count.
*Why:* Leads with 'force OCR' (common search term) and keeps the mixed scanned/embedded use case; adds how pages are selected. 'garbled text' omitted because the page body doesn't mention it yet. Edited at fan-in (length or wording).
#### Candidate phrases
force OCR *, garbled text *, OCR specific pages *, mixed scanned and digital PDF *, scanned pages *, embedded text, handwritten
#### Best phrases
force OCR; garbled text; OCR specific pages

### 23. Preprocessors
File: `Senseml reference/preprocessors/index.md`
#### Current excerpt (148 chars)
Learn about document preprocessors that clean up and prepare files before data extraction, including deskew, OCR, page range, multicolumn, and more.
#### Proposed excerpt (145 chars)
Clean up documents before extraction with preprocessing options: image pre-processing (deskew, rotate, scale), selective OCR, and header removal.
*Why:* Drops 'Learn about'; adds the two best phrases and replaces page range/multicolumn examples with image-cleanup ones searchers use. Edited at fan-in (length or wording).
#### Candidate phrases
preprocessing options *, image pre-processing *, document cleanup *, rotate pages *, remove headers and footers *, multi-column layout *, deskew, page range
#### Best phrases
preprocessing options; image pre-processing; document cleanup

### 29. Merge lines
File: `Senseml reference/preprocessors/merge-lines.md`
#### Current excerpt (139 chars)
Merge Lines preprocessor documentation covering how to fix oversplit, overlapping, or misaligned lines from poor scans or handwritten text.
#### Proposed excerpt (121 chars)
Fix broken text lines from poor quality scans and handwriting OCR by merging oversplit, overlapping, or misaligned lines.
*Why:* Drops 'documentation covering' filler; leads with the problem phrase searchers use, then names the preprocessor and what it fixes. *Rule: no self-naming (the slug is the page's name); removed the method/object/preprocessor name.*
#### Candidate phrases
fix broken text lines *, oversplit lines, misaligned text *, poor quality scans *, handwriting OCR, jittery lines, line merging *, text line detection *
#### Best phrases
fix broken text lines; poor quality scans; handwriting OCR

## SenseML fundamentals

### 31. SenseML reference introduction
File: `Senseml reference/senseml-reference-introduction.md`
#### Current excerpt (133 chars)
SenseML reference guide covering fields, preprocessors, LLM and layout-based methods, computed fields, sections, and config settings.
#### Proposed excerpt (134 chars)
SenseML is Sensible's document query language. Use this reference to configure fields, methods, preprocessors, sections, and settings.
*Why:* Leads with a one-line definition of SenseML and both Best phrases instead of a 'reference guide covering' list; trims the topic list. Edited at fan-in (length or wording).
#### Candidate phrases
document query language *, extraction configuration reference *, config reference *, JSON config *, extraction rules *, parsing rules *
#### Best phrases
document query language; extraction configuration reference

### 33. Field query object
File: `Senseml reference/field-query-object/index.md`
#### Current excerpt (158 chars)
How the SenseML Field query object works, including parameters and examples for extracting structured data from PDFs using layout-based and LLM-based methods.
#### Proposed excerpt (137 chars)
Define an extraction field, the basic SenseML query unit. A field uses a layout- or LLM-based method and returns its data as JSON output.
*Why:* Replaces the 'How X works, including' opener with what a field does and what it outputs; drops the PDF-only framing. *Rule: no self-naming (the slug is the page's name); removed the method/object/preprocessor name.*
#### Candidate phrases
extraction field definition *, JSON output *, key-value output *, data field *, field ID *, output schema *
#### Best phrases
extraction field definition; JSON output

### 11. Anchor object
File: `Senseml reference/field-query-object/anchor.md`
#### Current excerpt (118 chars)
How the Anchor object works in Sensible, including its parameters, simple and complex syntax, and how it locates data.
#### Proposed excerpt (140 chars)
Find data at variable positions by searching for a nearby keyword or landmark. Covers simple and complex syntax and search range parameters.
*Why:* Replaces the 'How X works' opener with the problem anchors solve (data that moves), using the new Best phrase 'variable positions'. *Rule: no self-naming (the slug is the page's name); removed the method/object/preprocessor name.*
#### Candidate phrases
keyword *, landmark *, search text *, text locator *, reference text *
#### Best phrases
variable positions; keyword; landmark

### 37. Match object
File: `Senseml reference/field-query-object/match.md`
#### Current excerpt (143 chars)
How Match objects define search criteria for locating text lines in documents, including string, regex, boolean, first, and repeat match types.
#### Proposed excerpt (109 chars)
Define text matching criteria for anchors and more: string, regex, fuzzy, boolean, first, and repeat matches.
*Why:* Light tweak: verb-first, puts 'text matching' up front, and adds fuzzy matching, which the page covers but the current description omits. *Rule: no self-naming (the slug is the page's name); removed the method/object/preprocessor name.*
#### Candidate phrases
text matching *, regex matching *, fuzzy match, approximate string matching *, case-insensitive match *, search criteria, boolean match
#### Best phrases
text matching; fuzzy match; regex matching

### 35. Types
File: `Senseml reference/field-query-object/types.md`
#### Current excerpt (154 chars)
Learn how to filter and format extracted data using Sensible's Type parameter, including address, boolean, currency, date, and other built-in field types.
#### Proposed excerpt (127 chars)
Normalize data: filter and format extracted values by data type, such as date, currency, and address, with custom date formats.
*Why:* Drops 'Learn how to', leads with 'normalize data', and names custom date formats, which the Date type supports. *Rule: no self-naming (the slug is the page's name); removed the method/object/preprocessor name.*
#### Candidate phrases
normalize data *, field formats *, data types *, data normalization *, date format, currency parsing *, address parsing *, type validation *
#### Best phrases
normalize data; data types; date format

## Layout-based methods

### 32. Layout-based methods
File: `Senseml reference/layout-based-methods/index.md`
#### Current excerpt (150 chars)
Layout-based extraction methods in Sensible, including Box, Table, Checkbox, Region, Regex, and more for deterministically extracting structured data.
#### Proposed excerpt (147 chars)
Positional, deterministic extraction methods in SenseML, such as Box, Table, Checkbox, Row, and Region, that extract data from documents by layout.
*Why:* Leads with 'positional, non-LLM extraction methods'; drops 'deterministically extracting' because #3 owns 'deterministic extraction'. *Revised per PR review: 'non-LLM' -> 'deterministic'.*
#### Candidate phrases
positional extraction *, non-LLM extraction *, extraction methods *, PDF extraction methods *, layout extraction *, deterministic extraction *
#### Best phrases
positional extraction; non-LLM extraction; extraction methods

### 7. Row
File: `Senseml reference/layout-based-methods/row.md`
#### Current excerpt (71 chars)
Row method matches text lines horizontally aligned with an anchor line.
#### Proposed excerpt (133 chars)
Extract text next to a label, such as the value in a key-value pair, or every line to the left or right of an anchor on the same row.
*Why:* Current is 71 chars and only defines alignment; new version says what you get (the value beside a label) and uses both Best phrases. *Revised per PR review: cut 'key-value pair extraction' (Row can return every cell in a row).* *Review round 3: cut method name; added key-value pair back, clarified that Row can return every line.*
#### Candidate phrases
extract text next to label *, value to the right of a label *, extract field by label *, key-value pair extraction *, label value pairs *, same line *, horizontal alignment *
#### Best phrases
extract text next to label; key-value pair extraction  *(review round 3: key-value pair restored, with clarification)*

### 8. Region
File: `Senseml reference/layout-based-methods/region.md`
#### Current excerpt (150 chars)
Extracts data from a rectangular region defined in inches using the Region SenseML method, with parameters for position, size, and overlap thresholds.
#### Proposed excerpt (145 chars)
Extract text from a fixed position: a rectangle set in inches from an anchor, for coordinate-based extraction. Or capture the region as an image.
*Why:* Adds the search terms for this technique and mentions image output, which the page covers; drops the overlap-threshold detail. *Revised per PR review: not zonal OCR; reworded around text vs. image (asImage) output.* *Review round 3: cut method name; added Best phrase 'coordinate-based extraction'.*
#### Candidate phrases
zonal OCR *, bounding box *, coordinate-based extraction *, fixed position extraction *, extract area of PDF *, template zone *, crop *, PDF region to image *
#### Best phrases
fixed position extraction; coordinate-based extraction  *(review: removed zonal OCR)*

### 9. Passthrough
File: `Senseml reference/layout-based-methods/passthrough.md`
#### Current excerpt (160 chars)
Learn how to use the Passthrough method to return anchor matches directly without additional extraction steps, ideal for regex-based text matching in documents.
#### Proposed excerpt (105 chars)
Return an anchor's regex match directly as output, for pattern matching without further extraction steps.
*Why:* Drops 'Learn how to use' and shortens from 160 chars; keeps the meaning and both Best phrases. *Rule: no self-naming (the slug is the page's name); removed the method/object/preprocessor name.*
#### Candidate phrases
regex match *, regular expression extraction *, pattern matching *, extract matching text *, return anchor *
#### Best phrases
regex match; pattern matching

### 10. Intersection
File: `Senseml reference/layout-based-methods/intersection.md`
#### Current excerpt (135 chars)
Learn how the Intersection method extracts data at the cross-point of two anchored lines, ideal for tables with optionally empty cells.
#### Proposed excerpt (138 chars)
Table cell lookup: extract the value at the cross-point of a row and column, ideal for tables with empty cells or variable text positions.
*Why:* Replaces the 'Learn how' opener and abstract 'cross-point of two anchored lines' with the cell-lookup wording readers search for; 'grid lookup' dropped for length. *Revised per PR review: your wording.* *Rule: no self-naming (the slug is the page's name); removed the method/object/preprocessor name.*
#### Candidate phrases
table cell lookup *, extract cell by row and column *, row and column intersection *, grid lookup *, empty table cells *, crosstab *
#### Best phrases
table cell lookup; grid lookup; extract cell by row and column; empty table cells

## LLM-based methods

### 34. LLM-based methods
File: `Senseml reference/llm-based-methods/index.md`
#### Current excerpt (111 chars)
Learn how to extract text from documents using LLM-based SenseML methods like List, Query Group, and NLP Table.
#### Proposed excerpt (145 chars)
Compare Sensible's AI extraction methods for extracting lists, tables, and key-value pairs from unstructured documents like contracts and leases.
*Why:* Replaces 'Learn how to extract text' opener with two Best phrases up front and the contracts use case the page opens with; keeps the three method names. *Revised per PR review: your wording.*
#### Candidate phrases
unstructured text extraction *, AI extraction methods *, generative AI extraction *, free text extraction *, extract from contracts *, extract from legal documents *
#### Best phrases
unstructured text extraction; AI extraction methods; extract from contracts

### 13. Query group
File: `Senseml reference/llm-based-methods/query-group.md`
#### Current excerpt (159 chars)
Query Group method extracts individual facts from documents or images using LLM prompts, with tips on grouping and phrasing queries for accurate, fast results.
#### Proposed excerpt (143 chars)
Use LLM extraction to pull facts and key-value pairs, such as an invoice date or policy limit, from documents and images. Includes prompt tips.
*Why:* Moves 'LLM extraction' into the first 40 chars and adds concrete examples from the page's opening; drops 'accurate, fast results' filler. 'document Q&A' omitted as the page never frames itself that way. *Revised per PR review: active voice; dropped 'Query Group method:' prefix (slug already names it).* *Review round 3: added key-value pairs ('individual' cut for length).*
#### Candidate phrases
LLM extraction *, AI field extraction *, extract facts *, question answering *, document Q&A *, GPT *, Claude *, Gemini *
#### Best phrases
LLM extraction; document Q&A

### 14. List
File: `Senseml reference/llm-based-methods/list.md`
#### Current excerpt (145 chars)
LLM-based List method extracts repeating data like resume work history, invoice line items, or insurance policy details from tables or free text.
#### Proposed excerpt (121 chars)
Extract lists from PDFs with an LLM, such as invoice line items, resume work history, or vehicles on an insurance policy.
*Why:* Current is decent; light rewrite to lead with the 'extract lists from PDF' Best phrase while keeping invoice line items and the page's own examples. *Revised per PR review: dropped 'List method:' prefix (applied 'same as query-group et al' here too).*
#### Candidate phrases
invoice line items *, array extraction *, extract lists from PDF *, LLM list extraction *
#### Best phrases
invoice line items; extract lists from PDF

## Tables and repeating data

### 12. Table methods
File: `Senseml reference/concepts/table-methods.md`
#### Current excerpt (153 chars)
Compare Sensible's three table extraction methods, NLP Table, Fixed Table, and Text Table, including supported features like merged cells and checkboxes.
#### Proposed excerpt (147 chars)
Extract PDF tables with the NLP Table, Fixed Table, or Text Table method. Compare methods' speed, multi-page support, merged cells, and checkboxes.
*Why:* Leads with 'extract PDF tables' and adds speed and multipage support, both of which the comparison tables cover; keeps the three method names. *Revised per PR review: 'Compare methods' speed'; 'Sensible's' -> 'the' for length.*
#### Candidate phrases
PDF table extraction *, extract tables from PDF *, table parsing *, table OCR *, line items *, table to JSON *, table to CSV *
#### Best phrases
PDF table extraction; extract PDF tables; extract table rows

### 15. NLP table
File: `Senseml reference/llm-based-methods/nlp-table.md`
#### Current excerpt (159 chars)
Extract tables from documents using natural language descriptions, with support for multi-page tables and column-level prompts via Sensible's NLP Table method.
#### Proposed excerpt (135 chars)
Prompt-based LLM table extraction: describe each column in plain language to extract tables, including tables that span multiple pages.
*Why:* Puts the method name and 'prompt-based table extraction' first; drops 'column-level prompts' jargon for plain wording; keeps multipage support. *Revised per PR review: active voice; dropped 'NLP Table method:' prefix.* *Review round 3: both Best phrases now in; 'each column' reflects column-level prompts.*
#### Candidate phrases
LLM table extraction *, AI table extraction *, extract tables with GPT *, natural language table *, table parsing *, line items *
#### Best phrases
LLM table extraction; prompt-based table extraction

### 16. Sections
File: `Senseml reference/sections/index.md`
#### Current excerpt (149 chars)
Use Sections to extract repeated or complex document elements like claims into structured arrays using horizontal or vertical section configurations.
#### Proposed excerpt (138 chars)
Extract nested or repeating data and nested tables, such as claims in a loss run, into an array of objects by defining repeating sections.
*Why:* Swaps 'structured arrays' for the Best phrases 'nested data' and 'array of objects'; adds loss runs, which the page's linked example covers. 'nested tables' left out to avoid stuffing. *Revised per PR review: dropped 'Sections method:' prefix; added Best phrase 'nested tables'.* *Review round 3: comment landed on the Current excerpt; the proposal already starts with 'Extract' and includes nested data and nested tables, so no change.* *Review round 4: your wording.*
#### Candidate phrases
nested data *, array of objects *, nested tables *, sub-documents *, group fields *, loss runs *
#### Best phrases
nested data; array of objects; nested tables

## Computed fields and data transformation

### 30. JsonLogic extensions
File: `Senseml reference/concepts/jsonlogic.md`
#### Current excerpt (157 chars)
How Sensible extends JsonLogic with custom operators for transforming and validating extracted document data, including syntax tips and supported operations.
#### Proposed excerpt (147 chars)
Transform extracted data and validate it with JsonLogic, a JSON rules engine, using Sensible's custom operators. Includes syntax tips and examples.
*Why:* Replaces 'How Sensible extends' opener with verb-first 'Transform extracted data' and names JsonLogic as a JSON rules engine for searchers who don't know the library.
#### Candidate phrases
JSON rules engine *, transform extracted data *, custom operators *, JSON logic expressions *, conditional logic *, data transformation rules *, logic-based rules *
#### Best phrases
JSON rules engine; transform extracted data; custom operators

### 40. Custom computation
File: `Senseml reference/advanced-computed-field-methods/custom-computation.md`
#### Current excerpt (147 chars)
Learn how to define custom computed fields using JsonLogic in Sensible, including summing fields, mapping arrays, and checking for non-null values.
#### Proposed excerpt (123 chars)
Define calculated fields with JsonLogic for post-processing, such as summing fields, mapping arrays, or checking for nulls.
*Why:* Drops 'Learn how to' opener, names the method, and swaps 'custom computed fields' for Best phrases 'calculated fields' and 'post-processing'; keeps the page's three examples. *Revised per PR review: dropped 'Custom Computation method:' prefix (applied 'same as query-group et al' here too).*
#### Candidate phrases
post-processing *, calculated fields *, custom logic *, derived fields *, data transformation, sum fields *
#### Best phrases
post-processing; calculated fields; custom logic

### 41. Custom computation group
File: `Senseml reference/advanced-computed-field-methods/custom-computation-group.md`
#### Current excerpt (141 chars)
Learn how to use the Custom Computation Group method with JsonLogic to transform extracted document data and return multiple computed fields.
#### Proposed excerpt (87 chars)
Transform extracted document data with JsonLogic and return multiple calculated fields.
*Why:* Drops 'Learn how to use' opener and works in both Best phrases verbatim; same claims as current. *Revised per PR review: active voice; dropped 'Custom Computation Group method:' prefix.* *Review round 3: your wording.*
#### Candidate phrases
multiple calculated fields *, data transformation *, transform extracted data *, post-processing *, custom logic *
#### Best phrases
multiple calculated fields; data transformation

## Document types, classification, and multi-document files

### 17. Fingerprint
File: `Senseml reference/config-settings/fingerprint.md`
#### Current excerpt (157 chars)
Learn how fingerprints test documents for matching text, so you can choose the config for a standalone document or find each document's pages in a portfolio.
#### Proposed excerpt (141 chars)
Handle multiple document layouts by matching text: choose a config per form revision or vendor, or find each document's pages in a portfolio.
*Why:* Replaces the 'Learn how' opener and puts 'multiple document layouts' up front; keeps both use cases (standalone config selection, portfolio pages). Skipped 'template matching' because Sensible calls these configs, not templates. Edited at fan-in (length or wording). *Revised per PR review: added 'or vendor'; cut 'Use fingerprints to'; added Best phrase 'layout detection'; dropped 'layout detection' for length.*
#### Candidate phrases
template matching *, layout detection *, document variant *, form version *, config selection *, document identification *, page classification *
#### Best phrases
multiple document layouts; template matching; layout detection; form revision

### 18. Classifying documents by type
File: `document type classification/classify.md`
#### Current excerpt (157 chars)
How Sensible classifies documents by type using classify-only APIs, single-doc extraction, and multi-doc requests including portfolios and email attachments.
#### Proposed excerpt (112 chars)
Classify documents by type with Sensible's document classification API, or as you extract portfolios and emails.
*Why:* Replaces the 'How Sensible classifies' opener with both Best phrases up front and says what you can do; covers the same three senses of classification. Edited at fan-in (length or wording). *Revised per PR review: cut 'automatically'.*
#### Candidate phrases
document classification *, document classifier *, classification API *, identify document type *, auto-classify *, document categorization *, document sorting *
#### Best phrases
document classification; classification API

### 19. Multi-document extractions
File: `document extraction/portfolio.md`
#### Current excerpt (126 chars)
Learn how to extract data from multi-document portfolio files using LLM-based or fingerprint segmentation methods in Sensible.
#### Proposed excerpt (149 chars)
Split a PDF containing multiple documents, such as a loan package, and extract each document's data separately using LLM or fingerprint segmentation.
*Why:* Leads with the task people search for ('split a PDF') instead of 'Learn how' plus 'portfolio' jargon; 'loan package' is only an example, supported by the page's 1040/bank statement/pay stub example. *Revised per PR review: 'containing multiple documents'.*
#### Candidate phrases
split PDF *, PDF splitter *, document splitting *, document segmentation *, multiple documents in one PDF *, combined PDF *, bundled documents *, packet *, loan packet *, mortgage package *
#### Best phrases
split PDF; document splitting; multiple documents in one PDF; loan package (possible)

## Quality control

### 20. Validating extractions
File: `monitor and qa/validate-extractions.md`
#### Current excerpt (142 chars)
Write JsonLogic-based validations in Sensible to quality-control document extractions, flag fields for human review, and test values and sums.
#### Proposed excerpt (149 chars)
Write JsonLogic validation rules to check extracted data, including field-level validation of values and sums, and flag extractions for human review.
*Why:* Light tweak of an already good description: swaps 'validations ... to quality-control' for the Best phrases 'validation rules' and 'field-level validation'.
#### Candidate phrases
data validation *, validation rules *, business rules *, data quality *, QA *, checksums *, flag for review *
#### Best phrases
data validation; validation rules; field-level validation

### 21. Qualifying LLM accuracy
File: `document extraction/best-practices/confidence.md`
#### Current excerpt (152 chars)
Learn how Sensible uses LLM confidence signals to qualify extraction accuracy, including signal types like ambiguous query and multiple possible answers
#### Proposed excerpt (134 chars)
Qualify extraction accuracy with LLM confidence signals like 'ambiguous query', which are more nuanced than numeric confidence scores.
*Why:* Drops 'Learn how'; adds 'confidence scores' accurately (the page contrasts signals with numeric scores) without implying Sensible returns numeric scores or detects hallucinations. Edited at fan-in (length or wording).
#### Candidate phrases
confidence scores *, LLM confidence *, extraction accuracy *, LLM accuracy *, uncertainty *, ambiguous answers *, hallucination *
#### Best phrases
confidence scores; extraction accuracy; LLM confidence

### 22. Human review
File: `monitor and qa/human-review.md`
#### Current excerpt (146 chars)
Learn how to use Sensible's Human Review tab to manually correct, approve, or reject flagged document extractions and resolve validation failures.
#### Proposed excerpt (146 chars)
Use the Human Review tab for human-in-the-loop (HITL) manual review: correct flagged extractions, check failed validations, and approve or reject.
*Why:* Drops 'Learn how'; leads with human-in-the-loop/HITL, which the current description lacks, and keeps the correct/approve/reject actions.
#### Candidate phrases
human-in-the-loop *, HITL *, manual review *, review queue *, review screen *, correct extracted data *, approve or reject
#### Best phrases
human-in-the-loop; HITL; manual review

## API and integrations

### 27. API Introduction
File: `reference/Introduction/choosing-an-endpoint.md`
#### Current excerpt (185 chars)
Overview of Sensible's API endpoints for extracting structured data from documents, including async/sync extraction, Excel conversion, portfolio extraction, and document classification.
#### Proposed excerpt (137 chars)
Choose a Sensible document data extraction API endpoint: async or sync extraction, PDF to Excel, portfolio extraction, or classification.
*Why:* Cut from 185 to 146 chars by dropping the 'Overview of' opener; leads with the Best phrase 'document data extraction API' and keeps the full endpoint list. 'PDF extraction API' and 'REST API' left out to avoid stuffing; better placed in body text. Edited at fan-in (length or wording).
#### Candidate phrases
document extraction API *, PDF extraction API *, REST API *, PDF to JSON API *, API getting started *, async vs. sync extraction, batch extraction *, polling *, webhooks
#### Best phrases
document data extraction API; PDF extraction API; REST API

### 38. API quickstart
File: `integrations/quickstart.md`
#### Current excerpt (130 chars)
Learn how to make your first Sensible API call using an example document and SenseML config to extract structured data in minutes.
#### Proposed excerpt (135 chars)
Make your first Sensible API call: run one curl command on an example document and get a hello world JSON response with extracted data.
*Why:* Light tweak: removes 'Learn how to', adds 'hello world' and curl, both of which the page actually uses.
#### Candidate phrases
first API call *, hello world, API example *, curl example *, Postman *, quickstart
#### Best phrases
first API call; hello world

### 36. API tutorial
File: `api/api-tutorial/index.md`
#### Current excerpt (157 chars)
Learn how to extract structured data from documents using the Sensible API with tutorials covering synchronous, asynchronous, and webhook extraction methods.
#### Proposed excerpt (147 chars)
Document extraction API tutorials: step-by-step guides to extracting structured data with the Sensible API via sync, async, and webhook extraction.
*Why:* Removes 'Learn how to' and leads with the Best phrase; same scope as current (sync, async, webhook tutorials).
#### Candidate phrases
document extraction API tutorial *, step-by-step API guide *, REST API tutorial *, sync vs. async extraction *, extraction API examples *
#### Best phrases
document extraction API tutorial; step-by-step API guide

### 42. Extract data from a document (sync)
File: `reference/Extraction/document-1/extract-data-from-a-document.md`
#### Current excerpt (35 chars; OpenAPI summary (no excerpt; page is spec-generated))
Extract data from a document (sync)
#### Proposed excerpt (140 chars)
Synchronous extraction API for testing: upload a PDF or image and get extracted data in the response. Use the async endpoints in production.
*Why:* Current text is only the 35-char operation summary. Page is spec-generated, so this would go in reference/openapi_extraction.json for operationId extract-data-from-a-document; probably not 'summary' (it doubles as the page title) but the opening of 'description' or whatever field ReadMe uses for the meta description and llms.txt. Needs checking.
#### Candidate phrases
synchronous extraction API *, sync extraction endpoint *, POST /extract *, upload PDF API *, extract endpoint *
#### Best phrases
synchronous extraction API; upload PDF API

### 24. Try a webhook
File: `api/api-tutorial/api-tutorial-webhook.md`
#### Current excerpt (158 chars)
Learn how to use webhooks with Sensible's extraction API to receive push notifications when document extraction status changes, using a step-by-step tutorial.
#### Proposed excerpt (137 chars)
Set a webhook URL on a Sensible extraction request and get the webhook payload pushed when extraction status changes, instead of polling.
*Why:* Removes 'Learn how to'; uses 'webhook URL' and 'webhook payload' and adds 'polling', which the page contrasts webhooks with. 'Callback URL' not used: the page never says it. Drops 'step-by-step tutorial'; the title 'Try a webhook' already signals that.
#### Candidate phrases
webhook URL *, callback URL *, webhook tutorial *, push notification *, webhook payload, asynchronous extraction, polling
#### Best phrases
webhook URL; callback URL; webhook payload

### 26. Integrating
File: `welcome/integrate.md`
#### Current excerpt (159 chars)
Learn how to integrate Sensible document extraction using SDKs, APIs, email, Zapier, MCP server, or quick extraction tools to automate document data workflows.
#### Proposed excerpt (137 chars)
Export extracted data or send it to any application with Sensible's SDKs, API, email forwarding, Zapier, MCP server, or quick extraction.
*Why:* Removes 'Learn how to integrate' and leads with two Best phrases (second paraphrased as 'send it to any application'); keeps the same six integration options listed on the page. 'Document ingestion' not used: no natural fit.
#### Candidate phrases
export extracted data *, send extracted data to apps *, document ingestion *, workflow automation *, no-code integration *, Python SDK *, Node.js SDK *, webhooks *, email parsing *, QuickBooks *, CSV export *, Google Sheets
#### Best phrases
export extracted data; send extracted data to any application; document ingestion

### 39. Getting started with email extraction
File: `integrations/getting-started-email.md`
#### Current excerpt (154 chars)
Learn how to automatically extract structured data from email bodies and attachments by forwarding emails to Sensible using email processors and webhooks.
#### Proposed excerpt (145 chars)
Email data extraction: forward emails to Sensible to extract structured data from email bodies and attachments, then get the results via webhook.
*Why:* Removes 'Learn how to', leads with 'email data extraction', and paraphrases 'extract data from email attachments'; no parse-words per terminology rule. Drops 'email processors' for room; 'email to JSON' not used because the page never says JSON in prose.
#### Candidate phrases
email parsing *, email parser *, email body parsing *, extract data from email attachments *, email to JSON *, email import *, forward emails *, inbox automation *
#### Best phrases
email data extraction; extract data from email attachments; email to JSON

Rows 29–42 added from ReadMe page-view data (past year; see checklist).

## Weak candidates (consider cutting)

crosstab (Intersection), crop (Region), packet (Portfolio), QA and checksums (Validation),
page classification (Fingerprint), document AI (also a Google product name),
hallucination (Confidence; the page covers LLM-reported uncertainty, not hallucination detection).

