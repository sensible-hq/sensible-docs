---
title: Extract doc at your URL
excerpt: ''
api:
  file: sensible.json
  operationId: provide-a-download-url-1
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---
Extract data asynchronously from a document at the specified `document_url`.  You must use this or other asynchronous endpoints for PDFs that are over 4.5MB in size or require over 30 seconds to process.

Take these steps:

1. Run this endpoint.

2. To retrieve the extraction or poll its status, use the extraction `id` returned in the response to call the GET documents/{id} endpoint.

For a step-by-step tutorial on calling this endpoint, see [Try asynchronous extraction from your URL](doc:api-tutorial-async-1).