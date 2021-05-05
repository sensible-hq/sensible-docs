---
title: "Document Range"
hidden: false
---
Matches all lines between the anchor and the `stop` or the end of the document, whichever comes first.
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`documentRange`",
    "1-0": "stop",
    "1-2": "optional, default: none. A [Matcher](ref:matcher) ] to stop extraction",
    "2-0": "includeAnchor",
    "2-2": "optional, default: false. Includes the anchor line in the method output",
    "3-0": "includeImages",
    "3-2": "optional, default: false. Returns the bounding boxes of images in the document range **instead of** the lines",
    "2-1": "`true`, `false`",
    "1-1": "[Matcher](ref:matcher)",
    "3-1": "`true`, `false`"
  },
  "cols": 3,
  "rows": 4
}
[/block]