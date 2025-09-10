---
title: "Box"
hidden: true

---

Extract lines inside a box. This method works by default with boxes that have a light background and dark, continuous borders. 

[**Parameters**](doc:box#parameters)
[**Examples**](doc:box#examples)

Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key             | value                | description                                                  |
| --------------- | -------------------- | ------------------------------------------------------------ |
|                 |                      |                                                              |
|                 |                      |                                                              |
|                 |                      |                                                              |
|                 |                      |                                                              |
| percentOverlapX | number. default: 0.9 | Configures the strictness of the criteria by which a box "contains" a line using this parameter.<br/>By default, Sensible determines that a box contains a line if they overlap by more than 90%  of the smaller of the two's width. Loosen the criteria if a line can partly fall outside a box. For example,  if you set this parameter to 0.5, then Sensible determines that a box contains a line if they overlap by more than 50%  of the smaller of the two's width. Note the line must also meet the Percent Overlap Y parameter's criteria. See [Lines overlapping box](doc:box#example-lines-overlapping-box) for an example. |
| percentOverlapY | number. default: 0.8 | Configures the strictness of the criteria by which a box "contains" a line using this parameter. For information about the criteria, see the [Region](doc:region) method.<br/>By default, Sensible determines that a box contains a line if their heights overlap by more than 80%  of the smaller of the two's height. Loosen the criteria if a line can partly fall outside a box. For example, if you set this parameter to 0.4, then Sensible determines that a box contains a line if they overlap by more than 40%  of the smaller of the two's height. Note the line must also meet the Percent Overlap X parameter's criteria. See [Lines overlapping box](doc:box#example-lines-overlapping-box) for an example. |
|                 |                      |                                                              |
|                 |                      |                                                              |
|                 |                      |                                                              |

Examples
====



## Example: Lines overlapping box

The following example shows extracting lines that partly fall inside a box.

**Config**

```json
{
  "fields": [
    {
      "id": "insured_item",
      /* extract all text (minus anchor) in the box containing the text  "subject" */
      "anchor": "subject",

      "method": {
        "id": "box",
        "position": "left",
        /* loosen the criteria for a box to 'contain' a line
           In detail, sets the percent by which 
           the box's and the
           line's widths must overlap in order to 
           extract the line.   
        */
        "overlapX": 0.5
      }
    }
  ]
}

```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_overlap.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/box_overlap.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "insured_item": {
    "type": "string",
    "value": "House"
  }
}
```



Box coordinates
----

You can use the Offset X and Offset Y parameters:

- to anchor on text *outside* the target box, for example, if all the box's contents are variable.
- as an alternative to the Offset Boxes parameter. Offsets provide faster performance, but are more sensitive to inconsistent box positioning across documents and require more configuration. 

The following example shows the same document as the Offset Boxes example, but uses distances in inches rather than boxes to define the offsets.



**Config**

```json
{
  "fields": [
    {
      "id": "auto_limit_in_policy_1",
      "anchor": "auto only",
      "match": "first",
      "method": {
        "id": "box",
        "offsetX": 1.5,
        "offsetY": 0.0
      }
    },
    {
      "id": "injury_limit_in_policy_2",
      "anchor": "dollar amount",
      "match": "last",
      "method": {
        "id": "box",
        "offsetX": 0.0,
        "offsetY": 1.0
      }
    },
    {
      "id": "oddly_formatted_boxes",
      "anchor": "spanning multiple",
      "method": {
        "id": "box",
        "offsetX": 1.0,
        "offsetY": 2.5
      }
    },
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_offset_3.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/box_offset.pdf) |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |

The red arrows in the preceding image show the offsets in inches from the point defined by the Position parameter. The green dots move as you adjust the inches coordinates, so you can visually tweak your measurements in the Sensible app.

**Output**

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

Troubleshoot box recognition
----

Use the Position parameter to fine tune box recognition.

**PROBLEM**

In the following error example, Sensible searches for borders starting from the middle point of the anchor line's left boundary  (`"position": "left"`). Since the point (the green dot) overlaps the box border, Sensible can't recognize the box.

Config

```json
{
  "fields": [
    {
      "id": "box_test",
      "anchor": "big anchor text",
      "method": {
        "id": "box",
        "position": "left",
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

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_position_left.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/box_recognition.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**SOLUTION**

If you specify `"position": "right"`, the green dot is far enough inside the borders that Sensible  recognizes the box:

Config

```json
{
  "fields": [
    {
      "id": "box_test",
      "anchor": "big anchor text",
      "method": {
        "id": "box",
        "position": "right",
        "wordFilters": [
          "cramped"
        ]
      }
    }
  ]
}
```

Example document

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_position_right.png)

Output

```json
{
  "box_test": {
    "type": "string",
    "value": " with some text to extract"
  }
}
```

Notes
====

The Box method is an alternative to the [Region method](doc:region) that requires less configuration and is slightly slower. Use the Region method instead of the Box method for faster performance, or if the borders of a box are incomplete or discontinuous.