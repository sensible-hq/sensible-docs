---
title: "Supported file types"
hidden: false
---

## File types

Sensible supports the following file types:



| File format | Extraction context | | | | | Extraction method | | |
|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| | **Sensible app's Extract tab** | **Single-file extraction with SDKs or API** | **Portfolio extraction with SDKs or API** | **Classification by type with SDKs or API** | | **Methods that require rendering non-text image pixels<sup>2</sup>** | **NLP Table method,<br/>Fixed Table method<sup>3</sup>** | **Extraction of text that requires OCR** |
| PDF | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ |
| Microsoft Word<br/> (DOC and DOCX) | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ |
| Spreadsheet formats<sup>1</sup><br/>(XLSX, XLS, XLSM, and CSV) | ✅ | ✅ | ❌ | ✅ | | ❌ | ❌ | ❌ |
| Single-page image formats<sup>1</sup><br/> (JPEG, PNG) | ❌ | ✅ | ❌ | ✅ | | ✅ | ✅ | ✅ |
| Multi-page image formats<sup>1</sup><br/> (TIFF) | ❌ | ✅ | ❌ | ✅ | | ❌ | ❌ | ✅ |
| Email bodies | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |


1. All [OCR](doc:ocr) settings are inapplicable for Microsoft Excel and CSV. 

2. Methods that require rendering an image include pixel-based methods, such as Box, Checkbox, Nearest Checkbox, and Signature methods, [multimodal](doc:query-group#parameters) LLM-based methods, and image coordinates returned by the Document Range method.

3. As alternatives to these Table methods, use the Fixed Table method or the List method.
## File sizes

Sensible supports the following file sizes:

| Operation              | Size limit for `/extract/{doc-type}` API endpoint                | Size limit for asynchronous calls |
| ---------------------- | ------------------------------------------------ | ----------------------- |
| Single-document file extraction | under 4.5MB, or under 30 seconds processing time | 6 GB                    |
| Portfolio extraction   | n/a                                              | 6 GB                    |
| Classification         | 4.5 MB                                           | 4.5 MB                  |

## Notes

- **Word documents**: Sensible converts the document to PDF before processing it.
- **Email bodies**: Sensible converts the body to PDF before processing it.
- **Spreadsheet documents**: Sensible extracts text directly from the file without OCR. Sensible represents the text both internally and in the Sensible app's editor as follows:
     - Standardizes the formatting of all text in the file. Each cell contains exactly one [line](doc:lines).
     - Standardizes cell height at 0.25'' tall and cell width at 1''. Overflow text in a cell is still available for extraction but isn't viewable in the Sensible app editor unless you click on a line in the rendered document to view its details. 
     - Standardizes the maximum page height at 15 inches. Sensible splits longer sheets into consecutive pages.

