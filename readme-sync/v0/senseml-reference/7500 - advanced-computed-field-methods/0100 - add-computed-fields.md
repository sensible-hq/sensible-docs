---
title: "Add Computed Fields"
hidden: true
---
Enables transforming the output of a table by adding an array of computed fields to the extracted table's output.  For example, you can add text to each cell in a row, concatenate columns, add or remove columns, and so forth. This computed method is similar in effect to using a [computed fields array in sections](doc:sections-example-copy-to-section).  In detail, this method:

- Automatically [zips](doc:zip) the source table. The output of a zipped table is identical in JSON structure to the output of [sections](doc:sections). Each table cell becomes a field whose ID is the column heading.
- Operates on the fields in the table using the array of computed fields you specify.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                                  | description                                                  |
| :----------------------- | :----------------------------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `addComputedFields`                                    |                                                              |
| source_id (**required**) | source field ID in the current config                  | The ID of the table you want to transform                    |
| fields                   | array of [computed fields](doc:computed-field-methods) | Specifies to output computed fields to the transformed table output. The computed fields have access to thesource  table's fields. To get access to and transform the output of fields that aren't in the source table, use the [Copy To Section](doc:copy-to-section) method. |



Examples
====

The following example shows how to transform table output so that it's consistent across different document formats.

In the following example, Insurer A excludes the vehicle details, such as the VIN and model, from their policy limits table. In contrast, Insurer B includes these details in their limits table:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/add_computed_fields_3.png)

The transformed output ensures that each table contains the same field IDs (`vin`, `policy_start`, `limits`, `amount` and `model`).  It does so by:

- adding vehicle details to the table for Insurer A 
- removing the vehicle make information from the table for Insurer B

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/add_computed_fields_2.png)



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
      "id": "_make_model",
      "anchor": "make and model",
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
        "id": "table",
        "columns": [
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
              /* copy in the vin that's positioned above the table 
                  so the information is accessible to this computed fields array
                  and is output in the transformed table */
              "id": "copy_to_section",
              "source_id": "_vin"
            }
          },
          {
            /* copy in the make and model that's positioned above the table 
               so the information is accessible to this computed fields array */
            "id": "copied_make_model",
            "method": {
              "id": "copy_to_section",
              "source_id": "_make_model"
            }
          },
          {
            /* output only the make, not the model */
            "id": "model",
            "method": {
              "id": "split",
              "source_id": "copied_make_model",
              "separator": " ",
              "index": 1
            }
          },
          {
            /* remove make and model; 
               output only the transformed model field */
            "id": "cleanup",
            "method": {
              "id": "suppressOutput",
              "source_ids": [
                "copied_make_model"
              ]
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
            /* output only the make, not the model */
            "id": "model",
            "method": {
              "id": "split",
              "source_id": "_make_model_column",
              "separator": " ",
              "index": 1
            }
          },
          {
            /* remove make and model; 
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
      "id": "cleanup",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "_vin",
          "_make_model",
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
        "value": "Toyota",
        "type": "string"
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
        "value": "Toyota",
        "type": "string"
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
        "value": "Toyota",
        "type": "string"
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



