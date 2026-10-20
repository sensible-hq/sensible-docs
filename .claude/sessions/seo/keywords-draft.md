# Keywords draft (for review)

- **Keywords**: candidate `metadata.keywords` entries. `*` = phrase does not appear anywhere in the
  page body today. Unmarked = already in the body.
- **Best 2–3 phrases**: the strongest synonyms to work into the excerpt, title, or body text, which is
  the only place search engines and LLM crawlers read them (ReadMe doesn't render
  `metadata.keywords` as a `<meta>` tag; see checklist). Each phrase is assigned to one primary page
  to avoid pages competing for the same term.
- **Revisions from competitor research**: proposed changes to Keywords and Best phrases, based on
  `competitors/*.md`. Notation: **+** add to keywords, **−** drop from keywords; **Best:** + / − = add to /
  remove from the best-phrases column, or "keep current". Source competitor in parentheses (phrases are verbatim from their titles, descriptions, or
  headings). "No change" = no competitor covers the concept.

### 1. Overview
File: `welcome/overview.md`
#### Keywords
document parser *, PDF parser *, document parsing API *, document data extraction API *, PDF data extraction *, PDF to JSON *, structured data from PDFs *, unstructured to structured data *, document AI *
#### Best phrases
PDF parser; document parsing API; PDF to JSON
#### Revisions from competitor research
**+** intelligent document processing (Ocrolus; we use it on `idp.md` but not here), extract text from PDF (Parseur). **−** document data extraction API (move to #27). Parser vocabulary confirmed: two competitors are named for it. **Best:** keep current.

### 2. Getting started
File: `welcome/getting-started-ai.md`
#### Keywords
tutorial *, AI document extraction *, extract data from PDF with LLM *, LLM PDF parsing *, GPT document extraction *, prompt-based extraction *, no-code document extraction *
#### Best phrases
AI document extraction; extract data from PDF with LLM
#### Revisions from competitor research
**+** AI data extraction (Parseur; zero hits in our docs), zero-shot (Nanonets; LLM extraction without training). **Best:** + AI data extraction; − AI document extraction.

### 3. Getting started with layout-based extractions
File: `document extraction/getting-started.md`
#### Keywords
SenseML tutorial *, template-based extraction *, rule-based extraction *, deterministic extraction *, coordinate-based extraction *, zonal OCR *, extract data from forms *, PDF parsing tutorial *
#### Best phrases
deterministic extraction; template-based extraction; rule-based extraction; extract data from forms
#### Revisions from competitor research
**+** template parsing (Parseur, "AI vs Template Parsing"), parsing rules (Docparser). **Best:** keep current.

### 4. Intelligent document processing
File: `Senseml reference/concepts/idp.md`
#### Keywords
document processing automation *, document automation *, automated data extraction *, AI document processing *, document AI *
#### Best phrases
document automation; automated data extraction
#### Revisions from competitor research
**+** document data capture / automate data capture (Docsumo), unstructured data into structured data (Docsumo; owner page for this phrase rather than #1), manual data entry (Docsumo). "Document automation" confirmed (two Ocrolus titles). **Best:** + document data capture.

### 5. Supported file types
File: `Senseml reference/concepts/file-types.md`
#### Keywords
supported formats *, file formats *, file size limits *, extract data from Excel *, extract data from Word *, scanned documents *, image to text *, email extraction *
#### Best phrases
extract data from Excel; extract data from Word; file size limits
#### Revisions from competitor research
**+** maximum document size (Parseur). (Password-protected PDFs dropped: not supported.) "File formats" is the competitors' term in 3 of 5 (we say "file types"). **Best:** + file formats; − extract data from Word.

### 6. OCR
File: `Senseml reference/concepts/ocr.md`
#### Keywords
OCR API *, scanned PDF *, image to text *, text recognition *, Amazon Textract *, Google Document AI *, Microsoft Azure *
#### Best phrases
OCR API; scanned PDF; image to text
#### Revisions from competitor research
**+** force OCR (Parseur, "When to Use the Force OCR Option": OCR a PDF even though it has embedded text, because the embedded text is garbled). Owner page for "force OCR": OCR preprocessor (#28). **Best:** keep current.

### 7. Row
File: `Senseml reference/layout-based-methods/row.md`
#### Keywords
extract text next to label *, value to the right of a label *, extract field by label *, key-value pair extraction *, label value pairs *, same line *, horizontal alignment *
#### Best phrases
key-value pair extraction; extract text next to label
#### Revisions from competitor research
No change.

### 8. Region
File: `Senseml reference/layout-based-methods/region.md`
#### Keywords
zonal OCR *, bounding box *, coordinate-based extraction *, fixed position extraction *, extract area of PDF *, template zone *, crop *, PDF region to image *
#### Best phrases
zonal OCR; bounding box; coordinate-based extraction
#### Revisions from competitor research
**+** extract text from a fixed position (Docparser title). **Best:** + fixed position extraction; − bounding box.

### 9. Passthrough
File: `Senseml reference/layout-based-methods/passthrough.md`
#### Keywords
regex match *, regular expression extraction *, pattern matching *, extract matching text *, return anchor *
#### Best phrases
regex match; pattern matching
#### Revisions from competitor research
No change.

### 10. Intersection
File: `Senseml reference/layout-based-methods/intersection.md`
#### Keywords
table cell lookup *, extract cell by row and column *, row and column intersection *, grid lookup *, empty table cells *, crosstab *
#### Best phrases
table cell lookup; grid lookup; extract cell by row and column; empty table cells
#### Revisions from competitor research
No change.

### 11. Anchor object
File: `Senseml reference/field-query-object/anchor.md`
#### Keywords
keyword *, landmark *, search text *, text locator *, reference text *
#### Best phrases
keyword; landmark
#### Revisions from competitor research
**+** variable positions (Docparser, "extract data from variable positions"), dynamically position fields (Parseur, "Use Labels to dynamically position fields"). **Best:** + variable positions.

### 12. Table methods
File: `Senseml reference/concepts/table-methods.md`
#### Keywords
PDF table extraction *, extract tables from PDF *, table parsing *, table OCR *, line items *, table to JSON *, table to CSV *
#### Best phrases
PDF table extraction; table parsing; table to CSV
#### Revisions from competitor research
**+** parse tables (Docparser), extract PDF tables (Parseur), extract table rows (Docparser), tables spanning several pages (Parseur). Tables is the topic where competitors converge most (4 of 5). **Best:** + parse tables, extract table rows; − table parsing, table to CSV.

### 13. Query group
File: `Senseml reference/llm-based-methods/query-group.md`
#### Keywords
LLM extraction *, AI field extraction *, extract facts *, question answering *, document Q&A *, GPT *, Claude *, Gemini *
#### Best phrases
LLM extraction; document Q&A
#### Revisions from competitor research
**+** key-value field extraction (Docsumo, "Key-Value Field Extraction Using LLM Prompts"; keywords only, since "key-value pair extraction" is Row's best phrase). **Best:** keep current.

### 14. List
File: `Senseml reference/llm-based-methods/list.md`
#### Keywords
invoice line items *, array extraction *, extract lists from PDF *, LLM list extraction *
#### Best phrases
invoice line items; extract lists from PDF
#### Revisions from competitor research
**+** repetitive structures (Parseur), line-items from purchase orders (Docparser). **Best:** keep current.

### 15. NLP table
File: `Senseml reference/llm-based-methods/nlp-table.md`
#### Keywords
LLM table extraction *, AI table extraction *, extract tables with GPT *, natural language table *, table parsing *, line items *
#### Best phrases
LLM table extraction; AI table extraction
#### Revisions from competitor research
**+** prompt-based table extraction (Docsumo title). **Best:** + prompt-based table extraction; − AI table extraction.

### 16. Sections
File: `Senseml reference/sections/index.md`
#### Keywords
nested data *, array of objects *, nested tables *, sub-documents *, group fields *, loss runs *
#### Best phrases
nested data; array of objects; nested tables
#### Revisions from competitor research
**+** table-in-table / tables inside tables (Parseur). "Nested tables" confirmed (Parseur). **Best:** keep current.

### 17. Fingerprint
File: `Senseml reference/config-settings/fingerprint.md`
#### Keywords
template matching *, layout detection *, document variant *, form version *, config selection *, document identification *, page classification *
#### Best phrases
template matching; layout detection; form version
#### Revisions from competitor research
**+** multiple document layouts, layout variation (Docparser), picks a template / template selection (Parseur, "Understand How Parseur Picks a Template"). **Best:** + multiple document layouts; − form version.

### 18. Classifying documents by type
File: `document type classification/classify.md`
#### Keywords
document classification *, document classifier *, classification API *, identify document type *, auto-classify *, document categorization *, document sorting *
#### Best phrases
document classification; classification API
#### Revisions from competitor research
**+** categorize a document (Docparser), classify mixed documents (Ocrolus), document routing (Nanonets, "Document Classification and Routing"). "Document classification" confirmed (Nanonets). **Best:** keep current.

### 19. Multi-document extractions
File: `document extraction/portfolio.md`
#### Keywords
split PDF *, PDF splitter *, document splitting *, document segmentation *, multiple documents in one PDF *, combined PDF *, bundled documents *, packet *, loan packet *, mortgage package *
#### Best phrases
split PDF; document segmentation; multiple documents in one PDF
#### Revisions from competitor research
**+** mixed PDF document, multi-page PDF (Ocrolus), automatically split (Docparser), combined document, PDF with multiple invoices (Docsumo), loan package (Ocrolus). **−** packet, loan packet (use Ocrolus's "loan package"). Splitting is the second most converged topic (4 of 5). **Best:** + document splitting; − document segmentation.

### 20. Validating extractions
File: `monitor and qa/validate-extractions.md`
#### Keywords
data validation *, validation rules *, business rules *, data quality *, QA *, checksums *, flag for review *
#### Best phrases
data validation; validation rules; data quality
#### Revisions from competitor research
**+** field-level validation (Docsumo), approval rules (Nanonets), logic-based rules (Ocrolus; plain-English for JsonLogic). "Business rules" confirmed (Nanonets). **Best:** + field-level validation; − data quality.

### 21. Qualifying LLM accuracy
File: `document extraction/best-practices/confidence.md`
#### Keywords
confidence scores *, LLM confidence *, extraction accuracy *, LLM accuracy *, uncertainty *, ambiguous answers *, hallucination *
#### Best phrases
confidence scores; extraction accuracy; LLM confidence
#### Revisions from competitor research
**+** extraction reasoning (Docsumo, "AI Extraction Reasoning & Confidence Scores"). "Confidence scores" confirmed (Nanonets, Docsumo); "extraction accuracy" confirmed (Docsumo). **Best:** keep current.

### 22. Human review
File: `monitor and qa/human-review.md`
#### Keywords
human-in-the-loop *, HITL *, manual review *, review queue *, review screen *, correct extracted data *, approve or reject
#### Best phrases
human-in-the-loop; HITL; manual review
#### Revisions from competitor research
**+** file review (Nanonets). "Human-in-the-loop"/"HITL" confirmed (Ocrolus); "review screen" confirmed (Docsumo). **Best:** keep current.

### 23. Preprocessors
File: `Senseml reference/preprocessors/index.md`
#### Keywords
preprocessing options *, image pre-processing *, document cleanup *, rotate pages *, remove headers and footers *, multi-column layout *, deskew, page range
#### Best phrases
preprocessing options; image pre-processing; document cleanup
#### Revisions from competitor research
No change. Both best phrases confirmed (Docparser, Docsumo).

### 24. Try a webhook
File: `api/api-tutorial/api-tutorial-webhook.md`
#### Keywords
webhook URL *, callback URL *, webhook tutorial *, push notification *, webhook payload, asynchronous extraction, polling
#### Best phrases
webhook URL; callback URL; webhook payload
#### Revisions from competitor research
**+** payload structure (Nanonets), real-time event notifications (Ocrolus), HTTP POST (Parseur). "Webhook URL" confirmed (Ocrolus). **Best:** keep current.

### 25. Out-of-the-box extractions
File: `document extraction/library-quickstart.md`
#### Keywords
prebuilt models *, pre-built templates *, document templates *, bank statement extraction *, pay stub extraction *, tax form extraction *, configuration library, cookbook *
#### Best phrases
prebuilt models; pre-built templates; bank statement extraction
#### Revisions from competitor research
**+** automated bank statement processing (Ocrolus title). "Prebuilt models" confirmed (Nanonets, "Pre-Built Model"). **Best:** keep current.

### 26. Integrating
File: `welcome/integrate.md`
#### Keywords
export extracted data *, send extracted data to apps *, document ingestion *, workflow automation *, no-code integration *, Python SDK *, Node.js SDK *, webhooks *, email parsing *, QuickBooks *, CSV export *, Google Sheets
#### Best phrases
export extracted data; workflow automation; Python SDK
#### Revisions from competitor research
**+** send extracted data to any application (Parseur title; replaces "send extracted data to apps"), email import (Nanonets). "Document ingestion" confirmed (Docsumo); Google Sheets appears in 4 of 5 competitors. **Best:** + send extracted data to any application, document ingestion; − workflow automation, Python SDK.

### 27. API Introduction
File: `reference/Introduction/choosing-an-endpoint.md`
#### Keywords
document extraction API *, PDF extraction API *, REST API *, PDF to JSON API *, API getting started *, async vs. sync extraction, batch extraction *, polling *, webhooks
#### Best phrases
document extraction API; PDF extraction API; REST API
#### Revisions from competitor research
**+** document data extraction API (moved from #1; Parseur's only hand-written meta keyword). **Best:** + document data extraction API; − document extraction API.

### 28. OCR preprocessor
File: `Senseml reference/preprocessors/ocr-preprocessor.md`
#### Keywords
force OCR *, garbled text *, OCR specific pages *, mixed scanned and digital PDF *, scanned pages *, embedded text, handwritten
#### Best phrases
force OCR; garbled text; OCR specific pages
#### Revisions from competitor research
Added from competitor research: "force OCR" is Parseur's term ("When to Use the Force OCR Option"). **Best:** keep current. Note: Sensible's default OCR level already runs OCR when embedded text is garbled (added to `ocr-level.md`), so the page should frame force OCR as the manual override for specific pages.

### 29. Merge lines
File: `Senseml reference/preprocessors/merge-lines.md`
#### Keywords
fix broken text lines *, oversplit lines, misaligned text *, poor quality scans *, handwriting OCR, jittery lines, line merging *, text line detection *
#### Best phrases
fix broken text lines; poor quality scans; handwriting OCR
#### Revisions from competitor research
No competitor equivalent. Closest: Docsumo "Image Pre-Processing" (owned by #23). **Best:** new row (added from site traffic).

### 30. JsonLogic extensions
File: `Senseml reference/concepts/jsonlogic.md`
#### Keywords
JSON rules engine *, transform extracted data *, custom operators *, JSON logic expressions *, conditional logic *, data transformation rules *, logic-based rules *
#### Best phrases
JSON rules engine; transform extracted data; custom operators
#### Revisions from competitor research
**+** logic-based rules (Ocrolus; keywords only, #20 owns validation phrases). **Best:** new row (added from site traffic).

### 31. SenseML reference introduction
File: `Senseml reference/senseml-reference-introduction.md`
#### Keywords
document query language *, extraction configuration reference *, config reference *, JSON config *, extraction rules *, parsing rules *
#### Best phrases
document query language; extraction configuration reference
#### Revisions from competitor research
**+** parsing rules (Docparser; keywords only, also on #3). **Best:** new row (added from site traffic).

### 32. Layout-based methods
File: `Senseml reference/layout-based-methods/index.md`
#### Keywords
positional extraction *, non-LLM extraction *, extraction methods *, PDF extraction methods *, layout extraction *, deterministic extraction *
#### Best phrases
positional extraction; non-LLM extraction; extraction methods
#### Revisions from competitor research
No change. "deterministic extraction" kept as keyword only; #3 owns it as a best phrase. **Best:** new row (added from site traffic).

### 33. Field query object
File: `Senseml reference/field-query-object/index.md`
#### Keywords
extraction field definition *, JSON output *, key-value output *, data field *, field ID *, output schema *
#### Best phrases
extraction field definition; JSON output
#### Revisions from competitor research
No competitor equivalent. **Best:** new row (added from site traffic).

### 34. LLM-based methods
File: `Senseml reference/llm-based-methods/index.md`
#### Keywords
unstructured text extraction *, AI extraction methods *, generative AI extraction *, free text extraction *, extract from contracts *, extract from legal documents *
#### Best phrases
unstructured text extraction; AI extraction methods; extract from contracts
#### Revisions from competitor research
No change. ("AI data extraction" is owned by #2.) **Best:** new row (added from site traffic).

### 35. Types
File: `Senseml reference/field-query-object/types.md`
#### Keywords
normalize data *, field formats *, data types *, data normalization *, date format, currency parsing *, address parsing *, type validation *
#### Best phrases
normalize data; data types; date format
#### Revisions from competitor research
**+** normalize data, field formats (Parseur, "Use Field Formats to Normalize Data"). **Best:** new row (added from site traffic).

### 36. API tutorial
File: `api/api-tutorial/index.md`
#### Keywords
document extraction API tutorial *, step-by-step API guide *, REST API tutorial *, sync vs. async extraction *, extraction API examples *
#### Best phrases
document extraction API tutorial; step-by-step API guide
#### Revisions from competitor research
No competitor equivalent. **Best:** new row (added from site traffic).

### 37. Match object
File: `Senseml reference/field-query-object/match.md`
#### Keywords
text matching *, regex matching *, fuzzy match, approximate string matching *, case-insensitive match *, search criteria, boolean match
#### Best phrases
text matching; fuzzy match; regex matching
#### Revisions from competitor research
No competitor equivalent. ("pattern matching" is owned by #9.) **Best:** new row (added from site traffic).

### 38. API quickstart
File: `integrations/quickstart.md`
#### Keywords
first API call *, hello world, API example *, curl example *, Postman *, quickstart
#### Best phrases
first API call; hello world
#### Revisions from competitor research
No competitor equivalent. Phrase "make your first API call" mirrors Payabli's llms.txt (not a competitor). **Best:** new row (added from site traffic).

### 39. Getting started with email extraction
File: `integrations/getting-started-email.md`
#### Keywords
email parsing *, email parser *, email body parsing *, extract data from email attachments *, email to JSON *, email import *, forward emails *, inbox automation *
#### Best phrases
email parsing; email parser; extract data from email attachments
#### Revisions from competitor research
**+** email body parsing (Docsumo title), email import (Nanonets). Parseur's core product is an email parser ("Create Your First Template to Extract Text From Emails"). Owner page for "email parsing" (keyword only on #26). **Best:** new row (added from site traffic).

### 40. Custom computation
File: `Senseml reference/advanced-computed-field-methods/custom-computation.md`
#### Keywords
post-processing *, calculated fields *, custom logic *, derived fields *, data transformation, sum fields *
#### Best phrases
post-processing; calculated fields; custom logic
#### Revisions from competitor research
**+** post-processing (Parseur, Nanonets, Docsumo "Post-Processing"; 3 of 5 competitors). **Best:** new row (added from site traffic).

### 41. Custom computation group
File: `Senseml reference/advanced-computed-field-methods/custom-computation-group.md`
#### Keywords
multiple calculated fields *, data transformation *, transform extracted data *, post-processing *, custom logic *
#### Best phrases
multiple calculated fields; data transformation
#### Revisions from competitor research
"post-processing" kept as keyword only; #40 owns it. **Best:** new row (added from site traffic).

### 42. Extract data from a document (sync)
File: `reference/Extraction/document-1/extract-data-from-a-document.md`
#### Keywords
synchronous extraction API *, sync extraction endpoint *, POST /extract *, upload PDF API *, extract endpoint *
#### Best phrases
synchronous extraction API; upload PDF API
#### Revisions from competitor research
No competitor equivalent. Note: the page's `.md` is a pointer to `openapi_extraction.json` (frontmatter = `api:` block only); keywords need a hand-added `metadata` block, and description/body text come from the OpenAPI operation. **Best:** new row (added from site traffic).

Rows 29–42 added from ReadMe page-view data (past year; see checklist).

## Weak candidates (consider cutting)

crosstab (Intersection), crop (Region), packet (Portfolio), QA and checksums (Validation),
page classification (Fingerprint), document AI (also a Google product name),
hallucination (Confidence; the page covers LLM-reported uncertainty, not hallucination detection).

Rows 21–25 added from competitor analysis (`competitors/summary.md`). Deliberately avoided
"pre-trained" for the library page: configs aren't trained models.
