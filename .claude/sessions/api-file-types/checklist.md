# api-file-types checklist

- Session: xlsb (1e71441a-3c84-48a0-baa5-c36aac379bbb)
- Worktree: `~/GitHub/sensible-docs-api-file-types`, branch `fe_api_file_types_in_descriptions`

Frances (2026-11-12): keep file-support information out of API reference descriptions; the link to Supported file types is enough. Enums, examples, and file-specific concepts (portfolio = PDF) are fine.

- [x] Rule in `.claude/skills/api-spec/SKILL.md` ("Prose quality in descriptions"), plus a pre-publish checklist item
- [x] Removed file-support claims from 6 descriptions: Classify and Classify async (CSV, and XLS/XLSM/XLSB as XLSX), Extract data from a document (base64 for XLS/XLSM/XLSB, and a dangling "see the following"), `ContentTypeParameter` (CSV requires it), `ConvertedUrlDocument` and `GoldenResponse.converted_url` (which types get converted)
- [x] Generalized "reference PDFs" and "put the PDF" to "document" (Delete a document type; reference document upload)
- [x] Moved the one fact the page lacked to footnote 1 of Supported file types: CSV needs the `content_type` body parameter on asynchronous endpoints
- [x] Kept, per Frances: the portfolio tag ("single PDF files"), Get Excel and Get CSV extraction ("for example from PDFs", "documents it finds in the PDF"), `DocumentTypeNames` ("PDF portfolio")
- [ ] Undecided: `encodedPdf.document` "any supported document type (not just PDF)". Kept for now: the schema is named `encodedPdf`, and the parenthetical stops readers assuming base64 is PDF-only
