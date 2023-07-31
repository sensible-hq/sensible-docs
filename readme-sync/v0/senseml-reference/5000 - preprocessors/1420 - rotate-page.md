---
title: "Rotate page"
hidden: true
---

Rotates page so that a matched anchor becomes horizontal.

In most cases, Sensible corrects page rotation automatically. If it doesn't, use the Rotate Page preprocessor. For example, if a scanned ID card is vertically oriented, and the scanner adds automatically generated horizontal text, Sensible can fail to automatically correct the mix of text orientations.

If the page is affected by translation, shear, or other [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm), or if the page rotation isn't a multiple of 90 degrees, use the [Deskew](doc:deskew) preprocessor.

Parameters
====

| key                 | value                                               | description                                                  |
| ------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| type (**required**) | `rotatePage`                                        |                                                              |
| match               | [Match object](doc:match) or array of Match objects | Sensible rotates the page to ensure that text that matches this parameter is horizontal.  Sensible rotates the page by 90 degrees multiples. |
| matchAll            | boolean                                             | If true, rotates all pages containing the line specified by the Match parameter. |

Examples
====

The following image shows that without the Rotate page preprocessor, extraction from a rotated PDF fails. The Region method returns null, because the targeted text isn't in the expected region:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate_page_1.png)

To solve this problem, define a text match using an example of text that you want to be horizonal, and Sensible rotates the page:

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

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/rotate_page.pdf) |
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



TODO:

- update notes in Scale topic and in Deskew topic:
-   "you don't need a preprocessor in most cases...automatically....if it doesn't, configure the [Rotate Page](doc:rotate-page) preprocessor"
- If pages are affected by scale, but are otherwise untransformed, use the Scale preprocessor as an easier-to-configure and more robust alternative to the Deskew preprocessor.
- 