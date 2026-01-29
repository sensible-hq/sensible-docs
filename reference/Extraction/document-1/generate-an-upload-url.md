---
title: Extract doc at a Sensible URL
excerpt: "Extract data asynchronously from a document with the following steps:\n\
  \  1. Use this endpoint to generate a Sensible URL.\n  2. PUT your document at the\
  \ `upload_url` returned from the previous step. Sensible extracts data from the\
  \ document.\n  3. To retrieve the extraction, use a webhook, or use the extraction\
  \ `id` returned in the response to poll the GET documents/{id} endpoint.\n\nFor\
  \ supported file size and types, see [Supported file types](doc:file-types).\n\n\
  For example, if your call to `/generate_upload_url` specifies the document type\
  \ with a `content_type` body parameter (recommended), your first two steps are as\
  \ follows:\n\nStep 1. Generate the Sensible URL:\n\n```curl\ncurl --location 'https://api.sensible.so/v0/generate_upload_url/<YOUR_DOCUMENT_TYPE>'\
  \ \\\n--header 'Content-Type: application/json' \\\n--header 'Accept: application/json'\
  \ \\\n--header 'Authorization: Bearer REDACTED' \\\n--data '{\"content_type\":\"\
  application/pdf\"}'\n```\n\nStep 2. PUT the document:\n\n```curl\ncurl --location\
  \ --request PUT 'https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/REDACTED'\
  \ \\\n--header 'Content-Type: application/pdf' \\\n--data 'YOUR_PATH_TO_DOCUMENT.pdf'\n\
  ```\n\nNote that in step 2:\n  - you must omit an authorization header\n  - the\
  \ `Content-Type` header must match the `content_type` body parameter in step 1\n\
  \  - the pre-signed `upload_url` doesn't support Base64 encoded documents, so you\
  \ PUT the document bytes directly to the endpoint.\n\n\nFor a step-by-step tutorial\
  \ on calling this endpoint, see\n[Try asynchronous extraction from a Sensible URL](https://docs.sensible.so/docs/api-tutorial-async-2).\n"
api:
  file: openapi_extraction.json
  operationId: generate-an-upload-url
hidden: false
metadata:
  description: Learn how to extract data asynchronously from documents using Sensible's
    URL generation endpoint with step-by-step API instructions.
---
