---
title: " jsonlogic draft"
hidden: true
---

## sort by



 Sorts an array of objects by the specified key. The key's values must all be of the same type, either strings or numbers. Sorts in ascending alphanumeric order.

```json
"sort_by":
[
 [ /* array_of_objects_to_sort */ ],
 "key_to_sort_by", 
]
```

For example, the following code sorts an array of dates:

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
              "date": {
                "source": "01/25/2024",
                "value": "2024-01-25T00:00:00.000Z",
                "type": "date"
              },
              "hours": {
                "source": "7.41",
                "value": 7.41,
                "type": "number"
              }
            },
            {
              "date": {
                "source": "01/27/2022",
                "value": "2022-01-27T00:00:00.000Z",
                "type": "date"
              },
              "hours": null
            },
            {
              "date": {
                "source": "01/28/2023",
                "value": "2023-01-28T00:00:00.000Z",
                "type": "date"
              },
              "hours": {
                "source": "2.00",
                "value": 2,
                "type": "number"
              }
            }
          ]
        },
        // Sort by the date field's value
        { "var": "date.value" }
      ]
    }
  }
}

```

The preceding code sample returns the following output:

```json
[
  {
    "date": {
      "source": "01/27/2022",
      "value": "2022-01-27T00:00:00.000Z",
      "type": "date"
    },
    "hours": null
  },
  {
    "date": {
      "source": "01/28/2023",
      "value": "2023-01-28T00:00:00.000Z",
      "type": "date"
    },
    "hours": {
      "source": "2.00",
      "value": 2,
      "type": "number"
    }
  },
  {
    "date": {
      "source": "01/25/2024",
      "value": "2024-01-25T00:00:00.000Z",
      "type": "date"
    },
    "hours": {
      "source": "7.41",
      "value": 7.41,
      "type": "number"
    }
  }
]
```

## 
