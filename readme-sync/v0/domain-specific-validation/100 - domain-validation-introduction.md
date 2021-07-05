---
title: "Domain validation introduction"
hidden: true
---

 

Quality control your data extractions by writing document-specific validation tests in  [JsonLogic](https://jsonlogic.com/).  Sensible's extractions are largely deterministic:  with the exception of OCR-dependent output, a Sensible config always returns the same output for a given PDF input. Given this determinism, confidence intervals don't make much sense as a measure of extraction quality. Instead, write tests to quantify your extraction quality. Then write your own logic based on the tests, for example:

- Pass a PDF extraction automatically through your pipeline if there are no errors and only 10% of warnings validations fail
- Flag a PDF extraction for human review if 5% of error validations fail



Parameters
====

| id                         | value               | notes                                                        |
| -------------------------- | ------------------- | ------------------------------------------------------------ |
| description (**required**) | string              | a description of the test                                    |
| condition (**required**)   | JsonLogic operation | Supports all [JsonLogic operations](https://jsonlogic.com/operations.html)  and extends them with the following Sensible operations:<br/> `{ match: [JsonLogic, string] }`, where `string` is a Javascript-flavored, JSON-escaped regular expression.<br>`{ exists: [JsonLogic] }`, most commonly used with the JsonLogic `var`  operation to test that an output value is not null.<br/>Note that a commonly used JsonLogic operation, `var`, extracts values from the `parsed_document` field in the extraction using a field `id` key. You must escape any dots in the key (for example, `delivery\\.zip\\.code`). |
| severity (**required**)    | `error`, `warning`  | The severity of the failing test                             |

Examples
====

The following shows example validations:

```
validations: [
    {
      description: "Rate must be a round number",
      condition: { "==": [{ "%": [{ var: "rate.value" }, 100] }, 0] },
      severity: "warning",
    },
    {
      description: "Zip code must be valid",
      condition: {
        match: [{ var: "delivery\\.zip\\.code.0.value" }, "^[0-9]{5}$"],
      },
      severity: "error",
    },
    {
      description: "Required field rate",
      condition: { exists: [{ var: "rate" }] },
      severity: "error",
    },
    {
      description: "Required field broker_contact_name",
      condition: { exists: [{ var: "broker_contact_name" }] },
      severity: "error",
    },

  ],
};
```

In the preceding example: 

- The "Rate must be a round number" test retrieves the value of an extracted `rate` key/value pair using the JsonLogic `var` operation, then uses the JsonLogic [modulo operation (%)](https://jsonlogic.com/operations.html#%25/) to divide the rate by 100, and passes the test if the remainder equals (`"=="`) 0. 
- The "Zip code must be valid" test uses a Sensible-specific operation (`match`) to test if an extracted zip code value matches the regular expression `"^[0-9]{5}$"`.
- The "Required field broker_contact_name" test uses a Sensible-specific operation (`exists`) to test that a `var`'s value is not null.

  

If all tests passed for a PDF except the "zip code must be valid" test, the extraction output could look something like this:

```json
{
	"id": "edeedb37-1c47-47d2-a64c-f355cf04835e",
	"created": "2021-07-05T20:50:56.390Z",
	"status": "COMPLETE",
	"type": "auto_insurance_quote",
	"configuration": "anyco",
	"validations": [{
		"description": "Zip code must be valid",
		"severity": "error"
	}],
	"parsed_document": {
		"rate": {
			"source": "$200",
			"value": 200,
			"unit": "$",
			"type": "currency"
		},
		"delivery.zip.code": {
			"type": "string",
			"value": "9876543214985192873698450"
		},

		"broker_contact_name": {
			"type": "string",
			"value": "Z. Abubakar"
		}
	},
	"download_url": "https://sensible-so-document-type-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/edeedb37-1c47-47d2-a64c-f355cf04835e.pdf?AWSAccessKeyId=REDACTED&Expires=1625519233&Signature=REDACTEDD&x-amz-security-token=REDACTED"
}
```



