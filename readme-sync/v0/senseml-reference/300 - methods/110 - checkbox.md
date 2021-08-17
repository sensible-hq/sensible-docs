---
title: "Checkbox"
hidden: false
---
Looks for a checkbox next to the anchor and returns a boolean indicating if the checkbox contains a checkmark or not.  This method works by default with boxes that have a light background and dark, continuous borders.  

[**Parameters**](doc:checkbox#section-parameters)
[**Examples**](doc:checkbox#section-examples)



Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key               | values                                  | description                                                  |
| ----------------- | --------------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `checkbox`                              | The maximum checkbox size supported is a square with sides 0.3 inches long. Sensible returns true if the checkbox contains a checkmark, "Y", or "X" character. |
| position          | `left`, `right`                         | The starting position from which Sensible expands outward to recognize a checkbox.  Sensible searches left or right from the midpoint of the left or right anchor line boundary, respectively. It searches for a maximum of 0.15 inches from the starting point until it finds dark pixels signifying the box border. If the anchor line's boundaries and the checkbox are separated by a greater horizontal distance, then use Offset X in combination with the Position parameter to find the box. |
| offsetX           | number (decimals allowed). default: 0   | The offset in inches along the X axis, from the starting point defined by the Position parameter, from which to expand out and recognize a checkbox. When you define an offset, Sensible expands out directly from the point specified to find the checkbox borders. |
| offsetY           | number (decimals allowed).   default: 0 | The offset in inches along the Y axis, from the starting point  defined by  the Position parameter, from which to expand out and recognize a checkbox. When you define an offset, Sensible expands out directly from the point specified to find the checkbox borders. |
| darknessThreshold | number between 1 and 0. default 0.9     | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this parameter when you have a checkbox with a dark background. |

Examples
====

The following image shows extracting three checkboxes:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main//readme-sync/assets/v0/images/checkbox_examples.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for checkboxes | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/example_checkbox.pdf) |
| -------------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "checkbox_left",
      "anchor": "left",
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
        "offsetY": 0.5,
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
        "offsetX": 0.2
      }
    }
  ]
}
```



