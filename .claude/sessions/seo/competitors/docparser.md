# Docparser: top 20 docs pages and the phrases they target

Researched 2026-10-19. Sites: https://help.docparser.com (Zendesk Help Center). Platform: Zendesk
Guide; data pulled from the public Help Center API (`/api/v2/help_center/en-us/articles.json`, 2
pages). Total pages: 183 articles across 17 sections (Parsing Rules, Filters, Table Parsing,
Integrations, Importing Documents, etc.).
Meta keywords usage: not retrievable. Article HTML returns 403 (Cloudflare) even with a Chrome
User-Agent and browser `Accept` headers (tested 2 URLs), so `<head>` meta description and meta
keywords could not be read. Instead, the Meta keywords column shows Zendesk `label_names`
(internal search labels). Only about 20 of 183 articles have labels, and only 3 of the 20 below.
Selection criteria: overview/getting started, the core extraction concepts (parsing rules,
filters, fixed versus variable position, table and line-item parsing, multiple layouts), AI/LLM
features, OCR and preprocessing, classification (keyword tagging), PDF splitting, file formats,
API, webhooks, and the integration overview. Skipped: billing/account, the 40+ one-filter pages
(for example "Remove Empty Columns"), per-field invoice presets, single-destination integrations
(Google Sheets, Dropbox), and redesign notes. Docparser has no validation or human-review article,
so that slot is empty. Phrases come from the title, H2s, H3s (many articles use only H3s, marked
"h3" below), or labels, and are matched case-insensitively. "Borrowable" = not found in the mapped
Sensible page body.

Data quirk: "What parsing rules does Docparser provide?" (16254880910356) has a body that's a copy
of the Invoice Number preset article, so it was excluded.

