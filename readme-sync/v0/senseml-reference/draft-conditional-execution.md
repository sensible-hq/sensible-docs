---
title: "Conditional execution"
hidden: true
---

*TODOs before publish:*

- *overview/ devops platform*
- *senseml reference introduction?*
- add info on 'conditional execution' as a more sophisticated form of falling back?



Extracts alternate sets of fields based on whether a [JsonLogic](doc:jsonlogic) rules passes or fails. TODO: example use cases. (frm real life)

TODO: simple example here w screenshot??

```json
id: conditional
rule: if 
fieldsOnPass:
fieldsOnFail:
```



## Parameters

TODO: look at Query Group parameters and see how they compare

### METHOD PARAMETERS (how to describe that?)

| key                                                          | value                                     | description                                                  |
| ------------------------------------------------------------ | ----------------------------------------- | ------------------------------------------------------------ |
| id (**required**)                                            | `conditional`                             | TBD this field type `if...then...else` conditional structure for extracting alternate lists of fields. You can nest conditional fields inside conditional fields. TODO better place to put this? |
| rule                                                         | [JsonLogic](doc:jsonlogic)                | evaluates to a boolean (true = pass, false = fail). Usually depends on evaluating extracted data from the document which determines what appropriate fields to extract. |
| fieldsOnPass 2do/todo: is 1 required but not both? either/or/and? check ... might be something to combo into 1 row if same lanugage. | array of [fields](doc:field-query-object) | Specifies fields to extract if the rule passes.              |
| fieldsOnFail                                                 |                                           | Specifies fields to extract if the rule fails. TODO note if you supress output for an invalid JsonLogic field (either through a conditioanl, or through suppress output field)  it will still show up as an error even if the fields pass -- so you can still troubleshoot it. |

## Examples



The following example shows TBD

**Config**

```json
{
  "fields": [
    {
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
        "rule": {
          "exists": {
            "var": "transaction_history"
          }
        },
        "fieldsOnPass": [
          {
            "id": "passed",
            "method": {
              "id": "constant",
              "value": "condition passes"
            }
          },
          // if transactions table not null, split it up into deposits and withdrawals
          {
            "id": "deposits",
            "method": {
              "id": "list",
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
            "id": "withdrawals",
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
          },
          {
            "id": "hide_fields",
            "method": {
              "id": "suppressOutput",
              "source_ids": [
                "transaction_history"
              ]
            }
          }
        ],
        "fieldsOnFail": [
          // if transactions table is null, extract the existing deposits and withdrawals tables
          {
            "id": "failed",
            "method": {
              "id": "constant",
              "value": "condition failed"
            }
          },
          {
            "id": "deposits",
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
            "id": "withdrawals",
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
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/conditional_execution.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TB_D.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
```