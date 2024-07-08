---
title: "Try asynchronous extraction from your URL"
hidden: false
---



Use Sensible's asynchronous endpoints in production scenarios. You have two options for asynchronous processing:

- Provide your own URLs for your documents. 

- Use URLs provided by Sensible for your documents. 

This topic covers providing your own URLs. This is a good option if you host your documents at either publicly accessible or a pre-signed URLs. The URL must respond to GET requests with document bytes.

For either option, you can get the results as soon as they're ready by specifying a [webhook](doc:api-tutorial-webhook).

Extract from a URL you provide 
====


Prerequisites
----

See [prerequisites](doc:api-tutorial#prerequisites).

Extract the data 
----

To try out the [extract_from_url](https://docs.sensible.so/reference/extract-from-url) endpoint, let's use an example document hosted in GitHub:

1. Copy the following code sample and replace `*YOUR_API_KEY*` with your [API key](https://app.sensible.so/account/):

   ```json
   curl --request POST 'https://api.sensible.so/v0/extract_from_url/tax_forms' \
   --header 'Authorization: Bearer YOUR_API_KEY' \
   --header 'Content-Type: application/json' \
   --data-raw '{"document_url":"https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf"}'
   ```

   

3. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_1.png)

3. Click **Send**, and you should see a response like:

   ```json
   {
       "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836",
       "created": "2021-06-15T16:29:27.875Z",
       "status": "WAITING",
       "type": "tax_forms"
   }
   ```

**Note:** You don't have to specify the config for document (`1040_2021`) in this call. Sensible looks at all the configs for the document type (`tax_forms`), and **automatically** chooses the one that fits best!

Retrieve extraction
----

 To retrieve the extraction results for the sample document, you have two options:

- Use the `/documents` endpoint. See the following steps.
- Use a webhook. See [Try a webhook](doc:api-tutorial-webhook).


To retrieve the extraction results with the  `/documents` endpoint, take the following steps:


1. In a previous step on this page, you got back a result that included an extraction ID:

   ```json
   {
       "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836"
   }
   ```
   
   Copy the document extraction `id` from that response. You'll use it to download the document extraction.
   
3. Copy the following code sample and replace `*YOUR_EXTRACTION_ID*` and `*YOUR_API_KEY*`:

```json
curl --request GET 'https://api.sensible.so/v0/documents/YOUR_EXTRACTION_ID' \
--header 'Authorization: Bearer YOUR_API_KEY'
```

3. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_2.png)

4. Click **Send**. The response includes a `parsed_document` object that looks something like the following:

```json
{
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

