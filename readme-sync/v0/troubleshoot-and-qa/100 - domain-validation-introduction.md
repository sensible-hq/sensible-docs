---
title: "Testing introduction"
hidden: true
---

 

Quality control your data extractions by writing domain-specific validation tests using  [JsonLogic](https://jsonlogic.com/).  Then write your own logic based on the tests, for example:

- pass a document extraction automatically through your pipeline if there are no errors and only 10% of warnings validations fail
- flag a document extraction for human review if 5% of error validations fail



Parameters
====

| id                         | value               | notes                                                        |
| -------------------------- | ------------------- | ------------------------------------------------------------ |
| description (**required**) | string              | A description of the test                                    |
| condition (**required**)   | JsonLogic operation | Supports all [JsonLogic operations](https://jsonlogic.com/operations.html)  and extends them with the following Sensible operations:<br/> `{ match: [JsonLogic, string] }`, where `string` is a Javascript-flavored regular expression. Note you have to double escape characters, since the regex is contained in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). <br>`{ exists: [JsonLogic] }`, most commonly used with the JsonLogic `var`  operation to test that an output value is not null. The  `var` operation retrieves values from the  `parsed_document` object in the extraction using field `id` keys. Note that you must escape any dots in the keys (for example, `delivery\\.zip\\.code`). |
| severity (**required**)    | `error`, `warning`  | The severity of the failing test                             |

Examples
====

The following shows example validations:

```
validations: [
    {
      description: "Rate must be a round number",
      condition: { "==": [{ "%": [{ var: "rate.value" }, 2] }, 0] },
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
- The "Zip code must be valid" test uses a Sensible operation (`match`) to test if an extracted zip code value matches the regular expression `"^[0-9]{5}$"`.
- The "Required field broker_contact_name" test uses a Sensible operation (`exists`) to test that a `var`'s value is not null.

  

If all tests passed for a PDF except the "zip code must be valid" test, the extraction output could look something like this:

```json
{
	"id": "edeedb37-1c47-47d2-a64c-f355cf04835e",
	"created": "2021-07-05T20:50:56.390Z",
	"status": "COMPLETE",
	"type": "test_doc_type",
	"configuration": "anyco",
	"validations": [{
		"description": "Zip code must be valid",
		"severity": "error"
	}],
	"parsed_document": {
		"rate": {
			"source": "$800",
			"value": 800,
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



Notes
====
Why does Sensible use domain-specific validation rather than confidence intervals? Sensible's extractions are largely deterministic: with the exception of OCR-dependent output, a Sensible config always returns the same output for a given PDF input. Given this determinism, confidence intervals aren't very useful as a measure of extraction quality. Domain-specific validation tests are a more useful measure, because they allow you to test the output for a specific document type. 