---
title: "Checkbox"
hidden: false
---
Looks for a checkbox next to the anchor and returns a boolean
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "values",
    "h-2": "description",
    "1-0": "position",
    "1-2": "The starting position for the checkbox search.\n\nIf `offsetX` or `offsetY` is defined, `checkbox` will move directly from the position to the defined offset for the box search. Otherwise, `checkbox` will start at the starting position and search in the appropriate direction for a box boundary, and then return the contents of that box",
    "1-1": "`left`, `right`",
    "2-0": "offsetX",
    "2-2": "optional\n\nThe offset in inches from the starting point along the X axis",
    "2-1": "a number in inches (decimals allowed)",
    "3-0": "offsetY",
    "3-2": "optional\n\nThe offset in inches from the starting point along the Y axis",
    "3-1": "a number in inches (decimals allowed)",
    "4-0": "darknessThreshold",
    "4-2": "optional, default 0.9.\n\nThe brightness threshold below which to consider a pixel a box boundary (white is 1.0).",
    "4-1": "a number between 0 and 1",
    "0-0": "id",
    "0-1": "`checkbox`"
  },
  "cols": 3,
  "rows": 5
}
[/block]