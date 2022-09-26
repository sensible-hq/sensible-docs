---
title: "Validate extractions"
hidden: false
---

 

Quality control the data extractions in a document type by writing validations using  [JsonLogic](https://jsonlogic.com/). Test extracted fields using Boolean, logic, numeric, array, string, and other operations. Then write your own logic based on the validations, for example:

- pass a document extraction automatically through your pipeline if there are no errors and 10% of warning validations fail
- flag a document extraction for human review if 5% of error validations fail

Create validations
----

**Sensible app**

To create validations in the Sensible app:

1. Click the document type.
2. Click **Create validation**.
3. Enter the parameters for the validation.
4. Click **Create**.

**API**

To create validations using the Sensible API, send a request like the following:

```curl
curl --location --request PUT 'https://api.sensible.so/v0/document_types/<TYPE_ID>' \
--header 'Authorization: Bearer <YOUR_API_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{"schema":{"validations":[{"description":"example validation to test broker email format","condition":{"match":[{"var":"broker\\.email.value"},"^\\S+\\@\\S+$"]},"severity":"warning","fields":["test"]}]}} '
```

For more information, see the [API reference](https://docs.sensible.so/reference/update-document-type).




Parameters
====

A validation has the following parameters:

| id                         | value                         | notes                                                        |
| -------------------------- | ----------------------------- | ------------------------------------------------------------ |
| description (**required**) | string                        | A description of the test                                    |
| severity (**required**)    | `error`, `warning`, `skipped` | The severity of the failing test.                            |
| prerequisite fields        | array                         | Use this parameter to generate `skipped` error messages when optional extracted fields are null. For example, if a missing broker's email address doesn't greatly affect the quality of your extraction, then write a condition to verify `broker.email` is properly formatted, but specify [`"broker\\.email"`]  in this parameter to skip the verification if the email is null. For an example, see Validation 3 in the Examples section. <br/>Double escape any dots in the field keys (for example, `delivery\\.zip\\.code`). |
| condition (**required**)   | JsonLogic operation           | Tests extracted fields using Boolean, logic, numeric, array, string, and other operations. Supports all [JsonLogic operations](https://jsonlogic.com/operations.html)  and extends them with the following Sensible operations:<br/><br/>`{"exists":[JsonLogic]}`, most commonly used with the JsonLogic `var`  operation to test that an output value isn't null. The  `var` operation retrieves extracted field values using field `id` keys. <br/><br/>`{"match":[JsonLogic,"regex"]}`, where `regex` is a Javascript-flavored regular expression. For example, use a  regex match when you want to test that the output matches a [type](doc:types) that's not supported by Sensible.<br/>Double escape special characters, since the regex is in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). This operation does *not* support regular expression flags such as `i` for case insensitive. <br><br/> Double escape any dots in the field keys (for example, `delivery\\.zip\\.code`). |

Examples
====

Imagine you have a document type "sales_quotes" with configs for

- company_A
- company_B
- company_C

You test sales quote extractions from all the companies with the following validations:

Validation 1
---

- **Description**:  The quoted rate value isn't null
- **Severity**: error
- **Condition**:`{"exists":[{"var":"quote_rate.value"}]}`

**Notes**: Tests that a field  (`quote_rate`) isn't null using the Sensible `exists` operation.

Validation 2
---

- **Description**:  The quote duration is a round number
- **Severity**: warning
- **Condition**:`{"==":[{"%":[{"var":"quote_duration.value"},2]},0]}`

**Notes**:  Retrieves the value of an extracted `quote_duration` field using the JsonLogic `var` operation, then uses the JsonLogic [modulo operation (%)](https://jsonlogic.com/operations.html#%25/) to divide the rate by 2 and passes the test if the remainder equals (`"=="`) 0.

Validation 3
---

- **Description**:  Broker's email is in string@string format
- **Severity**: warning
- **Prerequisite fields**: `["broker\\.email"]`
- **Condition**: `{"match":[{"var":"broker\\.email.value"},"^\\S+\\@\\S+$"]}`   

**Notes**:  If `broker.email` isn't null, then uses a Sensible operation (`match`) to test that the email matches a regular expression. If `broker.email` is null, skips this condition.

Validation 4
----

- **Description**:  The zip code is valid for USA or CA

- **Severity**: warning

- **Condition**:
```json
{"or":[
  {"and":[
    {"==":[{"var":"country.value"},"US"]},
    {"match":[{ "var":"zip_code.value" },"^[0-9]{5}$"]}]},
  {"and":[
    {"==":[{"var":"country.value"},"CA"]},
    {"match":[{"var":"zip_code.value"},"^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$"]}]}
]} 
```

Notes:   Tests that the `zip_code` is a 5-digit number if the `country`  field equals USA, or 6 alphanumeric characters if the `country`  field equals Canada. Uses a Sensible operation (`match`) to test regular expressions.

Validations output
---

The following extraction excerpt shows validating test data with the preceding conditions: 

- **Validation 3**  Sensible skips the broker email because the prerequisite field  `broker.email` is null
- **Validation 4**  (zip code) fails because  `zip_code`  is 17 digits

```json
{
	"parsed_document": {
		"quote_rate": {
			"source": "$800",
			"value": 800,
			"unit": "$",
			"type": "currency"
		},
		"quote_duration": {
			"type": "number",
			"value": "6"
		},
		"broker.email": null,
		"country": {
			"type": "string",
			"value": "USA"
		},
		"zip_code": {
			"type": "number",
			"value": "12345678901234456"
		},
		"validations": [{
			"description": "Zip code must be valid",
			"severity": "warning"
		}, {
			"description": "Broker's email is in string@string format",
			"severity": "skipped",
			"message": "Missing prerequisites: broker.email"
		}],
		"validation_summary": {
			"fields": 5,
			"fields_present": 4,
			"errors": 0,
			"warnings": 1,
			"skipped": 1
		}
	}
}
```

Notes
====
Why does Sensible use validation tests rather than confidence intervals? Sensible's extractions are largely deterministic. With the exception of OCR-dependent output, a Sensible config always returns the same output for a given PDF input. Given this, deterministic validation tests are more useful than confidence intervals as measures of extraction quality. 



