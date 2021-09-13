---
title: "Checkbox"
hidden: false
---
Searches for a checkbox next to the anchor and returns a boolean indicating if the checkbox contains a checkmark or not. This method works by default with boxes that have a light background and dark, continuous borders.  

[**Parameters**](doc:checkbox#section-parameters)
[**Examples**](doc:checkbox#section-examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key               | values                              | description                                                  |
| ----------------- | ----------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `checkbox`                          | The maximum checkbox size supported is a square with sides 0.3 inches long. Sensible returns true if the checkbox contains a checkmark, "Y", or "X" character. |
| position          | `left`, `right`                     | Searches horizontally for a checkbox starting at the left or right anchor line boundaries, respectively. Sensible searches horizontally for a maximum of 0.15 inches from the Position point until it finds dark pixels signifying the box border. If the anchor line's boundaries and the checkbox are separated horizontally by more than 0.15 inches, then use  the Offset X parameter in combination with the Position parameter to find the box. |
| offsetX           | number in inches. default: 0        | Searches for a box starting at a point offset horizontally from the point defined by the Position parameter. When you define an offset, Sensible expands out directly from the point specified to find the checkbox borders. |
| offsetY           | number in inches. default: 0        | Searches for a box starting at a point offset vertically from the point defined by the Position parameter.  When you define an offset, Sensible expands out directly from the point specified to find the checkbox borders. |
| darknessThreshold | number between 1 and 0. default 0.9 | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this parameter when you have a checkbox with a dark background. |

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



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main//readme-sync/assets/v0/images/final/checkbox_examples.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/checkbox_example.pdf) |
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













