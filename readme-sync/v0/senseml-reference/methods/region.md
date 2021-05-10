---
title: "Region"
hidden: false
---
Use the Region method to grab lines in a rectangular region, defined in inches. 

In general, use this method when you want to grab data from an area whose formatting doesn't exactly fit other Sensible methods, such as the Box or Row method. For example, you can use this method when a Label method doesn't work because the anchor is separated by too much whitespace from the data to grab.

Examples
-----

The following example config extracts a social security number from a W-9 form by defining a region to grab:

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
        "offsetY": 0.1,
        "whitespaceFilter": "all"
      }
    }
  ]
}
```



![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/region_ssn.png)

Parameters
----

| id                     | value                                               | description                                                  |
| ---------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)      | `region`                                            |                                                              |
| start (**required**)   | Direction, either `above`, `below`, `left`, `right` | A Direction specifying where to start relative to the anchor point. `right` starts at the middle of the right edge, `below` starts at the middle of the bottom edge, and so forth. |
| offsetX (**required**) | number                                              | The offset in inches from the `start` along the X axis       |
| offsetY (**required**) | number                                              | The offset in inches from the `start` along the Y axis       |
| width (**required**)   | number                                              | The width in inches of the extraction region                 |
| height (**required**)  | number                                              | The height in inches of the extraction region                |
| isAbsoluteOffset       | boolean. default: `false`                           | A flag to make the offsets relative to the 0,0 origin at the top left of the page rather than to the anchor start point |

Notes
----

If the region that you want to grab is a box that is bordered with dark lines, you can use the [Box method](doc:box) instead of the Region method.