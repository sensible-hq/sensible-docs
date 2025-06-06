---
title: "Conditional execution"
hidden: false
---

Use the Conditional method to handle [document variations](doc:document-variations) in a document type. This method extracts alternate sets of fields, depending on whether a [JsonLogic](doc:jsonlogic) condition passes or fails. For example, you want to extract data from two affiliate banks' statements. The statements' layouts are so similar that you can reuse 90 percent of your SenseML queries to handle both. Rather than authoring two separate configs, you can handle the remaining 10 percent  with conditional field execution. 

The following simplified code snippet shows an overview of the Conditional method: 

```json
id: conditional
condition: JsonLogic # condition about already extracted fields. must output a boolean 
fieldsOnPass: [] # fields to extract if the boolean is true
fieldsOnFail: [] # fields to extract if the boolean is false
```

## Parameters

| key                          | value                                     | description                                                  |
| ---------------------------- | ----------------------------------------- | ------------------------------------------------------------ |
| id (**required**)            | `conditional`                             | Specifies that this field extracts alternate lists of fields based on a pass/fail condition. You can nest conditions inside conditions to any depth. Fields can [fall back](doc:fallbacks) across conditions at any depth. For example, a `checking_transactions` field can fall back from a nested condition to a `checking_transactions` field in the top-level `fields` object, and vice versa. |
| condition (**required**)     | [JsonLogic](doc:jsonlogic)                | A logical condition that must output a Boolean. The condition passes if it outputs true and fails if it outputs false. For example, you can test if an extracted field is non-null, and extract alternate sets of fields depending on its presence. |
| fieldsOnPass  (**required**) | array of [fields](doc:field-query-object) | Specifies a list of fields to extract if the condition passes. |
| fieldsOnFail                 | array of [fields](doc:field-query-object) | Specifies a list of fields to extract if the condition fails. |

## Examples

The following example shows using conditional execution to standardize output across two similar banks. Bank A lists deposits and withdrawals separately in statements, and bank B combines them in a transactions table.  The example transforms Bank B's output so it's consistent with Bank A.

**Config**

