---
title: "Row"
hidden: false
---
Matches all lines to the left or right of the anchor line. The within 0.08 inches of the anchor's top line



| key               | value                                        | description                                   |
| ----------------- | -------------------------------------------- | --------------------------------------------- |
| id (**required**) | `row`                                        |                                               |
| includeAnchor     | boolean. default: `false`                    | Includes the anchor line in the method output |
| position          | `right`, `left`. Default: `right`            | Matches to the left or right                  |
| tiebreaker        | `first`, `second`, `third`, `last`, `>`, `<` | Which element in the row is the target        |

Example
----



```json
{
  "fields": [
    {
      "id": "number_1_language_on_github",
      "method": {
        "id": "row",
        "tiebreaker": "first",
        "position": "left",
        "includeAnchor": true
      },
      "anchor": {
        "match": [
          {
            "text": "Languages by Github rank",
            "type": "startsWith"
          },
          {
            "text": "1",
            "type": "startsWith"
          }
        ]
      }
    },
    {
      "id": "python_change_in_TIBOE_rating",
      "method": {
        "id": "row",
        "tiebreaker": "second"
      },
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
      }
    },
  ]
}
```



Parameters
-----

Notes
-----
TODO: refer to column?