---
title: Extra data
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: 'Access request-supplied extra data in configs'
  robots: index
next:
  description: ''
---
Returns a value from the `extra_data` record you supply in an asynchronous extraction request. Use this method to bring request-time context into a config's output so validations, postprocessors, and other computed fields can read it.

For information about attaching `extra_data` to a request, see the [Extract from URL](ref:extract-from-url) and [Generate upload URL](ref:generate-an-upload-url) endpoints.

<!-- TODO: add use cases section. Ideas:

  Chained extraction workflow:
  - Customer sends a loan application — Sensible extracts name, SSN, DOB
  - Script adds those three fields into the next API call as extra_data
  - Customer sends a bank statement — config uses extraData to pull name/DOB/SSN from the request
    and compares them against what's on the statement to check they match

  Combining with external data sources:
  - Customer parses an auto insurance document and extracts the VIN number
  - Customer makes an API call to a VIN lookup service and gets total mileage
  - Customer sends total mileage back as extra_data with another document
    and uses extraData + customComputation to verify the mileages match
-->

# Parameters

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter:

| key                | value       | description |
| :----------------- | :---------- | :---------- |
| id (**required**)  | `extraData` |             |
| key (**required**) | string      | Key to look up in the request's `extra_data` record. |

**Note:** if the request omits `extra_data`, if the record doesn't contain `key`, or if the value at `key` is explicitly `null`, Sensible returns null. These cases aren't distinguishable in the output.

# Examples

The following example uses `extra_data` to compare expected values from an upstream system against values Sensible extracts from the document. The request supplies expected premium and deductible amounts, and the config retrieves them with `extraData` then compares them to the extracted fields.

**Request body**

```json
{
  "document_url": "https://example.com/policy.pdf",
  "extra_data": {
    "expected_premium": 1250.00,
    "expected_deductible": 500
  }
}
```

**Config**

```json
{
  "fields": [
    {
      "id": "premium",
      "anchor": "total premium",
      "method": { "id": "row" }
    },
    {
      "id": "deductible",
      "anchor": "deductible",
      "method": { "id": "row" }
    }
  ],
  "computed_fields": [
    {
      "id": "expected_premium",
      "method": {
        "id": "extraData",
        "key": "expected_premium" // in extra_data: { "expected_premium": 1250.00, "expected_deductible": 500 }
      }
    },
    {
      "id": "expected_deductible",
      "method": {
        "id": "extraData",
        "key": "expected_deductible" // in extra_data: { "expected_premium": 1250.00, "expected_deductible": 500 }
      }
    },
    {
      "id": "premium_matches",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "==": [{ "var": "premium.value" }, { "var": "expected_premium.value" }]
        }
      }
    },
    {
      "id": "deductible_matches",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "==": [{ "var": "deductible.value" }, { "var": "expected_deductible.value" }]
        }
      }
    }
  ]
}
```

**Output**

```json
{
  "premium": { "value": 1250.00, "type": "number" },
  "deductible": { "value": 750, "type": "number" },
  "expected_premium": { "value": 1250.00, "type": "number" },
  "expected_deductible": { "value": 500, "type": "number" },
  "premium_matches": { "value": true, "type": "boolean" },
  "deductible_matches": { "value": false, "type": "boolean" }
}
```

<!-- TODO: replace this with a full worked example — real PDF document, screenshot, and actual output showing premium_matches: true and deductible_matches: false so readers can see the comparison in action -->
