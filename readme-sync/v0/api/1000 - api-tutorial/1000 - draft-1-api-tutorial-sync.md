---
title: "Try synchronous extraction"
hidden: true
---

Try out the most commonly used endpoint, the  [/extract endpoint](https://sensiblehq.readme.io/reference#rate-confirmations). This endpoint accepts a document (PDF or image file) and returns extracted data synchronously. 

Prerequisites
---

See [prerequisites](doc:api-tutorial#prerequisites).

Run the request in postman
----

Click through the following slides to see how to run a Sensible API request in Postman.





[block:html]
{
  "html": "<div style=\"position: relative; padding-bottom: calc(49.296875% + 41px); height: 0;\"><iframe src=\"https://demo.arcade.software/9o6EcG8ufjz322xHVN85/\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%;\"></iframe></div>"
}
[/block]
To follow along, you'll need:

- this sample code:


```curl
curl --request POST \
  --url 'https://api.sensible.so/v0/extract/auto_insurance_quote?environment=development' \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/pdf' \
  --data-binary '@/PATH_TO_DOWNLOADED_PDF/auto_insurance_anyco.pdf'
```


- the sample PDF:

| auto_insurance_anyco | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) |
| -------------------- | ------------------------------------------------------------ |



View the response
---


The response includes a `parsed_document` object that looks something like the following:

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