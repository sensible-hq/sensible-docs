---
title: "Try synchronous extraction"
hidden: false
---

Try out a test endpoint, the [/extract endpoint](https://docs.sensible.so/reference/extract-data-from-a-document). This endpoint accepts a document and returns extracted data synchronously. Use asynchronous endpoints in production.

Audience
---

If you're new to APIs, use this tutorial to return document data from an example tax document.

Or, if you're familiar with APIs:

- see the [API quickstart](doc:quickstart) to get a sample API response.

- explore the Sensible Postman collection:

![Run in Postman](https://run.pstmn.io/button.svg)

Prerequisites
---

To follow these tutorials, you need:

- An [API key](https://app.sensible.so/account). Create this key after you sign up for a [Sensible account](https://app.sensible.so/register). 
- [Postman](https://www.postman.com/) desktop app, or a command line with cURL installed.
- An example extraction configuration. See the following section.

## Configure the extraction

To create example extraction configuration, follow the steps in [Out-of-the-box extractions](doc:library-quickstart) to add support for the **1040s** document type to your account. You'll use this document type in the following steps.

Run the request in Postman
----

To run a Sensible API request in Postman, follow these steps:

1. Copy the following code sample, and replace `*YOUR_API_KEY*` with your [API key](https://app.sensible.so/account/):


```curl
curl --request POST \
  --url 'https://api.sensible.so/v0/extract/1040s' \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/pdf' \
  --data-binary '@/PATH_TO_DOWNLOADED_DOCUMENT.pdf'
```

2. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_import.png)

3. Download the following example document, which works with the prerequisite  **1040s**  document type:

| Example document | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/templates/Tax%20Forms/1040s/refdocs/1040_2021_sample.pdf) |
| ----------- | ------------------------------------------------------------ |

4.  Correct the path to the downloaded document: In the request, click the **Body** tab, select **binary**, then click **Select file** and select the document you downloaded:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_file.png)



5. Click **Send**. The response includes a `parsed_document` object that looks something like the following:

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

**Note:**  Did you notice that this API call doesn't specify a config (`1040_2021`)? As a convenience, Sensible evaluates all the configs for the document type  (`1040s`), and **automatically** chooses the one that fits best.

(Optional) See how it works in the Sensible app
=====

To see this example in the Sensible app:

1. Log into the [Sensible app](https://app.sensible.so/signin/).

2. On the **Document types** tab, select the **1040s** document type, then select the 1040_2021 configuration.

3. Visually examine the example document (middle pane), config (left pane), and extracted data (right pane) to better understand the configuration for the API call you just ran:

![q](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_app.png)
