---
title: "Column"
hidden: false
---
Matches all lines below the anchor line on the current page if:

- the anchor line x extent contains the target line x extent, or vice versa
- they overlap at least 50% of the narrower line’s x extent with more than 50% X-axis overlap 

Parameters
====


| key               | values                                       | description                                                  |
| :---------------- | :------------------------------------------- | :----------------------------------------------------------- |
| id (**required**) | `column`                                     |                                                              |
| tiebreaker        | `first`, `second`, `third`, `last`, `>`, `<` | Which line in the column is the target. Use the comparisons `>` and `<` to grab maximum and minimum values in the column. By default the comparisons are sorted alphanumerically using [unicode values](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Less_than).  If you want to compare numeric amounts and ignore non-numbers,  then add `type: number` or `type: currency` as a top-level parameter to the field. |
| includeAnchor     | `true`, `false`. default: false              | Includes the anchor line in the method output                |

Examples
====

The following example shows that:

- If you specify  `"type": "string"` (the default),  you get the entire column returned as a joined string.
- If you specify a tiebreaker, you get a single element in the column.

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/column_example.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for column | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/example_row_column.pdf) |
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

