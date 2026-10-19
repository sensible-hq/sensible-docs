# Keywords draft (for review)

- **Keywords**: candidate `metadata.keywords` entries. `*` = phrase does not appear anywhere in the
  page body today. Unmarked = already in the body.
- **Best 2–3 phrases**: the strongest synonyms to work into the excerpt, title, or body text, which is
  the only place search engines and LLM crawlers read them (ReadMe doesn't render
  `metadata.keywords` as a `<meta>` tag; see checklist). Each phrase is assigned to one primary page
  to avoid pages competing for the same term.

| # | Page | Keywords | Best 2–3 phrases (excerpt/body) |
|---|---|---|---|
| 1 | Overview<br>`welcome/overview.md` | document parser *, PDF parser *, document parsing API *, document data extraction API *, PDF data extraction *, PDF to JSON *, structured data from PDFs *, unstructured to structured data *, document AI * | PDF parser; document parsing API; PDF to JSON |
| 2 | Getting started<br>`welcome/getting-started-ai.md` | tutorial *, AI document extraction *, extract data from PDF with LLM *, LLM PDF parsing *, GPT document extraction *, prompt-based extraction *, no-code document extraction * | AI document extraction; extract data from PDF with LLM |
| 3 | Getting started with layout-based extractions<br>`document extraction/getting-started.md` | SenseML tutorial *, template-based extraction *, rule-based extraction *, deterministic extraction *, coordinate-based extraction *, zonal OCR *, extract data from forms *, PDF parsing tutorial * | deterministic extraction; template-based extraction; rule-based extraction; extract data from forms |
| 4 | Intelligent document processing<br>`Senseml reference/concepts/idp.md` | document processing automation *, document automation *, automated data extraction *, AI document processing *, document AI * | document automation; automated data extraction |
| 5 | Supported file types<br>`Senseml reference/concepts/file-types.md` | supported formats *, file formats *, file size limits *, extract data from Excel *, extract data from Word *, scanned documents *, image to text *, email extraction * | extract data from Excel; extract data from Word; file size limits |
| 6 | OCR<br>`Senseml reference/concepts/ocr.md` | OCR API *, scanned PDF *, image to text *, text recognition *, Amazon Textract *, Google Document AI *, Microsoft Azure * | OCR API; scanned PDF; image to text |
| 7 | Row<br>`Senseml reference/layout-based-methods/row.md` | extract text next to label *, value to the right of a label *, extract field by label *, key-value pair extraction *, label value pairs *, same line *, horizontal alignment * | key-value pair extraction; extract text next to label |
| 8 | Region<br>`Senseml reference/layout-based-methods/region.md` | zonal OCR *, bounding box *, coordinate-based extraction *, fixed position extraction *, extract area of PDF *, template zone *, crop *, PDF region to image * | zonal OCR; bounding box; coordinate-based extraction |
| 9 | Passthrough<br>`Senseml reference/layout-based-methods/passthrough.md` | regex match *, regular expression extraction *, pattern matching *, extract matching text *, return anchor * | regex match; pattern matching |
| 10 | Intersection<br>`Senseml reference/layout-based-methods/intersection.md` | table cell lookup *, extract cell by row and column *, row and column intersection *, grid lookup *, empty table cells *, crosstab * | table cell lookup; grid lookup; extract cell by row and column; empty table cells |
| 11 | Anchor object<br>`Senseml reference/field-query-object/anchor.md` | keyword *, landmark *, search text *, text locator *, reference text * | keyword; landmark |
| 12 | Table methods<br>`Senseml reference/concepts/table-methods.md` | PDF table extraction *, extract tables from PDF *, table parsing *, table OCR *, line items *, table to JSON *, table to CSV * | PDF table extraction; table parsing; table to CSV |
| 13 | Query group<br>`Senseml reference/llm-based-methods/query-group.md` | LLM extraction *, AI field extraction *, extract facts *, question answering *, document Q&A *, GPT *, Claude *, Gemini * | LLM extraction; document Q&A |
| 14 | List<br>`Senseml reference/llm-based-methods/list.md` | invoice line items *, array extraction *, extract lists from PDF *, LLM list extraction * | invoice line items; extract lists from PDF |
| 15 | NLP table<br>`Senseml reference/llm-based-methods/nlp-table.md` | LLM table extraction *, AI table extraction *, extract tables with GPT *, natural language table *, table parsing *, line items * | LLM table extraction; AI table extraction |
| 16 | Sections<br>`Senseml reference/sections/index.md` | nested data *, array of objects *, nested tables *, sub-documents *, group fields *, loss runs * | nested data; array of objects; nested tables |
| 17 | Fingerprint<br>`Senseml reference/config-settings/fingerprint.md` | template matching *, layout detection *, document variant *, form version *, config selection *, document identification *, page classification * | template matching; layout detection; form version |
| 18 | Classifying documents by type<br>`document type classification/classify.md` | document classification *, document classifier *, classification API *, identify document type *, auto-classify *, document categorization *, document sorting * | document classification; classification API |
| 19 | Multi-document extractions<br>`document extraction/portfolio.md` | split PDF *, PDF splitter *, document splitting *, document segmentation *, multiple documents in one PDF *, combined PDF *, bundled documents *, packet *, loan packet *, mortgage package * | split PDF; document segmentation; multiple documents in one PDF |
| 20 | Validating extractions<br>`monitor and qa/validate-extractions.md` | data validation *, validation rules *, business rules *, data quality *, QA *, checksums *, flag for review * | data validation; validation rules; data quality |
| 21 | Qualifying LLM accuracy<br>`document extraction/best-practices/confidence.md` | confidence scores *, LLM confidence *, extraction accuracy *, LLM accuracy *, uncertainty *, ambiguous answers *, hallucination * | confidence scores; extraction accuracy; LLM confidence |
| 22 | Human review<br>`monitor and qa/human-review.md` | human-in-the-loop *, HITL *, manual review *, review queue *, review screen *, correct extracted data *, approve or reject | human-in-the-loop; HITL; manual review |
| 23 | Preprocessors<br>`Senseml reference/preprocessors/index.md` | preprocessing options *, image pre-processing *, document cleanup *, rotate pages *, remove headers and footers *, multi-column layout *, deskew, page range | preprocessing options; image pre-processing; document cleanup |
| 24 | Try a webhook<br>`api/api-tutorial/api-tutorial-webhook.md` | webhook URL *, callback URL *, webhook tutorial *, push notification *, webhook payload, asynchronous extraction, polling | webhook URL; callback URL; webhook payload |
| 25 | Out-of-the-box extractions<br>`document extraction/library-quickstart.md` | prebuilt models *, pre-built templates *, document templates *, bank statement extraction *, pay stub extraction *, tax form extraction *, configuration library, cookbook * | prebuilt models; pre-built templates; bank statement extraction |

## Weak candidates (consider cutting)

crosstab (Intersection), crop (Region), packet (Portfolio), QA and checksums (Validation),
page classification (Fingerprint), document AI (also a Google product name),
hallucination (Confidence; the page covers LLM-reported uncertainty, not hallucination detection).

Rows 21–25 added from competitor analysis (`competitors/summary.md`). Deliberately avoided
"pre-trained" for the library page: configs aren't trained models.
