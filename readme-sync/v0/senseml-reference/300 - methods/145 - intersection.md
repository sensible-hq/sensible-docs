---
title: "Intersection"
hidden: true
---
Matches a line at the intersection of a horizontal line defined by an anchor, and a vertical line defined by a second anchor:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/screenshots/intersection_example_1.png)

This method is useful instead of the Row method when a table contains empty cells. With empty cells, a row's tiebreaker like "second" can return inconsistent results.

[**Parameters**](doc:fixed-table#section-parameters)
[**Examples**](doc:fixed-table#section-examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                           | value          | description                                                  |
| :---------------------------- | :------------- | :----------------------------------------------------------- |
| id (**required**)             | `intersection` |                                                              |
| verticalAnchor (**required**) | Anchor object  | An anchor object that defines a vertical line. Sensible extracts the line that is at the intersection of this vertical line, and the horizontal line defined by the field's anchor. |

Examples
=====

**Config**

```json
{
  "fields": [
    {
      "id": "col_3_cell",
      "anchor": "item 1b",
      "method": {
        "id": "intersection",
        "verticalAnchor": "col3"
      }
    }
  ]
}
```

**PDF**

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/screenshots/intersection_example_2.png)

**Output**

```json
{
  "col_3_cell": {
    "type": "string",
    "value": "Item 3b"
  }
}
```



