---
title: "Try asynchronous extraction from your URL"
hidden: false
---



Use Sensible's asynchronous endpoints to extract data from PDFs that are greater than 4.5MB in size or that require over 30 seconds of processing time. You have two options for asynchronous processing:

- Provide your own URLs for your documents. 

- Use URLs provided by Sensible for your documents. 

This topic covers providing your own URLs. This is a good option if you host your documents at either publicly accessible or a pre-signed URLs. The URL must respond to GET requests with PDF bytes.

For either option, you can get the results as soon as they're ready by specifying a [webhook](doc:api-tutorial-webhook).

Extract from a URL you provide 
====


Prerequisites
----

See [prerequisites](doc:api-tutorial#prerequisites).

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

   

2. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_api_quickstart_postman_file.png)

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


1. In a previous step on this page, you got back a result that included and extraction ID:

   ```json
   {
       "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836"
   }
   ```
   
   Copy the document extraction `id` from that response. You'll use it to download the PDF extraction.
   
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
    "created": "2021-08-31T17:22:33.984Z",
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

