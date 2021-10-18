---
title: "Region"
hidden: false

---

Extracts data in a rectangular region, defined in inches. The region omits lines that only partly fall inside the region. 

In general, use this method:

- for faster performance compared to the Box method
-  when you want to extract data from an area whose formatting doesn't exactly fit other SenseML methods. For example, you can use this method instead of the Label method for widely separated anchors and target lines.

[**Parameters**](doc:region#parameters)
[**Examples**](doc:region#examples)
[**Notes**](doc:region#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| id                     | value                             | description                                                  |
| ---------------------- | --------------------------------- | ------------------------------------------------------------ |
| id (**required**)      | `region`                          |                                                              |
| start (**required**)   | `above`, `below`, `left`, `right` | Defines the starting point for the extraction region relative to the anchor. `right`  specifies a start point at the middle of the right edge of the anchor, `below` specifies a start point at the middle of the bottom edge of the anchor, and so forth. |
| offsetX (**required**) | number                            | The horizontal offset in inches from the point defined in the Start parameter to the top left corner of the region.<br/>You can use interactive visual feedback in the Sensible app to determine this number. |
| offsetY (**required**) | number                            | The vertical offset in inches from the point defined in the Start parameter to the top left corner of the region.<br/>You can use interactive visual feedback in the Sensible app to determine this number. |
| width (**required**)   | number                            | The width in inches of the region. <br/>You can use interactive visual feedback in the Sensible app to determine this number. |
| height (**required**)  | number                            | The height in inches of the region. <br/>You can use interactive visual feedback in the Sensible app to determine this number. |
| isAbsoluteOffset       | boolean. default: `false`         | Makes the offsets relative to the 0,0 origin at the top left of the page rather than to the Start parameter. |

Examples
====

The following example shows extracting a social security number from a W-9 form by defining a region to extract.



**Config**

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

**PDF**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/region_ssn.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/region_w9.pdf) |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |

**Output**
```json
{
  "SSN": {
    "type": "string",
    "value": "1 2 3 4 5 7 8 9 3 – –"
  }
}
```


Notes
====

If the region that you want to extract is a box that's bordered with dark lines, you can use the [Box method](doc:box) instead of the Region method.