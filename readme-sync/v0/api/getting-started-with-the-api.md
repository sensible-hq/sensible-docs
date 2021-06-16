title: "Getting started with the API"
hidden: true

Let's get started with the Sensible API! We'll use Postman to get a quick sense of how the endpoints work together. 

Prerequisites
====



To follow this tutorial, you'll need:

- an example config
-  [Postman](https://www.postman.com/) desktop app (or follow along with cURL in the command line)

**Prerequisite: Create an example config**

1. You need an example config and doc type. If you haven't already done so, follow the steps in [Create a config](doc:quickstart#section-create-the-config) to create an example `anyco` config in an example  `auto_insurance_quote` document type. 
2. **Important!** Remember to click **Publish** in the Sensible app to publish your config, or your requests won't work:  

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/quickstart_publish_config.png).



**Download Postman**

For an easy way to run the cURL requests, download the [Postman](https://www.postman.com/) desktop app. 

 Try the synchronous extraction endpoint
 ====



Let's try out the most commonly used endpoint, the  [/extract endpoint](https://sensiblehq.readme.io/reference#rate-confirmations). This endpoint takes a PDF file and returns extracted data synchronously. 

**Import the request**

1. Copy the following code sample, and replace `YOUR_API_KEY` with your API key:

```curl
curl --request POST \
  --url https://api.sensible.so/v0/extract/auto_insurance_quote \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/pdf' \
  --data-binary '@/PATH_TO_DOWNLOADED_PDF/auto_insurance_anyco_golden.pdf'
```



2. In the Postman desktop app, click **Import**, select **Raw text**, and paste in the code sample:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/quickstart_postman_import.png)

2. Download the following example PDF, which works with the example `auto_insurance_quote` config you created previously:

   | auto_insurance_anyco_golden | [Download link](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf) |
   | --------------------------- | ------------------------------------------------------------ |

3. Correct the path to your downloaded PDF in your request:

- **If you're in the command line:** Replace `PATH_TO_DOWNLOADED_PDF` with the local directory path to the PDF.
- **If you're in Postman:** In the request, click the **Body** tab, select **binary**, then click **Select file** and select your PDF:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/quickstart_postman_1.png)

   

7. Click **Send**, and you should see a response like this:

```json
{
    "id": "b0ac180d-55d2-4946-80c0-a87243319746",
    "created": "2021-05-20T18:02:37.019Z",
    "status": "COMPLETE",
    "type": "auto_insurance_quote",
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
    }
}
```

**Note:** You don't have to specify the config you created (`anyco`) in this call. Sensible looks at all the configs for the document type you made in this quickstart (`auto_insurance_quote`), and **automatically** chooses the one that fits best! 

 Try the asynchronous endpoints
 ====

PDFs that are greater than 4.5MB in size or that require over 30 seconds of processing time must use Sensible's asynchronous endpoints. You have two options for asynchronously processing your PDF: - [generating an upload URL](https://sensiblehq.readme.io/reference#generate-an-upload-url), or [providing a download URL](https://sensiblehq.readme.io/reference#provide-a-download-url). You can then call the [/document endpoint](https://sensiblehq.readme.io/reference#retrieving-results) to get the results, or specify a webhook for us to push the results to as soon as they're ready. Let's walk through these options.

Extract from a URL Sensible provides
----

**Generate the upload URL**

Generate a one-time URL for the document extraction you want to run (this URL expires within minutes). 

 1. Copy the following code sample and replace YOUR_API_KEY:

```json
curl --location --request POST 'https://api.sensible.so/v0/generate_upload_url/auto_insurance_quote' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer YOUR_API_KEY'
```

2.  Import the code sample into Postman and click **Send**:

   ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_postman_3.png)

You should see a response like the following:

```json
{
    "id": "28c7e5ac-3943-4f86-bd72-8aac3fa38a43",
    "created": "2021-06-16T16:22:56.576Z",
    "status": "WAITING",
    "type": "auto_insurance_quote",
    "upload_url": "https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/28c7e5ac-3943-4f86-bd72-8aac3fa38a43.pdf?AWSAccessKeyId=REDACTED&Expires=1623861476&Signature=REDACTED&x-amz-security-token=REDACTED"
}
```



**Put the document at the URL for extraction**

Now use the one-time URL you just generated to extract data from the document:

1. Copy the following code sample. Replace the URL with the `upload_url` that you got as a response in the previous step:

