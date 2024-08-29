---
title: "Supported file types"
hidden: false
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
- For XLSX documents, Sensible converts the document to PDF. To style the document, Sensible:
     - Discards truncated text in cells. To retain the text, reformat or resize the cells in Excel so the text is visible.
     - Converts sheets to pages by scaling text so that all sheets have the same width and by breaking long sheets into consecutive pages.
     - Adds the sheet name as a header on each page.
- For TIFF documents, SenseML methods that attempt to render pages return an error, including:
     - pixel-based methods, such as Box, Checkbox, Signature, and image coordinates returned by the Document Range method.
     - Fixed Table method with the Stop parameter specified. Use the Text Table method as an alternative.

