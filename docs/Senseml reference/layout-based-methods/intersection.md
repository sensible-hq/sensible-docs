---
title: Intersection
excerpt: Find text at row/column intersections
deprecated: false
hidden: false
metadata:
  title: ''
  description: Find text at row/column intersections
  robots: index
next:
  description: ''
---
Extracts a target line at the intersection of a line defined by an anchor, and a second line defined by a second anchor:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/intersection_1.png)

For example, the Intersection method is an alternative to the Row method when a table contains optionally empty cells. A row's tiebreaker can return lines from unintended columns if cells are unpredictably populated.

[**Parameters**](doc:intersection#parameters)<br />[Examples](doc:intersection#examples)

# Parameters

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                                                         | value                                       | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| :---------------------------------------------------------- | :------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| id (**required**)                                           | `intersection`                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| verticalAnchor<br />or<br />horizontalAnchor (**required**) | Anchor object                               | An anchor object that defines an intersection with the field-level anchor. Sensible extracts lines that overlap to any extent with the intersection point of two perpendicular lines that each bisect one of the two anchors.<br /> When horizontal and vertical anchors are on different pages, the horizontal anchor determines which page Sensible find the anchor on.<br />To extract multiple intersections using one field, specify `"match":"all"` for the anchor at the field level. For examples, see examples 2 and 3.                                                                                                                                                                                                                                          |
| offsetX                                                     | number in inches. default: 0                | For the anchor bisected by a vertical line, offsets the line. Positive values offset to the right, negative values offset to the left.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| offsetY                                                     | number in inches. default: 0                | For the anchor bisected by a horizontal line, offsets the line. Positive values offset down the page, negative values offset up the page.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| height                                                      | number in inches. default: 0                | A non-zero number creates a region centered at the intersection point. If you also specify width, the region is a rectangle; otherwise, it's a vertical line. Sensible extracts lines contained in the region. For the full definition of "contained," see the [Region](doc:region) method. <br />If you don't specify this parameter, Sensible extracts lines that overlap to any extent with the intersection point.                                                                                                                                                                                                                                                                                                                                                    |
| width                                                       | number in inches<br />or `auto`. default: 0 | A non-zero number creates a region centered at the intersection point. If you also specify height, the region is a rectangle; otherwise, it's a horizontal line. Sensible extracts lines contained in the region. For the full definition of "contained," see the [Region](doc:region) method. If you specify `auto`, the region's width is equal to the width of the line specified by the Vertical Anchor parameter.  Sensible recommends  `auto` if you expect a column heading that you're anchoring on to be at least as wide as your target text. <br />If you don't specify this parameter, Sensible extracts lines that overlap to any extent with the intersection point.                                                                                        |
| percentOverlapX                                             | number. default: 0.9                        | If you use the Width or Height parameters to extract lines contained in a region, then you can configure the strictness of the criteria by which a region "contains" a line using this parameter. <br />By default, Sensible determines that a region contains a line if their widths overlap by more than 90%  of the smaller of the two's width. Loosen the criteria if a line can partly fall outside a region. For example,  if you set this parameter to 0.5, then Sensible determines that a region contains a line if their widths overlap by more than 50%  of the smaller of the two's width. Sensible recommends setting this parameter to 0 so that you accept any amount of overlap. Note the line must also meet the Percent Overlap Y parameter's criteria. |
| percentOverlapY                                             | number. default: 0.8                        | Configures strictness in the same manner as the Percent Overlap X parameter, but applies to height instead of width.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

## Syntax example

The following example shows the preceding parameters documented with in-line comments.

```json
/* Sensible uses JSON5 to support in-line comments*/    
{
  "id": "col_3_row_2_cell", /* user-friendly ID for extracted target data */
  "anchor": "row 2 label", /* defines the horizontal axis of the intersection (the row) */
  "method": {
    "id": "intersection",
    "verticalAnchor": "col 3 heading", /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
    "offsetX": 0, /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
    "offsetY": 0, /* default: 0. offset the horizontal line up (negative) or down (positive) in inches */
    "width": 0, /* default: 0. (zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
    "height": 0, /* default: 0 (same as width, but for height of the intersection region.) */
    "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be "inside" the region defined by Width or Height parameters; 0 accepts any overlap (recommended) */
    "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
  }
}
```

# Examples

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
        "height": 0.4,
        "percentOverlapX": 0,
        "percentOverlapY": 0
        
      }
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/intersection_2.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/intersection.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------ |

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
         and the vertical anchor (the FIRST instance of "naic") */
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
           this config specifies 0 to accept any overlap */
        "percentOverlapX": 0,
        "percentOverlapX": 0
      }
    }
  ]
}
```

**Example document**<br />The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/intersection_percent_overlap.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/intersection_percent_overlap.pdf) |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |

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
      "anchor": "option", /* defines the vertical axis of the intersection (the column) */
      "match": "all", /* creates an intersection for each instance of "option", enabling extraction of multiple cells from a row */
      "method": {
        "id": "intersection",
        "horizontalAnchor": "maximum", /* defines the horizontal axis (the row) */
        "width": 1.5,
        "height": 0.5,
        "percentOverlapX": 0,
        "percentOverlapX": 0
      }
    }
  ]
}
```

**Example document**<br />The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/intersection_horizontal.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/intersection_horizontal.pdf) |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------- |

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
