---
title: Retrieve results
excerpt: ''
api:
  file: sensible.json
  operationId: retrieving-results-1
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---
Use this endpoint in conjunction with asynchronous extraction requests to retrieve your results (using the `id` field returned by asynchronous request). You can also use this endpoint to retrieve the results for documents extractions from the synchronous /extract endpoint.

To poll extraction status, check the `status` field in this endpoint's response. When the extraction completes, the returned status is `COMPLETE` and the response includes results in the `parsed_document` field.  For fields in the extraction for which Sensible couldn't find a value, Sensible returns null.
