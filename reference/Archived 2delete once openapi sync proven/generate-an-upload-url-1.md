---
title: Extract doc at Sensible URL
excerpt: ''
api:
  file: sensible.json
  operationId: generate-an-upload-url-1
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---
Extract data asynchronously from a document with the following steps: 

1. Use this endpoint to generate a Sensible URL.
2. PUT the PDF you want to extract data from at the URL, where `SENSIBLE_UPLOAD_URL` is the URL you received from this endpoint's response. For example:

[block:code]
{
  "codes": [
    {
      "code": "curl -T ./sample.pdf \"SENSIBLE_UPLOAD_URL\"",
      "language": "shell"
    }
  ]
}
[/block]
 Note: the pre-signed upload_url does not support Base64 encoded PDFs. You PUT the PDF bytes directly to the endpoint and must omit the content-type header. 

3.  To retrieve the extraction or poll its status, use the extraction `id` returned in the response to call the GET documents/{id} endpoint.

You must use this or other asynchronous endpoints for PDFs that are over 4.5MB in size or require over 30 seconds to process.

For a step-by-step tutorial on calling this endpoint, see [Try asynchronous extraction from a Sensible URL](doc:api-tutorial-async-2).