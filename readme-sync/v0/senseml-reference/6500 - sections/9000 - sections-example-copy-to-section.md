---
title: "Advanced: Transform sections data"
hidden: false

---

The following example shows using the Copy To Field method to add a policy number and name, which are listed once in the document and which is globally applicable, to every extracted claim.  The example shows how to transform copied data, in this case by concatenating the copied fields. The example also shows how to transform data in the section, by redacting a phone number.

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
    {
      /* get monthly claims totals 
      with match all (simpler alternative to sections) */
      "id": "monthly_total_unprocessed_claims",
      "match": "all",
      "anchor": {
        "match": {
          "type": "includes",
          "text": "unprocessed claims:",
          "isCaseSensitive": true
        },
        "end": {
          "text": "total claims",
          "type": "startsWith"
        }
      },
      "method": {
        "id": "row",
        "position": "right",
        "includeAnchor": true
      }
    }
  ],
  /* get first 2 claims sections in doc.  
     each claim starts with "claim number" and ends with 
     "unprocessed claims" */
  "sections": [
    {
      "id": "unprocessed_sept_oct_claims_sections",
      "range": {
        "anchor": {
          "start": {
            "text": "September",
            "type": "startsWith",
            "isCaseSensitive": true
          },
          "match": {
            "type": "includes",
            "text": "claim number"
          },
          "end": {
            "type": "startsWith",
            "text": "November",
            "isCaseSensitive": true
          }
        },
        "stop": {
          "type": "includes",
          "text": "unprocessed claims:",
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
          "id": "phone_number",
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
      /* copy policy number and name from outside sections
         into each claim, and concatenate them */
      "computed_fields": [
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
        {
          "id": "cleanup",
          "method": {
            "id": "suppressOutput",
            "source_ids": [
              "copied_policy_name",
              "copied_policy_number"
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
  "monthly_total_unprocessed_claims": [
    {
      "type": "string",
      "value": "Sept unprocessed claims: 2"
    },
    {
      "type": "string",
      "value": "Oct unprocessed claims: 1"
    },
    {
      "type": "string",
      "value": "Nov unprocessed claims: 2"
    }
  ],
  "unprocessed_sept_oct_claims_sections": [
    {
      "claim_number": {
        "source": "1223456789",
        "value": 1223456789,
        "type": "number"
      },
      "phone_number": {
        "type": "phoneNumber",
        "source": "512 409 8765",
        "value": "+15124098765"
      },
      "policy_name_and_number": {
        "value": "National Landscaping Solutions 5501234567",
        "type": "string"
      }
    },
    {
      "claim_number": {
        "source": "9876543211",
        "value": 9876543211,
        "type": "number"
      },
      "phone_number": null,
      "policy_name_and_number": {
        "value": "National Landscaping Solutions 5501234567",
        "type": "string"
      }
    },
    {
      "claim_number": {
        "source": "6785439210",
        "value": 6785439210,
        "type": "number"
      },
      "phone_number": {
        "type": "phoneNumber",
        "source": "505 238 8765",
        "value": "+15052388765"
      },
      "policy_name_and_number": {
        "value": "National Landscaping Solutions 5501234567",
        "type": "string"
      }
    }
  ]
}
```
