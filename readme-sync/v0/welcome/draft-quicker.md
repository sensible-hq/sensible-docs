---
title: "Quicker start"
hidden: true

---

Run an extraction on a doc
=====

1. Clone the code sample of your choice:
 [Python](https://github.com/fscelliott/sens-code-example)


2. Add your API_KEY to the code sample:

  

  [block:code]
  {
   "codes": [
   {
     "code": "1. CD to the cloned code sample directory, sens-code-example\n2. Make a new file: `touch secrets.py`\n3. Add the API key to the file: `API_KEY = \"YOUR_API_KEY\"`\n4. Verify that `.gitignore` lists `secrets` so that you don't expose your key",
     "language": "text",
     "name": "python"
   },
   {
     "code": "",
     "language": "text",
     "name": "otherlangsTBD"
   }
   ]
  }
  [/block]

  

3. Run the code sample:



[block:code]
{
  "codes": [
    {
      "code": " `python extract_doc.py`",
      "language": "text",
      "name": "python"
    },
    {
      "code": "",
      "language": "text",
      "name": "otherlangsTBD"
    }
  ]
}
[/block]


You should see a response like the following:



```json
   {
   	"id": "234b2afd-5165-4022-a41f-bd31ad89c3ff",
   	"created": "2021-09-22T20:16:34.841Z",
   	"status": "COMPLETE",
   	"type": "auto_insurance_quote_api_test",
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
   		"property_liability_premium": {
   			"source": "$10",
   			"value": 10,
   			"unit": "$",
   			"type": "currency"
   		},
   		"policy_number": {
   			"source": "123456789",
   			"value": 123456789,
   			"type": "number"
   		}
   	},
   	"validations": [],
   	"validation_summary": {
   		"fields": 4,
   		"fields_present": 4,
   		"errors": 0,
   		"warnings": 0,
   		"skipped": 0
   	},
   	"download_url": "https://sensible-so-document-type-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/sensible/41775922-b9ac-4d2d-b1af-4292e68947a0/EXTRACTION/234b2afd-5165-4022-a41f-bd31ad89c3ff.pdf?AWSAccessKeyId=REDACTED&x-amz-security-token=REDACTED"
   }
```

 


(Optional) see how it works in the Sensible app
=====

   To see this example in the Sensible app:

   1. Navigate to [https://app.sensible.so/dashboard/?d=auto_insurance_quote_api_test](https://app.sensible.so/dashboard/?d=auto_insurance_quote_api_test).
   1. Click **Upload document** and upload the [example PDF](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf).
   2. Click the **anyco** config and visually examine the PDF (middle pane), config (left pane), and parsed document (right pane) you just ran in the previous code sample:
![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_config_1.png)

