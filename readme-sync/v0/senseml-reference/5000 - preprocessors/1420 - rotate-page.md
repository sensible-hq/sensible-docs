---
title: "Rotate page"
hidden: true
---



TODO:

- update notes in Scale topic:

-   "you don't need a preprocessor in most cases...automatically....if it doesn't, configure the [Rotate Page](doc:rotate-page) preprocessor"

  



Rotates page so that a matched anchor becomes horizontal. Use this when Sensible's default rotation handling behavior fails to rotate a page. For example, if a scanned ID card is vertically oriented, and the scanner adds automatically generated text in a horizontal orientation, Sensible can fail to rotate the page.  If the page is both rotated and skewed, use the Deskew preprocessor.

Parameters
====

| key                 | value                                  | description                                                  |
| ------------------- | -------------------------------------- | ------------------------------------------------------------ |
| type (**required**) | `rotatePage`                           | Rotates page by up to 90 degrees. TODO more,, what if it's not quite at 90? |
| match               | Match object or array of Match objects | See [Match object](doc:match)                                |
| matchAll            | boolean                                | If true, rotates all pages containing the line specified by the Match parameter. |

Examples
====

The following image shows that without the Rotate page preprocessor, extraction from a rotated PDF fails. The Label method returns null, because the targeted text  isn't in the expected position (`right` ):

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate_page_1.png)

To solve this problem, define a text match that you want to be horizonal, and Sensible rotates the page accordingly:

**Config**

```json
{
  "preprocessors": [
    {
      /* preprocessor necessary here
      because there are many lines of vertical text 
      with fewer vertical lines, Sensible would rotate automatically */
      "type": "rotatePage",
      "match": "first dog ID card"
    }
  ],
  "fields": [
    {
      "id": "pet_name",
      "anchor": "name:",
      "method": {
        "id": "label",
        "position": "right"
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
  "pet_name": {
    "type": "string",
    "value": "Pushinka"
  }
}
```

Notes
----

**Alternatives to Rotate Page preprocessor**

- If pages are affected by translation, shear, or other [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm) in addition to or instead of rotation and scale, use the [Deskew preprocessor](https://docs.sensible.so/docs/deskew).