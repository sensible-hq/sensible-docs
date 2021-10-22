---
title: "Nearest checkbox"
hidden: true
---
Searches for the checkbox nearest to the anchor in any direction, and returns a boolean indicating if it is selected or unselected. 

Use this method when the Checkbox method can't recognize a checkbox. The advantage of the Nearest Checkbox method is that it is more flexible and requires less configuration. The disadvantage is that is slower than the Checkbox method. 



[**Parameters**](doc:nearestcheckbox#parameters)
[**Examples**](doc:nearestcheckbox#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                     | values                       | description                                                  |
| ----------------------- | ---------------------------- | ------------------------------------------------------------ |
| id (**required**)       | `nearestCheckbox`            | Sensible returns true if the selection mark is a checkmark, "Y", or "X" character.  Sensible returns false if the selection mark is missing or any other character.  This method can recognize selection marks with discontinuous borders, for example, `{X}`. |
| position (**required**) | `left`, `right`              | Defines the starting point for searching for the nearest selection mark. Sensible searches outward from this point in all directions.  `right`  specifies starting at the midpoint of the anchor line's right boundary, and `left` specifies starting at the midpoint of the anchor line's left boundary. |
| offsetX                 | number in inches. default: 0 | Searches for a selection mark starting at a point offset horizontally from the point defined by the Position parameter. |
| offsetY                 | number in inches. default: 0 | Searches for a selection mark starting at a point offset vertically from the point defined by the Position parameter. |

Examples
====

The following example shows extracting three checkboxes:

**Config**

```json
{
  "fields": [
    {
      "id": "checkbox_left",
      "anchor": "checkbox",
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "checkbox_below",
      "anchor": "below",
      "method": {
        "id": "checkbox",
        "position": "left",
        "offsetY": 0.3,
        "offsetX": 0.3
      }
    },
    {
      "id": "checkbox_dark",
      "anchor": "dark",
      "method": {
        "id": "checkbox",
        "position": "right",
        "darknessThreshold": 0.4,
        "offsetX": 0.8
      }
    }
  ]
}
```

**PDF**
The following image shows the example PDF used with this example config:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main//readme-sync/assets/v0/images/final/checkbox.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/checkbox.pdf) |
| ----------- | ------------------------------------------------------------ |




**Output**

```json
{
  "checkbox_left": {
    "type": "boolean",
    "value": true
  },
  "checkbox_below": {
    "type": "boolean",
    "value": true
  },
  "checkbox_dark": {
    "type": "boolean",
    "value": true
  }
}
```













