---
title: "Try a webhook"
hidden: false
---

For asynchronous extractions, you can retrieve extraction results using either API endpoints or a webhook. A webhook allows you to receive the extraction as a push, rather than waiting for responses from API endpoints. 

For this tutorial, let's try a webhook in combination with the `/extract_from_url/` endpoint.

Prerequisites
====

See [prerequisites](doc:api-tutorial#prerequisites). 


Configure the webhook
====

1. Generate a destination for the webhook: navigate to [https://webhook.site/](https://webhook.site/) to automatically create a unique test page:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_webhook_1.png)
**Note:** Use this website [only for testing](https://webhook.site/terms). In production, implement your own destination for the webhook payload.

2. Copy the following code sample, and replace `YOUR_UNIQUE_URL` with your uniquely generated webhook.site URL:

```json
curl --location --request POST 'https://api.sensible.so/v0/extract_from_url/auto_insurance_quote' \
--header 'Authorization: Bearer YOUR_API_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf",
"webhook": {"url":"YOUR_WEBHOOK_URL","payload":"some info you want to include that's additional to the default payload, which includes extraction id, type, and parsed doc"}}'
```

3. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

   

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_webhook_2.png)

4. Click **Send** in Postman.

Check the webhook response
====

Visit your unique URL at webhook.site to verify there is a response at the URL like the following: 

```
{
  "id": "4dee64e9-4b08-4c2c-baef-02649b40b488",
  "created": "2021-08-31T17:24:43.185Z",
  "status": "COMPLETE",
  "type": "auto_insurance_quote",
  "configuration": "anyco",
  "webhook": {
    "payload": "some info you want to include that's additional to the default payload, which includes extraction id, type, and parsed doc",
    "url": "https://webhook.site/b37c53a3-fb75-48d6-df696ebd1388"
  },
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
  "validations": [],
  "validation_summary": {
    "fields": 3,
    "fields_present": 3,
    "errors": 0,
    "warnings": 0,
    "skipped": 0
  },
  "download_url": "https://sensible-so-document-type-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=ASIAR355P7ASRMWOLX6W&Expires=1623790786&Signature=REDACTED-amz-security-token=REDACTED",
  "payload": "some info you want to include that's additional to the default payload, which includes extraction id, type, and parsed doc"
}
```

