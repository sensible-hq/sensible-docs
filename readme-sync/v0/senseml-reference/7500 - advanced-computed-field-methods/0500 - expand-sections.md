---
title: "transformTable"
hidden: true
---
Gives you access to computed fields array in an extracted table. This computed method is similar in effect to adding a Computed Fields array to a sections group. It gives you the same power to modify individual cells in a table as you'd have the power to modify fields in a section group.

This method:

1.  Converts an extracted table into a section group (where each section is a row), 

![image-20231219112031226](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20231219112031226.png)

For example, it converts:

```json
{
  "epl_table": {
    "columns": [
      {
        "id": "limit",
        "values": [
          {
            "source": "$500,000",
            "value": 500000,
            "unit": "$",
            "type": "currency"
          },
          {
            "source": "$1,000,000",
            "value": 1000000,
            "unit": "$",
            "type": "currency"
          }
        ]
      },
      {
        "id": "10k_retention_separate",
        "values": [
          {
            "source": "$3,996",
            "value": 3996,
            "unit": "$",
            "type": "currency"
          },
          {
            "source": "$5,328",
            "value": 5328,
            "unit": "$",
            "type": "currency"
          }
        ]
      },
      {
        "id": "10k_retention_shared",
        "values": [
          {
            "source": "$2,997",
            "value": 2997,
            "unit": "$",
            "type": "currency"
          },
          {
            "source": "$3,996",
            "value": 3996,
            "unit": "$",
            "type": "currency"
          }
        ]
      }
    ]
  },
```

To the following section group, where each row is one section, and where each table column ID becomes a field ID **Note this is the same as section output so TODO link to Zip**:

```
"epl_table_section": [
    {
      "limit": {
        "source": "$500,000",
        "value": 500000,
        "unit": "$",
        "type": "currency"
      },
      "10k_retention_separate": {
        "source": "$3,996",
        "value": 3996,
        "unit": "$",
        "type": "currency"
      },
      "10k_retention_shared": {
        "source": "$2,997",
        "value": 2997,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "limit": {
        "source": "$1,000,000",
        "value": 1000000,
        "unit": "$",
        "type": "currency"
      },
      "10k_retention_separate": {
        "source": "$5,328",
        "value": 5328,
        "unit": "$",
        "type": "currency"
      },
      "10k_retention_shared": {
        "source": "$3,996",
        "value": 3996,
        "unit": "$",
        "type": "currency"
      }
    }
  ]
```



2. Lets you specify an array of computed fields to append to each "section". This is similar to this [example](do:sections-example-copy-to-section) of adding computed fields to a section group.

For example, say you want to concatenate two columns and suppress the output of other columns:

```json
{
      "id": "epl_table_sections_onestep",
      "method": {
        "id": "expandSections",
        "source_id": "epl_table",
        "fields": [
          {
            "id": "clean",
            "method": {
              "id": "suppressOutput",
              "source_ids": [
                "10k_retention_separate", // the columns (now field IDs in sections) you want to suppress
                "10k_retention_shared", 
              ]
            }
          },
          {
            "id": "transformed_field_in_table",
            "method": {
              "id": "concat",
              "source_ids": ["10k_retention_shared", "10k_retention_separate"] // todo clean up source IDs
            }
          }
        ]
      }
    },
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


| key                      | value                                 | description                                                  |
| :----------------------- | :------------------------------------ | :----------------------------------------------------------- |
| id (**required**)        | `copy_to_section`                     |                                                              |
| source_id (**required**) | source field ID in the current config | The source ID to copy must be in a field array or section that is one level up in the hierarchy relative to the destination section. For example, in a sections group, copy from the base fields array. In a nested sections group, copy from the parent section group's field array. For example, if you use Copy  To Sections to copy a global policy number into each claims section, you can then transform it in each section, for example by |

Examples
====

For an example, see [Advanced: Add global information to sections](doc:sections-example-copy-to-section).

TODO: add to the copy to fields example or to the parameters section

```
"computed_fields": [
        
        {
          "id": "copied_claims",
          "method": {
            "id": "copy_to_section",
            "source_id": "_total_unprocessed_claims",
          }
        },
        {
          "id": "transform_copied",
          "method": {
            "id": "split",
            "source_id":  "copied_claims",
          
            "separator": " "
          }
        }
      ]
    }
```

