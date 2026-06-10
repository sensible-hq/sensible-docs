---
title: Nearest checkbox
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Find nearest checkbox to anchor and extract its state'
  robots: index
next:
  description: ''
---
Searches for the checkbox nearest to the anchor in any direction, and returns a boolean indicating if it's selected or unselected. 

Use this method as an alterative to the Checkbox method. The advantage of the Nearest Checkbox method is that it's more flexible, requires less configuration, and recognizes a wider range of checkbox formats. The disadvantage is that it's slower than the Checkbox method, because the Nearest Checkbox method uses OCR. 

Sensible extracts selection status using the following methods:

* If the document is a PDF that contains checkbox metadata, or "form data", then Sensible preferentially uses the metadata to extract selection status.  

* If there's no metadata, Sensible falls back to OCR and machine learning to capture a wide range of checkbox formats.

[**Parameters**](doc:nearest-checkbox#parameters)\
[**Examples**](doc:nearest-checkbox#examples)

# Parameters

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                     | value                        | description                                                  |
| ----------------------- | ---------------------------- | ------------------------------------------------------------ |
| id (**required**)       | `nearestCheckbox`            | Sensible returns true for selected checkboxes and false for unselected checkboxes. |
| position (**required**) | `left`, `right`              | Defines the starting point for searching for the nearest checkbox. Sensible searches outward from this point in all directions.  `right`  specifies starting at the midpoint of the anchor line's right boundary, and `left` specifies starting at the midpoint of the anchor line's left boundary. |
| offsetX                 | number in inches. default: 0 | Searches for a checkbox starting at a point offset from the point defined by the Position parameter. Positive values offset to the right, negative values offset to the left. |
| offsetY                 | number in inches. default: 0 | Searches for a checkbox starting at a point offset from the point defined by the Position parameter. Positive values offset down the page, negative values offset up the page. |
| maxYDistance            | number in inches.            | Specifies the maximum number of inches Sensible searches up or down the page from the starting point.  For example, configure this parameter to restrict the checkbox search in successive rows of tightly spaced checkboxes. |
| ignoreFormData          | boolean. default: false      | Set this option to true to troubleshoot situations in which Sensible fails to recognize a checkbox because of a document's inaccurate form data. For example, a PDF editor can run partially successful form recognition on a scanned document and embed incomplete form data in the PDF.  When true, this option bypasses Sensible's default use of checkbox metadata and uses this method's fallback process for checkbox recognition. |

# Examples

The following example shows extracting the checkboxes that are nearest to their respective anchors. For a checkbox that is nearer to another line's checkbox than to its own checkbox, the example shows using an Offset parameter to close the gap:

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

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/nearest_checkbox.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/nearest_checkbox.pdf) |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------- |

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
