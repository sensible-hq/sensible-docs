---
title: "Supported file types"
hidden: false
---

## File types

Sensible supports the following file types:

|                                                              | PDF  | Microsoft Word<br/> (DOC and DOCX) | Microsoft Excel<sup>1</sup><br/>(XLSX) | single-page image formats<br/> (JPEG, PNG) | multi-page image formats<br> (TIFF) |
| ------------------------------------------------------------ | ---- | ---------------------------------- | -------------------------------------- | ------------------------------------------ | ----------------------------------- |
| **Extraction context**                                       |      |                                    |                                        |                                            |                                     |
| Sensible app's Extract tab                                   | ✅    | ✅                                  | ✅                                      | ❌                                          | ❌                                   |
| Single-file extraction with SDKs or API                      | ✅    | ✅                                  | ✅                                      | ✅                                          | ✅                                   |
| Portfolio extraction with SDKs or API                        | ✅    | ✅                                  | ❌                                      | ❌                                          | ❌                                   |
| Classification with SDKs or API                              | ✅    | ✅                                  | ✅                                      | ✅                                          | ✅                                   |
|                                                              |      |                                    |                                        |                                            |                                     |
| **Extraction method**                                        |      |                                    |                                        |                                            |                                     |
| Methods that require rendering non-text image pixels<sup>2</sup> | ✅    | ✅                                  | ❌                                      | ✅                                          | ❌                                   |
| NLP Table method,<br/>Fixed Table method<sup>3</sup><br/>    | ✅    | ✅                                  | ❌                                      | ✅                                          | ❌                                   |
| Extraction of text that requires [OCR](doc:ocr)              | ✅    | ✅                                  | ❌                                      | ✅                                          | ✅                                   |


1. All [OCR](doc:ocr) settings are inapplicable for this file type.

2. Methods that require rendering an image include pixel-based methods, such as Box, Checkbox, Nearest Checkbox, and Signature methods, [multimodal](doc:query-group#parameters) LLM-based methods, and image coordinates returned by the Document Range method.

3. As alternatives to these Table methods, use the Fixed Table method or the List method.
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
     - Sensible doesn't support the following methods for this file type:
       - Pixel-based methods, such as Box, Checkbox, Nearest Checkbox, and Signature methods, images returned by the Multi Modal Engine parameter on the Query Group method, and image coordinates returned by the Document Range method.
       - OCR-based methods, such as NLP Table and Fixed Table methods. Use Text Table or List as alternatives. All [OCR](doc:ocr) settings are inapplicable for this file type.
- For TIFF documents, SenseML methods that attempt to render pages return an error, including:
     - pixel- or image-based methods, such as Box, Checkbox, Signature, and image coordinates returned by the Document Range method.
     - Fixed Table method with the Stop parameter specified. Use the Text Table method as an alternative.

