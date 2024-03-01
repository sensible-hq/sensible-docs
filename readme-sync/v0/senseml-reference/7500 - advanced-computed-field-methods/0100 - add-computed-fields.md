---
title: "Add Computed Fields"
hidden: false
---
Enables transforming a table by adding an array of computed fields that operate on the extracted table. For example, you can add text to each cell in a row, concatenate columns, add or remove columns, and so forth. This method is similar to adding a [computed fields array to sections](doc:sections-example-copy-to-section).  In detail, this method:

- Automatically [zips](doc:zip) the source table. After the zip, each table cell is a field whose ID is the column heading. Note that zipped tables have the same JSON output structure as sections. This enables you to use section-specific computed fields to transform the table, such as  the Copy To Section method. 
- Operates on the fields in the table using the array of computed fields you specify.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                                  | description                                                  |
| :----------------------- | :----------------------------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `addComputedFields`                                    |                                                              |
| source_id (**required**) | source field ID in the current config                  | The ID of the table you want to transform. To transform fields in a section, add a [computed fields array to sections](doc:sections-example-copy-to-section). |
| fields                   | array of [computed fields](doc:computed-field-methods) | Specifies to output computed fields in the new table. The computed fields have access to the source  table's fields. To get access to and transform the output of fields that aren't in the source table, use the [Copy to section](doc:copy-to-section) method. |

Examples
====

The following example shows how to transform extracted tables so they're consistent across different document formats.

In the following example, Insurer A excludes the vehicle VIN and model from their policy limits table. In contrast, Insurer B includes the vehicle VIN, model, and make in their limits table:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/add_computed_fields_3.png)

This example uses the Add Computed Fields method to ensure that each table contains the same field IDs (`vin`, `policy_start`, `limits`, `amount`, and `model`):

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/add_computed_fields_2.png)

To ensure consistency, this example transforms the tables as follows:

- for Insurer A, copies vehicle details into the table
- for Insurer B, removes the vehicle make

**Config**

```json
{
  "fields": [
    {
      /* source field, suppressed from output.
         vehicle info to add to Insurer A table */
      "id": "_vin",
      "anchor": "vin:",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      /* source field, suppressed from output.
         vehicle info to add to Insurer A table */
      "id": "_model",
      "anchor": "model:",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      /* source table, suppressed from output */
      "id": "_raw_insurer_a_table",
      "anchor": "insurer a",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 3,
        "startOnRow": 1,
        "columns": [
          {
            "id": "policy_start",
            "index": 0
          },
          {
            "id": "limits",
            "index": 1
          },
          {
            "id": "amount",
            "index": 2
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "see appendix"
        }
      }
    },
    {
      /* source table, suppressed from output */
      "id": "_raw_insurer_b_table",
      "anchor": "insurer b",
      "type": "table",
      "method": {
        "id": "table",
        "columns": [
          {
            /* source column, suppressed from output */
            "id": "_make_model_column",
            "terms": [
              "make",
              "model"
            ],
          },
          {
            "id": "vin",
            "terms": [
              "vehicle",
              "vin"
            ],
          },
          {
            "id": "policy_start",
            "terms": [
              "effective",
              "date"
            ],
          },
          {
            "id": "limits",
            "terms": [
              "limits"
            ],
          },
          {
            "id": "amount",
            "terms": [
              "dollar amount"
            ],
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "per person"
        }
      }
    }
  ],
  "computed_fields": [
    {
      "id": "insurer_a_transformed",
      "method": {
        "id": "addComputedFields",
        "source_id": "_raw_insurer_a_table",
        "fields": [
          {
            "id": "vin",
            "method": {
              /* copy in the VIN positioned above the table 
                  so the information is accessible to this computed fields array
                  and is outputted in the transformed table */
              "id": "copy_to_section",
              "source_id": "_vin"
            }
          },
          {
            /* copy in model positioned above the table 
               so the information is accessible to this computed fields array
               and is outputted in the transformed table */
            "id": "model",
            "method": {
              "id": "copy_to_section",
              "source_id": "_model"
            }
          }
        ]
      }
    },
    {
      "id": "insurer_b_transformed",
      "method": {
        "id": "addComputedFields",
        "source_id": "_raw_insurer_b_table",
        "fields": [
          {
            /* split the make from the model, for consistency with insurer A */
            "id": "model",
            "method": {
              "id": "split",
              "source_id": "_make_model_column",
              "separator": " ",
              "index": 1
            }
          },
          {
            /* remove make and model field; 
               output only the transformed model field */
            "id": "cleanup",
            "method": {
              "id": "suppressOutput",
              "source_ids": [
                "_make_model_column"
              ]
            }
          }
        ]
      }
    },
    {
      /* output only transformed tables */
      "id": "cleanup",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "_vin",
          "_model",
          "_raw_insurer_a_table",
          "_raw_insurer_b_table"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/add_computed_fields_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/add_computed_fields.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "insurer_a_transformed": [
    {
      "policy_start": {
        "value": "02/19/21",
        "type": "string"
      },
      "limits": {
        "value": "Property damage (per accident)",
        "type": "string"
      },
      "amount": {
        "value": "$5,000",
        "type": "string"
      },
      "vin": {
        "type": "string",
        "value": "12345678"
      },
      "model": {
        "type": "string",
        "value": "Camry"
      }
    },
    {
      "policy_start": {
        "value": "02/19/21",
        "type": "string"
      },
      "limits": {
        "value": "Bodily injury (per person)",
        "type": "string"
      },
      "amount": {
        "value": "$3,000",
        "type": "string"
      },
      "vin": {
        "type": "string",
        "value": "12345678"
      },
      "model": {
        "type": "string",
        "value": "Camry"
      }
    },
    {
      "policy_start": {
        "value": "02/19/21",
        "type": "string"
      },
      "limits": {
        "value": "Auto only (per incident)",
        "type": "string"
      },
      "amount": {
        "value": "$2,000",
        "type": "string"
      },
      "vin": {
        "type": "string",
        "value": "12345678"
      },
      "model": {
        "type": "string",
        "value": "Camry"
      }
    }
  ],
  "insurer_b_transformed": [
    {
      "vin": {
        "value": "92343156",
        "type": "string"
      },
      "policy_start": {
        "value": "12/19/20",
        "type": "string"
      },
      "limits": {
        "value": "Property damage*",
        "type": "string"
      },
      "amount": {
        "value": "$6,000",
        "type": "string"
      },
      "model": {
        "value": "Accord",
        "type": "string"
      }
    },
    {
      "vin": {
        "value": "92343156",
        "type": "string"
      },
      "policy_start": {
        "value": "12/19/20",
        "type": "string"
      },
      "limits": {
        "value": "Bodily injury**",
        "type": "string"
      },
      "amount": {
        "value": "$4,000",
        "type": "string"
      },
      "model": {
        "value": "Accord",
        "type": "string"
      }
    },
    {
      "vin": {
        "value": "92343156",
        "type": "string"
      },
      "policy_start": {
        "value": "12/19/20",
        "type": "string"
      },
      "limits": {
        "value": "Auto only*",
        "type": "string"
      },
      "amount": {
        "value": "$1,000",
        "type": "string"
      },
      "model": {
        "value": "Accord",
        "type": "string"
      }
    }
  ]
}
```



