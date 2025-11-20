---
title: Classify document by type
excerpt: >-
  Classify a document into one of the document types you defined in your
  Sensible account. For more information, see [Classifying documents by
  type](doc:classify).

  To retrieve document's classification, poll the `download_link` in this
  endpoint's response until it returns a non-error response.


  Use this endpoint:

   - In an extraction workflow. For example, determine which documents to extract prior to calling a Sensible extraction endpoint.
   - Outside an extraction workflow. For example, determine where to route each document or to label each document in a system of record.

  To post the document bytes, specify the non-encoded document bytes as the
  entire request body,and specify the `Content-Type` header, for
  example,"application/pdf" or "image/jpeg".


  For supported file size and types, see [Supported file types](doc:file-types).
api:
  file: classification-1.json
  operationId: classify-document
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---