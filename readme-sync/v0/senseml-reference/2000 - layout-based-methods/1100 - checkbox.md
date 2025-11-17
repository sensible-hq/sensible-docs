---
title: "Checkbox"
hidden: false
---

Searches for a checkbox near to the anchor and returns a boolean indicating if it is selected or unselected. 

Sensible uses one of two data sources, pixels or metadata, to extract selection status:

- If the document is a PDF that contains checkbox metadata, then Sensible preferentially uses the metadata to extract selection status.  

- If there's no metadata, Sensible falls back to pixel recognition. By default Sensible recognizes pixels as checkboxes if they have a light background and dark, continuous borders. The maximum checkbox size supported by default for pixel recognition is a square with sides 0.3 inches long. Sensible returns true if  there are more that 5% darkened pixels within the box, indicating that it contains a selection mark.  Sensible  returns false if the box is empty. 

[**Parameters**](doc:checkbox#parameters)
[**Examples**](doc:checkbox#examples)

Parameters
=====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key               | values                          | description                                                  |
| ----------------- | ------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `checkbox`                      |                                                              |
| position          | `left`, `right`                 | Searches horizontally for a checkbox starting at the left or right anchor line boundaries and ending at the page margin. |
| offsetX           | number in inches. default: 0    | Indicates a point inside the checkbox. Instead of searching horizontally, Sensible  expands the search out in all directions from the point specified to find the checkbox bounding box.<br/><br/> For difficult pixel recognition, for example for large checkboxes or selection marks with no borders,  use the offset parameters in combination with Width and Height parameters to define the selection mark region. |
| offsetY           | number in inches. default: 0    | Indicates a point inside the checkbox. Instead of searching horizontally, Sensible  expands the search out in all directions from the point specified to find the checkbox bounding box.<br/><br/>For difficult pixel recognition, for example for large checkboxes or selection marks with no borders,  use the offset parameters in combination with Width and Height parameters to define the selection mark region. |
| width             | number in inches. default: none | **For pixel recognition:**  Configure this parameter for pixel recognition of checkboxes larger than the default supported size, or for checkboxes with discontinuous or missing borders.<br/><br/>The Width and Height parameters define a region in which to find a selection mark. Specify a region inside the checkbox borders that doesn't touch the borders. |
| height            | number in inches. default: none | **For pixel recognition:**  Configure this parameter for pixel recognition of checkboxes larger than the default supported size, or for checkboxes with discontinuous or missing borders.<br/><br/>The Width and Height parameters define a region in which to find a selection mark. Specify a region inside the checkbox borders that doesn't touch the borders. |
| darknessThreshold | number between 1 and 0.         | **For pixel recognition:**  The brightness threshold below which to consider a pixel a box boundary. White is 1.0. Configure this parameter for checkboxes with dark backgrounds relative to the surrounding background.<br/>If the document has dark or mottled background, for example as the result of a scan, then Sensible automatically chooses a default value based on the amount of contrast in the document. |

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
The following image shows the example document used with this example config:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main//readme-sync/assets/v0/images/final/checkbox.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/checkbox.pdf) |
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

Notes
---

See also: [Nearest Checkbox method](doc:nearest-checkbox)











