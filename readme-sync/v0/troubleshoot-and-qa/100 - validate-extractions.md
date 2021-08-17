---
title: "Validate extractions"
hidden: true
---

 

Quality control the data extractions in a document type by writing validation tests using  [JsonLogic](https://jsonlogic.com/).  Then write your own logic based on the tests, for example:

- pass a document extraction automatically through your pipeline if there are no errors and only 10% of warnings validations fail
- flag a document extraction for human review if 5% of error validations fail

TODO: iron out: Write validations in the Sensible app:

1. Click the document type Settings
2. For each extracted field that you want to validate, click the plus sign.

Parameters
====

Each validation test you write has the following parameters:

| id                         | value               | notes                                                        |
| -------------------------- | ------------------- | ------------------------------------------------------------ |
| description (**required**) | string              | A description of the test                                    |
| Prerequisite fields        | array               | Skip the condition if these fields are null. For example, if a "Additional fees" section of a document is often left blank, then specify a prerequisite field in that section (e.g., [`"first\\.additional\\.fee"`])  in each validation for each field in the section. If the whole section is intentionally blank, you avoid meaningless errors and warnings for the section's fields.<br/>Double escape any dots in the keys (for example, `delivery\\.zip\\.code`). |
| condition (**required**)   | JsonLogic operation | Supports all [JsonLogic operations](https://jsonlogic.com/operations.html)  and extends them with the following Sensible operations:<br/><br/>`{ exists: [JsonLogic] }`, most commonly used with the JsonLogic `var`  operation to test that an output value is not null. The  `var` operation retrieves values from the  `parsed_document` object in the extraction using field `id` keys. `{ match: [JsonLogic, regex] }`, where `regex` is a Javascript-flavored regular expression. For example, use this  regex match when you want to test that the output is a [type](doc:types) that is not supported by Sensible.<br/><br/>Double escape special characters, since the regex is contained in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). This operation does *not* support regular expression flags such as `i` for case insensitive. <br><br/><br/>Double escape any dots in the keys (for example, `delivery\\.zip\\.code`). |
| severity (**required**)    | `error`, `warning`  | The severity of the failing test                             |

Examples
====

Imagine you have a document type "sales_quotes" with configs for

- company_A
- company_B
- company_C

For all companies, you test that the sales quote extraction is valid with the following conditions:

| Description                                        | Prerequisite fields | Condition                                                    | Severity | Notes                                                        |
| -------------------------------------------------- | ------------------- | ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
| The quote value is not null                        |                     | `{ exists: [{ var: "rate.value" }] }`                        | error    | Uses the Sensible `exists` operation to test that a field's output exists. |
| The quoted rate is a round number                  |                     | `{ "==": [{ "%": [{ var: "rate.value" }, 2] }, 0] }`         | warning  | Retrieves the value of an extracted `rate` field  using the JsonLogic `var` operation, then uses the JsonLogic [modulo operation (%)](https://jsonlogic.com/operations.html#%25/) to divide the rate by 2 and passes the test if the remainder equals (`"=="`) 0. |
| Second broker's email is in `string@string` format | broker2.name        | `match: [{ var: "broker2\\.email.value" }, "^?\\S+\\@\\S+$"]` | warning  | If the box for a second broker contact is filled out, then uses a Sensible operation (`match`) to test that the second broker's email matches a regular expression. Otherwise, skips this condition. |
| The zip code is valid for USA or CA                |                     | `{"or": [`<br/>   `{"and": [`<br/>      `{"==": [{"var": "country.value"}, "US"]},`<br/>      `{"match": [{ "var": "zip_code.value" }, "^[0-9]{5}$"]} ] },`<br/> `{"and": [`<br/>    ` {"==": [{"var": "country.value"}, "CA"]},`<br/>    `{"match": [{ "var": "zip_code.value" }, "^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$"]} ] }`<br/>`]}` | warning  | Tests if the zip code is a 5-digit number if the country is USA, or 6 alphanumeric characters if the country  is Canada. Uses a Sensible operation (`match`) to test regular expressions. |

For the preceding conditions, here's an example extraction output in which:

- the "zip code must be valid" test fails
- the "second broker phone" test is skipped because the second.broker.name field doesn't exist

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
Why does Sensible use validation tests rather than confidence intervals? Sensible's extractions are largely deterministic: with the exception of OCR-dependent output, a Sensible config always returns the same output for a given PDF input. Given this, deterministic validation tests are more useful than confidence intervals as measures of extraction quality. 



