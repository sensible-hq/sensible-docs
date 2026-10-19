# Competitor keyphrases: cross-competitor summary

Researched 2026-10-19. Sources: `parseur.md`, `docparser.md`, `nanonets.md`, `docsumo.md`, `ocrolus.md`
in this folder (20 pages each; phrases are verbatim from competitor titles, descriptions, and headings).

## Meta keywords

Nobody curates them. One exception: Parseur's developer "Getting started" page has a hand-set
`Document Data Extraction API`; the rest of developer.parseur.com is Apidog boilerplate. Nanonets,
Docsumo, Ocrolus (all ReadMe): none. Docparser: unknown (403), Zendesk labels on 3 of 20 pages.

## Where competitors converge (phrases from 2+ competitors)

| Topic | Phrases (competitor) | Sensible page | In our draft already? |
|---|---|---|---|
| Tables | parse tables, extract table rows (Docparser); extract PDF tables, tables spanning several pages (Parseur); capture data from tables (Nanonets); prompt-based table extraction (Docsumo) | `concepts/table-methods.md`, `llm-based-methods/nlp-table.md` | partly (PDF table extraction, table parsing) |
| Splitting | document splitting, multi-page documents (Parseur); automatically split (Docparser); PDF with multiple invoices, combined document (Docsumo); mixed PDF document, multi-page PDF, loan package (Ocrolus) | `document extraction/portfolio.md` | partly (split PDF, document splitting, combined PDF) |
| Classification | categorize a document (Docparser); document classification (Nanonets); classify mixed documents (Ocrolus) | `document type classification/classify.md` | yes (document classification) |
| File support | file formats, password protected documents (Docparser); maximum document size, password-protected PDFs (Parseur); file formats (Nanonets) | `concepts/file-types.md` | partly (file formats, file size limits) |
| Accuracy | confidence scores (Nanonets, Docsumo); extraction accuracy (Docsumo) | `best-practices/confidence.md` | no (page not in our 20) |
| Review / validation | approval rules, business rules (Nanonets); field-level validation, review screen (Docsumo); human-in-the-loop, HITL, logic-based rules (Ocrolus) | `monitor and qa/validate-extractions.md`, `monitor and qa/human-review.md` | partly (business rules); human review page not in our 20 |
| Umbrella terms | document AI, unstructured data into structured data, automate data capture (Docsumo); intelligent document processing, document automation (Ocrolus); agentic extraction (Nanonets) | `concepts/idp.md`, `welcome/overview.md` | partly (document AI, document automation, unstructured to structured data) |
| Preprocessing | preprocessing options (Docparser); image pre-processing (Docsumo) | `preprocessors/index.md` | no (page not in our 20) |
| API | payload format (Parseur); payload structure (Nanonets); polling, webhook URL (Ocrolus) | `api/api-tutorial/*` | no (pages not in our 20) |

## Single-competitor phrases worth considering

- fixed position → Region; variable positions → Anchor; multiple document layouts / layout variation → Fingerprint (Docparser)
- nested tables → Sections (Parseur)
- zero-shot; pre-trained model / prebuilt models → `library-quickstart.md` (Nanonets)
- key-value field extraction → Query group (Docsumo)

## Vocabulary gaps in Sensible docs

- **parse / parser / parsing**: two competitors are named for it; Sensible docs barely use it.
- **human-in-the-loop / HITL**: standard industry term, absent from our human review page.
- **document classification**: absent from our main classification page.
- **file formats**: we only say "file types."
- **zero-shot, pre-trained, agent/agentic**: absent.

## Title patterns

- Parseur and Docparser title pages as tasks or questions ("Extract PDF Tables With OCR",
  "How can I extract text from a fixed position?"). These match how people phrase search and AI
  queries.
- Nanonets titles pages with its own product names; Ocrolus mostly uses ReadMe defaults (nav labels,
  auto-excerpt descriptions), with ~6 hand-tuned "Phrase | Ocrolus" titles.
- Sensible titles pages with feature names (Row, Region, Fingerprint).

## Candidate pages to add to our 20

Competitors invest in topics that our 20 skip: `best-practices/confidence.md`,
`monitor and qa/human-review.md`, `preprocessors/index.md`, `api/api-tutorial/api-tutorial-webhook.md`,
`document extraction/library-quickstart.md`.

## Caveats

- Each file's Borrowable column is a literal substring check against one mapped Sensible page; a
  phrase marked borrowable may exist on another Sensible page. Use each file's ranked top-10 list,
  which filters out competitor product names.
- Docparser data comes from the Zendesk API (article pages return 403); no meta descriptions.
- Password-protected PDFs: verify Sensible supports them before using the phrase.
