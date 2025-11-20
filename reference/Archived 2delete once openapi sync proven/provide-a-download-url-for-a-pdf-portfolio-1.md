---
title: Extract portfolio at your URL
excerpt: ''
api:
  file: sensible.json
  operationId: provide-a-download-url-for-a-pdf-portfolio-1
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---
Use this endpoint with multiple documents that are packaged into one PDF file (a PDF "portfolio").

Segments a PDF at the specified `document_url` into the specified document types (for example, 1099, w2, and bank\_statement) and then runs extractions asynchronously for each document Sensible finds in the PDF portfolio. 

Take these steps:

1. Run this endpoint.

2. To retrieve the extraction results or poll status, use the extraction `id` returned in the response to call the GET documents/\{id} endpoint. 

For more about extracting from PDF portfolios, see [Extracting from document portfolios](doc:portfolio).
