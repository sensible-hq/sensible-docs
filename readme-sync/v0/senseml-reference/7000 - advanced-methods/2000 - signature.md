---
title: "Signature"
hidden: false
---
Returns true if more than 3% of the pixels in the specified region are dark.
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`signature`",
    "1-0": "start",
    "1-1": "Direction, one of `above`, `below`, `left`, `right`",
    "1-2": "A direction specifying where to start relative to the anchor point. For  example, `right` starts at the middle of the right edge, and `below` starts at the middle of the bottom edge.
    "2-0": "offsetX",
    "2-2": "The offset in inches from the starting point along the X axis",
    "2-1": "number",
    "3-0": "offsetY",
    "3-1": "number",
    "3-2": "The offset in inches from the starting point along the Y axis",
    "4-0": "width",
    "4-2": "The width in inches of the extraction region",
    "5-0": "height",
    "5-2": "The height in inches of the extraction region",
    "6-0": "isAbsoluteOffset",
    "6-2": "optional, default false\n\nA flag to make the offsets relative to the top left of the page rather than to the anchor start point",
    "6-1": "`true`, `false`",
    "5-1": "number",
    "4-1": "number"
  },
  "cols": 3,
  "rows": 7
}
[/block]