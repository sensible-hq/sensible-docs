---
title: "Region"
hidden: false

---

Use the Region method to grab data in a rectangular region, defined in inches. The region omits lines that only partly fall inside the region. 

In general, use this method when you want to grab data from an area whose formatting doesn't exactly fit other SenseML methods, such as the Box method. For example, you can use this method when a Label method doesn't work because the anchor is separated by too much whitespace from the data to grab.

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| id                     | value                             | description                                                                                                                                                                                                                                 |
| ---------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id (**required**)      | `region`                          |                                                                                                                                                                                                                                             |
| start (**required**)   | `above`, `below`, `left`, `right` | A Direction specifying where to start relative to the anchor. `right`  specifies a start point at the middle of the right edge of the anchor, `below` specifies a start point at the middle of the bottom edge of the anchor, and so forth. |
| offsetX (**required**) | number                            | The offset in inches along the X axis:<br/>- from the point defined in the Start parameter <br/>- to the top left corner of the region                                                                                                      |
| offsetY (**required**) | number                            | The offset in inches along the Y axis:<br/>- from the point defined in the Start parameter <br/>- to the top left corner of the region                                                                                                      |
| width (**required**)   | number                            | The width in inches of the extraction region.                                                                                                                                                                                               |
| height (**required**)  | number                            | The height in inches of the extraction region.                                                                                                                                                                                              |
| isAbsoluteOffset       | boolean. default: `false`         | When specified, makes the offsets relative to the 0,0 origin at the top left of the page rather than to the Start parameter.                                                                                                                |

Examples
====

The following image shows extracting a social security number from a W-9 form by defining a region to grab:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/region_ssn.png)

You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for box recognition | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/example_box_recognition.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "SSN",
      "anchor": {
        "match": {
          "type": "equals",
          "text": "Social security number",
          "isCaseSensitive": true
        }
      },
      "method": {
        "id": "region",
        "start": "below",
        "width": 2.15,
        "height": 0.25,
        "offsetX": -0.55,
        "offsetY": 0.1
      }
    }
  ]
}
```

Notes
===

If the region that you want to grab is a box that is bordered with dark lines, you can use the [Box method](doc:box) instead of the Region method.