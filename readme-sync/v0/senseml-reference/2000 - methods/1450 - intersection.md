---
title: "Intersection"
hidden: false
---
Extracts a target line at the intersection of a line defined by an anchor, and a second line defined by a second anchor:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_1.png)

For example, the Intersection method is an alternative to the Row method when a table contains optionally empty cells.  A row's tiebreaker can return lines from unintended columns if cells are unpredictably populated.

[**Parameters**](doc:intersection#parameters)
[**Examples**](doc:intersection#examples)

Parameters
=====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.


| key                                                       | value                        | description                                                  |
| :-------------------------------------------------------- | :--------------------------- | :----------------------------------------------------------- |
| id (**required**)                                         | `intersection`               |                                                              |
| verticalAnchor<br/>or<br/>horizontalAnchor (**required**) | Anchor object                | An anchor object that defines an intersection with the field-level anchor. Sensible extracts lines that overlap to any extent with the intersection point of two perpendicular lines that bisect the two anchors. This anchor parameter can be on a different page from the field-level anchor. <br/>To extract multiple intersections using one field, specify `"match":"all"` for the anchor at the field level. For examples, see examples 2 and 3. |
| offsetX                                                   | number in inches. default: 0 | For the anchor bisected by a vertical line, offsets the line.   Positive values offset to the right, negative values offset to the left. |
| offsetY                                                   | number in inches. default: 0 | For the anchor bisected by a horizontal line, offsets the line. Positive values offset down the page, negative values offset up the page. |
| height                                                    | number in inches. default: 0 | Specifies to create a rectangular region centered at the intersection point. Sensible extracts lines contained in the region. For the full definition of "contained," see the [Region](doc:region) method. <br/>If you don't specify this parameter, Sensible extracts lines that overlap to any extent with the intersection point. |
| width                                                     | number in inches. default: 0 | Specifies to create a rectangular region centered at the intersection point. Sensible extracts lines contained in the region. For the full definition of "contained," see the [Region](doc:region) method. <br/>If you don't specify this parameter, Sensible extracts lines that overlap to any extent with the intersection point. |
| percentOverlapX                                           | number. default: 0.9         | If you use the Width or Height parameters to extract lines contained in a region, then you can configure the strictness of the criteria by which a region "contains" a line using this parameter. For information about the criteria, see the [Region](doc:region) method.<br/>Configures the percent by which a region and line's x-extant must overlap in order for Sensible to determine that the region "contains" the line. For example, if you set this parameter to 0.5, then Sensible determines that a region contains a line if their boundary boxes overlap by more than 50%  of the smaller of the two's width. |
| percentOverlapY                                           | number. default: 0.8         | If you use the Width or Height parameters to extract lines contained in a region, then you can configure the strictness of the criteria by which a region "contains" a line using this parameter. For information about the criteria, see the [Region](doc:region) method.<br/>Configures the percent by which a region and line's y-extant must overlap in order for Sensible to determine that the region "contains" the line. For example, if you set this parameter to 0.4, then Sensible determines that a region contains a line if their boundary boxes overlap by more than 40%  of the smaller of the two's height. |


Examples
=====

### Example 1: Empty cells in tables

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



### Example 2: Variable text positions

The following example shows extracting variably positioned lines by relaxing the criteria by which Sensible determines that a region at the intersection point "contains" lines.

**Config**

```json
{
  "fields": [
    {
      "id": "a_insurers",
      /* extract text at the intersection of "insurer a"
         and the vertical anchor ("naic") */
      "anchor": "insurer a",
      /* create an intersection for each instance of "insurer a" */  
      "match": "all",
      "method": {
        "id": "intersection",
        "verticalAnchor": "naic",
        /* create a zero-height, 1"-wide rectangle at the
           intersection point and extract all lines that overlap
           with the rectangle  */
        "width": 1,
        "height": 0,
        /* Sets the percent by which 
           the rectangle's and the
           line's widths must overlap in order to 
           extract the line. 
           To extract variably positioned lines,
           this config specifies a lower percent
           than the default */
        "percentOverlapX": 0.5
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_percent_overlap.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/intersection_percent_overlap.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "a_insurers": [
    {
      "type": "string",
      "value": "39993"
    },
    {
      "type": "string",
      "value": "16535"
    },
    {
      "type": "string",
      "value": "72222"
    }
  ]
}
```

### Example 3: Multiple cells in row

The following example shows using a horizontal anchor to extract multiple cells from a row. This is an alternative when it's not possible to use the [Row](doc:row) method.

**Config**

```json
{
  "fields": [
    {
      "id": "max_limit_options",
      "anchor": "option",
      /* create an intersection for each instance of "option" */  
      "match": "all",
      "method": {
        "id": "intersection",
        "horizontalAnchor": "maximum",
        "width": 1.5,
        "height": 0.5
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_horizontal.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/intersection_horizontal.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "max_limit_options": [
    {
      "type": "string",
      "value": "$2M"
    },
    {
      "type": "string",
      "value": "$3M"
    }
  ]
}
```
