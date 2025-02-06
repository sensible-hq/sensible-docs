---
title: "Custom computation group"
hidden: false
---

Define your own [computed field method](doc:computed-field-methods) using [JsonLogic](doc:jsonlogic). Can return multiple fields.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                             | description                                                  |
| :----------------------- | :-------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `customComputationGroup`          | This method has access to the  `parsed_document` object at [verbosity](doc:verbosity) = 0. |
| jsonLogic (**required**) | JsonLogic object | Transforms the output of one or more [Field objects](https://docs.sensible.so/docs/field-query-object) using [JsonLogic operations](doc:jsonlogic). Expects to output an object as the result of the JsonLogic operations. Converts the attributes of the output object to fields. |

Examples
====

The following example shows using the Custom Computation Group method in combination with the Pick Values operator to copy fields from the parent `fields` object into sections.

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
        "id": "row",
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
          },
        },
        "stop": {
          "type": "includes",
          "text": "Date of claim",
          "isCaseSensitive": true
        }
      },
      /* return each claim as object containing claim # 
      and other fields */
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
        
        /* to access the `_raw_policy_number` field from
          inside the `claims_sections field`, use
          ../../ syntax to traverse levels of scope in the
          JSON output. e.g., use
          ../_raw_policy_name since it's in a parent array
          */
        /* as an alternative to this syntax, see the copy_to_section method */
        
        {
          "method": {
            /* use the custom computation group to output multiple fields */
            "id": "customComputationGroup",
            "jsonLogic": {
              /* copies the specified fields from the parent object
                 to each section */
              "pick_fields": [
                {
                  "var": "../"
                },
                [
                  "_raw_policy_number",
                  "_raw_policy_name"
                ]
              ]
              }
            }
          }
    
        ]
    }
    ]
  }
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections.pdf) |
| ---------------- | ------------------------------------------------------------ |

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
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      }
    },
    {
      "claim_number": {
        "source": "9876543211",
        "value": 9876543211,
        "type": "number"
      },
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      }
    },
    {
      "claim_number": {
        "source": "6785439210",
        "value": 6785439210,
        "type": "number"
      },
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      }
    },
    {
      "claim_number": {
        "source": "7235439210",
        "value": 7235439210,
        "type": "number"
      },
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      }
    },
    {
      "claim_number": {
        "source": "8235439211",
        "value": 8235439211,
        "type": "number"
      },
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      }
    }
  ]
}
```
