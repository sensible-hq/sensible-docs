---
title: "Supported file types"
hidden: false
---

## File types

Sensible supports the following file types:

| Operation                              | PDF  | Microsoft Word<br/> (DOC and DOCX) | Microsoft Excel<br/>(XLSX) | image formats<br/>(JPEG, PNG, and TIFF) |
| -------------------------------------- | ---- | ---------------------------------- | --------------------------------------- | --------------------------------------- |
| Sensible app's Extract tab    | ✅    | ✅                                  | ✅                                 | ❌                                       |
| Single-file extraction with SDK or API | ✅    | ✅                                  | ✅                                 | ✅                                       |
| Portfolio extraction with SDK or API   | ✅    | ✅                                  | ✅                                 | ❌                                       |
| Classification with SDK or API         | ✅    | ✅                                  | ✅                                 | ✅                                       |

## File sizes

Sensible supports the following file sizes:

| Operation              | Synchronous size limit (API only)                | Asynchronous size limit |
| ---------------------- | ------------------------------------------------ | ----------------------- |
| Single-document file extraction | under 4.5MB, or under 30 seconds processing time | 6 GB                    |
| Portfolio extraction   | n/a                                              | 6 GB                    |
| Classification         | 4.5 MB                                           | 4.5 MB                  |

## Notes

- When extracting from image file formats, Sensible ignores OCR or OCR preprocessor settings you configure in the document type or SenseML configuration. For more information about OCR, see [OCR level](doc:ocr-level).
- For DOC and DOCX documents, Sensible converts the document to PDF before processing it.
- For XLSX documents, Sensible converts the document to PDF. To style the document, Sensible:
     - Discards truncated text in cells. To retain the text, reformat or resize the cells in Excel so the text is visible, then re-run the extraction.
     - Scales text so that each sheet is the width of a US letter-sized page.
     - Adds the sheet name as a header on each page.
     - Breaks long sheets into multiple pages. 
- For TIFF documents, SenseML methods that attempts to return a rendered page returns an error, including:
     - pixel-based methods, such as Box, Checkbox, Signature, and image coordinates returned by the Document Range method
     - Key/Value method
     - Fixed Table and Table methods with the Stop parameter specified. Use the Text Table method as an alternative.

