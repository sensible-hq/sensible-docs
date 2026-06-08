---
title: Box
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Extract text from a bordered box'
  robots: index
next:
  description: ''
---
Extract lines inside a box. This method works by default with boxes that have a light background and dark, continuous borders.

[**Parameters**](doc:box#parameters)  
[**Examples**](doc:box#examples)

# Parameters

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key               | value                                                        | description                                                  |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**) | `box`                                                        | Extracts all lines in a box. If you define an anchor that's outside the box borders, then use offset parameters to define a point that's inside the box borders so that Sensible recognizes the box. |
| position          | `right`, `left`, `below`, `above`. When unspecified, defaults to center of the anchor line's bounding box | Use this parameter to fine tune box recognition. Defines the starting point for the box recognition search relative to the anchor line's boundaries. For example, `right` specifies starting at the midpoint of the anchor line's right boundary, and `below` specifies starting at the midpoint of the anchor line's bottom boundary.  Sensible searches outward from this point until it finds dark pixels signifying the box border. <br /> For an example of how to use this parameter, see the following [Examples section](doc:box#examples). |
| offsetX           | number in inches default: 0                                  | Searches for a box starting at a point offset from the point defined by the Position parameter. Positive values offset to the right, negative values offset to the left. For an example of how to use this parameter, see the following [Examples section](doc:box#examples). |
| offsetY           | number in inches default: 0                                  | Searches for a box starting at a point offset from the point defined by the Position parameter. Positive values offset down the page, negative values offset up the page.  For an example of how to use this parameter, see the following [Examples section](doc:box#examples). |
| percentOverlapX   | number. default: 0.9                                         | Configures the strictness of the criteria by which a box "contains" a line using this parameter.<br />By default, Sensible determines that a box contains a line if they overlap by more than 90%  of the smaller of the two's width. Loosen the criteria if a line can partly fall outside a box. For example,  if you set this parameter to 0.5, then Sensible determines that a box contains a line if they overlap by more than 50%  of the smaller of the two's width. Note the line must also meet the Percent Overlap Y parameter's criteria. See [Lines overlapping box](doc:box#example-lines-overlapping-box) for an example. |
| percentOverlapY   | number. default: 0.8                                         | Configures strictness in the same manner as the Percent Overlap X parameter, but applies to height instead of width. |
| offsetBoxes       | object. default: `none`                                      | Recognize a box offset from the point defined in the Position parameter by a number of contiguous boxes that share borders. For example, use this parameter for tables or grids where borders surround every cell. Contains the following parameters:<br />- `direction`: The direction to search in (`above, below, right, left`, relative to the starting box.<br />- `number`: The number of boxes to offset by.<br />For an example of how to use this parameter, see the following [Examples section](doc:box#examples). |
| darknessThreshold | number between 0 and 1. default: 0.9                         | The brightness threshold below which to consider a pixel a box boundary. White is 1.0. Configure this parameter for checkboxes with dark backgrounds relative to the surrounding background.<br />If the document has a white background, the default value is 0.9.<br />If the document has dark or mottled background, for example as the result of a scan, then Sensible automatically chooses a default value based on the amount of contrast in the document. For an example of how to use this parameter, see the following [Examples section](doc:box#examples). |
| includeAnchor     | `true`, `false`. default: false                              | If true, includes anchors lines that are inside the box borders in the method output. Ignores anchor lines that are outside box borders. |

## Syntax example

```json
    {
      "id": "field1", /* user-friendly ID for extracted target data */
      "anchor": "some text" /* an anchor is text that always occurs in the same position relative to your target data. Without an anchor, Sensible wouldn't know which page to search in for your target data. */,
      "method": {
        "id": "box", /* extracts all lines inside a box */
        "position": "right", /* starting point for searching outward in all directions until Sensible recognizes a box. point is relative to anchor boundaries. default: center of anchor line's bounding box. enums: right | left | below | above */
        "offsetX": 0, /* default: 0. shifts box search starting point horizontally from Position parameter. positive: right, negative: left */
        "offsetY": 0, /* default: 0. shifts box search starting point vertically from Position parameter. positive: down, negative: up */
        "percentOverlapX": 0.9, /* default: 0.9. minimum fractional width overlap for a line to be "contained" in the box */
        "percentOverlapY": 0.8, /* default: 0.8. minimum fractional height overlap for a line to be "contained" in the box */
        "offsetBoxes": { /* default: none. recognize a box offset from the starting box by a number of contiguous boxes sharing borders */
          "direction": "right", /* direction in which to search for the offset box. enums: above | below | right | left */
          "number": 1 /* number of boxes to offset by */
        },
        "darknessThreshold": 0.9, /* default: 0.9. brightness threshold below which a pixel is considered a box border. white is 1.0 */
        "includeAnchor": false /* default: false. if true, includes anchor lines inside box borders in the output */
      }
    }
```

# Examples

## Simple box

The following example shows extracting a dollar amount from a box in a 1099 form, based on anchor text matching in the box.

**Config**

```json
{
 "fields": [
   {
     /* find the first box in the document 
         containing the text 'rents'
        and return all the other text in the box */
     "id": "rents_income", /* user-friendly ID for extracted target data */
     "type": "currency", /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
     "method": {
       "id": "box", /* extracts all lines inside a box */
     },
     "anchor": "rents" /* text that always occurs in the same position relative to your target data */
   }
 ]
}
```

**Example document**  
The following image shows the example document used with this example config:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_1099.png" />

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/box_1099.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "rents_income": {
    "source": "4,200",
    "value": 4200,
    "unit": "$",
    "type": "currency"
  }
}
```

## Dark box

The following example shows extracting text from a box with a dark background and light text using the `darknessThreshold` parameter.

**Config**

```json
{
  "fields": [
    {
      "id": "dark_box", /* user-friendly ID for extracted target data */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        "darknessThreshold": 0.8 /* lowers the brightness threshold for box border detection; use for boxes with dark backgrounds. default: 0.9, white is 1.0 */
      },
      "anchor": "dark box with light text", /* text that always occurs in the same position relative to your target data */
    }
  ]
}
```

**Example document**  
The following image shows the example document used with this example config:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_dark.png" />

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/box_dark.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "dark_box": {
    "type": "string",
    "value": "Here’s some more text"
  }
}
```

## Offset boxes

The following example shows recognizing boxes relative to other boxes using the Box Offset parameter.

**Config**

```json
{
  "fields": [
    {
      "id": "auto_limit_in_policy_1", /* user-friendly ID for extracted target data */
      "anchor": "auto only", /* text that always occurs in the same position relative to your target data */
      "match": "first", /* use the first occurrence of the anchor */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        "offsetBoxes": { /* recognize a box offset from the starting box by contiguous boxes sharing borders */
          "direction": "right", /* search to the right of the starting box */
          "number": 1 /* offset by 1 box to the right */
        }
      }
    },
    {
      "id": "injury_limit_in_policy_2", /* user-friendly ID for extracted target data */
      "anchor": "dollar amount", /* text that always occurs in the same position relative to your target data */
      "match": "last", /* use the last occurrence of the anchor */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        "offsetBoxes": { /* recognize a box offset from the starting box by contiguous boxes sharing borders */
          "direction": "below", /* search below the starting box */
          "number": 2 /* offset by 2 boxes below */
        }
      }
    },
    {
      "id": "offset_boxes", /* user-friendly ID for extracted target data */
      "anchor": "spanning multiple", /* text that always occurs in the same position relative to your target data */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        "offsetBoxes": { /* recognize a box offset from the starting box by contiguous boxes sharing borders */
          "direction": "below", /* search below the starting box */
          "number": 3 /* offset by 3 boxes below */
        }
      }
    },
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_offset.png" />


| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/box_offset.pdf) |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```
{
  "auto_limit_in_policy_1": {
    "type": "string",
    "value": "$2,000"
  },
  "injury_limit_in_policy_2": {
    "type": "string",
    "value": "$4,000"
  },
  "offset_boxes": {
    "type": "string",
    "value": "Third offset box"
  }
}
```

**Notes**

The following image illustrates how Sensible recognizes offset boxes after the first box:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_offset_2.png" />

1. Recognize the starting box by searching for the dark borders of the box. The search starts at the green dot defined by the Position parameter. The search expansion is in all directions, not just the cardinal directions shown by the red arrows in the image.
2. Find a bottom border (`"direction": "below"`) that's shared with the next box. Choose a point ( represented as the second green dot) on the bottom border that's in the middle of the starting box's border and that's just inside the next box's borders.
3. Search from that point  to recognize the next box's borders.
4. Repeat steps 2 and 3 for the next box.

When boxes are complex (inconsistently sized, spanned, or aligned, as in the preceding image), Sensible's  methods for recognizing boxes can be correspondingly complex. In such cases, use the Sensible app to [visually examine](doc:color) and understand the extraction. Or, see the following example for an alternative approach.

## Example: Lines overlapping box

The following example shows extracting lines that partly fall inside a box.

**Config**

```json
{
  "fields": [
    {
      "id": "insured_item", /* user-friendly ID for extracted target data */
      "anchor": "subject", /* text that always occurs in the same position relative to your target data */

      "method": {
        "id": "box", /* extracts all lines inside a box */
        "position": "left", /* starts box recognition at the midpoint of the anchor line's left boundary */
        /* loosen the criteria for a box to 'contain' a line
           In detail, sets the percent by which 
           the box's and the
           line's widths must overlap in order to 
           extract the line.   
        */
        "percentOverlapX": 0.5 /* minimum fractional width overlap for a line to be "contained" in the box; lower values allow lines that partly fall outside the box. default: 0.9 */
      }
    }
  ]
}

```

**Example document**  
The following image shows the example document used with this example config:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_overlap.png" />

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/box_overlap.pdf) |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "insured_item": {
    "type": "string",
    "value": "House"
  }
}
```

## Box coordinates

You can use the Offset X and Offset Y parameters:

* to anchor on text _outside_ the target box, for example, if the box's title is outside the box.
* as an alternative to the Offset Boxes parameter. Offsets provide faster performance, but are more sensitive to inconsistent box positioning across documents and require more configuration.

The following example shows the same document as the Offset Boxes example, but uses distances in inches rather than boxes to define the offsets.

**Config**

```json
{
  "fields": [
    {
      "id": "auto_limit_in_policy_1", /* user-friendly ID for extracted target data */
      "anchor": "auto only", /* text that always occurs in the same position relative to your target data */
      "match": "first", /* use the first occurrence of the anchor */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        "offsetX": 1.5, /* shifts box search point to the right from position (positive: right, negative: left) */
        "offsetY": 0.0 /* no vertical shift from position (positive: down, negative: up) */
      }
    },
    {
      "id": "injury_limit_in_policy_2", /* user-friendly ID for extracted target data */
      "anchor": "dollar amount", /* text that always occurs in the same position relative to your target data */
      "match": "last", /* use the last occurrence of the anchor */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        "offsetX": 0.0, /* no horizontal shift from position (positive: right, negative: left) */
        "offsetY": 1.0 /* shifts box search point down from position (positive: down, negative: up) */
      }
    },
    {
      "id": "oddly_formatted_boxes", /* user-friendly ID for extracted target data */
      "anchor": "spanning multiple", /* text that always occurs in the same position relative to your target data */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        "offsetX": 1.0, /* shifts box search point to the right from position (positive: right, negative: left) */
        "offsetY": 2.5 /* shifts box search point down from position (positive: down, negative: up) */
      }
    },
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_offset_3.png" />

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/box_offset.pdf) |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------- |

The red arrows in the preceding image show the offsets in inches from the point defined by the Position parameter. The green dots move as you adjust the inches coordinates, so you can visually tweak your measurements in the Sensible app.

**Output**

```json
{
  "auto_limit_in_policy_1": {
    "type": "string",
    "value": "$2,000"
  },
  "injury_limit_in_policy_2": {
    "type": "string",
    "value": "$6,000"
  },
  "oddly_formatted_boxes": {
    "type": "string",
    "value": "Third offset box"
  }
}
```

## Troubleshoot box recognition

Use the Position parameter to fine tune box recognition.

**PROBLEM**

In the following error example, Sensible searches for borders starting from the middle point of the anchor line's left boundary  (`"position": "left"`). Since the point (the green dot) overlaps the box border, Sensible can't recognize the box.

Config

```json
{
  "fields": [
    {
      "id": "box_test", /* user-friendly ID for extracted target data */
      "anchor": "big anchor text", /* text that always occurs in the same position relative to your target data */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        /* With the following position, Sensible can't recognize the box 
        because the starting point (green dot) overlaps the box border*/
        "position": "left", /* starts box recognition at midpoint of anchor's left boundary */
        "wordFilters": [
          "cramped"
        ]
      }
    }
  ]
}
```

Example document

The following image shows the example document used with this example config:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_position_left.png" />

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/box_recognition.pdf) |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |

**SOLUTION**

If you specify `"position": "right"`, the green dot is far enough inside the borders that Sensible  recognizes the box:

Config

```json
{
  "fields": [
    {
      "id": "box_test", /* user-friendly ID for extracted target data */
      "anchor": "big anchor text", /* text that always occurs in the same position relative to your target data */
      "method": {
        "id": "box", /* extracts all lines inside a box */
        /* change the starting position with the Position parameter or (not shown) with the Offset parameters */
        "position": "right", /* starts box recognition at midpoint of anchor's right boundary, inside box borders */
        "wordFilters": [
          "cramped"
        ]
      }
    }
  ]
}
```

Example document

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_position_right.png" />

Output

```json
{
  "box_test": {
    "type": "string",
    "value": " with some text to extract"
  }
}
```

# Notes

The Box method is an alternative to the [Region method](doc:region) that requires less configuration and is slightly slower. Use the Region method instead of the Box method for faster performance, or if the borders of a box are incomplete or discontinuous.
