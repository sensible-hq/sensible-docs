---
title: "Deskew"
hidden: false
---

Corrects the alignment of text in documents that are skewed, for example as a result of being photographed at an angle instead of straight on. ID cards and receipts are common examples of such documents. Sensible uses [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm) to correct scaling, rotation, translation, and shear. 

See the Notes section for when *not* to use this preprocessor and for alternative preprocessors that correct page transformations.  

[**Parameters**](doc:deskew#parameters)
[**Examples**](doc:deskew#examples)
[**Notes**](doc:deskew#notes)

Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| type (**required**)     | `deskew` |                                                    |
| fixedPoints (**required**) | object | Deskews the text in a skewed document by mapping the positions of three skewed points to their ideal positions in an unskewed document. Define the ideal Fixed Points using the coordinates of text in an unskewed example of the document. Choose points that form as large a triangle as possible, ideally at three corners of the document. Choosing the best points can take trial and error. <br/>Contains an array of 3 objects, each containing the following parameters: <br/>-   `match` -  the text to match for a Fixed Point. Choose `"type": "startsWith"`  or `"type": "endsWith"` to avoid problems with lines oversplit by skew. See [Match object](doc:match) for more details.<br/>- `targetPosition` - contains  `x` and  `y` parameters that define the coordinates of the Fixed Points in inches relative to the 0,0 origin at the top left corner of the page. For more information about defining the positions, see the Examples section. |
| start | `left` , `right`. default: `left` | Specifies whether the Fixed Point is at the upper-*left* corner of the anchor line's boundaries, or the upper-*right* corner. <br/>With a Match parameter of `"type": "startsWith"`, use `left`.<br/>With a Match parameter of `"type": "endsWith"`, use `right`. |

Examples
----

The following image shows that without the Deskew preprocessor, extraction from a skewed document fails. The Region method returns null, because the targeted date range is in an unexpected position (to the left of the anchor, `tenure`) rather than in the expected position (`below`):

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/deskew_1.png)

To solve this problem:

1. Define three widely spaced points in a well-aligned example of this document type: The following image shows using the displayed coordinates of a line to define the X and Y parameters for one of three Fixed Point parameters:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/deskew_2.png)

For more information about choosing points, see [Best Practices](doc:deskew#best-practices).


2. Check the Deskew preprocessor against the skewed example to reveal a remaining problem:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/deskew_3.png)

The remaining problem is that the Deskew Preprocessor  doesn't merge lines that were split by the skew. As a result, the region starts at the middle of the word "tenure" instead of the middle of the complete line "White house tenure". Since the new start shifts the region to the right, the region misses the first year of the date range and returns `-1963`.



3. To fix this problem, apply a Merge Lines preprocessor after the Deskew preprocessor: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/deskew_4.png)

Now Sensible captures the full date range, because the region starts at the middle of the complete line "White house tenure".

Try out this example in the Sensible app using the following documents and config:

| Example aligned document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/deskew_1.pdf) |
| -------------------- | ------------------------------------------------------------ |

| Example skewed document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/deskew_2.pdf) |
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
    },    
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.15,
      "adjacentThreshold": 0.8,
      "yOverlapThreshold": 0.1
    },
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


Notes
----

**Page transformation preprocessors**

See the following table for preprocessors that correct page transformations:

| page transformation                                          | preprocessor | notes                                                        |
| ------------------------------------------------------------ | ------------ | ------------------------------------------------------------ |
| translation, shear, or other [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm) in addition to or instead of rotation and scale | Deskew       | Handles complex page transformations, requires advanced configuration. |
| rotation                                                     | Rotate Page  | If a document contains pages that are rotated but otherwise untransformed, in most cases you don't need a preprocessor. Sensible corrects rotation automatically. If it doesn't, configure the [Rotate Page](doc:rotate-page) preprocessor. |
| scale                                                        | Scale        | If pages are affected by scale but not by affine transformations, use the [Scale](doc:scale) preprocessor as an easier-to-configure and more robust alternative to the Deskew preprocessor. |



**Tips for viewing skewed documents**

To view the deskewed document in the Sensible app, click the document, then click the eye (👁) icon:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/deskew_5.png)

This visual representation of how the Sensible app deskews documents can be useful for authoring or troubleshooting deskew preprocessors and configs.

**Fixed Points tips**

- Click on a line in the document pane in the Sensible app to view line coordinates for defining the Fixed Points.
- Choose text anchors for Fixed Points that form as large a triangle as possible, ideally at three corners of the document. Choosing the best points can take trial and error. 
- For the Match parameter, choose `"type": "startsWith"` or `"type": "endsWith"` to avoid problems with lines split by skew. If you choose `"endsWith"`, then also define `"start:right"`. You can also define a Merge Lines preprocessor to clean up oversplit lines.

- For the aligned reference document, choose a slightly enlarged version of the document so that the Fixed Points triangle is large. The Deskew preprocessor corrects scaling for smaller skewed images.

  





