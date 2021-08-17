---
title: "Validate extractions"
hidden: true
---

 

Quality control the data extractions in a document type by writing validation tests using  [JsonLogic](https://jsonlogic.com/).  Then write your own logic based on the tests, for example:

- pass a document extraction automatically through your pipeline if there are no errors and only 10% of warnings validations fail
- flag a document extraction for human review if 5% of error validations fail

To write validations in the Sensible app:

1. Click the document type.
2. Click **Create validation**.
3. Enter the parameters for the validation.
4. Click **Create**.

TODO: add screenshot when finalized.

Parameters
====

Each validation has the following parameters:

| id                         | value               | notes                                                        |
| -------------------------- | ------------------- | ------------------------------------------------------------ |
| description (**required**) | string              | A description of the test                                    |
| severity (**required**)    | `error`, `warning`  | The severity of the failing test                             |
| prerequisite fields        | array               | Skip the condition if these fields are null. For example, if a "Additional fees" section of a document is often left blank, then specify a prerequisite field in that section (e.g., [`"first\\.additional\\.fee"`])  in each validation for the section's fields. If the whole section is intentionally blank, you avoid meaningless errors and warnings for the section's fields.<br/>Double escape any dots in the keys (for example, `delivery\\.zip\\.code`). |
| condition (**required**)   | JsonLogic operation | Supports all [JsonLogic operations](https://jsonlogic.com/operations.html)  and extends them with the following Sensible operations:<br/><br/>`{ exists: [JsonLogic] }`, most commonly used with the JsonLogic `var`  operation to test that an output value is not null. The  `var` operation retrieves values from the  `parsed_document` object in the extraction using field `id` keys. <br/><br/>`{ match: [JsonLogic, regex] }`, where `regex` is a Javascript-flavored regular expression. For example, use this  regex match when you want to test that the output matches a [type](doc:types) that is not supported by Sensible.<br/>Double escape special characters, since the regex is contained in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). This operation does *not* support regular expression flags such as `i` for case insensitive. <br><br/> For all operations, double escape any dots in the extracted field keys (for example, `delivery\\.zip\\.code`). |

Examples
====

Imagine you have a document type "sales_quotes" with configs for

- company_A
- company_B
- company_C

You test sales quote extractions from all the companies with the following validations:

**Validation 1**

- **Description**:  The quote value is not null
- **Severity**: error
- **Condition**:`{"exists": [{"var": "rate.value" }] }`

Notes: Uses the Sensible `exists` operation to test that a field's output exists

**Validation 2**

- **Description**:  The quoted rate is a round number
- **Severity**: warning
- **Condition**:`{ "==": [{ "%": [{"var": "rate.value" }, 2] }, 0] }`

Notes:   Retrieves the value of an extracted `rate` field  using the JsonLogic `var` operation, then uses the JsonLogic [modulo operation (%)](https://jsonlogic.com/operations.html#%25/) to divide the rate by 2 and passes the test if the remainder equals (`"=="`) 0.

**Validation 3**

- **Description**:  Second broker's email is in `string@string` format
- **Severity**: warning
- **Prerequisite fields**: `["second\\.broker\\.name"]`
- **Condition**: `{"match": [{"var": "second\\.broker\\.email.value" }, {"^\\S+\\@\\S+$"}]}`

Notes:   If the box for a second broker contact is filled out, then uses a Sensible operation (`match`) to test that the second broker's email matches a regular expression. Otherwise, skips this condition.

**Validation 4**

- **Description**:  The zip code is valid for USA or CA

- **Severity**: warning

- **Condition**:
```json
{"or": [
  {"and": [
    {"==": [{"var": "country.value"}, "US"]},
    {"match": [{ "var": "zip_code.value" }, "^[0-9]{5}$"]} ] },
  {"and": [
    {"==": [{"var": "country.value"}, "CA"]},
    {"match": [{ "var": "zip_code.value" }, "^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$"]} ] }
]} 
```

Notes:   Tests that the `zip_code` is a 5-digit number if the `country`  field is USA, or 6 alphanumeric characters if the `country`  field is Canada. Uses a Sensible operation (`match`) to test regular expressions.

**Validation output**

For the preceding validations, here's an example extraction output in which:

- the " zip code is valid" test fails
- the "second broker email" test is skipped because the prerequisite field  `second\\.broker\\.name` is null

```json
{
	"id": "edeedb37-1c47-47d2-a64c-f355cf04835e",
	"created": "2021-07-05T20:50:56.390Z",
	"status": "COMPLETE",
	"type": "test_doc_type",
	"configuration": "anyco",
	"validations": [{
		"description": "Zip code must be valid",
		"severity": "warning"
	}],
	"parsed_document": {
		"rate": {
			"source": "$800",
			"value": 800,
			"unit": "$",
			"type": "currency"
		},
        "second.broker.name": null,
		"second.broker.email": null,
        "country": {
			"type": "string",
			"value": "USA"
		},
        "zip_code": {
			"type": "number",
			"value": "12345678901234456"
		}
	},
	"download_url": "https://sensible-so-document-type-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/edeedb37-1c47-47d2-a64c-f355cf04835e.pdf?AWSAccessKeyId=REDACTED&Expires=1625519233&Signature=REDACTEDD&x-amz-security-token=REDACTED"
}
```

**TODO:** if we add skipped validations to the array, add them in the above response

Notes
====
Why does Sensible use validation tests rather than confidence intervals? Sensible's extractions are largely deterministic: with the exception of OCR-dependent output, a Sensible config always returns the same output for a given PDF input. Given this, deterministic validation tests are more useful than confidence intervals as measures of extraction quality. 



