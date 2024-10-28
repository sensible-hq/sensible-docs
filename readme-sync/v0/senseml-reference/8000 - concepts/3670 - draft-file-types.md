---
title: "Supported file types"
hidden: true
---

## File types

Sensible supports the following file types:

|                    | PDF  | Microsoft Word<br/> (DOC and DOCX) | Microsoft Excel<sup>2</sup><br/>(XLSX) | single-page image formats<br/> (JPEG, PNG) | multi-page image formats<br> (TIFF) |
| -------------------------------------- | ---- | ---------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| **Operation** |  |  |  |  |  |
| Sensible app's Extract tab    | ✅    | ✅                                  | ✅                                 | ❌                                       | ❌                                      |
| Single-file extraction with SDKs or API | ✅    | ✅                                  | ✅                                 | ✅                                       | ✅                                      |
| Portfolio extraction with SDKs or API   | ✅    | ✅                                  | ❌ | ❌                                       | ❌                                      |
| Classification with SDKs or API         | ✅    | ✅                                  | ✅                                 | ✅                                       | ✅                                      |
|  |  |  |  |  |  |
| **Feature** |  |  |  |  |  |
| Methods that require rendering non-text image pixels<sup>1</sup> | ✅ | ✅ | ❌ | ✅ | ❌ |
| NLP Table,<br/> Fixed Table (no Stop)<br/>  (textractPage/ Microsoft OCR) | ✅ | ✅ |  | ✅ | ❌ |
| Fixed Table with Stop<br/> (renderer.recognizeInvoice ... OCR whole page) | ✅ | ✅ | ❌ | ✅ | ❌ |
| OCR'd text (not direct-text extraction) | ✅ | ✅ | ❌ | ✅ | ✅ |


1. Methods that require rendering an image include pixel-based methods, such as Box, Checkbox, Nearest Checkbox, and Signature methods, [multimodal](doc:query-group#parameters) LLM-based methods, and image coordinates returned by the Document Range method.

2. All [OCR](doc:ocr) settings are inapplicable for this file type.

MY TESTS:


|                    | PDF  | Microsoft Word<br/> (DOC and DOCX) | Microsoft Excel<sup>2</sup><br/>(XLSX) | single-page image formats<br/> (JPEG, PNG) | multi-page image formats<br> (TIFF) |
| -------------------------------------- | ---- | ---------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| -                                                            |                       |                                    |                                                              |                                            |                                                              |
|                                                              |                       |                                    |                                                              |                                            |                                                              |
| MY TESTS w null fields on checkbox, nearestCheckbox, box, multimodal | as expected no errors | as expected no errors | unexpected: **no errors** except on MULTIMODAL               | no errors             | **unexpected: no errors** only nulls when field was gonna return null anyway. when field is potentially non-null, then you get the expected errors. |
| *OCR-based methods<sup>2</sup>*                              | ✅                     | ✅                     | ❌                                                            | ✅                     | ❌                                                            |
| My tests w/ null fields on NLP Table (I assume "detectTableStruct" makes no difference) and Fixed Table no stop (**MIcrosoft OCR**) | as expected no errors | as expected no errors | **unexpected**: unsupported image type on NLP TABLE BUT NONE on Fixed Table w/ No Stop | as expected no errors | **unexpected**: unsupported image type on NLP TABLE BUT NONE on Fixed Table w/ No Stop, even though it did return null |
| *misc*                                                       |                       |                       |                                                              |                       |                                                              |
| Fixed Table w Stop (Amazon table recognition)                |                       |                       | null + error message   (unsupported image type)              | as expected no errors | null + error message   (unsupported image type)              |

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

- For XLSX documents, Sensible extracts text directly from the file. Sensible takes these steps:
     - Standardizes the formatting of all text in the file. Each cell contains exactly one [line](doc:lines).
     
     - Standardizes cell height at 0.25'' tall and cell width at 1''. Overflow text in a cell is still available for extraction but isn't viewable in the JSON editor unless you click on a line in the rendered document to view its details. 
     
     - Standardizes the maximum page height at 15 inches. Sensible splits longer sheets into consecutive pages.
     
       

