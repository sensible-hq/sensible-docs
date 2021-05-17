---
title: "Row"
hidden: false
---
Matches all lines to the left or right of the anchor line.  A "row" is defined as lines that are vertically aligned with the anchor, within 0.08 inches of the top line of the anchor's bounding box. For example, the following image highlights the line that defines a row:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/row_align.png)


Examples
----

The following example demonstrates choosing data from two consecutive tables:

1. The first field has an anchor with two matches: first the anchor matches the heading `Languages by Github rank`  to ensure we are in the first table, and then it matches on the text  `first`  to find the row with the top-ranked Github language. The method then grabs the language name to the left of the last anchor match (`first`). 
2. The second field also has an anchor with two matches: first the anchor matches  the heading `Languages ranked by search engine` to ensure we are in the second table, and then it finds the word `Python` to find the first row with that text.  The method then grabs the % change in ranking for Python by taking the second item in the row to the right of the anchor match (`Python`).

```json
{
  "fields": [
    {
      "id": "number_1_language_on_github",
      "anchor": {
        "match": [
          {
            "text": "Languages by Github rank",
            "type": "startsWith"
          },
          {
            "text": "first",
            "type": "startsWith"
          }
        ]
      },
      "method": {
        "id": "row",
        "tiebreaker": "first",
        "position": "left",
        "includeAnchor": true
      }
    },
    {
      "id": "python_change_in_TIBOE_rating",
      "anchor": {
        "match": [
          {
            "text": "Languages ranked by search engine",
            "type": "startsWith"
          },
          {
            "text": "Python",
            "type": "startsWith"
          }
        ]
      },
      "method": {
        "id": "row",
        "tiebreaker": "second"
      }
    },
  ]
}
```

The following image shows this example in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/row_example.png)



Parameters
------


| key               | value                                        | description                                                  |
| ----------------- | -------------------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `row`                                        |                                                              |
| includeAnchor     | boolean. default: `false`                    | Includes the anchor line in the method output                |
| position          | `right`, `left`. Default: `right`            | Matches to the left or right                                 |
| tiebreaker        | `first`, `second`, `third`, `last`, `>`, `<` | Which line in the row is the target. Use `>` and `<` to grab maximum and minimum numeric values in the row. If the values in the row are alphanumeric rather than strictly numeric, then `<` and `>`  return values sorted alphanumerically rather than by amount (for example, in a row containing the lines "1", "2", a", and "z", `<` returns "1" and `>` returns "z".) |


Notes
-----
TODO: refer to column?