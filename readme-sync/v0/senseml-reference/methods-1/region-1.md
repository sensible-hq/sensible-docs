---
title: "Region"
slug: "region-1"
hidden: false
createdAt: "2021-05-05T20:43:43.304Z"
updatedAt: "2021-05-05T20:43:43.304Z"
---
Return lines within a given document region, defined in inches as a bounding box

[block:parameters]
{
  "data": {
    "h-0": "id",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`region`",
    "1-0": "start",
    "1-2": "A [Direction](ref:direction)  specifying where to start relative to the anchor point. `right` starts at the middle of the right edge, `below` starts at the middle of the bottom edge, and so forth",
    "1-1": "[Direction](ref:direction), either `above`, `below`, `left`, `right`",
    "2-0": "offsetX",
    "3-0": "offsetY",
    "2-2": "The offset in inches from the starting point along the X axis",
    "2-1": "number",
    "3-2": "The offset in inches from the starting point along the Y axis",
    "3-1": "number",
    "4-0": "width",
    "5-0": "height",
    "5-2": "The height in inches of the extraction region",
    "4-2": "The width in inches of the extraction region",
    "4-1": "number",
    "5-1": "number",
    "6-0": "isAbsoluteOffset",
    "6-2": "optional, default: false\n\nA flag to make the offsets relative to the top left of the page rather than to the anchor start point",
    "6-1": "`true`, `false`"
  },
  "cols": 3,
  "rows": 7
}
[/block]