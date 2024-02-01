---
title: "OCR level"
hidden: false
---
Sensible handles OCR for documents automatically, except for advanced edge cases that you can configure using:

- the [OCR preprocessor](doc:ocr) (at the config level)
- the OCR Level parameter (at the document type level)

To understand how these configurations interact, see the following overview of how Sensible OCRs files:

1. Sensible converts DOC and DOCX files into PDFs.

2. Sensible transforms the bytes of the document into raw text, and determines whether the document needs OCR:

   - If the file type is an image (for example, PNG), Sensible runs OCR for the whole document, as specified by the document type's OCR Engine parameter.

   - **(Configurable)** if the file is a PDF, Sensible processes the file, as specified by the document type's OCR Level parameter. For more information, see the following table.

3. **(Configurable)** After additional intervening steps, Sensible applies your configured preprocessors, including the OCR preprocessor. This preprocessor runs for documents that don't trigger whole-document OCR in a previous step.

## Enums

The following table shows the enums available for the OCR Level parameter. 

**Note:** Set this parameter in the [Sensible API](ref:create-document-type).

| enum | description                                                  |
| ---- | ------------------------------------------------------------ |
| 0    | Sensible doesn't run OCR for PDFs.                           |
| 2    | Default for single-document PDF extractions.<br/> Sensible detects if the whole document needs OCR using heuristics. For example, Sensible averages the number of lines per page in the document. If the average is fewer than 10, Sensible runs OCR on the whole document. |
| 4    | Sensible detects if the whole document needs OCR by rendering the first page and testing it. If that page needs OCR, Sensible runs OCR on the entire document. |
| 5    | Default for portfolio PDF extractions.<br/>Sensible renders and tests each page in the document to determine whether to run OCR on that page.<br/>Set this level if you use a document type to process both single documents and portfolio, so that your OCR level is consistent for single documents and portfolios. |

