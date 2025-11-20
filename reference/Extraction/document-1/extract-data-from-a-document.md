---
title: Extract data from a document (sync)
excerpt: >-
  **Note:** Use this endpoint for testing. Use the asynchronous extraction
  endpoints for production.


  Extract data from a local document synchronously.


  To explore this endpoint, use this interactive API reference, or use one of
  the following options:


  - For a quick "hello world" response to this endpoint, see the [API
  quickstart](doc:quickstart)

  - For a step-by-step tutorial about calling this endpoint, see [Try
  synchronous extraction](doc:api-tutorial-sync).

  - Run this endpoint in the Sensible Postman collection.
    [![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/16839934-45339059-3fec-4c31-a891-9a12a3e1c22b?action=collection%2Ffork&collection-url=entityId%3D16839934-45339059-3fec-4c31-a891-9a12a3e1c22b%26entityType%3Dcollection%26workspaceId%3Ddbde09dc-b7dd-487d-a68f-20d32b008f90)

  There are two options for posting the document bytes.
    1. (often preferred) specify the non-encoded document bytes as the entire request body,and specify the `Content-Type` header, for example,"application/pdf" or "image/jpeg".
       See the following for supported file formats.
    2. Base64 encode the document bytes, specify them in a body "document" field, and specify application/json for the `Content-Type` header.

  For a list of  supported document file types, see [Supported file
  types](doc:file-types).
api:
  file: extraction.json
  operationId: extract-data-from-a-document
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---