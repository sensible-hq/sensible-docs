---
title: Classify document by type (sync)
excerpt: "\n**Note:** Use this Classify endpoint for testing. Use the asynchronous\
  \ Classify endpoint for production.\n\nClassify a document into one of the document\
  \ types you defined in your Sensible account. For more information, see [Classifying\
  \ documents by type](doc:classify).\n\nUse this endpoint:\n\n - In an extraction\
  \ workflow. For example, determine which documents to extract prior to calling a\
  \ Sensible extraction endpoint.\n - Outside an extraction workflow. For example,\
  \ determine where to route each document or to label each document in a system of\
  \ record.\n\nTo post the document bytes, specify the non-encoded document bytes\
  \ as the entire request body,and specify the `Content-Type` header, for example,\"\
  application/pdf\" or \"image/jpeg\".\n\nFor supported file size and types, see [Supported\
  \ file types](doc:file-types).\n    \n"
api:
  file: openapi_classification.json
  operationId: classify-document-sync
hidden: false
metadata:
  description: 'null'
---
