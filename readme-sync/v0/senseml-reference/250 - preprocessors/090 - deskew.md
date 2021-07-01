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
| `fixedPoints` (**required**) | object | An object mapping the position of three text anchors to their ideal position if the photo were taken head-on without skew. To choose these fixed points, use an example document with no skew. Choose anchors using that form as large a triangle as possible, ideally at three corners of the document. parameters:<br/>`match` - the text to match for the fixed point. See [Match object](docs:match-object) for more details.<br/>`targetPosition` - contains an `x` and a `y` parameter to define in inches, relative to the 0,0 origin at the top left corner of the page.<br/>`start` |

Examples
----



```

```

Notes
----

