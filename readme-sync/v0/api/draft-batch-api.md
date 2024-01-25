---
title: "Group extractions by batch ID"
hidden: true
---

You can use batch extraction endpoints to associate a set of documents to a batch ID and batch description. For example, if you want to identify a set of extractions as originating from an uploaded folder so that you can combine them into one Excel sheet, you can group them by a batch ID.

##  Overview

See the following steps for an overview of the endpoints to call for this use case:  

1. Create a batch of N document names to be extracted with `POST extract/batch`. The endpoint returns the batch ID.
2.  Create upload URLs for M of the documents with  `PUT extract/batch/upload_urls/{batch_id}/{start_index}/{end_index}`. The endpoint returns the URLs.
3. Upload the documents to their corresponding URLs.
4. Retrieve each extraction with `documents/{extraction_id}`. Each extraction includes the `batchID`.

## Steps

1. 