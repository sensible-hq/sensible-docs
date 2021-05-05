---
title: "Box"
hidden: false
---
The box method finds lines that are surrounded by a dark-bordered box, like on certificates of insurance or W-2 forms. 
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-2": "",
    "0-1": "`box`",
    "2-0": "offsetY",
    "2-2": "optional, default: 0\n\nThe offset in inches from the starting point along the Y axis",
    "2-1": "number",
    "3-0": "offsetBoxes",
    "3-2": "optional, default: none\n\nThe number of detected boxes to offset by in a given direction.",
    "3-1": "An object with the keys:\n- `direction`: The `Direction` to search in relative to the starting box\n- `number`: The number of boxes to offset by",
    "4-0": "position",
    "4-2": "A `Direction` specifying where to start relative to the anchor point. `right` starts at the middle of the right edge, `below` starts at the middle of the bottom edge, and so forth",
    "4-1": "`right`, `left`, `below`, `above`",
    "5-0": "darknessThreshold",
    "5-2": "optional, default: 0.9\n\nThe brightness threshold below which to consider a pixel a box boundary (white is 1.0)",
    "5-1": "a number between 0 and 1",
    "1-0": "offsetX",
    "1-1": "number",
    "1-2": "optional, default: 0\n\nThe offset in inches from the starting point along the X axis"
  },
  "cols": 3,
  "rows": 6
}
[/block]