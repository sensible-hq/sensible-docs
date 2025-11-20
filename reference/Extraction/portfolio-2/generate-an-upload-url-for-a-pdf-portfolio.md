---
title: Extract portfolio at a Sensible URL
excerpt: >-
  Use this endpoint with multiple documents that are packaged into one PDF file
  (a PDF "portfolio").  Segments a PDF at the specified `document_url` into the
  specified document types (for example, 1099, w2, and bank_statement)  and then
  runs extractions asynchronously for each document Sensible finds in the PDF
  portfolio. Take the following steps. 1. Run this endpoint. 2. To retrieve the
  extraction results or poll status, use the extraction `id` returned in the
  response to call  the GET documents/{id} endpoint. For more about extracting
  from PDF portfolios, see [Extracting from document portfolios](doc:portfolio).
api:
  file: extraction.json
  operationId: generate-an-upload-url-for-a-pdf-portfolio
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---