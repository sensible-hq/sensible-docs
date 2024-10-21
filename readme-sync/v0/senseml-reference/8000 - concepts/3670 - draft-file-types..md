---
title: "Supported file types"
hidden: true
---

## File types

Sensible supports the following file types:

|                    | PDF  | Microsoft Word<br/> (DOC and DOCX) | Microsoft Excel<br/>(XLSX) | single-page image formats<br/> (JPEG, PNG) | multi-page image formats<br> (TIFF) |
| -------------------------------------- | ---- | ---------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| **Operation** |  |  |  |  |  |
| Sensible app's Extract tab    | ✅    | ✅                                  | ✅                                 | ❌                                       | ❌                                      |
| Single-file extraction with SDKs or API | ✅    | ✅                                  | ✅                                 | ✅                                       | ✅                                      |
| Portfolio extraction with SDKs or API   | ✅    | ✅                                  | ✅ TODO: is this no longer true now that we don't convert XLSX to PDF? | ❌                                       | ❌                                      |
| Classification with SDKs or API         | ✅    | ✅                                  | ✅                                 | ✅                                       | ✅                                      |
| **Feature** |  |  |  |  |  |
| Methods that require rendering an image<sup>1</sup> | ✅ | ✅ | ❌ | ✅ | ❌ |
| OCR-based methods<sup>2</sup> | ✅ | ✅ | ❌ | ✅ | ❌ |

1. Methods that require rendering an image include pixel-based methods, such as Box, Checkbox, Nearest Checkbox, and Signature methods, [multimodal](doc:query-group#parameters) LLM-based methods, image coordinates returned by the Document Range method.

2. OCR-based methods include NLP Table and Fixed Table methods. Use Text Table or List as alternatives. All [OCR](doc:ocr) settings are inapplicable for this file type.

TODO: Where does "Fixed Table method with the Stop parameter specified" fit into all this? Is it pixel/render-based or OCR-based? How about NLP Table?



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
     
       

