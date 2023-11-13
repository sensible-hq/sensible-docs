---
title: "OCR level"
hidden: true
---
Sensible handles OCR for documents automatically, except for advanced edge cases that you can configure using:

- the [OCR preprocess](doc:ocr)
- the OCR Level parameter

You can set the OCR Level parameter at the document level and at the config level. The config-level parameter overrides the document-level parameter. If unspecified, default OCR level for a document type is the minimum OCR level defined among its configurations

| level | description                                                  |
| ----- | ------------------------------------------------------------ |
| 0     | Sensible doesn't run OCR. As a result, Sensible skips processing image file formats and whole-scanned files, and ignores OCR preprocessor settings. QUESTION: is this 2nd sentence true, I didn't check the code. |
| 2     | default for single-document extractions<br/>Sensible averages the number of lines per page in the document. If the average is fewer than 10, Sensible runs OCR on the whole document. |
| 4     | Sensible always renders the first page and tests it to determine whether to run OCR on the whole document. |
| 5     | default for portfolio extractions<br/>Sensible renders and tests each page in the document to determine whether to run OCR on that page.<br/>Set this level in a configuration if you use the configuration to process both single documents and portfolio, so that your OCR settings between single documents and portfolios are consistent. |





