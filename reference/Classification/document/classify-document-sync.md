---
title: Classify document by type (sync)
excerpt: >-
  **Note:** Use this Classify endpoint for testing. Use the asynchronous
  Classify endpoint for production.


  Classify a document into one of the document types you defined in your
  Sensible account. For more information, see [Classifying documents by
  type](doc:classify).


  Use this endpoint:

   - In an extraction workflow. For example, determine which documents to extract prior to calling a Sensible extraction endpoint.
   - Outside an extraction workflow. For example, determine where to route each document or to label each document in a system of record.

  To post the document bytes, specify the non-encoded document bytes as the
  entire request body,and specify the `Content-Type` header, for
  example,"application/pdf" or "image/jpeg".


  For supported file size and types, see [Supported file types](doc:file-types).
api:
  file: classification-1.json
  operationId: classify-document-sync
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---