---
title: "Column"
hidden: false
---
Matches all lines below the anchor line on the current page if:

- The anchor line's left and right boundaries ("x extent") contain the target line's x extent, or vice versa. 

  Or:

- The anchor line and target line overlap by at least 50% of the narrower line's x extent.

[**Parameters**](doc:column#section-parameters)
[**Examples**](doc:column#section-examples)

  

Parameters
====


| key               | values                                       | description                                                  |
| :---------------- | :------------------------------------------- | :----------------------------------------------------------- |
| id (**required**) | `column`                                     |                                                              |
| tiebreaker        | `first`, `second`, `third`, `last`, `>`, `<` | Which line in the column's cells is the target. Use the comparisons `>` and `<` to grab maximum and minimum values in the column. By default the comparisons are sorted alphanumerically using [unicode values](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Less_than).  If you want to compare numeric amounts and ignore non-numbers,  then add `type: number` or `type: currency` as a top-level parameter to the field. |
| includeAnchor     | `true`, `false`. default: false              | Includes the anchor line in the method output                |

Examples
====

The following example shows that:

- If you specify  `"type": "string"` (the default),  you get the entire column returned as a joined string.
- If you specify a tiebreaker, you get a single element in the column.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/column_example.png)


Try out this example in the Sensible app using the following PDF and config:

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/example_row_column.pdf) |
| ---------------------- | ------------------------------------------------------------ |

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

