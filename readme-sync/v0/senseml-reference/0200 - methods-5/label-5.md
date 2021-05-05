---
title: "Label"
hidden: false
---
Return lines near the anchor point

[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`label`",
    "1-0": "position",
    "1-2": "What direction the target data is relative to the anchor point.",
    "1-1": "[Direction](ref:direction) (`above`, `below`, `left`, `right`)",
    "2-0": "stop",
    "2-2": "optional, default first. Only applies to when `position` is `below`. \n\nThe stopping criterion for line extraction. By default `label` only matches one line, but if `gap` or a `Matcher` are supplied it will match aligned lines until it reaches a gap of 0.2 inches or a matching line, respectively",
    "2-1": "`first`, `gap`, or a [Matcher](ref:matcher)",
    "3-0": "textAlignment",
    "3-2": "optional, default: `left`. Used with vertical matching (`position: below` or `position: above`).\n\nDetermines whether to match lines aligned to the anchor at the `left` edge or the `right` edge. \n\nFor `position: below` you may specify `hangingIndent` to match the closest line along the X axis, to the right, from the line below the anchor",
    "3-1": "`left`, `right`, `hangingIndent`",
    "4-0": "includeAnchor",
    "4-2": "optional, default false. \n\nWhether to include the anchor line in the method output.\n\nFor horizontal matching (`position: left` or `position: right`) the method will return the remainder of the anchor line if its final `Matcher` didn't match the full line. For example, if the anchor line is \"Premium: $500\" and the `Matcher` is `{ \"type\": \"startsWith\", \"text\": \"Premium: \" }`, `label` will return \"$500\""
  },
  "cols": 3,
  "rows": 5
}
[/block]