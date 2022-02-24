---
title: "Checkbox"
hidden: false
---
Searches for a checkbox next to the anchor and returns a boolean indicating if it is selected or unselected. This method works by default with boxes that have a light background and dark, continuous borders. 

[**Parameters**](doc:checkbox#parameters)
[**Examples**](doc:checkbox#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key               | values                              | description                                                  |
| ----------------- | ----------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `checkbox`                          | The maximum checkbox size supported by default is a square with sides 0.3 inches long. Sensible returns true if  there are more that 5% darkened pixels within the box, indicating that it contains a selection mark. Sensible  returns false if the box is empty. |
| position          | `left`, `right`                     | Searches horizontally for a checkbox starting at the left or right anchor line boundaries, respectively. Sensible searches horizontally for a maximum of 0.15 inches from the Position point until it finds dark pixels signifying the box border. If more than 0.15 inches of whitespace separate the anchor line's boundaries and the checkbox, then use  the Offset X parameter in combination with the Position parameter to find the box. |
| offsetX           | number in inches. default: 0        | Searches for checkbox starting at a point offset horizontally from the point defined by the Position parameter. When you define an offset, Sensible expands out in all directions from the point specified to find either 1. the checkbox borders and selection mark 2. solely the selection mark, if you set Width and Height parameters. |
| offsetY           | number in inches. default: 0        | Searches for box starting at a point offset horizontally from the point defined by the Position parameter. When you define an offset, Sensible expands out in all directions from the point specified to find either 1. the checkbox borders and selection mark 2. solely the selection mark, if you set Width and Height parameters. |
| width             | number in inches. default: none     | Searches for a selection mark, not box borders, inside a region defined by the Width and Height parameters. Use these parameters for checkboxes larger than the default supported size, or for checkboxes with discontinuous or missing borders. Specify a region inside the checkbox borders that doesn't touch the borders. |
| height            | number in inches. default: none     | Searches for a selection mark, not box borders, inside a region defined by the Width and Height parameters. Use these parameters for checkboxes larger than the default supported size, or for checkboxes with discontinuous or missing borders. Specify a region inside the checkbox borders that doesn't touch the borders. |
| darknessThreshold | number between 1 and 0. default 0.9 | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this parameter for checkboxes with dark backgrounds. |

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

**Example document**
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













