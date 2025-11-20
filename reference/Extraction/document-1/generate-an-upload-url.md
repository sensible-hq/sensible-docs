---
title: Extract doc at a Sensible URL
excerpt: >-
  Extract data asynchronously from a document with the following steps. You must
  use this or other asynchronous endpoints for documents that are over 4.5MB in
  size or require over 30 seconds to process. 
    1. Use this endpoint to generate a Sensible URL.
    2. PUT the document you want to extract data from at the URL, where `SENSIBLE_UPLOAD_URL` is the URL you received 
  from this endpoint's response. For example, `curl -T ./sample.pdf
  "SENSIBLE_UPLOAD_URL"`.  Note: the pre-signed upload_url does not support
  Base64 encoded documents. You PUT the document bytes directly to the
  endpoint,  and you must match the "Content-Type" header to that specified in
  the POST that creates the URL. If you omit the parameter, you must omit the
  header, and if you specify the parameter, you must include the exact header in
  the PUT.
    3.  To retrieve the extraction or poll its status, use the extraction `id` returned in the response to call the 
  GET documents/{id} endpoint.

  For a step-by-step tutorial on calling this endpoint, see  [Try asynchronous
  extraction from a Sensible
  URL](https://docs.sensible.so/docs/api-tutorial-async-2).
api:
  file: extraction.json
  operationId: generate-an-upload-url
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---