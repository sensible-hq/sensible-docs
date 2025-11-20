---
title: Extract portfolio at a Sensible URL
excerpt: >-
  Use this endpoint with multiple documents that are packaged into one file (a
  "portfolio"). For a list of supported file types, see [Supported file
  types](doc:file-types).

  Segments a portfolio file into the specified document types (for example,
  1099, w2, and bank_statement) and then runs extractions

  asynchronously for each document Sensible finds in the portfolio.  Take the
  following steps -

  1. Use this endpoint to generate a Sensible URL.

  2. PUT the document you want to extract data from at the URL, where
  `SENSIBLE_UPLOAD_URL` is the URL you received

  from this endpoint's response. For more information about how to PUT the
  document, see the
  [generate_upload_url/{document_type}](ref:generate-upload-url) endpoint.

  3. To retrieve the extraction, use a webhook, or use the extraction `id`
  returned in the  response to poll the GET documents/{id} endpoint.

  For more about extracting from portfolios, see [Multi-document
  extractions](doc:portfolio).
api:
  file: extraction.json
  operationId: generate-an-upload-url-for-a-pdf-portfolio
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---