---
title: "OCR level"
hidden: false
---
Sensible handles OCR for documents automatically, except for advanced edge cases that you can configure using:

- the [OCR preprocessor](doc:ocr) (at the config level)
- the OCR Level parameter (at the document type level)

When applying these configurations, Sensible takes the following steps: 

1. Sensible converts DOC and DOCX files into PDFs.

2. Sensible transforms the bytes of the document into raw text, and determines whether the document needs OCR:

   - If the file is an image file (for example, PNG), Sensible runs OCR for the whole document.

   - **(Configurable)** if the file is a PDF, Sensible processes the file according the OCR Level parameter.

3. **(Configurable)** After additional intervening steps, Sensible applies your configured preprocessors, including the OCR preprocessor. Configure this preprocessor for documents that don't trigger whole-document OCR as determined by the OCR level.

## Parameters

The following table shows the enums available for the OCR Level parameter. 

**Note:** Set this parameter in the [Sensible API](ref:create-document-type).

| enum | description                                                  |
| ---- | ------------------------------------------------------------ |
| 0    | Sensible doesn't run OCR for PDFs.                           |
| 2    | Default for single-document PDF extractions.<br/> Sensible detects if the whole document needs OCR using heuristics. For example, Sensible averages the number of lines per page in the document. If the average is fewer than 10, Sensible runs OCR on the whole document. |
| 4    | Default for portfolio PDF extractions.<br/>Sensible detects if the whole document needs OCR by rendering the first page and testing it. If that page needs OCR, Sensible runs OCR on the entire document. |
| 5    | Sensible renders and tests each page in the document to determine whether to run OCR on that page.<br/>Set this level in a document type if you use the type to process both single documents and portfolio, so that your OCR settings between single documents and portfolios are consistent. |
