---
title: "Try asynchronous extraction from your URL"
hidden: false
---



PDFs that are greater than 4.5MB in size or that require over 30 seconds of processing time must use Sensible's asynchronous endpoints. You have two options for asynchronously processing your PDF:

- extracting from a PDF at a URL you provide

- extracting from a PDF at a Sensible-provided URL 

This topic covers the first option. 

For either option, you can specify a [webhook](doc:api-tutorial-webhook) for Sensible to push the results to as soon as they're ready.

Extract from a URL you provide 
====


Prerequisites
----

This tutorial assumes you've completed the [prerequisites](doc:api-tutorial#section-prerequisites). 

Extract the data 
----

To try out the [extract_from_url](https://sensiblehq.readme.io/reference#provide-a-download-url) endpoint, let's use an example PDF hosted in GitHub:

1. Copy the following code sample and replace YOUR_API_KEY with your API key:

   ```json
   curl --request POST 'https://api.sensible.so/v0/extract_from_url/auto_insurance_quote' \
   --header 'Authorization: Bearer YOUR_API_KEY' \
   --header 'Content-Type: application/json' \
   --data-raw '{"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf"}'
   ```

   **Note:**  In the preceding code sample, the `document_url` must be a URL that responds to a GET request with PDF bytes. For testing purposes, we're using a sample PDF at this URL: `https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf`.

2. In the Postman desktop app, click **Import**, select **Raw text**, and paste in the code sample:

   ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_postman_1.png)

3. Click **Send**, and you should see a response like:

   ```json
   {
       "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836",
       "created": "2021-06-15T16:29:27.875Z",
       "status": "WAITING",
       "type": "auto_insurance_quote"
   }
   ```

**Note:** You don't have to specify the config you created (`anyco`) in this call. Sensible looks at all the configs for the document type you made in this quickstart (`auto_insurance_quote`), and **automatically** chooses the one that fits best!

Retrieve extraction
----

 To retrieve the extraction results for the sample PDF, you have two options:

- Use the `/documents` endpoint. See the following steps.
- Use a webhook. See [Try a webhook](doc:api-tutorial-webhook).


To retrieve the extraction results with the  `/documents` endpoint, take the following steps:


1. In a previous step on this page, you got back a result that included information like this:

   ```json
   {
       "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836",
       "created": "2021-06-16T16:22:56.576Z",
       "status": "WAITING",
   ```

   

2. Copy the document extraction `id` from that response. You'll use it to download the PDF extraction.

3. Copy the following code sample and replace YOUR_EXTRACTION_ID and YOUR_API_KEY:

```json
curl --request GET 'https://api.sensible.so/v0/documents/YOUR_EXTRACTION_ID' \
--header 'Authorization: Bearer YOUR_API_KEY'
```

3. In the Postman desktop app, click **Import**, select **Raw text**, and paste in the code sample:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_postman_2.png)

4. Click **Send**. You should see a response like the following:

```json
{
    "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836",
    "created": "2021-06-15T16:44:18.917Z",
    "status": "COMPLETE",
    "type": "auto_insurance_quote",
    "configuration": "anyco",
    "parsed_document": {
        "policy_period": {
            "type": "string",
            "value": "April 14, 2021 - Oct 14, 2021"
        },
        "comprehensive_premium": {
            "source": "$150",
            "value": 150,
            "unit": "$",
            "type": "currency"
        },
        "policy_number": {
            "type": "string",
            "value": "123456789"
        }
    },
    "download_url": "https://sensible-so-document-type-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=ASIAR355P7ASRMWOLX6W&Expires=1623790786&Signature=REDACTED-amz-security-token=REDACTED"
}
```

