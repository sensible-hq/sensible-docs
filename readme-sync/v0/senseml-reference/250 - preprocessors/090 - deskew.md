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
| `fixedPoints` (**required**) | object | An object mapping the position of three points in the skewed document to their ideal position if the document had no skew. Define these fixed points using text anchors in an unskewed example of the document. Choose text anchors that form as large a triangle as possible, ideally at three corners of the document.  Choosing the best points can take some trial and error. Parameters:<br/>`match` - the text to match for the fixed point.  Choose types "startsWith" or "endsWith" to avoid problems with lines split by skew. See [Match object](docs:match-object) for more details.<br/>`targetPosition` - contains an `x` and a `y` parameter to define in inches, relative to the 0,0 origin at the top left corner of the page. For more information defining the positions, see the Examples section<br/> |
| `start` | `left` , `right`. default: `left` | Use the coordinates of the upper-right corner of the anchor line's boundaries, vs the upper-left corner coordinates, as a Fixed Point.  Leave the default with a Match object where `"type": "startsWith"`, and use `right` with a Match object where `"type": "endsWith"`. |

Examples
----

First, take a look at the following image to see the problem with extracting from a skewed PDF.  This config attempts to extract a date range using the Region method and anchoring on the text "tenure."  The config fails, because the word "tenure" is so skewed, it isn't even recognized as an anchor. Even if the anchor were recognizable, the Region method wouldn't work, because the year range is to the left rather than directly below the word "tenure":

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_1.png)

To start to tackle this problem, let's first define three widely spaced points where we expect the text to be in a well aligned example of this document type:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_2.png)

For more information about how to choose points, see [Best Practices](doc:deskew#section-best-practices).

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

We're almost there! The text lines are unskewed and are now aligned in roughly the same positions as the lines in the reference PDF. However, the Deskew Preprocessor didn't fix lines that were split by the skew. As a result, the region starting point shifted to the middle of the word "tenure" instead of the middle of the complete line:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_5.png)

Since the region is shifted to the right, it misses the start of the date range.

To fix this, let's apply a Merge Lines preprocessor after the Deskew preprocessor: 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_4.png)

Now we've captured the full date range, because the region starts from the middle of the complete line "White house tenure": 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_6.png)





This config uses the following Merge Lines preprocessor:

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

Define th

Limitations
-----

- This preprocessor currently breaks methods that rely on pixel recognition, such as the Box method and the Checkbox method. Use the Region method instead of these methods.
- For scanned PDFs that are only slightly rotated, this preprocessor isn't necessary.  If you select "microsoft OCR" (the default) in the app for in the document type settings, then this OCR engine corrects slight rotation by default.
- Deskew does not correct for line jitter that may occur as a result of a skewed scan. To correct for these, configure preprocessors in addition to the Deskew preprocessor, such as the Split Lines and Merge Lines preprocessors.

