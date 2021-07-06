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

First, let's define fixed points based on an unskewed example of an ID:



```

```

Notes
----

- This preprocessor currently breaks methods that rely on pixel recognition, such as the Box method and the Checkbox method. Use the Region method instead of these methods.
- For scanned PDFs that are only slightly rotated, this preprocessor isn't necessary.  If you select "microsoft OCR" (the default) in the app for in the document type settings, then this OCR engine corrects slight rotation by default.
