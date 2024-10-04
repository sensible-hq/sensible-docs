---
title: "Try asynchronous extraction from a Sensible URL"
hidden: false
---

Use Sensible's asynchronous endpoints in production scenarios. You have two options for asynchronous processing:

- Provide your own URLs for your documents. 

- Use URLs provided by Sensible for your documents. 

This topic covers using URLs provided by Sensible. This is a good option if you can't create either publicly accessible or pre-signed URLs for your documents.

For either option, you can get the results as soon as they're ready by specifying a [webhook](doc:api-tutorial-webhook).

Extract from a URL Sensible provides
====

## Prerequisites


To follow these tutorials, you need:

- An [API key](https://app.sensible.so/account). Create this key after you sign up for a [Sensible account](https://app.sensible.so/register). 
- [Postman](https://www.postman.com/) desktop app, or a command line with cURL installed..

## Configure the extraction

To create example extraction configuration, follow the steps in [Out-of-the-box extractions](doc:library-quickstart) to add support for the **1040s** document type to your account. You'll use this document type in the following steps.


## Generate the upload URL



Generate a temporary, one-time Sensible URL for a document: 

  1. Copy the following code sample and replace `*YOUR_API_KEY*` with your [API key](https://app.sensible.so/account/):


```json
curl --request POST 'https://api.sensible.so/v0/generate_upload_url/1040s' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_API_KEY' \
--data '{"content_type":"application/pdf"}'
```

2. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import the code sample.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_3.png)

3. Click **Send**. The response looks something like the following:

```json
{
    "id": "14d82783-c12b-4e70-b0ae-ca1ce35a9836",
    "created": "2021-06-16T16:22:56.576Z",
    "status": "WAITING",
    "type": "1040s",
    "upload_url": "https://sensible-so-utility-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=REDACTED&Expires=1623861476&Signature=REDACTED&x-amz-security-token=REDACTED"
}
```

## Extract the data 



Use the one-time URL you generated in the previous step to extract data from the document:

1. Copy the following code sample. Replace `YOUR_UPLOAD_URL` with the `upload_url` that you received as a response in the previous steps:

```json
curl --request PUT 'YOUR_UPLOAD_URL' \
--data-binary '@/PATH_TO_DOWNLOADED_DOCUMENT.pdf' \
--header 'Content-Type: application/pdf' \
```

2. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_4.png)

**Troubleshoot**: Postman can automatically add authorization and content-type headers that cause errors:

- If Postman automatically specifies authorization for the request, then specify **No Auth** in the request's **Auth** tab :

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_no_auth.png)

- If Postman automatically specifies a content type header, then ensure that the value of the Content-Type header matches that of the `content_type` body parameter in the request in step 1. In this case, it must be `application/pdf`.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_headers_2.png)

3. If you haven't already, download the following example document, which works with the example `1040s` document type you created in the **Prerequisites** section:

| Example document | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/templates/Tax%20Forms/1040s/refdocs/1040_2021_sample.pdf) |
| --------------------------- | ------------------------------------------------------------ |

4. Correct the path to the downloaded document in your request: click the **Body** tab, select **binary**, then click **Select file** and select the document:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_file.png)

  

5. Click **Send** to send the request. The response is  `200`:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_200.png) 


## Retrieve extraction


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

