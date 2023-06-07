---
title: "OCR"
hidden: true
---

Selectively OCRs pages. This preprocessor is useful when a PDF has a mix of pages that contain embedded text as well as images of text or handwriting. Selectively OCRing the pages containing text images, rather than the entire document, improves performance. 

If the whole document is a scan or image file, you don't need to configure this preprocessor. In that case, Sensible automatically OCRs the whole document.

Parameters
====

|        |                                                              |                                                              |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| engine | `amazon`,<br/>`google`,<br>`microsoft`,<br/>`lazarus`,<br/>default: `amazon` | Specifies the OCR engine for this preprocessor. This preprocessor overrides the document type's OCR engine for this config.<br/> - Amazon is the default engine for this preprocessor.<br/>- Microsoft is suited to typewritten and long documents. Lazarus is faster than Microsoft and produces similar output.<br/>- Google is faster than Microsoft and suited to handwriting and short documents (25 pages or under). The Google engine doesn't merge words into lines automatically. Use the Merge Lines preprocessor in your configurations to do so. |
|        |                                                              |                                                              |
|        |                                                              |                                                              |
|        |                                                              |                                                              |
|        |                                                              |                                                              |
|        |                                                              |                                                              |

