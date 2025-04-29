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
 <array_to_group>,
 "key_to_group_by", 
[[<field_to_return>], [<field_to_return>] ... ]]
]
```



Example:

```json
{
  /* groups a list of items by a property (`category`),
  and for each group, returns computed information abt the group
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
          /*  return the values of the group keys  */
          [
            "group_key",
            {
              "var": "key"
            }
          ],
          /* return group item counts */
          [
            "count_of_items_in_group",
            {
              "length": {
                "var": "values"
              }
            }
          ],
          /* return colors of items in groups*/
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

equivalent to `Object.entries(obj).map( ([key, value]) => ...)`

The custom `mapObject` operator in your `jsonlogic` implementation functions like `Object.entries(obj).map(([key, value]) => ...)`, letting you iterate over an object and apply logic per key-value pair.

LEFT OFF:
why doesn't this work? https://dev.sensible.so/editor/?d=frances_playground&c=map_object&g=postprocessor_llm_humana_1_redact&v=

```json
{
  "fields": [
    {
      "id": "date_shift_1",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "mapObject": [
            {
              "key1": 2,
              "key2": 3,
            },
            [
              // rule for the key: leave unchanged
              {
                "var": "key"
              },
              // rule for the value
              {
                "+": [
                  {
                    "var": "value"
                  },
                  4
                ]
              },
            ],
          ]
        }
      }
    },
  ]
}
```







### ✅ What it does:

It takes **two arguments**:

1. An **object** to iterate over.
2. A **rule or set of rules** to apply to each `[key, value]` pair in that object.

The rule(s) you pass are evaluated per *pair*, and the results are collected into an array and returned.

  ```
  mapObject: [
      { var: "obj" },
      [
        { var: "key" },
        { "*": [{ var: "value" }, 2] },
      ],
    ]
  }
  ```









------

### 🔍 Breakdown of Test Cases:

1. **Basic usage with transformation**

   ```
   tsCopyEdit{
     mapObject: [
       { var: "obj" },
       [
         { var: "key" },
         { "*": [{ var: "value" }, 2] },
       ],
     ]
   }
   ```

   ➡️ Transforms to:

   ```
   ts
   
   
   CopyEdit
   [["key1", 2], ["key2", 4], ["key3", 6]]
   ```

2. **Single rule (not in array)**

   ```
   tsCopyEdit{
     mapObject: [{ var: "obj" }, { var: "key" }]
   }
   ```

   ➡️ Extracts only the keys: `["key1", "key2", "key3"]`

3. **Null output for some entries**

   ```
   tsCopyEdit{
     mapObject: [
       { var: "obj" },
       {
         if: [
           { "===": [{ var: "key" }, "key1"] },
           null,
           [
             { var: "key" },
             { "*": [{ var: "value" }, 2] }
           ],
         ],
       },
     ]
   }
   ```

   ➡️ Conditional transformation: `[null, ["key2", 4], ["key3", 6]]`

4. **Single rule in an array**

   ```
   ts
   
   
   CopyEdit
   mapObject: [{ var: "obj" }, [{ var: "key" }]]
   ```

   ➡️ Each result is wrapped in an array: `[["key1"], ["key2"], ["key3"]]`

5. **Multiple rules per entry**

   ```
   tsCopyEditmapObject: [
     { var: "obj" },
     [
       { var: "key" },
       { "*": [{ var: "value" }, 2] },
       { cat: [{ var: "key" }, " testing"] }
     ]
   ]
   ```

   ➡️ Outputs 3 values per entry: `["key1", 2, "key1 testing"]` etc.

6. **Empty object returns empty array**

   ```
   ts
   
   
   CopyEdit
   mapObject: [{ var: "emptyObj" }, [{ var: "key" }, { var: "value" }]]
   ```

   ➡️ `[]`

7. **Invalid args**

   ```
   ts
   
   
   CopyEdit
   mapObject: { var: "obj" }
   ```

   ➡️ Throws `"Invalid args for mapObject"` – must be an array of arguments.

8. **Non-object input**

   ```
   ts
   
   
   CopyEdit
   mapObject: ["not an object", [{ var: "key" }, { var: "value" }]]
   ```

   ➡️ Throws `"Invalid args for mapObject"` – input must be a proper object.

------

### 🧠 Summary

Your `mapObject` operator is a custom JsonLogic extension that brings functional-style `Object.entries().map()` capability to JsonLogic. It supports:

- Single or multiple return values per entry
- Conditionals
- Empty object safety
- Type checks for invalid usage

It makes it easy to transform objects dynamically in JsonLogic rules without manually iterating or restructuring them outside logic.

Want a sample implementation of this custom operator in code?

