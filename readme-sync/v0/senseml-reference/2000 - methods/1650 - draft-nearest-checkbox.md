---
title: "Nearest checkbox"
hidden: true
---
Searches for the checkbox nearest to the anchor in any direction, and returns a boolean indicating if it's selected or unselected. 

Use this method as an alterative to the Checkbox method. The advantage of the Nearest Checkbox method is that it's more flexible, requires less configuration, and recognizes a wider range of checkbox formats. The disadvantage is that it's slower than the Checkbox method, because the Nearest Checkbox method uses OCR. 



**Parameters** doc:nearest-checkbox#parameters TODO: fix link syntax before go-live
**Examples**doc:nearest-checkbox#examples

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                     | values                       | description                                                  |
| ----------------------- | ---------------------------- | ------------------------------------------------------------ |
| id (**required**)       | `nearestCheckbox`            | Sensible returns true for selected checkboxes and false for unselected checkboxes. This method uses Azure Form Recognizer’s checkbox detection. This detection uses OCR and machine learning and captures a wide range of checkbox formats. |
| position (**required**) | `left`, `right`              | Defines the starting point for searching for the nearest selection mark. Sensible searches outward from this point in all directions.  `right`  specifies starting at the midpoint of the anchor line's right boundary, and `left` specifies starting at the midpoint of the anchor line's left boundary. |
| offsetX                 | number in inches. default: 0 | Searches for a selection mark starting at a point offset horizontally from the point defined by the Position parameter. |
| offsetY                 | number in inches. default: 0 | Searches for a selection mark starting at a point offset vertically from the point defined by the Position parameter. |

Examples
====

The following example shows extracting the checkboxes that are nearest to their respective anchors:

```json
{
  "fields": [
    {
      "id": "checkbox_right",
      "anchor": "checkbox",
      "method": {
        "id": "nearestCheckbox",
        "position": "right"
      }
    },
    {
      "id": "checkbox_below",
      "anchor": "below",
      "method": {
        "id": "nearestCheckbox",
        "position": "right"
      }
    },
    {
      "id": "checkbox_no_border",
      "anchor": "border",
      "method": {
        "id": "nearestCheckbox",
        "position": "right"
      }
    },
    {
      "id": "checkbox_far",
      "anchor": "far",
      "method": {
        "id": "nearestCheckbox",
        "position": "left",
        "offsetX": -2
      }
    }
  ]
}
```

**PDF**
The following image shows the example PDF used with this example config:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main//readme-sync/assets/v0/images/final/nearest_checkbox.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/nearest_checkbox.pdf) |
| ----------- | ------------------------------------------------------------ |




**Output**

```json
{
  "checkbox_right": {
    "type": "boolean",
    "value": true
  },
  "checkbox_below": {
    "type": "boolean",
    "value": false
  },
  "checkbox_no_border": {
    "type": "boolean",
    "value": true
  },
  "checkbox_far": {
    "type": "boolean",
    "value": false
  }
}
```













