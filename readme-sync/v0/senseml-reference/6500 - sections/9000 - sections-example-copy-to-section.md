---
title: "Advanced: Transform sections data"
hidden: false
---

The following example shows using computed fields to transform sections data. The example:

- Copies a policy number and name from the parent `fields` object to each section using the Custom Computation method. The policy number and name are listed once in the document and are relevant to each extracted claim. To access the parent object's scope from inside each section, the method uses data-structure traversal syntax (`../`). The example shows how to transform copied data, in this case by concatenating the copied fields.
- Redacts a telephone number. The example uses the Custom Computation method to replace digits in the number, and the Suppress Output method to omit the complete number from the output.

**Config**

```json
{
  "fields": [
    {
      /* capture raw policy # to copy into 
      each claim  */
      "id": "_raw_policy_number",
      "type": "number",
      "anchor": "policy number",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      /* capture raw policy name to copy into 
      each claim  */
      "id": "_raw_policy_name",
      "anchor": "policy name",
      "method": {
        "id": "row"
      }
    },
    /*    each claim starts with "claim number" and ends with 
     "Date of claim" */
    {
      "id": "claims_sections",
      "type": "sections",
      "range": {
        "anchor": {
          "match": {
            "type": "includes",
            "text": "claim number"
          }
        },
        "stop": {
          "type": "includes",
          "text": "Date of claim",
          "isCaseSensitive": true
        }
      },
      /* return each claim as object containing claim # 
      and phone # fields */
      "fields": [
        {
          "id": "claim_number",
          "type": "number",
          "anchor": {
            "match": {
              "type": "startsWith",
              "text": "Claim number:",
              "isCaseSensitive": true
            }
          },
          "method": {
            "id": "label",
            "position": "right"
          }
        },
        {
          "id": "_raw_phone_number",
          "type": "phoneNumber",
          "anchor": {
            "match": {
              "type": "includes",
              "text": "Phone number",
              "isCaseSensitive": true
            }
          },
          "method": {
            "id": "row",
            "position": "right"
          }
        },
        {
          /* to access the `_raw_policy_number` and `_raw_policy_name`
          fields from inside the `claims_sections field`, use ../ syntax
          to traverse levels of scope in the JSON output.
          e.g., use ../_raw_policy_name since it's in the parent object, one level above the "claims_sections" array */

          /* as an alternative to this syntax, see the copy_to_section method */
          "id": "policy_name_and_number",
          "method": {
            "id": "customComputation",
            "jsonLogic": {
              /* concat the policy name + number w/ an underscore separator */
              "cat": [
                {
                  /* print a log message and field value to Errors output
                  to verify what gets returned by the logged rule */
                  "log": [
                    "testing traversal for policy name",
                    {
                      "var": "../_raw_policy_name.value"
                    }
                  ]
                },
                "_",
                {
                  "var": "../_raw_policy_number.value"
                }
              ]
            }
          }
        },
        /* redact the phone number using Custom Computation method's regex replace operation */
        {
          "id": "redacted_phone_number",
          "method": {
            "id": "customComputation",
            "jsonLogic": {
              "replace": {
                "source": {
                  "var": "_raw_phone_number.value"
                },
                "find_regex": "^.*(\\d{4})$",
                "replace": "***$1"
              }
            }
          }
        },
        {
          "id": "cleanup",
          "method": {
            "id": "suppressOutput",
            "source_ids": [
              "_raw_phone_number"
            ]
          }
        }
      ]
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/copy_to_section.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "_raw_policy_number": {
    "source": "5501234567",
    "value": 5501234567,
    "type": "number"
  },
  "_raw_policy_name": {
    "type": "string",
    "value": "National Landscaping Solutions"
  },
  "claims_sections": [
    {
      "claim_number": {
        "source": "1223456789",
        "value": 1223456789,
        "type": "number"
      },
      "policy_name_and_number": {
        "value": "National Landscaping Solutions_5501234567",
        "type": "string"
      },
      "redacted_phone_number": {
        "value": "***8765",
        "type": "string"
      }
    },
    {
      "claim_number": {
        "source": "9876543211",
        "value": 9876543211,
        "type": "number"
      },
      "policy_name_and_number": {
        "value": "National Landscaping Solutions_5501234567",
        "type": "string"
      },
      "redacted_phone_number": {
        "value": "null",
        "type": "string"
      }
    },
    {
      "claim_number": {
        "source": "6785439210",
        "value": 6785439210,
        "type": "number"
      },
      "policy_name_and_number": {
        "value": "National Landscaping Solutions_5501234567",
        "type": "string"
      },
      "redacted_phone_number": {
        "value": "***8765",
        "type": "string"
      }
    },
    {
      "claim_number": {
        "source": "7235439210",
        "value": 7235439210,
        "type": "number"
      },
      "policy_name_and_number": {
        "value": "National Landscaping Solutions_5501234567",
        "type": "string"
      },
      "redacted_phone_number": {
        "value": "***8344",
        "type": "string"
      }
    },
    {
      "claim_number": {
        "source": "8235439211",
        "value": 8235439211,
        "type": "number"
      },
      "policy_name_and_number": {
        "value": "National Landscaping Solutions_5501234567",
        "type": "string"
      },
      "redacted_phone_number": {
        "value": "***9856",
        "type": "string"
      }
    }
  ]
}
```

And the `errors` output for the log operations is as follows:

```json
[
  {
    "type": "log",
    "message": "testing traversal for policy name",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy name",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy name",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy name",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy name",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  }
]
```
