---
title: "Try asynchronous extraction from a Sensible URL"
hidden: false
---

Use Sensible's asynchronous endpoints to extract data from PDFs that are greater than 4.5MB in size or that require over 30 seconds of processing time. You have two options for asynchronous processing:

- Provide your own URLs for your documents. 

- Use URLs provided by Sensible for your documents. 

This topic covers using URLs provided by Sensible. This is a good option if you can't create either publicly accessible or pre-signed URLs for your PDFs.

For either option, you can get the results as soon as they're ready by specifying a [webhook](doc:api-tutorial-webhook).

Extract from a URL Sensible provides
====

Prerequisites
----

See [prerequisites](doc:api-tutorial#prerequisites).


Generate the upload URL
----


Generate a one-time Sensible URL for a document (this URL expires within minutes): 

  1. Copy the following code sample and replace `YOUR_API_KEY` with your API key:

```json
curl --request POST 'https://api.sensible.so/v0/generate_upload_url/auto_insurance_quote' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_API_KEY'
```

2. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_3.png)

3. Click **Send**. The response looks something like the following:

```json
{
    "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836",
    "created": "2021-06-16T16:22:56.576Z",
    "status": "WAITING",
    "type": "auto_insurance_quote",
    "upload_url": "https://sensible-so-utility-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=REDACTED&Expires=1623861476&Signature=REDACTED&x-amz-security-token=REDACTED"
}
```

Extract the data 
----


Use the one-time URL you generated in the previous step to extract data from the document:

1. Copy the following code sample. Replace `YOUR_UPLOAD_URL` with the `upload_url` that you received as a response in the previous steps:

```json
curl --request PUT 'YOUR_UPLOAD_URL' \
--header 'Content-Type: ' \
--header 'Authorization: ' \
--data-binary '@/PATH_TO_DOWNLOADED_PDF/auto_insurance_anyco_golden.pdf'
```

2. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_4.png)

3. If you haven't already, download the following example PDF, which works with the example `auto_insurance_quote` config you created previously in the **Prerequisites** section:

| auto_insurance_anyco | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) |
| --------------------------- | ------------------------------------------------------------ |

4. Correct the path to the downloaded PDF in your request: click the **Body** tab, select **binary**, then click **Select file** and select the PDF:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_file.png)

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_headers_2.png)

   

5. Click **Send** to send the request. The response is  `200`:



  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_200.png) 




Retrieve extraction
----

 To retrieve the document extraction, you have two options:

- Use the `/documents` endpoint. See the following steps.
- Use a webhook. See [Try a webhook](doc:api-tutorial-webhook).


To retrieve the extraction results with the  `/documents` endpoint, take the following steps:


1. In a previous step on this page,  you generated a URL and got back a response that included an extraction ID:

   ```json
   {
       "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836"
   }
   ```
   
2. Copy the document extraction `id` from that response.

3. Copy the following code sample and replace YOUR_EXTRACTION_ID and YOUR_API_KEY:

```json
curl --request GET 'https://api.sensible.so/v0/documents/YOUR_EXTRACTION_ID' \
--header 'Authorization: Bearer YOUR_API_KEY'
```

3. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_2.png)

4. Click **Send**. The response looks something like the following:

```json
{
    "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836",
    "created": "2021-06-16T16:22:56.576Z",
    "status": "COMPLETE",
    "type": "auto_insurance_quote",
    "configuration": "anyco",
    "parsed_document": {
        "policy_number": {
            "type": "string",
            "value": "123456789"
        },
        "policy_period": {
            "type": "string",
            "value": " April 14, 2021 - Oct 14, 2021"
        },
        "comprehensive_premium": {
            "source": "$150",
            "value": 150,
            "unit": "$",
            "type": "currency"
        }
    },
    "validations": [],
    "validation_summary": {
        "fields": 3,
        "fields_present": 3,
        "errors": 0,
        "warnings": 0,
        "skipped": 0
    },
    "download_url": "https://sensible-so-document-type-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=ASIAR355P7ASRMWOLX6W&Expires=1623790786&Signature=REDACTED-amz-security-token=REDACTED"
}
```

