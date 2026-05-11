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
Returns a value from the `extra_data` object you supply in an asynchronous extraction request. Use this method to bring request-time context into a config's output so validations, postprocessors, and other computed fields can read it.

For information about attaching `extra_data` to a request, see the [Extract from URL](ref:extract-from-url) and [Generate upload URL](ref:generate-an-upload-url) endpoints.

Common use cases include:

- **Cross-document validation**: Extract fields from a first document (for example, name and date of birth from a loan application), then pass them as `extra_data` into a subsequent extraction request for the loan applicant's bank statement. The config for the bank statement compares the `extra_data` values to the values in the bank statement and outputs Boolean values to indicate if the applicant's name and date of birth are consistent in both documents.
- **Incorporating external data**: After extracting a VIN from an auto insurance document, call a third-party lookup service and pass the result (for example, recorded mileage) back as `extra_data` in a follow-up request. The config uses `extraData` with `customComputation` to flag any discrepancy between the lookup value and what the document shows.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/extra_data_overview.png)

# Parameters

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter:

| key                | value       | description |
| :----------------- | :---------- | :---------- |
| id (**required**)  | `extraData` |             |
| key (**required**) | string      | Key to look up in the request's `extra_data` object. |

**Note:** if the request omits `extra_data`, if the object doesn't contain `key`, or if the value at `key` is explicitly `null`, Sensible returns null. These cases aren't distinguishable in the output.

**Note:** The `extra_data` object has the following constraints:
- Values must be flat: strings, numbers, booleans, or null. Nested objects and arrays are not supported.
- The object has a maximum size of 16 KiB.

# Examples

The following example uses `extra_data` to cross-check values from a policy management system against a GEICO auto insurance declarations page. Numeric values (deductibles) use `customComputation` for exact equality comparison. A vehicle description uses `queryGroup` with `source_ids` for a semantic comparison that handles format differences between systems. For example, `"NISSAN ROGUE 2010"` (policy system) matches `"2010 Nissan Rogue"` (document) even though the strings aren't equal.

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
        "tiebreaker": "first" /* leftmost value = the Limits and/or Deductibles column */
      }
    },
    {
      "id": "expected_insured_vehicle", /* in fields (not computed_fields) so source_ids can reference it below */
      "method": { "id": "extraData", "key": "expected_insured_vehicle" }
    },
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "insured_vehicle",
            "description": "year, make, and model of the first vehicle listed on the policy",
            "type": "string"
          }
        ]
      }
    },
    {
      "method": {
        "id": "queryGroup",
        "source_ids": ["expected_insured_vehicle", "insured_vehicle"], /* gives the LLM both values as context for a semantic comparison */
        "queries": [
          {
            "id": "vehicle_matches",
            "description": "Do these two vehicle descriptions refer to the same vehicle? Ignore differences in capitalization and word order. Answer true or false.",
            "type": "boolean"
          }
        ]
      }
    }
  ],
  "computed_fields": [
    {
      "id": "expected_collision_deductible", /* pulled from the request's extra_data object */
      "method": { "id": "extraData", "key": "expected_collision_deductible" }
    },
    {
      "id": "expected_comprehensive_deductible", /* pulled from the request's extra_data object */
      "method": { "id": "extraData", "key": "expected_comprehensive_deductible" }
    },
    {
      "id": "collision_deductible_matches", /* true if the document's deductible matches what the upstream system expects */
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "==": [{ "var": "collision_deductible.value" }, { "var": "expected_collision_deductible.value" }]
        }
      }
    },
    {
      "id": "comprehensive_deductible_matches", /* true if the document's deductible matches what the upstream system expects */
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

To run this request, create a document type in the Sensible app and add a config to it using the preceding SenseML, then run the following command in a terminal:

```bash
curl --location 'https://api.sensible.so/v0/extract_from_url/your_doc_type' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_API_KEY' \
--data '{
  "document_url": "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/extra_data.pdf",
  "extra_data": {
    "expected_collision_deductible": 500,
    "expected_comprehensive_deductible": 300,
    "expected_insured_vehicle": "NISSAN ROGUE 2010"
  }
}'
```

**Example document**

The example document is a GEICO auto insurance declarations page with collision ($500) and comprehensive ($250) deductibles, and a 2010 Nissan Rogue as the first listed vehicle.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/extra_data.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/extra_data.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------- |

**Output**

`vehicle_matches` is `true` even though `"NISSAN ROGUE 2010"` (policy system) doesn't equal `"2010 Nissan Rogue"` (document). The LLM recognizes they refer to the same vehicle. `collision_deductible_matches` is `true` because the deductible ($500) matches the expected value. `comprehensive_deductible_matches` is `false` because the document shows $250, not the expected $300.

```json
{
  "collision_deductible": { "value": 500, "type": "currency", "unit": "$", "source": "$500" },
  "comprehensive_deductible": { "value": 250, "type": "currency", "unit": "$", "source": "$250" },
  "expected_insured_vehicle": { "value": "NISSAN ROGUE 2010", "type": "string" },
  "insured_vehicle": { "value": "2010 Nissan Rogue", "type": "string" },
  "vehicle_matches": { "value": true, "type": "boolean" },
  "expected_collision_deductible": { "value": 500, "type": "number" },
  "expected_comprehensive_deductible": { "value": 300, "type": "number" },
  "collision_deductible_matches": { "value": true, "type": "boolean" },
  "comprehensive_deductible_matches": { "value": false, "type": "boolean" }
}
```

# Portfolio extractions

When you submit a portfolio extraction with `extra_data`, Sensible passes the same object to every document extracted from the portfolio. Each document's config can access any value in the object using `extraData`. You don't need to pass separate objects per document type.

For example, if a portfolio contains an auto insurance declarations page and a loan application, both configs can independently read the same `extra_data` values and produce their own computed fields based on them.

For information about the portfolio endpoints, see [Provide a download URL for a PDF portfolio](ref:provide-a-download-url-for-a-pdf-portfolio) and [Generate an upload URL for a PDF portfolio](ref:generate-an-upload-url-for-a-pdf-portfolio).
