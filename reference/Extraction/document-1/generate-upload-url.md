---
title: Extract doc at a Sensible URL
excerpt: >-
  Extract data asynchronously from a document with the following steps:
    1. Use this endpoint to generate a Sensible URL.
    2. PUT your document at the `upload_url` returned from the previous step. Sensible extracts data from the document.
    3. To retrieve the extraction, use a webhook, or use the extraction `id` returned in the response to poll the GET documents/{id} endpoint.

  For supported file size and types, see [Supported file types](doc:file-types).


  For example, if your call to `/generate_upload_url` specifies the document
  type with a `content_type` body parameter (recommended), your first two steps
  are as follows:


  Step 1. Generate the Sensible URL:


  ```curl

  curl --location
  'https://api.sensible.so/v0/generate_upload_url/<YOUR_DOCUMENT_TYPE>' \

  --header 'Content-Type: application/json' \

  --header 'Accept: application/json' \

  --header 'Authorization: Bearer REDACTED' \

  --data '{"content_type":"application/pdf"}'

  ```


  Step 2. PUT the document:


  ```curl

  curl --location --request PUT
  'https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/REDACTED'
  \

  --header 'Content-Type: application/pdf' \

  --data 'YOUR_PATH_TO_DOCUMENT.pdf'

  ```


  Note that in step 2:
    - you must omit an authorization header
    - the `Content-Type` header must match the `content_type` body parameter in step 1
    - the pre-signed `upload_url` doesn't support Base64 encoded documents, so you PUT the document bytes directly to the endpoint.


  For a step-by-step tutorial on calling this endpoint, see

  [Try asynchronous extraction from a Sensible
  URL](https://docs.sensible.so/docs/api-tutorial-async-2).
api:
  file: extraction.json
  operationId: generate-an-upload-url
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---