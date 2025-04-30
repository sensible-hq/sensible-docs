---
title: " style notes"
hidden: true
---

*TODO: style guide:* 

- *operation or operator* 

+ *how to relate that to 'rule' , 'condition' or 'logic'? be consistent across this + other topics*

## Group

 Groups an array of objects by the specified key and returns computed fields for each group.

```json
"group":
[
 <array_of_objects_to_group>,
 "key_to_group_by", 
/* specify each <field_to_return> with syntax ["key", JsonLogic] */
[[<field_to_return>], [<field_to_return>] ... ]]
]
```



Example:

```json
{
  /* groups a list of items by a property (`apparel_type`),
  and for each group, returns computed fields
  */
  "fields": [],
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      /* */
      "group": [
        {
          /*
            input an array to be grouped
            in practice, you often input an
            array with `{"var":"field_key"}` syntax.
            this example uses 'preserve' to input a
            simple array constant
            as literal JSON rather than JsonLogic
          */
          "preserve": [
            {
              "apparel_type": "shirt",
              "color": "yellow"
            },
            {
              "apparel_type": "dress",
              "color": "green"
            },
            {
              "apparel_type": "shirt",
              "color": "red"
            }
          ]
        },
        /* group by the `apparel_type` key */
        "apparel_type",
        /* for each group, return the following computed fields:
             - group key
             - count of items in group
             - array of colors of items in group  */
        [
          /*  return a field with the value of the group key  */
          [
            "group_key",
            {
              "var": "key"
            }
          ],
          /* return a field with the group item count */
          [
            "count_of_items_in_group",
            {
              "length": {
                "var": "values"
              }
            }
          ],
          /* return a field with the colors of items in the group*/
          [
            "colors_in_group",
            {
              "map": [
                {
                  "var": "values"
                },
                {
                  "var": "color"
                }
              ]
            }
          ]
        ]
      ]
    }
  }
}
```

This outputs:

```json
[
  {
    "group_key": "shirt",
    "count_of_items_in_group": 2,
    "colors_in_group": [
      "yellow",
      "red"
    ]
  },
  {
    "group_key": "dress",
    "count_of_items_in_group": 1,
    "colors_in_group": [
      "green"
    ]
  }
]
```



## Map Object

Takes an object containing key-value pairs, and iterate over the object performing operations on each key and each value.

**Config**

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "lime pies",
            "description": "number of lime pies",
            "type": "number"
          },
          {
            "id": "apple pies",
            "description": "number of apple pies",
            "type": "number"
          },
        ]
      }
    }
  ],
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      "mapObject": [
        {
          /* the object to map. in this case, the current context, 
          i.e. the extracted fields
          */
          "var": ""
        },
        [
          {
            // operation to perform on each field's key
            "cat": [
              // prefix each key with its meal category
              "DESSERT_",
              {
                "var": "key"
              },
            ]
          },
          // operation to perform on each field's value 
          {
            // multiply the value by 4
            "*": [
              {
                // since each field's value is an object,
                // access nested value with value.value
                "var": "value.value"
              },
              4
            ]
          }
        ]
      ]
    }
  }
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/map_object.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TB_D.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
// FIELD OUTPUT
{
  "lime pies": {
    "source": "3",
    "value": 3,
    "type": "number",
    "confidenceSignal": "confident_answer"
  },
  "apple pies": {
    "source": "5",
    "value": 5,
    "type": "number",
    "confidenceSignal": "confident_answer"
  }
}

//POSTPROCESSOR OUTPUT
[
  [
    "DESSERT_lime pies",
    12
  ],
  [
    "DESSERT_apple pies",
    20
  ]
]


```

