---
title: "Advanced: Transform sections data"
hidden: true

---

The following example shows using computed fields to transform sections data. The example:

- Copies a policy number and name from the parent `fields` array  to each section using the Custom Computation method. The policy number and name are listed once in the document and are relevant to each extracted claim.  To access the parent array's scope from inside each section, the method uses data-structure traversal syntax (`../../`).  The example shows how to transform copied data, in this case by concatenating the copied fields. 
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
        /*  **** TRANSFORM SECTION DATA ***** */
        /* OPTION 1: use `pick_fields` to copy fields into each section
        then concatenate them */
        {
          "method": {
             /* output multiple fields with one jsonLogic rule */
            "id": "customComputationGroup",
            "jsonLogic": {
              /* copy the policy name and policy number from the parent `fields`
            array into each section in the `claims_sections` array */
              "pick_fields": [
                {
                  /* source context for the fields is 1 level up in data hierarchy 
                     so use traversal syntax, i.e. "../../.."*/
                  "var": "../"
                },
                [
                  // the IDs of the fields to output into this section
                  "_raw_policy_number",
                  "_raw_policy_name"
                ]
              ]
            }
          }
        },
        /* concatenate the fields copied into each section */
        {
          "id": "policy_num_and_name_syntax_option_1",
          "method": {
            "id": "concat",
            "delimiter": "_",
            "source_ids": [
              "_raw_policy_number",
              "_raw_policy_name"
            ]
          }
        },
        /* OPTION 2: test traversal syntax with `log`,
           then copy and concat fields' values into each section
        */
        {
          "id": "log_test",
          "method": {
            "id": "customComputation",
            "jsonLogic": {
              /*
          print the value for ../_raw_policy_name as a field using the
          "log" operator to ensure you're at the right traversal level
           */
              "log": [
                "testing traversal for policy number w/ output as field",
                {
                  "var": {
                    /* to evaluate tranversal syntax,
                          concatenate it first,
                          e.g., "cat" outputs 
                          "../_raw_policy_name.value" */
                    "cat": [
                      "../",
                      "_raw_policy_number.value"
                    ]
                  }
                }
              ]
            },
          }
        },
        {
          /* copy the policy name and policy number from the parent `fields`
            array into each section in the `claims_sections` array,
            and concatenate them w/ an underscore separator */
          "id": "policy_num_and_name_syntax_option_2",
          "method": {
            "id": "customComputation",
            "jsonLogic": {
              "cat": [
                {
                  /* print a log message and field value to Errors output
                     instead of fields output */
                  "log": [
                    "testing traversal for policy number, no field output",
                    {
                      "var": {
                        /* to evaluate tranversal syntax,
                          concatenate it first,
                          e.g., "cat" outputs 
                          "../_raw_policy_number.value" */
                        "cat": [
                          "../",
                          "_raw_policy_number.value"
                        ]
                      }
                    },
                  ]
                },
                "_",
                {
                  "var": {
                    "cat": [
                      "../",
                      "_raw_policy_name.value"
                    ]
                  }
                }
              ]
            }
          }
        },
      ],
      "computed_fields": [
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
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      },
      "policy_num_and_name_syntax_option_1": {
        "value": "5501234567_National Landscaping Solutions",
        "type": "string"
      },
      "log_test": {
        "value": 5501234567,
        "type": "number"
      },
      "policy_num_and_name_syntax_option_2": {
        "value": "5501234567_National Landscaping Solutions",
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
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      },
      "policy_num_and_name_syntax_option_1": {
        "value": "5501234567_National Landscaping Solutions",
        "type": "string"
      },
      "log_test": {
        "value": 5501234567,
        "type": "number"
      },
      "policy_num_and_name_syntax_option_2": {
        "value": "5501234567_National Landscaping Solutions",
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
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      },
      "policy_num_and_name_syntax_option_1": {
        "value": "5501234567_National Landscaping Solutions",
        "type": "string"
      },
      "log_test": {
        "value": 5501234567,
        "type": "number"
      },
      "policy_num_and_name_syntax_option_2": {
        "value": "5501234567_National Landscaping Solutions",
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
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      },
      "policy_num_and_name_syntax_option_1": {
        "value": "5501234567_National Landscaping Solutions",
        "type": "string"
      },
      "log_test": {
        "value": 5501234567,
        "type": "number"
      },
      "policy_num_and_name_syntax_option_2": {
        "value": "5501234567_National Landscaping Solutions",
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
      "_raw_policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      },
      "_raw_policy_name": {
        "type": "string",
        "value": "National Landscaping Solutions"
      },
      "policy_num_and_name_syntax_option_1": {
        "value": "5501234567_National Landscaping Solutions",
        "type": "string"
      },
      "log_test": {
        "value": 5501234567,
        "type": "number"
      },
      "policy_num_and_name_syntax_option_2": {
        "value": "5501234567_National Landscaping Solutions",
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
    "message": "testing traversal for policy number w/ output as field",
    "result": "5501234567",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number, no field output",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number w/ output as field",
    "result": "5501234567",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number, no field output",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number w/ output as field",
    "result": "5501234567",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number, no field output",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number w/ output as field",
    "result": "5501234567",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number, no field output",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number w/ output as field",
    "result": "5501234567",
    "field_id": "claims_sections.undefined"
  },
  {
    "type": "log",
    "message": "testing traversal for policy number, no field output",
    "result": "National Landscaping Solutions",
    "field_id": "claims_sections.undefined"
  }
]
```

