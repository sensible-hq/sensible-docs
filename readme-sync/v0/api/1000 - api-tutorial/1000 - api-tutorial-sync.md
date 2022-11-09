---
title: "Try synchronous extraction"
hidden: false
---

Try out the most commonly used endpoint, the  [/extract endpoint](https://sensiblehq.readme.io/reference#rate-confirmations). This endpoint accepts a document (PDF or image file) and returns extracted data synchronously. 

Audience
---

If you're new to APIs, use this tutorial to return meaningful document data from an example insurance quote.

Or, if you're familiar with APIs:

- see the [quickstart](doc:quickstart) to get a sample API response.

- explore the Sensible Postman collection:

![Run in Postman](https://run.pstmn.io/button.svg) 

Prerequisites
---

See [prerequisites](doc:api-tutorial#prerequisites).

Run the request in Postman
----

Click through the following slides to see how to run a Sensible API request in the [Postman web app](https://www.postman.com/planetary-meteor-85425/workspace/new-team-workspace/documentation/18249768-38adacb4-d8f7-4365-9ee0-fa1d59a3bd03).  You'll need the code sample and the example PDF listed in the following steps.

[block:html]
{
  "html": "<div style=\"position: relative; padding-bottom: calc(87.19723183391004% + 41px); height: 0;\"><iframe src=\"https://demo.arcade.software/jgr2VsTcHXr3xI9zk25P/\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%;\"></iframe></div>"
}
[/block]



If you don't want to click through the slides, follow these steps instead:


1. Verify that you published the **anyco** config listed in the prerequisites to the Development environment (in the Sensible app, select the config and click **Publish>Publish to Development**).

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_publish_config.png)

1. Copy the following code sample, and replace `YOUR_API_KEY` with your API key:

```curl
curl --request POST \
  --url 'https://api.sensible.so/v0/extract/auto_insurance_quote?environment=development' \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/pdf' \
  --data-binary '@/PATH_TO_DOWNLOADED_PDF/auto_insurance_anyco.pdf'
```



2. In your Postman workspace, click **Import**, select **Raw text**, paste the code sample, and follow the prompts to import to code sample.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_import.png)

3. Download the following example PDF, which works with the prerequisite  `auto_insurance_quote` config:

| auto_insurance_anyco | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) |
| --------------------------- | ------------------------------------------------------------ |

4. Correct the path to the downloaded PDF: In the request, click the **Body** tab, select **binary**, then click **Select file** and select the PDF:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_file.png)

   

5. Click **Send**. The response includes a `parsed_document` object that looks something like the following:

```json
{
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

**Note:**  Did you notice that this API call doesn't specify a config (`anyco`)? As a convenience, Sensible evaluates all the configs for the document type  (`auto_insurance_quote`), and **automatically** chooses the one that fits best.