---
title: "Supported file types"
hidden: true
---

## File types

Sensible supports the following file types:

| Operation                              | PDF  | Microsoft Word<br/> (DOC and DOCX) | Microsoft Excel<br/>(XLSX) | image formats<br/>(JPEG, PNG, and TIFF) |
| -------------------------------------- | ---- | ---------------------------------- | --------------------------------------- | --------------------------------------- |
| Sensible app's Extract tab    | ✅    | ✅                                  | ✅                                 | ❌                                       |
| Single-file extraction with SDKs or API | ✅    | ✅                                  | ✅                                 | ✅                                       |
| Portfolio extraction with SDKs or API   | ✅    | ✅                                  | ✅                                 | ❌                                       |
| Classification with SDKs or API         | ✅    | ✅                                  | ✅                                 | ✅                                       |

## File sizes

Sensible supports the following file sizes:

| Operation              | Size limit for `/extract/{doc-type}` API endpoint                | Size limit for aysnchronous calls |
| ---------------------- | ------------------------------------------------ | ----------------------- |
| Single-document file extraction | under 4.5MB, or under 30 seconds processing time | 6 GB                    |
| Portfolio extraction   | n/a                                              | 6 GB                    |
| Classification         | 4.5 MB                                           | 4.5 MB                  |

## Notes

- When extracting from image file formats, Sensible ignores OCR or OCR preprocessor settings you configure in the document type or SenseML configuration. For more information about OCR, see [OCR level](doc:ocr-level).
- For DOC and DOCX documents, Sensible converts the document to PDF before processing it.
- For XLSX documents, Sensible extracts text directly from the file. All [OCR](doc:ocr) settings are inapplicable. Sensible takes these steps:
     - Standardizes the formatting of all text in the file and removes extra whitespaces and newlines, so that each cell contains exactly one [line](doc:lines).
     - Standardizes cell height at 0.5'' tall and cell width at 1''. Overflow text in the cell is still available for extraction but not viewable in the JSON editor unless you click on the cell's details. 
     
- For TIFF documents, SenseML methods that attempt to render pages return an error, including:
     - pixel-based methods, such as Box, Checkbox, Signature, and image coordinates returned by the Document Range method
     - Key/Value method
     - Fixed Table method with the Stop parameter specified. Use the Text Table method as an alternative.

