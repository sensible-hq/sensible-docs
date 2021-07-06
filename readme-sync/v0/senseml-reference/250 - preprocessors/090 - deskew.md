---
title: "deskew"
hidden: true
---

Correct the alignment of PDF documents that are skewed, for example as a result of being  photographed at an angle instead of straight-on.  ID cards and receipts are common examples of such documents.  Sensible uses [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm)  to correct scaling, rotation, translation, and shear. 



Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)     | `deskew` |                                                    |
| `fixedPoints` (**required**) | object | An object mapping the position of three points in the skewed document to their ideal position if the document had no skew. Define these fixed points using text anchors in an unskewed example of the document. Choose text anchors that form as large a triangle as possible, ideally at three corners of the document. Choosing the best points can take some trial and error. Parameters:<br/>`match` - the text to match for the fixed point. See [Match object](docs:match-object) for more details.<br/>`targetPosition` - contains an `x` and a `y` parameter to define in inches, relative to the 0,0 origin at the top left corner of the page. For more information defining the positions, see the Examples section<br/> |
| `start` | `left` , `right`. default: left | Use the coordinates of the upper-right corner of the anchor line's boundaries, vs the upper-left corner coordinates, as a Fixed Point. |

Examples
----

First, take a look at the following image to see the problem with extracting from a skewed PDF.  In this case, the word "tenure" is so skewed, it isn't even recognized as an anchor, and the Region method wouldn't work even if Sensible could recognize the word "tenure," because the year range isn't below the word "tenure" where we expect it to be:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_1.png)

To start to tackle this problem, let's first define three widely spaced points where we expect the text to be in an unskewed example of this document type:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_2.png)

You can try out this example yourself in the Sensible app using the following downloadable PDFs and config:

| Example aligned  PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/deskew_example_1.pdf) |
| -------------------- | ------------------------------------------------------------ |

| Example skewed PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/deskew_example_2.pdf) |
| -------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "preprocessors": [
    {
      "type": "deskew",
      "fixedPoints": [
        {
          "match": {
            "type": "equals",
            "text": "first"
          },
          "targetPosition": {
            "x": 2.76,
            "y": 1.6
          },
          "start": "left"
        },
        {
          "match": {
            "type": "startsWith",
            "text": "Owner"
          },
          "targetPosition": {
            "x": 2.76,
            "y": 3.74
          },
          "start": "left"
        },
        {
          "match": {
            "type": "endsWith",
            "text": "tenure:"
          },
          "targetPosition": {
            "x": 7.29,
            "y": 3.61
          },
          "start": "right"
        }
      ]
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



Now, let's try out the preprocessor we just defined with our skewed example:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_3.png)

Almost there! The text lines are unskewed and are now aligned in roughly the same positions as the lines in the unskewed reference PDF. However, the Deskew Preprocessor didn't address some lines that were split by the original skew. As a result, the Region starting point shifted to the middle of a single word, "tenure:"

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_5.png)



When we were expecting it to start from the middle of the complete line "white house tenure":

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_6.png)

 To fix this, let's apply a Merge Lines preprocessor after the Deskew preprocessor: 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_4.png)

Now we've captured the full date range. This config uses the following Merge Lines preprocessor:

```json
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.15,
      "adjacentThreshold": 0.8,
      "yOverlapThreshold": 0.1
    },
```









Notes
====

Best practices
-----

Limitations
-----

- This preprocessor currently breaks methods that rely on pixel recognition, such as the Box method and the Checkbox method. Use the Region method instead of these methods.
- For scanned PDFs that are only slightly rotated, this preprocessor isn't necessary.  If you select "microsoft OCR" (the default) in the app for in the document type settings, then this OCR engine corrects slight rotation by default.
- Deskew does not correct for line jitter that may occur as a result of a skewed scan. To correct for these, configure preprocessors in addition to the Deskew preprocessor, such as the Split Lines and Merge Lines preprocessors.

