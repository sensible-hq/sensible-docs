---
title: "Rotate page"
hidden: false
---

Rotates page so that a matched anchor becomes horizontal.

In most cases, Sensible corrects page rotation automatically. If it doesn't, configure this preprocessor. For example, if a scanned ID card is vertically oriented, and the scanner adds automatically generated horizontal text, you can use this preprocessor to correct the mix of text orientations. Configure the preprocessor to match the text that you want to see horizontally aligned.

Parameters
====

| key                 | value                                               | description                                                  |
| ------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| type (**required**) | `rotatePage`                                        |                                                              |
| match               | [Match object](doc:match) or array of Match objects | Sensible rotates the page to ensure that text that matches this parameter is horizontal.  Sensible rotates the page by multiples of 90 degrees. If the page is affected by translation, shear, or other [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm), or if the page rotation isn't a multiple of 90 degrees, use the [Deskew](doc:deskew) preprocessor. |
| matchAll            | boolean                                             | If true, rotates all pages containing the line specified by the Match parameter. |

Examples
====

The following image shows that without the Rotate page preprocessor, extraction from a rotated PDF fails. The Region method returns null, because the targeted text isn't in the expected region:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate_page_1.png)

To solve this problem, configure a match for text that you want to be horizontal, and Sensible rotates the page:

**Config**

```json
{
  "preprocessors": [
    {
      "type": "rotatePage",
      "match": "first dog ID card"
    }
  ],
  "fields": [
    {
      "id": "tenure",
      "anchor": {
        "match": {
          "type": "endsWith",
          "text": "tenure:"
        }
      },
      "method": {
        "id": "region",
        "start": "below",
        "width": 1.6,
        "height": 0.5,
        "offsetX": -1,
        "offsetY": 0
      }
    }
  ]
}
```

**Example document**

The following images show the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate_page_2.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/rotate_page.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

**Output**

```json
{
  "tenure": {
    "type": "string",
    "value": "1961 -1963"
  }
}
```
