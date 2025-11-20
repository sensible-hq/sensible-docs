---
title: Extract doc at your URL
excerpt: >-
  Extract data asynchronously from a document at the specified
  `document_url`.<br/>

  For supported file size and types, see [Supported file types](doc:file-types).

  Take the following steps.

  1. Run this endpoint. Sensible recommends including `content_type` body
  parameter:


  ```curl

  curl --location
  'https://api.sensible.so/v0/extract_from_url/<YOUR_DOCUMENT_TYPE>' \

  --header 'Content-Type: application/json' \

  --header 'Accept: application/json' \

  --header 'Authorization: Bearer REDACTED' \

  --data '{"document_url": "YOUR_DOC_URL", content_type":"application/pdf"}'

  ```


  3. To retrieve the extraction, use a webhook, or use the extraction `id`
  returned in the  response to poll the GET documents/{id} endpoint.

  For a step-by-step tutorial on calling this endpoint,

  see [Try asynchronous extraction from your URL](doc:api-tutorial-async-1).
api:
  file: extraction.json
  operationId: provide-a-download-url
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---