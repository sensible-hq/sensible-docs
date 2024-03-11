---
title: "Validating extractions"
hidden: false
---

 

Quality control the data extractions in a document type by writing validations using  [JsonLogic](https://jsonlogic.com/):

- Test extracted fields using Boolean, logic, numeric, array, string, and other operations.
- If Sensible extracted a field from OCR'd text,  test the confidence score for the field's anchor and value as a measure of the quality of the text images. For example, test that text in a scanned document isn't blurry or illegible.

Then write your own logic based on the validations, for example:

- pass a document extraction automatically through your pipeline if there are no errors and 10% of warning validations fail
- flag a document extraction for human review if 5% of error validations fail

Sensible uses validation errors to calculate [coverage](doc:metrics) for an extraction.

Create validations
----

**Sensible app**

To create validations in the Sensible app:

1. Click the document type.
2. Click **Create validation**.
3. Enter the parameters for the validation.
4. Click **Create**.


Parameters
====

A validation has the following parameters:

| id                         | value                         | notes                                                        |
| -------------------------- | ----------------------------- | ------------------------------------------------------------ |
| description (**required**) | string                        | A description of the test                                    |
| severity (**required**)    | `error`, `warning`, `skipped` | The severity of the failing test.                            |
| prerequisite fields        | array                         | Use this parameter to generate `skipped` error messages when optional extracted fields are null. For example, if a missing broker's email address doesn't greatly affect the quality of your extraction, then write a condition to verify `broker.email` is properly formatted, but specify [`"broker\\.email"`]  in this parameter to skip the verification if the email is null. For an example, see Validation 3 in the Examples section. <br/>Double escape any dots in the field keys (for example, `delivery\\.zip\\.code`). |
| condition (**required**)   | JsonLogic object              | Tests extracted fields using Boolean, logic, numeric, array, string, and other operations. Supports all [JsonLogic operations](https://jsonlogic.com/operations.html)  and extends them with Sensible operations. For the list of Sensible operations, and for more information about syntax, see the [Custom Computation](doc:custom-computation) method. |

Examples
====

Say that you have a document type for scanned sales quotes, called "sales_quotes", with configs for

- company_A
- company_B
- company_C

You test sales quote extractions from all the companies with the following validations:

Validation 1
---

- **Description**:  If OCR'd, the source text for quoted rate value is a high-quality, unblurred image.
- **Severity**: warning
- **Condition**:
```json
{"or":[
  {"!":[
    {"exists":{"var":"quote_rate.valueConfidence"}}]},
  {"and":[
    {">=": [{"var":"quote_rate.valueConfidence"},"0.90"]},
    {">=": [{"var":"quote_rate.anchorConfidence"},"0.90"]}]}
]} 
```

**Notes**: Since some sales quotes for `company_A` are scanned documents, check if the field came from OCR'd text. If it was OCR'd (confidence score is not null), then test that it has a high OCR confidence score for both the anchor text and the extracted value text. This validation requires that you set a high [verbosity setting](doc:verbosity) in the SenseML configuration.


Validation 2
---

- **Description**:  The quoted rate value isn't null

- **Severity**: error

- **Condition**:

```{"exists":[{"var":"quote_rate.value"}]}```

**Notes**: Tests that a field  (`quote_rate`) isn't null using the Sensible `exists` operation.

Validation 3
---

- **Description**:  The quote duration is a round number
- **Severity**: warning
- **Condition**:`{"==":[{"%":[{"var":"quote_duration.value"},2]},0]}`

**Notes**:  Retrieves the value of an extracted `quote_duration` field using the JsonLogic `var` operation, then uses the JsonLogic [modulo operation (%)](https://jsonlogic.com/operations.html#%25/) to divide the rate by 2 and passes the test if the remainder equals (`"=="`) 0.

Validation 4
---

- **Description**:  Broker's email is in string@string format
- **Severity**: warning
- **Prerequisite fields**: `["broker\\.email"]`
- **Condition**: `{"match":[{"var":"broker\\.email.value"},"^\\S+\\@\\S+$"]}`   

**Notes**:  If `broker.email` isn't null, then uses a Sensible operation (`match`) to test that the email matches a regular expression. If `broker.email` is null, skips this condition.

Validation 5
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

For example output of the preceding conditions, see the following extraction excerpt and validation output: 

**Extraction excerpt**

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
		}
}
```

**Validations output**

For the preceding extraction excerpt, Sensible outputs the following validations:
- **Validation 4**:  Sensible skips the broker email because the prerequisite field  `broker.email` is null

- **Validation 5**:  fails because  `zip_code`  is 17 digits

```json
{        
       "validations": [{
			"description": "The zip code is valid for USA or CA",
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

​	

