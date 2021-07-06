---
title: "deskew"
hidden: true
---

Correct the alignment of PDF documents that are skewed, for example as a result of being  photographed at an angle instead of straight-on.  ID cards and receipts are common examples of such documents.  Sensible uses [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm)  to correct scaling, rotation, translation, and shear. 

For PDFs that are only slightly rotated, this preprocessor isn't necessary.   Sensible's default OCR engine (Microsoft)  corrects slight rotation automatically.



Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)     | `deskew` |                                                    |
| `fixedPoints` (**required**) | object | An object mapping the position of three points in the skewed document to their ideal position if the document had no skew. Define these fixed points using text anchors in an unskewed example of the document. Choose text anchors that form as large a triangle as possible, ideally at three corners of the document.  Choosing the best points can take some trial and error. Parameters:<br/>`match` - the text to match for the fixed point.  Choose types "startsWith" or "endsWith" to avoid problems with lines split by skew. See [Match object](docs:match-object) for more details.<br/>`targetPosition` - contains an `x` and a `y` parameter to define in inches, relative to the 0,0 origin at the top left corner of the page. For more information defining the positions, see the Examples section. |
| `start` | `left` , `right`. default: `left` | Use the coordinates of the upper-right corner of the anchor line's boundaries, vs the upper-left corner coordinates, as a Fixed Point.  Leave the default with a Match parameter where `"type": "startsWith"`, and use `right` with a Match parameter where `"type": "endsWith"`. |

Examples
----

The following image shows some problems with extracting data from a skewed PDF.  This config attempts to extract a date range using a Region method anchored on the word "tenure." The config fails, because the word "tenure" too skewed for Sensible to recognize the word. The Region method independently fails, because the date range is to the left rather than directly below the anchor:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_1.png)

To solve this problem, first define three widely spaced points in a well-aligned example of this document type. The following image shows using the displayed coordinates of the line starting with "first" to define the X and Y parameters for one of three Fixed Point parameters:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_2.png)

For more information about choosing points, see [Best Practices](doc:deskew#section-best-practices).

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



Now, check this Deskew preprocessor against the skewed example:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_3.png)

The problem is almost solved! The text lines are unskewed and are now aligned in roughly the same positions as the lines in the reference PDF. However, the Deskew Preprocessor didn't fix lines that were split by the skew. As a result, the region starts at the middle of the word "tenure" instead of the middle of the complete line "White house tenure":

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_5.png)

Since the region is shifted to the right, it misses the start of the date range.

To fix this, apply a Merge Lines preprocessor after the Deskew preprocessor: 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/deskew_example_4.png)

Now Sensible captures the full date range, because the region starts at the middle of the complete line "White house tenure": 

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

Tips
-----

- Click on a line in the document pane in the Sensible app to view line coordinates for defining the Fixed Points.
- Choose text anchors for Fixed Points that form as large a triangle as possible, ideally at three corners of the document.  Choosing the best points can take some trial and error. 
- For the Match parameter, choose types "startsWith" or "endsWith" to avoid problems with lines split by skew.  If you choose "endsWith", then also define `"start:right"`.
- For the aligned reference PDF, choose a slightly enlarged image of the document so that the Fixed Points triangle is large. The Deskew preprocessor corrects scaling for smaller skewed images.
- Define a Merge Lines or Split Lines preprocessor to clean up after the Deskew preprocessor. 

Limitations
-----

This preprocessor currently breaks methods that rely on pixel recognition, such as the Box method and the Checkbox method. Use the Region method instead of these methods.



