---
title: " merge objects + stateful map drafts"
hidden: true
---

*TODO: style guide:* 

- *operation or operator* 

+ *how to relate that to 'rule' , 'condition' or 'logic'? be consistent across this + other topics*



## Merge objects

*devon comments? merge objects:*
**Re: the note in the example, an example without `eachKey` would start with some original data that is then accessed in the example with `var` -*  



For an array of objects, returns a single object containing all the fields from each object. 

Edge cases:

- If passed an empty array, it returns an empty object
- If passed an array containing a value that is `null` or `undefined`, ignores that value but still returns an object based on object values that were passed
- If passed an array containing a value that is not an object, `null`, or `undefined`, throws an error
- If passed multiple fields that use the same key, uses the **last** value that is passed for that key (same rules as when spreading JS objects)

For example, simplified:

```json
{ 
  /* Note: this example works in a Postprocessor object
  it doesn't work in a Custom Computation method because of output schema constraints */
  "merge_objects": [
    { "eachKey": { "field1": "hello" } },
    { "eachKey": { "field2": "world" } }
  ]
}

```

returns:

``` json
{
  "field1": "hello",
  "field2": "world"
}
```

### Examples

See the Stateful Map operation for an example.



## Stateful Map

This operator maps an array and persists a `state` variable across items in the array.

Example use cases include:

- Keeping a rolling balance of transactions.
- Mixed headers and items data in a table: persist the headers and apply them to items until the header changes. 

```json
{
  "stateful_map": [
    [ /* 1st arg: array_to_map */ ],
    {
      /* 2nd arg: mapping function that has access to:
         - `current` var - the current item in the array
         - `index` var - index of item in the array
         - `state` var - the current state
         
         The function is expected to output an array with 2 elements:
         [  mapped item(s) ,  updated state  ]
      */
    },
    { 
      /* 3rd arg (optional): initialize the state for 1st item in array
      */
    }
  ]
}

```



### Examples

The following example shows using the Stateful Map and Merge Objects operations to transform an extracted table into a list of rows. The table contains a mix of header and data rows, and the JsonLogic operation transforms the table by skipping header rows and appending header information to each row.

```json
{
  "fields": [
    {
      /* Step 1: Extract a fixed table starting at row 1 with 2 columns
         Each column is defined with an id and index, and optionally a type */
      "id": "raw_table_contents",
      "anchor": "paint",
      "method": {
        "id": "fixedTable",
        "columnCount": 2,
        "startOnRow": 1,
        "columns": [
          {
            "id": "description",
            "index": 0
          },
          {
            "id": "rank",
            "index": 1,
            "type": "number"
          },
          
        ]
      }
    },
    {
      /* Step 2: Convert the table from column-wise format into an array of row objects */
      "id": "raw_ranked_paints",
      "method": {
        "id": "zip",
        "source_ids": [
          "raw_table_contents"
        ]
      }
    },
    {
      /* The stateful_map operation is used to track which header we’re currently in.

         If a row has rank: null, it's a header row, and its description becomes the new state.

         If a row has a rank value, it's a data row, and the current state (i.e., the last header) is used to set the vendor

         The result is a flat list of rows, each annotated with the appropriate vendor inferred from the most recent header. */
      "id": "ranked_paints",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "stateful_map": [
            {
              /* The input array to map over: each item is a row from the table */
              "var": "raw_ranked_paints"
            },
            {
              /* the stateful mapping function
                 It has access to:
                 - the `current` item in the array, 
                 - the `index` of the current item in the array
                 - a `state` variable 
                 Sensible expects the mapping function to return [mapped items, new state] */
              "if": [
                {
                  "==": [
                    /* Check if 'volume' cell is null to identify a header row */
                    {
                      "var": "current.rank"
                    },
                    null
                  ]
                },
                /* If it's a header row:
                   - add nothing (empty array) to the mapped items
                   - Update the state to the current vendor (e.g. "ACME CO") */
                [
                  [], /* adds no output to the mapped items */
                  {
                    /* new state = this row’s description */
                    "var": "current.description"
                  }
                ],
                /* If it's a data row:
                   - Add the current row to the mapped items, merging in a field `vendor` field from state
                   - Retain the current state */
                [
                  /* add current row to mapped items */
                  {
                    /* To the current row, merge in a new key 'vendor' from state */
                    "merge_objects": [
                      {
                        "var": "current"
                      },
                      {
                        "eachKey": {
                          "vendor": {
                            "var": "state"
                          }
                        }
                      }
                    ]
                  },
                  {
                    /* Retain current state (the last header description) */
                    "var": "state"
                  }
                ]
              ]
            }
          ]
        }
      }
    }
  ],
  "computed_fields": [
    {
      /* Suppress intermediate outputs so they don't appear in the final result */
      "id": "suppressOutput",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "raw_table_contents",
          "raw_ranked_paints"
        ]
      }
    }
  ]
}
```



**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/stateful_map_merge_objects.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/stateful_map_merge_objects.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "ranked_paints": [
    {
      "description": {
        "value": "Alabaster",
        "type": "string"
      },
      "rank": {
        "source": "1",
        "value": 1,
        "type": "number"
      },
      "vendor": {
        "value": "ACME CO",
        "type": "string"
      }
    },
    {
      "description": {
        "value": "Sonoma blue",
        "type": "string"
      },
      "rank": {
        "source": "2",
        "value": 2,
        "type": "number"
      },
      "vendor": {
        "value": "ACME CO",
        "type": "string"
      }
    },
    {
      "description": {
        "value": "Mushroom",
        "type": "string"
      },
      "rank": {
        "source": "3",
        "value": 3,
        "type": "number"
      },
      "vendor": {
        "value": "ACME CO",
        "type": "string"
      }
    },
    {
      "description": {
        "value": "Slate gray",
        "type": "string"
      },
      "rank": {
        "source": "1",
        "value": 1,
        "type": "number"
      },
      "vendor": {
        "value": "ANYCO INC",
        "type": "string"
      }
    },
    {
      "description": {
        "value": "Buttercream",
        "type": "string"
      },
      "rank": {
        "source": "2",
        "value": 2,
        "type": "number"
      },
      "vendor": {
        "value": "ANYCO INC",
        "type": "string"
      }
    },
    {
      "description": {
        "value": "Seaspray",
        "type": "string"
      },
      "rank": {
        "source": "3",
        "value": 3,
        "type": "number"
      },
      "vendor": {
        "value": "ANYCO INC",
        "type": "string"
      }
    }
  ]
}
```

