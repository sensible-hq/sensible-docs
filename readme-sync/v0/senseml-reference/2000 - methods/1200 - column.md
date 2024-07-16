---
title: "Column"
hidden: false
---
Extracts all lines below the anchor line on the current page if:

- The anchor line's left and right boundaries ("x extent") contain the target lines' x extent, or vice versa. 

  Or:

- The anchor line and target lines overlap by at least 50% of the narrower line's x extent.

[**Parameters**](doc:column#parameters)
[**Examples**](doc:column#examples)

Parameters
====


| key               | values                             | description                                                  |
| :---------------- | :--------------------------------- | :----------------------------------------------------------- |
| id (**required**) | `column`                           |                                                              |
| tiebreaker        | tiebreaker                         | For information about this global parameter, see [Method](doc:method#parameters). |
| includeAnchor     | `true`, `false`. default: false    | Includes the anchor line in the method output                |
| position          | `below`, `above`. default: `below` | Matches above or below the anchor line. For example, if you anchor on the bottom line of a column, set this to `above` to extract the column. |

Examples
====

The following example shows that:

- By default, Sensible returns the entire column as a joined string.
- Specifying a tiebreaker returns single element in the column.

**Config**

```json
{
  "fields": [
    {
      "id": "example_column",
      "anchor": "may 2020",
      "type": "string",
      "method": {
        "id": "column"
      }
    },
    {
      "id": "example_column_2",
      "anchor": "may 2020",
      "type":"number",
      "method": {
        "id": "column",
        "tiebreaker": ">"
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/column.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/row_column.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "example_column": {
    "type": "string",
    "value": "1 3 2 4 5"
  },
  "example_column_2": {
    "source": "5",
    "value": 5,
    "type": "number"
  }
}
```



 