| # | Page | Meta keywords | Meta description | Phrases they target | Closest Sensible page | Borrowable |
|---|---|---|---|---|---|---|
| 1 | [What Docparser can do for you](https://help.docparser.com/hc/en-us/articles/16254844875924-What-Docparser-can-do-for-you) | none | not retrievable (403) | things you can automate (h3); where your data can go (h3); behind the scenes (h3) | `docs/welcome/overview.md` | things you can automate (weak; no real search phrases on this page) |
| 2 | [How to Create a Parser](https://help.docparser.com/hc/en-us/articles/41795272268820-How-to-Create-a-Parser) | labels: getting-started, create-parser | not retrievable (403) | create a parser; choose a document type; name your parser | `docs/document extraction/getting-started.md` | create a parser; choose a document type |
| 3 | [What is a parsing rule and how do I create one?](https://help.docparser.com/hc/en-us/articles/16254858374036-What-is-a-parsing-rule-and-how-do-I-create-one) | none | not retrievable (403) | parsing rule; creating a parsing rule; how parsing rules work; choose a preset; refine your results | `docs/Senseml reference/layout-based-methods/index.md` | parsing rule; how parsing rules work |
| 4 | [What filters are available in Docparser?](https://help.docparser.com/hc/en-us/articles/16254942687892-What-filters-are-available-in-Docparser) | none | not retrievable (403) | filters; refine your parsed data; text filters; table filters; parsed data | `docs/Senseml reference/computed-field-methods/index.md` | parsed data; text filters; table filters |
| 5 | [How can I extract table rows from a document?](https://help.docparser.com/hc/en-us/articles/16254864913044-How-can-I-extract-table-rows-from-a-document) | none | not retrievable (403) | extract table rows; table rows; extract table rows from a document | `docs/Senseml reference/concepts/table-methods.md` | extract table rows; table rows |
| 6 | [How to parse tables with complex layouts?](https://help.docparser.com/hc/en-us/articles/16254898388756-How-to-parse-tables-with-complex-layouts) | none | not retrievable (403) | parse tables; complex layouts; table extraction tool; secondary rows; merge fields | `docs/Senseml reference/concepts/table-methods.md` | parse tables; complex layouts; merge fields |
| 7 | [How can I extract text from a fixed position?](https://help.docparser.com/hc/en-us/articles/16254807116564-How-can-I-extract-text-from-a-fixed-position) | none | not retrievable (403) | extract text from a fixed position; fixed position; refine parsed results; parsing rule | `docs/Senseml reference/layout-based-methods/region.md` | extract text from a fixed position; fixed position |
| 8 | [How to extract line-items from recurring invoices and purchase orders?](https://help.docparser.com/hc/en-us/articles/16254876002196-How-to-extract-line-items-from-recurring-invoices-and-purchase-orders) | none | not retrievable (403) | extract line-items; recurring invoices; purchase orders; column borders; line-item parsing rule | `docs/Senseml reference/layout-based-methods/fixed-table.md` | extract line-items; purchase orders; column borders |
| 9 | [How do I use the Docparser AI template?](https://help.docparser.com/hc/en-us/articles/24597690982804-How-do-I-use-the-Docparser-AI-template) | labels: AI, machine learning, smart parser, handwriting | not retrievable (403) | AI template; machine learning; smart parser; handwriting | `docs/welcome/getting-started-ai.md` | AI template; handwriting; machine learning |
| 10 | [Content Summarization Filter](https://help.docparser.com/hc/en-us/articles/34787472756884-Content-Summarization-Filter) | labels: AI, content, summarization | not retrievable (403) | content summarization; summarization filter; summarization | `docs/Senseml reference/llm-based-methods/query-group.md` | content summarization |
| 11 | [What are OCR Modes?](https://help.docparser.com/hc/en-us/articles/16254859786132-What-are-OCR-Modes) | none | not retrievable (403) | OCR modes; OCR | `docs/Senseml reference/concepts/ocr.md` | OCR modes |
| 12 | [What are the preprocessing options for documents?](https://help.docparser.com/hc/en-us/articles/16254896583444-What-are-the-preprocessing-options-for-documents) | none | not retrievable (403) | preprocessing options; optical character recognition; clean & normalize scans for OCR; keep & drop specific pages; split documents when importing; decrypt password protected documents | `docs/Senseml reference/preprocessors/index.md` | preprocessing options; optical character recognition; password protected documents |
| 13 | [How can I categorize a document by keywords?](https://help.docparser.com/hc/en-us/articles/16254884886292-How-can-I-categorize-a-document-by-keywords) | none | not retrievable (403) | categorize a document; categorize a document by keywords; keywords | `docs/document type classification/classify.md` | categorize a document; categorize a document by keywords |
| 14 | [Is it possible to automatically split incoming PDF files?](https://help.docparser.com/hc/en-us/articles/16254816797204-Is-it-possible-to-automatically-split-incoming-PDF-files) | none | not retrievable (403) | split incoming PDF files; automatically split; every [x] pages; keywords on first page; RegEx pattern | `docs/document extraction/portfolio.md` | automatically split; split incoming PDF files |
| 15 | [What file formats are supported by Docparser?](https://help.docparser.com/hc/en-us/articles/16254836642580-What-file-formats-are-supported-by-Docparser) | none | not retrievable (403) | file formats; file formats are supported | `docs/Senseml reference/concepts/file-types.md` | file formats |
| 16 | [Does Docparser offer an API?](https://help.docparser.com/hc/en-us/articles/16255060521364-Does-Docparser-offer-an-API) | none | not retrievable (403) | offer an API; API | `docs/api/api-reference.md` | none useful |
| 17 | [How do Advanced Webhooks work?](https://help.docparser.com/hc/en-us/articles/16254950012308-How-do-Advanced-Webhooks-work) | labels: advanced webhook, webhook | not retrievable (403) | advanced webhooks; webhook; target URL (h3); HTTP verb (h3); additional headers (h3); body template editor (h3) | `docs/api/api-tutorial/api-tutorial-webhook.md` | target URL; additional headers |
| 18 | [What are webhooks and cloud integrations?](https://help.docparser.com/hc/en-us/articles/16254867308948-What-are-webhooks-and-cloud-integrations) | none | not retrievable (403) | webhooks and cloud integrations; cloud integrations; direct integrations; integration platforms; custom webhooks | `docs/integrations/quickstart.md` | cloud integrations; integration platforms; custom webhooks |
| 19 | [How to Process Multiple Layouts with One Document Parser](https://help.docparser.com/hc/en-us/articles/16254933523732-How-to-Process-Multiple-Layouts-with-One-Document-Parser) | none | not retrievable (403) | process multiple layouts; multiple document layouts; layout model; document layout; layout variation (h3) | `docs/Senseml reference/config-settings/fingerprint.md` | multiple document layouts; document layout; layout variation |
| 20 | [How to extract data from variable positions?](https://help.docparser.com/hc/en-us/articles/16254826813972-How-to-extract-data-from-variable-positions) | none | not retrievable (403) | extract data from variable positions; variable positions; anchor keywords; extract data based on patterns; text variable position (h3) | `docs/Senseml reference/field-query-object/anchor.md` | variable positions; anchor keywords; extract data based on patterns |

Borrowable lists drop Docparser-only UI labels (for example "choose a preset", "refine your
results", "body template editor", "HTTP verb") even where they're technically missing from
Sensible, because nobody searches for them.

## Patterns

- Titles are task questions ("How can I extract table rows from a document?", "How to extract data
  from variable positions?"). That form matches how people type questions into search and AI
  chat. Sensible titles are mostly feature nouns ("Region", "Anchor object") that only make sense
  if you already know SenseML.
- Their core verb is "parse" ("parse tables", "parsing rule", "parsed data"), and "extract" comes
  second. Sensible's docs avoid "parse" almost completely: zero hits for "parse tables" across
  `docs/`. Search users say "PDF parser" and "parse tables" a lot, so this is the biggest
  vocabulary gap.
- Position vocabulary is explicit: "fixed position" and "variable positions" each get a page, and
  each appears in zero Sensible docs. These phrases are the plain-English version of Sensible's
  Region and Anchor/Row split.
- Their table vocabulary is concrete: "table rows", "line-items", "column borders", "complex
  layouts", "secondary rows". Sensible uses "line items" in only 4 files and never uses "table
  rows".
- Their AI coverage is thin and buried: a beta "AI template" and an OpenAI-backed "Content
  Summarization Filter". Sensible's LLM docs go much deeper, but Docparser at least names the
  feature with words people search for ("AI", "machine learning", "handwriting").
- Labels are sparse (3 of these 20 pages have them) and look like internal search tags, not an
  SEO strategy. This matches the earlier finding that competitors don't curate keywords.

## Top borrowable phrases

1. **parse tables** (also "parse tables with complex layouts"): `Senseml reference/concepts/table-methods.md`
2. **extract table rows** / **table rows**: `Senseml reference/concepts/table-methods.md`
3. **variable positions** (as in "extract data from variable positions"): `Senseml reference/field-query-object/anchor.md`
4. **fixed position** (as in "extract text from a fixed position"): `Senseml reference/layout-based-methods/region.md`
5. **multiple document layouts** / **layout variation**: `Senseml reference/config-settings/fingerprint.md`
6. **file formats** (zero hits in all of `docs/`; we only say "file types"): `Senseml reference/concepts/file-types.md`
7. **password protected documents**: `Senseml reference/concepts/file-types.md` (zero hits in `docs/`; check whether Sensible supports it before adding)
8. **automatically split** / **split incoming PDF files**: `document extraction/portfolio.md`
9. **categorize a document**: `document type classification/classify.md`
10. **preprocessing options**: `Senseml reference/preprocessors/index.md` (zero hits for "preprocessing" in `docs/`)
