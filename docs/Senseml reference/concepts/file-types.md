---
title: Supported file types
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Supported document file formats'
  robots: index
next:
  description: ''
---
## File types

Sensible supports the following file types.

**Extraction context**

| File format                                                    | Sensible app's Extract tab | Single-file extraction with SDKs or API | Portfolio extraction | Classification by type with SDKs or API |
| -------------------------------------------------------------- | -------------------------- | --------------------------------------- | ------------------------------------- | --------------------------------------- |
| PDF                                                            | ✅                         | ✅                                      | ✅                                    | ✅                                      |
| Microsoft Word<br/> (DOC and DOCX)                             | ✅                         | ✅                                      | ✅                                    | ✅                                      |
| Spreadsheet formats<sup>1</sup><br/>(XLSX, XLS, XLSM, and CSV) | ✅                         | ✅                                      | ❌                                    | ✅                                      |
| Single-page image formats<br/> (JPEG, PNG)                     | ✅                         | ✅                                      | ✅<sup>4</sup>                                    | ✅                                      |
| Multi-page image formats<br/> (TIFF)                           | ❌                         | ✅                                      | ❌                                    | ✅                                      |
| Email bodies                                                   | ✅                         | ✅                                      | ❌                                    | ✅                                      |
| Email attachments                                              | ✅                         | ✅                                      | ✅                                    | ✅                                      |


**SenseML extraction method**

| File format                                                    | Methods that render non-text pixels<sup>2</sup> | NLP Table method,<br/>Fixed Table method<sup>3</sup> | Extraction of text that requires OCR |
| -------------------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------- | ------------------------------------ |
| PDF                                                            | ✅                                                    | ✅                                                   | ✅                                   |
| Microsoft Word<br/> (DOC and DOCX)                             | ✅                                                    | ✅                                                   | ✅                                   |
| Spreadsheet formats<sup>1</sup><br/>(XLSX, XLS, XLSM, and CSV) | ❌                                                    | ❌                                                   | ❌                                   |
| Single-page image formats<br/> (JPEG, PNG)                     | ✅                                                    | ✅                                                   | ✅                                   |
| Multi-page image formats<br/> (TIFF)                           | ❌                                                    | ❌                                                   | ✅                                   |
| Email bodies                                                   | ✅                                                    | ✅                                                   | ✅                                   |
| Email attachments                                              | ✅                                                    | ✅                                                   | ✅                                   |


1. All [OCR](doc:ocr) settings are inapplicable for this file type.

2. Methods that render non-text image pixels include pixel-based methods, such as Box, Checkbox, Nearest Checkbox, and Signature methods, [multimodal](doc:query-group#parameters) LLM-based methods, and image coordinates returned by the Document Range method.

3. As alternatives to these Table methods, use the Fixed Table method or the List method.

4. Most JPEG or PNG files are single-document files. For the edge case where a JPEG or PNG is a portfolio file, Sensible extracts from the first document it identifies in the portfolio.

## File sizes

Sensible supports the following file sizes:

| Operation                       | Size limit for `/extract/{doc-type}` API endpoint | Size limit for asynchronous calls |
| ------------------------------- | ------------------------------------------------- | --------------------------------- |
| Single-document file extraction | under 4.5MB, or under 30 seconds processing time  | 6 GB                              |
| Portfolio extraction            | n/a                                               | 6 GB                              |
| Classification                  | 4.5 MB                                            | 4.5 MB                            |

## Notes

* **Word documents**: Sensible converts the document to PDF before processing it.
* **Email bodies**: Sensible converts the body to PDF before processing it.
* **Spreadsheet documents**: Sensible extracts text directly from the file without OCR. Sensible represents the text both internally and in the Sensible app's editor as follows:
  * Standardizes the formatting of all text in the file. Each cell contains exactly one [line](doc:lines).
  * Standardizes cell height at 0.25'' tall and cell width at 1''. Overflow text in a cell is still available for extraction but isn't viewable in the Sensible app editor unless you click on a line in the rendered document to view its details. 
  * Standardizes the maximum page height at 15 inches. Sensible splits longer sheets into consecutive pages.
