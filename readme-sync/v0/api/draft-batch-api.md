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

1. Create a batch:

   ```curl
   curl 'https://api.sensible.so/v0/extract/batch' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: Bearer YOUR_API_KEY' \
   --data '{"documentNames":["doc1.pdf", "doc2.pdf"],
   "description":"test batch",
   "docType":"contracts",
   }'
   ```

   You'll get back a batch ID in the response: 

   ```
   "c73c7932-82c0-438c-a339-175d7d0771bd"
   ```
The following parameters are available to you for the `extract/batch` endpoint:

| Parmeter                      | type | description                     |
| ----------------------------- | ---- | ------------------------------- |
| documentNames: string[];      |      | The maximum batch size is 5000. |
| description?: string;         |      |                                 |
| docType?: string;             |      |                                 |
| portfolioDocTypes?: string[]; |      |                                 |
| configuration?: string;       |      |                                 |


2. Create  upload URLs for an indexed range of the documents in the batch. Use zero-based indices to upload the documents in the same order that you listed them in the previous step. For example, to upload the two documents in the previous step :

   ```curl
   curl 'https://api.sensible.so/v0/extract/batch/upload_urls/c73c7932-82c0-438c-a339-175d7d0771bd/0/1' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: Bearer YOUR_API_KEY' \
   --data ''
   ```

   The response is an array of upload URLs, where each URL's path includes the extraction IDs for each document: 

```json
[
    "https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/c024cd1c-5f33-4a82-b2ea-2c807e44988b/6bd67eb5-9e28-4161-9ae1-43015e6b680c/EXTRACTION/0b34ce99-bf15-4e0d-a391-b03e4c830414REDACTED",
    "https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/c024cd1c-5f33-4a82-b2ea-2c807e44988b/6bd67eb5-9e28-4161-9ae1-43015e6b680c/EXTRACTION/a122f739-3f4a-443d-bb70-718fd2828af1REDACTED"
]   
```

3. 