---
title: "Rotate page"
hidden: true
---



TODO:

- update notes in Scale topic and in Deskew topic:

-   "you don't need a preprocessor in most cases...automatically....if it doesn't, configure the [Rotate Page](doc:rotate-page) preprocessor"

- If pages are affected by scale, but are otherwise untransformed, use the Scale preprocessor as an easier-to-configure and more robust alternative to the Deskew preprocessor.

- 

  



Rotates page so that a matched anchor becomes horizontal. Use this when Sensible's default rotation handling behavior fails to rotate a page. For example, if a scanned ID card is vertically oriented, and the scanner adds automatically generated text in a horizontal orientation, Sensible can fail to rotate the page without this preprocessor.  If the page is both rotated and skewed, or if the page rotation isn't a multiple of 90 degrees, use the Deskew preprocessor.



See the Notes section for when *not* to use this preprocessor and for alternatives.



Parameters
====

| key                 | value                                               | description                                                  |
| ------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| type (**required**) | `rotatePage`                                        |                                                              |
| match               | [Match object](doc:match) or array of Match objects | Sensible rotates the page to make that text that matches this parameter horizontal.  Sensible rotates the page in 90 degrees multiples. |
| matchAll            | boolean                                             | If true, rotates all pages containing the line specified by the Match parameter. |

Examples
====

The following image shows that without the Rotate page preprocessor, extraction from a rotated PDF fails. The Label method returns null, because the targeted text  isn't in the expected region:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate_page_1.png)

To solve this problem, define a text match that you want to be horizonal, and Sensible rotates the page accordingly:

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

Notes
----

**Alternatives to Rotate Page preprocessor**

- If a document contains pages that are rotated but otherwise untransformed, you don't need a preprocessor. Sensible's default OCR engine (Microsoft) corrects rotation automatically. If the rotated pages contain a mix of vertical and horizonal text, it can cause automatic rotation to fail. in that case use the Rotate Page preprocessor. 
- If pages are affected by translation, shear, or other [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm) in addition to or instead of rotation and scale, use the [Deskew preprocessor](https://docs.sensible.so/docs/deskew).
- If pages are affected by scale, but are otherwise untransformed, use the Scale preprocessor as an easier-to-configure and more robust alternative to the Deskew preprocessor.