---
title: Region
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Extract from a  rectangular region defined in inch coordinates'
  robots: index
next:
  description: ''
---
Extracts data in a rectangular region, defined in inches. The region extracts lines contained inside the region (for the definition of "contained", see the Parameters section). 

In general, use this method:

* for faster performance compared to the Box method
* when you want to extract data from an area whose formatting doesn't fit other SenseML methods. For example, you can use this method instead of the Label method for widely separated anchors and target lines.

[**Parameters**](doc:region#parameters)\
[**Examples**](doc:region#examples)\
[**Notes**](doc:region#notes)

# Parameters

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                    | value                             | description                                                  |
| ---------------------- | --------------------------------- | ------------------------------------------------------------ |
| id (**required**)      | `region`                          | Extracts lines contained in the region, where "contained" means:<br/>  - condition 1: the region and the line's widths overlap by more than 90% of the smaller of the two's width.<br/> AND<br/> - condition 2: the region and the line's heights overlap by more than 80% of the smaller of the two's height. |
| start (**required**)   | `above`, `below`, `left`, `right` | Defines the initial coordinates of the region's top-left corner (its "start point") relative to the anchor line's boundaries. For example,  `right`  specifies that the corner is at the midpoint of the anchor line's right boundary, and `below` specifies that the corner is at the midpoint of the anchor line's bottom boundary. |
| offsetX (**required**) | number                            | Horizontally shifts the region's top-left corner from the point defined in the Start parameter by the specified number of inches. Positive values offset to the right, negative values offset to the left.<br/>You can visually determine this number in the Sensible app by changing the number and watching the green region box resize, or by clicking a point in the document in the Sensible app, then dragging to display inch dimensions. |
| offsetY (**required**) | number                            | Vertically shifts the region's top-left corner from the point defined in the Start parameter by the specified number of inches. Positive values offset down the page, negative values offset up the page.<br/>You can visually determine this number in the Sensible app by changing the number and watching the green region box resize, or by clicking a point in the document in the Sensible app, then dragging to display inch dimensions. |
| width (**required**)   | number                            | The width in inches of the region. <br/>You can visually determine this number in the Sensible app by changing the number and watching the green region box resize, or by clicking a point in the document in the Sensible app, then dragging to display inch dimensions. |
| height (**required**)  | number                            | The height in inches of the region. <br/>You can visually determine this number in the Sensible app by changing the number and watching the green region box resize, or by clicking a point in the document in the Sensible app, then dragging to display inch dimensions. |
| isAbsoluteOffset       | boolean. default: `false`         | Makes the offsets relative to the 0,0 origin at the top left of the page rather than to the point defined in the Start parameter. |

## Syntax example

```json
    {
      "id": "field1", /* user-friendly ID for extracted target data */
      "anchor": "some text" /* an anchor is text that always occurs in the same position relative to your target data. Without an anchor, Sensible wouldn't know which page to search in for your target data. */,
      "method": {
        "id": "region", /* extracts lines contained in a defined rectangular region */
        "start": "below", /* initial coordinates for region's top-left corner relative to anchor's boundaries. enums: above | below | left | right */
        "offsetX": 0.00, /* horizontally shifts the region's top-left corner from the Start parameter by specified number of inches. positive: right, negative: left */
        "offsetY": 0.00, /* vertically shifts the region's top-left corner from the Start parameter by the specified number of inches. positive: down, negative: up */
        "width": 0.00, /* width of the region in inches */
        "height": 0.00, /* height of the region in inches */
        "isAbsoluteOffset": false /* default: false. if true, offsets are relative to the top-left of the page, not the Start parameter */
      }
    }
```

# Examples

The following example shows extracting a social security number from a W-9 form by defining a region to extract.

**Config**

```json
{
  "fields": [
    {
      "id": "SSN", /* user-friendly ID for extracted target data */
      "anchor": { /* an anchor is text that always occurs in the same position relative to your target data. */
        "match": { /* Match object specifying how to find the anchor line */
          "type": "equals", /* matching line must equal the string exactly */
          "text": "Social security number", /* string to match */
          "isCaseSensitive": true /* match is case-sensitive */
        }
      },
      "method": {
        "id": "region", /* extracts lines contained in a defined rectangular region */
        "start": "below", /* region's top-left corner starts at midpoint of anchor's bottom boundary */
        "width": 2.15, /* region width in inches */
        "height": 0.25, /* region height in inches */
        "offsetX": -0.55, /* shifts region's top-left corner to the left from the Start parameter by the specified number of inches (positive: right, negative: left) */
        "offsetY": 0.1 /* shifts region's top-left corner down from the Start parameter by the specified number of inches (positive: down, negative: up */
      }
    }
  ]
}
```

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/region_ssn.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/region_w9.pdf) |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "SSN": {
    "type": "string",
    "value": "1 2 3 4 5 7 8 9 3 – –"
  }
}
```

# Notes

If the region that you want to extract is a box that's bordered with dark lines, you can use the [Box method](doc:box) instead of the Region method.
