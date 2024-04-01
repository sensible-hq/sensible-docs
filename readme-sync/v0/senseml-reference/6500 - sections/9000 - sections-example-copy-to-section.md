---
title: "Advanced: Transform sections data"
hidden: false

---

The following example shows using computed fields to transform sections data. The example:

- Adds a policy number and name to each section using the Copy To Section method. The policy number and name are listed once in the document and are globally applicable to every extracted claim.  The example shows how to transform copied data, in this case by concatenating the copied fields. 
- Redacts a telephone number. The example uses the Custom Computation method to replace digits in the number, and the Suppress Output method to omit the complete number from the output.

**Config**

```json
{
  "fields": [
    {
      /* capture raw policy # to copy into 
      each claim using copy_to_section */
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
      each claim using copy_to_section */
      "id": "_raw_policy_name",
      "anchor": "policy name",
      "method": {
        "id": "row",
      }
    },
  ],
  /*
     each claim starts with "claim number" and ends with 
     "Date of claim" */
  "sections": [
    {
      "id": "claims_sections",
      "range": {
        "anchor": {
          "match": {
            "type": "includes",
            "text": "claim number"
          },
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
        }
      ],
      "computed_fields": [
        /* copy policy number and name from outside sections
         into each claim, and concatenate them */
        {
          "id": "copied_policy_number",
          "method": {
            "id": "copy_to_section",
            "source_id": "_raw_policy_number"
          }
        },
        {
          "id": "copied_policy_name",
          "method": {
            "id": "copy_to_section",
            "source_id": "_raw_policy_name"
          }
        },
        {
          "id": "policy_name_and_number",
          "method": {
            "id": "concat",
            "source_ids": [
              "copied_policy_name",
              "copied_policy_number"
            ]
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
                "replace": "***$1",
              }
            }
          }
        },
        {
          "id": "cleanup",
          "method": {
            "id": "suppressOutput",
            "source_ids": [
              "copied_policy_name",
              "copied_policy_number",
              "_raw_phone_number"
            ]
          }
        },
      ]
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/copy_to_section.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections.pdf) |
| ---------------------- | ------------------------------------------------------------ |

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
        "value": "National Landscaping Solutions 5501234567",
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
        "value": "National Landscaping Solutions 5501234567",
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
        "value": "National Landscaping Solutions 5501234567",
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
        "value": "National Landscaping Solutions 5501234567",
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
        "value": "National Landscaping Solutions 5501234567",
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
