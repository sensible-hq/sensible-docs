---
title: "OCR Level"
hidden: true
---
Sensible handles OCR for documents automatically except for advanced edge cases that you can configure using:

- the [OCR preprocess](doc:ocr)
- the OCR Level parameter

You can set the OCR Level parameter at the document level and at the config level. The config-level parameter overrides the document-level parameter. If unspecified, default OCR level for a document type is the minimum OCR level defined among its configurations



| level | defaults                               | description                                                  |      |
| ----- | -------------------------------------- | ------------------------------------------------------------ | ---- |
| 0     |                                        | Sensible doesn't perform OCR. As a result, Sensible skips processing image file formats and whole-scanned files, and ignores OCR preprocessor settings. |      |
| 2     | default for single-document extraction | Sensible averages the number of lines per page in the document, and if it's fewer than 10, Sensible runs OCR on the whole document. |      |
| 4     |                                        | Sensible always renders the first page and tests it to determine whether to run OCR on the whole document. |      |
| 5     | default for portfolio extractions      | This is the same behavior as level 4, except Sensible renders and tests each page in the document to determine whether to run OCR instead of just the first page.<br/>Use this setting if you process single documents and portfolio with the same configurations, to avoid inconsistent results. |      |





