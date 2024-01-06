---
title: "Add Computed Fields"
hidden: true
---
Enables transforming the output of a table by adding an array of computed fields to the extracted table's output.  For example, you can add text to each cell in a row, concatenate columns, add or remove columns, and so forth. This computed method is similar in effect to  using a [Computed Fields array in sections](doc:sections-example-copy-to-section).  In detail, this method:

- Automatically [zips](doc:zip) the source table. The output of a zipped table is identical in JSON structure to the output of  [sections](doc:sections). Each table cell becomes a field whose ID is the column heading.
- Operates on the fields in the table using the array of computed fields you specify. The computed fields have access to the table's fields. To get access to and transform the output of fields that aren't in the table, use the [Copy To Section](doc:copy-to-section) method.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                                  | description                                                  |
| :----------------------- | :----------------------------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `addComputedFields`                                    |                                                              |
| source_id (**required**) | source field ID in the current config                  | The ID of the table you want to transform                    |
| fields                   | array of [computed fields](doc:computed-field-methods) | Specifies to output computed fields to the transformed table output.  The computed fields have access to the table's fields. To get access to and transform the output of fields that aren't in the source table, use the [Copy To Section](doc:copy-to-section) method. |



Examples
====

The following example shows how to transform table output so that it's consistent across different document formats.

In the following example, Insurer A excludes the vehicle details, such as the VIN and model, from the policy limits table, but Insurer B includes them in the table. 





![image-20231222142631494](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20231222142631494.png)



Note that you can't get them identically ordered rows but that's fine b/c it's all json keys underlying this.

```
{
  "fields": [
    {
      "id": "_vin",
      "anchor": "vin",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      "id": "_make_model",
      "anchor": "make and model",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      "id": "_raw_vendor_a_table",
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
      "id": "_raw_vendor_b_table",
      "anchor": "insurer b",
      "type": "table",
      "method": {
        "id": "table",
        "columns": [
          {
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
      "id": "vendor_b_zipped", //same row format as produced by addComputedFields
      "method": {
        "id": "zip",
        "source_ids": [
          "_raw_vendor_b_table"
        ]
      }
    },
    {
      "id": "vendor_b_zipped_and_computed",
      "method": {
        "id": "addComputedFields",
        "source_id": "_raw_vendor_b_table",
        "fields": [
          {
            "id": "model_split", // let's just get the model
            "method": {
              "id": "split",
              "source_id": "_make_model_column",
              "separator": " ",
              "index": 1
            }
          },
          {
            "id": "hide_columns", // let's hide the make-model column
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
      "id": "vendor_a_zipped_n_computed",
      "method": {
        "id": "addComputedFields",
        "source_id": "_raw_vendor_a_table",
        "fields": [
          {
            "id": "vin",
            "method": {
              "id": "copy_to_section", // copy in the vin that's positioned above the table in the object, so it's accessible to the table object
              "source_id": "_vin"
            }
          },
          {
            "id": "copied_make_model", // // copy in the make and model for same reason
            "method": {
              "id": "copy_to_section",
              "source_id": "_make_model"
            }
          },
          {
            "id": "model_split", // output only the make, not the model
            "method": {
              "id": "split",
              "source_id": "copied_make_model",
              "separator": " ",
              "index": 1
            }
          },
          {
            "id": "hide_columns", // hide the copied make and model field, we only want the model
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
      "id": "cleanup",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "_vin",
          "_make_model",
          "_raw_vendor_a_table",
          "_raw_vendor_b_table"
        ]
      }
    }
  ]
}
```