```json
curl --location --request PUT 'https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/28c7e5ac-3943-4f86-bd72-8aac3fa38a43.pdf?AWSAccessKeyId=REDACTED&Expires=1623861476&Signature=wpUXfUcnoaoE2u%2FV7JSB%2FQ7iJo0%3D&x-amz-security-token=REDACTED' \
--header 'Content-Type: text/plain' \
--data-binary '@/PATH_TO_DOWNLOADED_PDF/auto_insurance_anyco_golden.pdf'
```

2. Import the code sample into Postman:

   ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_postman_4.png)

1. If you haven't already done so, download the following example PDF, which works with the example `auto_insurance_quote` config you created previously in the **Prerequisites** section:

| auto_insurance_anyco_golden | [Download link](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf) |
| --------------------------- | ------------------------------------------------------------ |

3. Correct the path to your downloaded PDF in your request:

- **If you're in the command line:** Replace `PATH_TO_DOWNLOADED_PDF` with the local directory path to the PDF.
- **If you're in Postman:** In the request, click the **Body** tab, select **binary**, then click **Select file** and select your PDF:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/quickstart_postman_1.png)

4. Click **Send** to send the request. You should see an empty 200 response. 



**Retrieve results**

To retrieve the extraction results for the sample PDF, you have two options:

- Use the `/documents` endpoint. See the following steps.
- Use a webhook. See [Try a webhook](doc:getting-started-with-the-api#section-try-a-webhook).

To retrieve the results with an endpoint:

1. Copy the following code sample, and replace YOUR_API_KEY and YOUR_EXTRACTION_ID.  Use the `id` you got in the response to the `/generate_upload_url` endpoint in the previous step, **Generate the upload URL**:

   ```json
   curl --location --request GET 'https://api.sensible.so/dev/documents/YOUR_EXTRACTION_ID' \
   --header 'Authorization: Bearer YOUR_API_KEY'
   ```
2. Import the code sample into Postman:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_postman_5.png)

3. Click **Send**. You should see a response like the following:

   ```json
   {
       "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836",
       "created": "2021-06-15T16:44:18.917Z",
       "status": "COMPLETE",
       "type": "auto_insurance_quote",
       "configuration": "anyco2",
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
       "download_url": "https://sensible-so-document-type-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=REDACTED&Expires=1623790786&Signature=REDACTED&x-amz-security-token=REDACTED"
   }
   ```

   


Extract from a URL you provide 
----

****

**Prerequisites**

To try out the [extract_from_url](https://sensiblehq.readme.io/reference#provide-a-download-url) endpoint, let's use:

- an example PDF hosted in GitHub
-  the example config and document type you created  in the **Prerequisites** section

**Extract from URL**

1. Copy the following code sample and replace YOUR_API_KEY with your API key:

   ```json
   curl --location --request POST 'https://api.sensible.so/v0/extract_from_url/auto_insurance_quote' \
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

4. Copy the document extraction `id` from the response. You'll use it to download the PDF extraction.

5. Copy the following code sample and replace YOUR_EXTRACTION_ID and YOUR_API_KEY:

   ```json
   curl --location --request GET 'https://api.sensible.so/v0/documents/YOUR_EXTRACTION_ID' \
   --header 'Authorization: Bearer YOUR_API_KEY'
   ```

6. In the Postman desktop app, click **Import**, select **Raw text**, and paste in the code sample:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_postman_2.png)

You should see a response like the following:

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
    "download_url": "https://sensible-so-document-type-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=ASIAR355P7ASRMWOLX6W&Expires=1623790786&Signature=REDACTED-amz-security-token=REDACTED"
}
```


Try a webhook
====

For asynchronous extractions, you can retrieve results using either the `/documents` endpoint or a webhook. Let's try using a webhook with the `/extract_from_url/` endpoint:

1. Follow the steps in [Extract from a URL you provide](doc:getting-started-with-the-api#section-extract-from-a-url-you-provide).
2. Generate a test destination for the webhook using a free service: navigate to [https://webhook.site/](https://webhook.site/), and you should be directed to an automatically generated unique page for your testing:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_webhook_1.png)

3. Copy the unique URL generated for you by webhook.site, and paste it into the following code sample:

   ```json
   {"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf",
   "webhook": {"url":"YOUR_UNIQUE_URL","payload":"some info you want to include that is additional to the built-in payload which includes extraction id, type, and parsed doc"}}
   ```

4. In your request in Postman, replace the content of  the **Body** tab with the preceding code sample:

      ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_webhook_2.png)

