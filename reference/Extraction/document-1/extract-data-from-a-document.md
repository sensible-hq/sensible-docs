---
title: Extract data from a document
excerpt: >-
  Extract data from a local document synchronously.  For a step-by-step tutorial
  on calling this endpoint,  see [Try synchronous
  extraction](doc:api-tutorial-sync).

  There are two options for posting the document bytes.
    1. (often preferred) specify the non-encoded document bytes as the entire request body, 
    and specify the content-type as one of "application/pdf", "image/jpeg", or "image/png", as appropriate.
    2. Base64 encode the document bytes, specify them in a body "document" field, and specify application/json for the content type.
api:
  file: extraction.json
  operationId: extract-data-from-a-document
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---