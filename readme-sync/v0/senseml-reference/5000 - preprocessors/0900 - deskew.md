---
title: "Deskew"
hidden: false
---

Use this preprocessor to deskew documents in advanced cases where Sensible doesn't automatically correct the alignment of text in documents. ID cards and receipts are documents that can often be skewed, for example as a result of being photographed at an angle instead of straight on.  

See the Notes section for when *not* to use this preprocessor and for alternative preprocessors that correct page transformations.  

[**Parameters**](doc:deskew#parameters)
[**Examples**](doc:deskew#examples)
[**Notes**](doc:deskew#notes)

Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| type (**required**)     | `deskew` |                                                    |
| fixedPoints (**required**) | object | Deskews the text in a skewed document by mapping the positions of three skewed points to their ideal positions in an unskewed document. Define the target Fixed Points using the coordinates of [lines](doc:lines) in an unskewed example of the document. Choose points that form as large a triangle as possible on a single page, ideally at three corners of the document page. Choosing the best points can take trial and error. <br/>Contains an array of 3 objects, each containing the following parameters: <br/>-   `match` -  the text to match for a Fixed Point. Choose `"type": "startsWith"`  or `"type": "endsWith"` to avoid problems with lines oversplit by skew. See [Match object](doc:match) for more details.<br/>- `targetPosition` - contains  `x` and  `y` parameters that define the coordinates of the Fixed Points in inches relative to the 0,0 origin at the top left corner of the page.<br/>Sensible uses [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm) to correct scaling, rotation, translation, and shear. |
| matchAll | Boolean. default: false | If true, deskews all pages containing the lines specified by the Fixed Points parameter. |
| start | `left` , `right`. default: `left` | Specifies whether the Fixed Point is at the upper-*left* corner of the anchor line's boundaries, or the upper-*right* corner. <br/>With a Match parameter of `"type": "startsWith"`, use `left`.<br/>With a Match parameter of `"type": "endsWith"`, use `right`. |


Notes
----

**Page transformation preprocessors**

See the following table for preprocessors that correct page transformations:

| page transformation                                          | preprocessor | notes                                                        |
| ------------------------------------------------------------ | ------------ | ------------------------------------------------------------ |
| translation, shear, or other [affine transformations](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm) in addition to or instead of rotation and scale | Deskew       | Handles complex page transformations, requires advanced configuration. |
| rotation                                                     | Rotate Page  | If a document contains pages that are rotated but otherwise untransformed, in most cases you don't need a preprocessor. Sensible corrects rotation automatically. If it doesn't, configure the [Rotate Page](doc:rotate-page) preprocessor. |
| scale                                                        | Scale        | If pages are affected by scale but not by affine transformations, use the [Scale](doc:scale) preprocessor as an easier-to-configure and more robust alternative to the Deskew preprocessor. |

**Fixed Points tips**

- Click on a line in the document pane in the Sensible app to view line coordinates for defining the Fixed Points.
- Choose text anchors for Fixed Points that form as large a triangle as possible, ideally at three corners of the document. Choosing the best points can take trial and error. 
- For the Match parameter, choose `"type": "startsWith"` or `"type": "endsWith"` to avoid problems with lines split by skew. If you choose `"endsWith"`, then also define `"start:right"`. You can also define a Merge Lines preprocessor to clean up oversplit lines.

- For the aligned reference document, choose a slightly enlarged version of the document so that the Fixed Points triangle is large. The Deskew preprocessor corrects scaling for smaller skewed images.

  





