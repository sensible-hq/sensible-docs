---
title: "Try a webhook"
hidden: false
---

For asynchronous extractions, you can retrieve extraction results using either API endpoints or a webhook. A webhook allows you to receive the extraction as a push, rather than waiting for responses from API endpoints. 

For this tutorial, let's try a webhook in combination with the `/extract_from_url` endpoint. Note you can also use the webhook with the `/generate_upload_url` endpoint and other asynchronous endpoints. 

Prerequisites
====

See [prerequisites](doc:api-tutorial#prerequisites). 


Configure the webhook
====

1. Generate a destination for the webhook: navigate to [https://webhook.site/](https://webhook.site/) to automatically create a unique test page:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_webhook_1.png)
**Note:** Use this website [solely for testing](https://webhook.site/terms). In production, make your own destination for the webhook payload.

2. Copy the following code sample, and replace `YOUR_UNIQUE_URL` with your uniquely generated webhook.site URL: 

```json
curl --location --request POST 'https://api.sensible.so/v0/extract_from_url/tax_forms' \
--header 'Authorization: Bearer YOUR_API_KEY' \
--header 'Content-Type: application/json' \
--data-raw '{"document_url":"https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf",
"webhook": {"url":"YOUR_WEBHOOK_URL","payload":"some info you want to include in addition to the default payload, which includes extraction id, type, and parsed doc"}}'
```

3. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

   

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_webhook_2.png)

4. Click **Send** in Postman.

Check the webhook response
====

Visit your unique URL at webhook.site to verify there's a response at the URL that includes  `parsed_document` and  `webhook` objects that look something like the following: 

```
{

	"webhook": {
		"payload": "some info you want to include in addition to the default payload, which includes extraction id, type, and parsed doc",
		"url": "https://webhook.site/b37c53a3-fb75-48d6-df696ebd1388"
	},
	"parsed_document": {
		"year": {
			"type": "string",
			"value": "2021"
		},
		"filing_status.single": {
			"type": "boolean",
			"value": true
		},
		"filing_status.married_filing_jointly": {
			"type": "boolean",
			"value": false
		},
		"filing_status.married_filing_separately": {
			"type": "boolean",
			"value": false
		},
		"filing_status.head_of_household": {
			"type": "boolean",
			"value": false
		},
		"filing_status.qualifying_widow": {
			"type": "boolean",
			"value": false
		},
		"name": {
			"type": "string",
			"value": "Connor Roy"
		},
		"ssn": {
			"type": "string",
			"value": "337-18-2333"
		}
	}


}
```

