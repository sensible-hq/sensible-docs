---
title: "Add Computed Fields"
hidden: true
---
This lets you specify an array of computed fields to add the output of a table or other 'zipped' field. You *can* use it with sections, but you shouldn't, because it has the same effect as declaring a Computed Fields array inside a section group defintion.

The most comom use case for this method is to transform table output.



Gives you access to computed fields array in an extracted table. This computed method is similar in effect to adding a Computed Fields array to a sections group. It gives you the same power to modify individual cells in a table as you'd have the power to modify fields in a section group.

This method:

1.  Converts an extracted table into a section group (where each section is a row), 



For example, it converts:

```json

```

To the following section group, where each row is one section, and where each table column ID becomes a field ID **Note this is the same as section output so TODO link to Zip**:

```

```



2. Lets you specify an array of computed fields to append to each "section". This is similar to this [example](do:sections-example-copy-to-section) of adding computed fields to a section group.

For example, say you want to concatenate two columns and suppress the output of other columns:

```json

```



The output is then like this:

```
TODO
```









**Alternatives**

- 

Copies a field into each section in a section group, or from a parent section into each section in a nested section group. 

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                 | description |
| :----------------------- | :------------------------------------ | :---------- |
| id (**required**)        | `addComputedFields`                   |             |
| source_id (**required**) | source field ID in the current config | TODO        |
| fields                   |                                       | TODO        |

Examples
====

https://dev.sensible.so/editor/?d=frances_playground&c=add_computed_fields&g=add_computed_fields



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

