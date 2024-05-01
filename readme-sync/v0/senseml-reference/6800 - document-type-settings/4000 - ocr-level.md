---
title: "OCR level"
hidden: false
---
Sensible handles OCR for documents automatically, except for advanced cases. This topic covers advanced cases. For information about additional OCR options, see [OCR](doc:ocr).

Use this option to configure the criteria by which Sensible determines if a whole document requires OCR.

## Enums

The following table shows the enums available for the OCR Level parameter. 

**Note:** Set this parameter in the [Sensible API](ref:create-document-type).

| enum | description                                                  |
| ---- | ------------------------------------------------------------ |
| 0    | Sensible doesn't run OCR for PDFs.                           |
| 2    | Default for single-document PDF extractions.<br/> Sensible detects if the whole document needs OCR using heuristics. For example, Sensible averages the number of lines per page in the document. If the average is fewer than 10, Sensible runs OCR on the whole document. |
| 4    | Sensible detects if the whole document needs OCR by rendering the first page and testing it. If that page needs OCR, Sensible runs OCR on the entire document. |
| 5    | Default for portfolio PDF extractions.<br/>Sensible renders and tests each page in the document to determine whether to run OCR on that page.<br/>Set this level if you use a document type to process both single documents and portfolio in a document type, so that your OCR level is consistent for single documents and portfolios. |