```json
{
  "fields": [
    {
      /* no matter which bank authored the statement, always attempt to extract a transactions table */
      "id": "transaction_history",
      "anchor": "transaction history",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 3,
        "columns": [
          {
            "id": "date",
            "index": 0
          },
          {
            "id": "description",
            "index": 1
          },
          {
            "id": "amount",
            "index": 2
          }
        ]
      }
    },
    {
      "method": {
        "id": "conditional",
        "condition": {
          "exists": {
            /* if Sensible successfully extracted the transaction_history table 
            (i.e. it's non-null),
            the document is a statement from Sensible Bank */
            "var": "transaction_history"
          }
        },
        "fieldsOnPass": [
          /* if it's a statement from Sensible Bank, 
             split the extracted transactions table up into deposits and withdrawals 
             for consistency with bank statements from Practical Bank */
          {
            "id": "_deposits",
            "method": {
              "id": "list",
              /* source_ids prompts the LLM to extract the list from
                 an extracted field, transaction_history */
              "source_ids": [
                "transaction_history"
              ],
              "description": "deposits",
              "properties": [
                {
                  "id": "date",
                  "description": "date",
                  "type": "string"
                },
                {
                  "id": "description",
                  "description": "description",
                  "type": "string"
                },
                {
                  "id": "amount",
                  "description": "amount",
                  "type": "string"
                }
              ]
            }
          },
          {
            "id": "_withdrawals",
            "method": {
              "id": "list",
              "source_ids": [
                "transaction_history"
              ],
              "description": "withdrawals. ",
              "properties": [
                {
                  "id": "date",
                  "description": "date",
                  "type": "string"
                },
                {
                  "id": "description",
                  "description": "description",
                  "type": "string"
                },
                {
                  "id": "amount",
                  "description": "amount. if the withdrawal amount is denoted with paratheses, reformat it to a negative sign, ie, change (45.56) to -45.56",
                  "type": "string"
                }
              ]
            }
          }
        ],
        "fieldsOnFail": [
          /* if transactions table is null, the statement is from Practical Bank;
          extract the deposits and withdrawals tables as-is from the document */
          {
            "id": "_deposits",
            "method": {
              "id": "list",
              "description": "deposits",
              "properties": [
                {
                  "id": "date",
                  "description": "date",
                  "type": "string"
                },
                {
                  "id": "description",
                  "description": "description",
                  "type": "string"
                },
                {
                  "id": "amount",
                  "description": "amount",
                  "type": "string"
                }
              ]
            }
          },
          {
            "id": "_withdrawals",
            "method": {
              "id": "list",
              "description": "withdrawals",
              "properties": [
                {
                  "id": "date",
                  "description": "date",
                  "type": "string"
                },
                {
                  "id": "description",
                  "description": "description",
                  "type": "string"
                },
                {
                  "id": "amount",
                  "description": "amount. if the withdrawal amount is denoted with paratheses, reformat it to a negative sign, ie, change (45.56) to -45.56",
                  "type": "string"
                }
              ]
            }
          },
        ]
      }
    },
    /* zip the deposits for easier viewing */
    {
      "id": "deposits",
      "method": {
        "id": "zip",
        "source_ids": [
          "_deposits"
        ]
      }
    },
      /* zip the withdrawals for easier viewing */
    {
      "id": "withdrawals",
      "method": {
        "id": "zip",
        "source_ids": [
          "_withdrawals"
        ]
      }
    },
    {
      /* hide source fields for cleaner output */
      "id": "hide_fields",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "transaction_history",
          "_deposits",
          "_withdrawals"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example documents used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/conditional_execution.png)

| Example document 1 | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/conditional_execution_1.pdf) |
| ------------------ | ------------------------------------------------------------ |

| Example document 2 | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/conditional_execution_2.pdf) |
| ------------------ | ------------------------------------------------------------ |

**Output1  **

The output for the Practical Bank statement is the following:

```json
{
  "deposits": [
    {
      "date": {
        "value": "05/16/23",
        "type": "string"
      },
      "description": {
        "value": "Payment received - Munder Difflin Inc.",
        "type": "string"
      },
      "amount": {
        "value": "1,505.33",
        "type": "string"
      }
    },
    {
      "date": {
        "value": "05/25/23",
        "type": "string"
      },
      "description": {
        "value": "Money received - Tim B.",
        "type": "string"
      },
      "amount": {
        "value": "35.00",
        "type": "string"
      }
    }
  ],
  "withdrawals": [
    {
      "date": {
        "value": "04/07/23",
        "type": "string"
      },
      "description": {
        "value": "BarStucks coffee",
        "type": "string"
      },
      "amount": {
        "value": "-4.56",
        "type": "string"
      }
    },
    {
      "date": {
        "value": "04/15/23",
        "type": "string"
      },
      "description": {
        "value": "MalWart neighborhood groceries",
        "type": "string"
      },
      "amount": {
        "value": "-130.40",
        "type": "string"
      }
    },
    {
      "date": {
        "value": "04/19/23",
        "type": "string"
      },
      "description": {
        "value": "Wint mobile",
        "type": "string"
      },
      "amount": {
        "value": "-15.68",
        "type": "string"
      }
    }
  ]
}
```

**Output 2  **

The output for the Sensible Bank statement is the following:

```json
{
  "deposits": [
    {
      "date": {
        "value": "04/15/23",
        "type": "string"
      },
      "description": {
        "value": "Payment received - Munder Difflin Inc.",
        "type": "string"
      },
      "amount": {
        "value": "1,305.45",
        "type": "string"
      }
    },
    {
      "date": {
        "value": "4/23/23",
        "type": "string"
      },
      "description": {
        "value": "Money received - Andy B.",
        "type": "string"
      },
      "amount": {
        "value": "235.00",
        "type": "string"
      }
    }
  ],
  "withdrawals": [
    {
      "date": {
        "value": "04/10/23",
        "type": "string"
      },
      "description": {
        "value": "Stanley’s cafe",
        "type": "string"
      },
      "amount": {
        "value": "-4.33",
        "type": "string"
      }
    },
    {
      "date": {
        "value": "04/11/23",
        "type": "string"
      },
      "description": {
        "value": "Pam’s bookstore",
        "type": "string"
      },
      "amount": {
        "value": "-30.50",
        "type": "string"
      }
    },
    {
      "date": {
        "value": "04/13/23",
        "type": "string"
      },
      "description": {
        "value": "Michael’s paper warehouse",
        "type": "string"
      },
      "amount": {
        "value": "-122.98",
        "type": "string"
      }
    },
    {
      "date": {
        "value": "04/15/23",
        "type": "string"
      },
      "description": {
        "value": "Angela’s cat store",
        "type": "string"
      },
      "amount": {
        "value": "-42.70",
        "type": "string"
      }
    },
    {
      "date": {
        "value": "04/19/23",
        "type": "string"
      },
      "description": {
        "value": "Dwight’s farm",
        "type": "string"
      },
      "amount": {
        "value": "-32.43",
        "type": "string"
      }
    }
  ]
}
```

