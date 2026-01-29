---
title: Extract data from a document (sync)
excerpt: "\n**Note:** Use this endpoint for testing. Use the asynchronous extraction\
  \ endpoints when in production.\n\nExtract data from a local document synchronously.\n\
  \nTo explore this endpoint, use this interactive API reference, or use one of the\
  \ following options:\n\n- For a quick \"hello world\" response to this endpoint,\
  \ see the [API quickstart](doc:quickstart)\n- For a step-by-step tutorial about\
  \ calling this endpoint, see [Try synchronous extraction](doc:api-tutorial-sync).\n\
  - Run this endpoint in the Sensible Postman collection.\n  [![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/16839934-45339059-3fec-4c31-a891-9a12a3e1c22b?action=collection%2Ffork&collection-url=entityId%3D16839934-45339059-3fec-4c31-a891-9a12a3e1c22b%26entityType%3Dcollection%26workspaceId%3Ddbde09dc-b7dd-487d-a68f-20d32b008f90)\n\
  \nThere are two options for posting the document bytes.\n  1. (often preferred)\
  \ specify the non-encoded document bytes as the entire request body,and specify\
  \ the `Content-Type` header, for example,\"application/pdf\" or \"image/jpeg\".\n\
  \     See the following for supported file formats.\n  2. Base64 encode the document\
  \ bytes, specify them in a body \"document\" field, and specify application/json\
  \ for the `Content-Type` header.\n\nFor a list of  supported document file types,\
  \ see [Supported file types](doc:file-types).\n"
api:
  file: openapi_extraction.json
  operationId: extract-data-from-a-document
hidden: false
metadata:
  description: 'null'
---
