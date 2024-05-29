---
title: "Intersection"
hidden: false
---
Extracts a target line at the intersection of a horizontal line defined by an anchor, and a vertical line defined by a second anchor:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_1.png)

For example, the Intersection method is an alternative to the Row method when a table contains optionally empty cells.  A row's tiebreaker can return lines from unintended columns if cells are unpredictably populated.

[**Parameters**](doc:intersection#parameters)
[**Examples**](doc:intersection#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.


| key                           | value                        | description                                                  |
| :---------------------------- | :--------------------------- | :----------------------------------------------------------- |
| id (**required**)             | `intersection`               |                                                              |
| verticalAnchor (**required**) | Anchor object                | An anchor object that defines a vertical line that bisects that anchor. Sensible extracts the line that's at the intersection of this vertical line and the horizontal line defined by the field's anchor. The Vertical Anchor can be on a different page from the anchor. |
| offsetX                       | number in inches. default: 0 | Offsets the vertical line that bisects the vertical anchor.  Positive values offset to the right, negative values offset to the left. |
| offsetY                       | number in inches. default: 0 | Offsets the horizontal line that bisects the anchor. Positive values offset down the page, negative values offset up the page. |
| height                        | number in inches. default: 0 | Specifies to create a rectangular region centered at the intersection point. Sensible extracts lines contained in the region. For the full definition of "contained," see the [Region](doc:region) method. <br/>If you don't specify this parameter, Sensible extracts lines that overlap to any extent with the intersection point. |
| width                         | number in inches. default: 0 | Specifies to create a rectangular region centered at the intersection point. Sensible extracts lines contained in the region. For the full definition of "contained," see the [Region](doc:region) method. <br/>If you don't specify this parameter, Sensible extracts lines that overlap to any extent with the intersection point. |
| percentOverlapX               | number. default: 0.9         | If you use the Width or Height parameters to extract lines contained in a region, then you can configure the strictness of the criteria by which a region "contains" a line using this parameter. For information about the criteria, see the [Region](doc:region) method.<br/>Configures the percent by which a region and line's x-extant must overlap in order for Sensible to determine that the region "contains" the line. For example, if you set this parameter to 0.5, then Sensible determines that a region contains a line if their boundary boxes overlap by more than 50%  of the smaller of the two's width. |
| percentOverlapY               | number. default: 0.8         | If you use the Width or Height parameters to extract lines contained in a region, then you can configure the strictness of the criteria by which a region "contains" a line using this parameter. For information about the criteria, see the [Region](doc:region) method.<br/>Configures the percent by which a region and line's y-extant must overlap in order for Sensible to determine that the region "contains" the line. For example, if you set this parameter to 0.4, then Sensible determines that a region contains a line if their boundary boxes overlap by more than 40%  of the smaller of the two's height. |


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
        "verticalAnchor": "col3",
        "width": 1.2,
        "height": 0.4
      }
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_2.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/intersection.pdf) |
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



