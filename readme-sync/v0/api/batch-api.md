---
title: "Group extractions by batch ID"
hidden: true
---

You can use batch extraction endpoints to associate a set of documents to a batch ID and batch description. For example, if you want to combine the extractions from one uploaded documents folder into a single Excel file, you can use a batch ID to track which extractions to combine.

##  Overview

See the following steps for an overview of the endpoints to call for this use case:  

1. Create a batch of N document file names to be extracted with `POST extract/batch`. The endpoint returns the batch ID.
2.  Create upload URLs for M of the documents with  `PUT extract/batch/upload_urls/{batch_id}/{start_index}/{end_index}`. The endpoint returns the URLs.
3. Upload the documents to their corresponding URLs to request extractions.
4. Retrieve each extraction with `GET documents/{extraction_id}`. Each extraction includes the `batchID`.

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
The following parameters are available to you for the `POST extract/batch` endpoint:

| Parameter                    | description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| documentNames (**required**) | Array of the file names of the documents in the batch, for example, `["1.pdf", "2.png"]`. The maximum batch size is 5,000. |
| contentTypes                 | Array of the content types of the documents in the Document Names array, for example, `["application/pdf",  "image/png"]`. For information about supported content types, see [Supported file types](doc:file-types). |
| description                  | Description of the batch.                                    |
| docType (**required**)       | The document type in your Sensible account to extract from.  If you don't specify this parameter, you must specify the Portfolio Doc Types parameter. |
| portfolioDocTypes            | Array of document types to extract from, if all the documents in the batch are [portfolio](doc:portfolio) documents. |
| configuration                | The configuration to use when extracting the documents in the batch. N/A for the Portfolio Doc Types parameter. |




2. Create  upload URLs for an indexed range of the documents in the batch. Use zero-based indices to upload the documents in the same order that you listed them in the previous step. For example, to upload the two documents in the previous step :

```curl
   curl 'https://api.sensible.so/v0/extract/batch/upload_urls/c73c7932-82c0-438c-a339-175d7d0771bd/0/1' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: Bearer YOUR_API_KEY' \
```

   The response is an array of upload URLs, where each URL's path includes the extraction IDs. 

```json
[
    "https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/c024cd1c-5f33-4a82-b2ea-2c807e44988b/6bd67eb5-9e28-4161-9ae1-43015e6b680c/EXTRACTION/0b34ce99-bf15-4e0d-a391-b03e4c830414REDACTED",
    "https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/c024cd1c-5f33-4a82-b2ea-2c807e44988b/6bd67eb5-9e28-4161-9ae1-43015e6b680c/EXTRACTION/a122f739-3f4a-443d-bb70-718fd2828af1REDACTED"
]   
```

3. Put each document to its upload URL to request extraction, using the same guidelines as you'd use for the [generate_upload_url](ref:generate-upload-url) endpoint.  For example:

```json
   curl --request PUT 'https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/c024cd1c-5f33-4a82-b2ea-2c807e44988b/6bd67eb5-9e28-4161-9ae1-43015e6b680c/EXTRACTION/0b34ce99-bf15-4e0d-a391-b03e4c830414REDACTED' \
   --header 'Content-Type: application/pdf' \
   --data 'YOUR_PATH_TO_DOCUMENT/doc1.pdf'
```

   You should get an empty success response.



4. Retrieve each extraction using the [documents/{extraction_id}](ref:retrieving-results) endpoint. 

   You can poll status calling `GET /extract/batch/{batchId}`. For example, while the requested extraction for `doc1.pdf` is in progress, the batch details for the batch created in a previous step are:

```json
   {
       "id": "c73c7932-82c0-438c-a339-175d7d0771bd",
       "description": "test batch",
       "extraction_ids": [
           "0b34ce99-bf15-4e0d-a391-b03e4c830414",
           "a122f739-3f4a-443d-bb70-718fd2828af1"
       ],
       "waiting": 1
   }
```

You can update the batch description using `PUT extract/batch/{batchId}` and specifying the new `description` in the body as JSON.

Each extraction returns the `batchID`. For example:

```json
   curl 'https://api.sensible.so/v0/documents/0b34ce99-bf15-4e0d-a391-b03e4c830414' \
   --header 'Authorization: Bearer YOUR_API_KEY'
```

   returns:

```json
   {
       "id": "0b34ce99-bf15-4e0d-a391-b03e4c830414",
       "created": "2024-01-23T19:30:41.356Z",
       "completed": "2024-01-23T19:42:21.584Z",
       "status": "COMPLETE",
       "type": "contracts",
       "document_name": "doc1.pdf",
       "parsed_document":
       /* JSON data abbreviated */
       "batchId": "c73c7932-82c0-438c-a339-175d7d0771bd"
   }
```

  

5. You can generate an Excel file that combines the completed extractions in the batch by using the batch ID. For example:

   ```curl
   curl 'https://api.sensible.so/v0/generate_excel_from_batch/c73c7932-82c0-438c-a339-175d7d0771bd' \
   --header 'Authorization: Bearer YOUR_API_KEY'
   ```

   For more information about converting extractions to Excel, see [SenseML to spreadsheet reference](doc:excel-reference). 

   