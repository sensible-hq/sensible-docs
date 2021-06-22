---
title: "Try synchronous extraction"
hidden: false
---



Let's try out the most commonly used endpoint, the  [/extract endpoint](https://sensiblehq.readme.io/reference#rate-confirmations). This endpoint takes a PDF file and returns extracted data synchronously. 

Prerequisites
---

This tutorial assumes you've completed the [prerequisites](doc:api-tutorial#section-prerequisites).




Import the request
----


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

3. Download the following example PDF, which works with the example `auto_insurance_quote` config you created previously in the Prerequisites:

| auto_insurance_anyco_golden | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf) |
| --------------------------- | ------------------------------------------------------------ |

4. Correct the path to your downloaded PDF: In the request, click the **Body** tab, select **binary**, then click **Select file** and select your PDF:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/quickstart_postman_1.png)

   

5. Click **Send**, and you should see a response like this:

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

