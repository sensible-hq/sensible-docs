---
title: "Column"
hidden: false
---
Extracts all lines below the anchor line on the current page if:

- The anchor line's left and right boundaries ("x extent") contain the target line's x extent, or vice versa. 

  Or:

- The anchor line and target line overlap by at least 50% of the narrower line's x extent.

[**Parameters**](doc:column#parameters)
[**Examples**](doc:column#examples)

Parameters
====


| key               | values                                       | description                                                  |
| :---------------- | :------------------------------------------- | :----------------------------------------------------------- |
| id (**required**) | `column`                                     |                                                              |
| tiebreaker        | `first`, `second`, `third`, `last`, `>`, `<` | Which line in the column is the target. Use the comparisons `>` and `<` to extract maximum and minimum values in the column. Lines are [sorted](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators#relational_operators) alphanumerically using unicode values. If you want to compare numeric amounts and ignore non-numbers in the row,  then add a numeric [type](doc:types) such as  `type: currency` as a top-level parameter to the field. |
| includeAnchor     | `true`, `false`. default: false              | Includes the anchor line in the method output                |

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

**PDF**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/column.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/row_column.pdf) |
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



 
