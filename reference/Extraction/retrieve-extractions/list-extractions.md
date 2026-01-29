---
title: List extractions
excerpt: "Use this endpoint to get a filtered list of past extractions.\nThis endpoint\
  \ returns a summary for each extraction, listed in reverse chronological order.\
  \ \nTo get details about an extraction, use the [Retrieve extraction by ID](ref:retrieving-results)\
  \ endpoint.\nThis endpoint uses keyset pagination to retrieve the next page of results.\n\
  By default it returns a first page of 20 extractions and an opaque `continuation_token`\
  \ that you can pass in the next request to get the next page of results, until the\
  \ endpoint returns `continuation_token` to indicate the last page. \nUse the `limit`\
  \ parameter to configure page size. \n"
api:
  file: openapi_extraction.json
  operationId: list-extractions
hidden: false
metadata:
  description: 'null'
---
