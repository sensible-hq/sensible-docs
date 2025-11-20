---
title: Extract portfolio at your URL
excerpt: >-
  Use this endpoint with multiple documents that are packaged into one PDF file
  (a PDF "portfolio"). Segments a PDF into the specified document types (for
  example, 1099, w2, and bank_statement) and then runs extractions 
  asynchronously for each document Sensible finds in the PDF portfolio.  Take
  the following steps -   1. Use this endpoint to generate a Sensible URL. 2.
  PUT the PDF you want to extract data from at the URL, where
  `SENSIBLE_UPLOAD_URL` is the URL you received  from this endpoint's response.
  For example, `curl -T ./sample.pdf "SENSIBLE_UPLOAD_URL"` Note - the
  pre-signed upload_url does not support Base64 encoded PDFs.  You PUT the PDF
  bytes directly to the endpoint and must omit the content-type header.   3. To
  retrieve the extraction or poll its status, use the extraction `id` returned
  in  the response to call the GET documents/{id} endpoint. For more about
  extracting from PDF portfolios, see [Extracting from document
  portfolios](doc:portfolio).
api:
  file: extraction.json
  operationId: provide-a-download-url-for-a-pdf-portfolio
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---