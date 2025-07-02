---
title: " jsonlogic draft"
hidden: true
---

## sort by



 Sorts an array of objects by the specified key. Expects numbers or strings for the key's values. Sorts in ascending alphanumeric order. Numbers are treated as strings when sorting.

```json
"sort_by":
[
 [ /* array_of_objects_to_sort */ ],
 "key_to_sort_by", 
]
```

For example, the following code sorts an array:

```json
{
  "fields": [],
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      "sort_by": [
        {
          /*
            The array of objects to sort.
            In practice, you often input an
            array with `{"var":"field_key"}` syntax.
            This example uses `preserve` to input an
            array constant
            as literal JSON rather than JsonLogic
          */
          "preserve": [
            {
              "x": {
                "value": 20,
                "type": "number"
              },
              "y": {
                "value": 4
              }
            },
            {
              "x": {
                "value": "1_a_string",
                "type": "string"
              },
              "y": {
                "value": 2
              }
            },
            {
              "x": {
                "value": "20",
                "type": "string"
              },
              "y": {
                "value": 5
              }
            },
            {
              "x": {
                "value": "20_",
                "type": "string"
              },
              "y": {
                "value": 5
              }
            },
            {
              "x": {
                "value": 1,
                "type": "number"
              },
              "y": {
                "value": 3
              }
            },
            {
              "x": {
                "value": "z_string",
                "type": "string"
              },
              "y": {
                "value": 1
              }
            },
            {
              "x": {
                "value": "a_string",
                "type": "string"
              },
              "y": {
                "value": 1
              }
            }
          ]
        },
        // Sort by the x field's value
        { "var": "x.value" }
      ]
    }
  }
}

```

The preceding code sample returns the following output:

```json
[
  {
    "x": {
      "value": 1,
      "type": "number"
    },
    "y": {
      "value": 3
    }
  },
  {
    "x": {
      "value": "1_a_string",
      "type": "string"
    },
    "y": {
      "value": 2
    }
  },
  {
    "x": {
      "value": 20,
      "type": "number"
    },
    "y": {
      "value": 4
    }
  },
  {
    "x": {
      "value": "20",
      "type": "string"
    },
    "y": {
      "value": 5
    }
  },
  {
    "x": {
      "value": "20_",
      "type": "string"
    },
    "y": {
      "value": 5
    }
  },
  {
    "x": {
      "value": "a_string",
      "type": "string"
    },
    "y": {
      "value": 1
    }
  },
  {
    "x": {
      "value": "z_string",
      "type": "string"
    },
    "y": {
      "value": 1
    }
  }
]
```

## 
