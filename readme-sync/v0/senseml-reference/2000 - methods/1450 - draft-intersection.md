---
title: "Intersection"
hidden: true
---
Extracts a target line at the intersection of a horizontal line defined by an anchor, and a vertical line defined by a second anchor:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_1.png)

For example, the Intersection method is an alternative to the Row method when a table contains empty cells. A row's tiebreaker, like "second", can return lines from unintended columns if there are empty cells.

[**Parameters**](doc:intersection#parameters)
[**Examples**](doc:intersection#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.


| key                           | value                        | description                                                  |
| :---------------------------- | :--------------------------- | :----------------------------------------------------------- |
| id (**required**)             | `intersection`               |                                                              |
| verticalAnchor (**required**) | Anchor object                | An anchor object that defines a vertical line that bisects that anchor. Sensible extracts the line that's at the intersection of this vertical line, and the horizontal line defined by the field's anchor. The Vertical Anchor can be on a different page from the anchor. |
| offsetX                       | number in inches. default: 0 | Offsets the vertical line that bisects the vertical anchor.  Positive values offset to the right, negative values offset to the left. |
| offsetY                       | number in inches. default: 0 | Offsets the horizontal line that bisects the anchor. Positive values offset down the page, negative values offset up the page. |
| height                        | number in inches. default: 0 | When specified, Sensible creates a rectangular region centered at the intersection point. Sensible extracts lines that overlap to any extent with the region. If you don't specify the Width parameter, Sensible sets it to 0. |
| width                         | number in inches. default: 0 | When specified, Sensible creates a rectangular region centered at the intersection point. Sensible extracts lines that overlap to any extent with the region. If you don't specify the Height parameter, Sensible sets it to 0. |

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

**Example document**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_2.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/intersection.pdf) |
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



