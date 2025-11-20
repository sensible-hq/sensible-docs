---
title: Get Excel extraction
excerpt: >-
  You can use this endpoint to get Excel files from documents, for example from
  PDFs. In more detail, this endpoint converts your JSON document extraction to
  an Excel spreadsheet.

  To compile multiple documents into one Excel file, specify the IDs of their
  recent extractions in the request separated by commas, for example,

  `/generate_excel/867514cc-fce7-40eb-8e9d-e6ec48cdac34,5093c65f-05bd-46a3-8df7-da3ed00f6d35`.

  For the best compiled spreadsheet results, configure your SenseML so that the
  documents output identically named fields.

  For more information about the conversion process, see [SenseML to spreadsheet
  reference](doc:excel-reference).


  For portfolio extractions, Sensible returns an Excel file containing fields
  for all the documents it finds in the PDF. For more information, see
  [Multi-document spreadsheet](doc:excel-reference#multi-document-spreadsheet).


  For a list of document file types that Sensible can extract data from, see
  [Supported file types](doc:file-types).

  Call this endpoint after an extraction completes. For more information about
  checking extraction status,

  see the `GET /documents/{id}` endpoint.
api:
  file: extraction.json
  operationId: get-excel-extraction
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---