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

Common use cases include:

- **Cross-document validation**: Extract fields from a first document (for example, name and date of birth from a loan application), then pass them as `extra_data` into a subsequent extraction request for the loan applicant's bank statement. The config for the bank statement compares the `extra_data` values to the values in the bank statement and outputs Boolean values to indicate if the applicant's name and date of birth are consistent in both documents.
- **Incorporating external data**: After extracting a VIN from an auto insurance document, call a third-party lookup service and pass the result (for example, recorded mileage) back as `extra_data` in a follow-up request. The config uses `extraData` with `customComputation` to flag any discrepancy between the lookup value and what the document shows.

# Parameters

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter:

| key                | value       | description |
| :----------------- | :---------- | :---------- |
| id (**required**)  | `extraData` |             |
| key (**required**) | string      | Key to look up in the request's `extra_data` record. |

**Note:** if the request omits `extra_data`, if the record doesn't contain `key`, or if the value at `key` is explicitly `null`, Sensible returns null. These cases aren't distinguishable in the output.

# Examples

The following example uses `extra_data` to cross-check deductible amounts from a policy management system against a customer's GEICO auto insurance declarations page. The request supplies the system's expected deductibles; the config retrieves them with `extraData` and flags any mismatches using `customComputation`.

**Config**

```json
{
  "fields": [
    {
      "id": "collision_deductible",
      "type": "currency",
      "anchor": {
        "match": [
          { "text": "Coverages", "type": "startsWith" },
          { "text": "Collision", "type": "startsWith" }
        ]
      },
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "first" /* leftmost value = the Limits and/or Deductibles column */
      }
    },
    {
      "id": "comprehensive_deductible",
      "type": "currency",
      "anchor": {
        "match": [
          { "text": "Coverages", "type": "startsWith" },
          { "text": "Comprehensive", "type": "startsWith" }
        ]
      },
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "first"
      }
    }
  ],
  "computed_fields": [
    {
      /* pull expected values from the request's extra_data record */
      "id": "expected_collision_deductible",
      "method": { "id": "extraData", "key": "expected_collision_deductible" }
    },
    {
      "id": "expected_comprehensive_deductible",
      "method": { "id": "extraData", "key": "expected_comprehensive_deductible" }
    },
    {
      /* true if the document's deductible matches what the upstream system expects */
      "id": "collision_deductible_matches",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "==": [{ "var": "collision_deductible.value" }, { "var": "expected_collision_deductible.value" }]
        }
      }
    },
    {
      "id": "comprehensive_deductible_matches",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "==": [{ "var": "comprehensive_deductible.value" }, { "var": "expected_comprehensive_deductible.value" }]
        }
      }
    }
  ]
}
```

**Request**

To run this request, create a document type in the Sensible app and add a config to it using the preceding SenseML.

```bash
curl --location 'https://api.sensible.so/v0/extract_from_url/your_doc_type' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_API_KEY' \
--data '{
  "document_url": "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/extra_data.pdf",
  "extra_data": {
    "expected_collision_deductible": 500,
    "expected_comprehensive_deductible": 300
  }
}'
```

**Example document**

The example document is a GEICO auto insurance declarations page with collision ($500) and comprehensive ($250) deductibles.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/extra_data.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/extra_data.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------- |

**Output**

`collision_deductible_matches` is `true` because the document ($500) matches the expected value. `comprehensive_deductible_matches` is `false` because the document shows $250, not the expected $300.

```json
{
  "collision_deductible": { "value": 500, "type": "currency", "unit": "$", "source": "$500" },
  "comprehensive_deductible": { "value": 250, "type": "currency", "unit": "$", "source": "$250" },
  "expected_collision_deductible": { "value": 500, "type": "number" },
  "expected_comprehensive_deductible": { "value": 300, "type": "number" },
  "collision_deductible_matches": { "value": true, "type": "boolean" },
  "comprehensive_deductible_matches": { "value": false, "type": "boolean" }
}
```
