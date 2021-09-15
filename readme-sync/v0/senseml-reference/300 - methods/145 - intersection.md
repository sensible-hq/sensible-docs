---
title: "Intersection"
hidden: false
---
Extracts a target line at the intersection of a horizontal line defined by an anchor, and a vertical line defined by a second anchor:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_example_1.png)

For example, the Intersection method is an alternative to the Row method when a table contains empty cells. (A row's tiebreaker, like "second", can return lines from unintended columns if there are empty cells).

[**Parameters**](doc:intersection#section-parameters)
[**Examples**](doc:intersection#section-examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                           | value                        | description                                                  |
| :---------------------------- | :--------------------------- | :----------------------------------------------------------- |
| id (**required**)             | `intersection`               |                                                              |
| verticalAnchor (**required**) | Anchor object                | An anchor object that defines a vertical line. Sensible extracts the line that is at the intersection of this vertical line, and the horizontal line defined by the field's anchor. Both lines pass through the midpoints of the anchors' boundaries. |
| offsetX                       | number in inches. default: 0 | Offsets the vertical line defined by the Vertical Anchor parameter to the left or right. |
| offsetY                       | number in inches. default: 0 | Offsets the horizontal line defined by the anchor up or down. |

Examples
=====

The following example shows using the Intersection method to extract a cell from a table that has empty cells.

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

The following image shows the example PDF used with this example config:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_example_2.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/intersection_example.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "col_3_cell": {
    "type": "string",
    "value": "Item 3b"
  }
}
```



