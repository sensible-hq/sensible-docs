---
title: "deskew"
hidden: true
---


Correct the alignment of PDF documents that were photographed at an angle instead of straight-on, or that were poorly scanned.  ID cards and receipts are common examples of such documents.

Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)     | `deskew` |                                                    |
| `fixedPoints` (**required**) | object | An object mapping the position of three text anchors to their ideal position if the photo were taken head-on without skew. Choose anchors that form as large a triangle as possible. To determine the ideal fixed points, use |

Examples
----

This config shows using a ligature mapping preprocessor and outputting the whole document in order to check the ligature replacement accuracy: 

```

```

Notes
----

