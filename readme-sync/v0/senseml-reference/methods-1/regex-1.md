---
title: "Regex"
slug: "regex-1"
hidden: false
createdAt: "2021-05-05T20:43:14.443Z"
updatedAt: "2021-05-05T20:43:14.443Z"
---
Returns lines matching a regular expression. If the regular expression has capturing groups, `regex` will return the contents of the first capturing group. Otherwise, it will return the full contents of the matched line. 
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`regex`",
    "1-0": "pattern",
    "1-1": "valid regex",
    "1-2": "An escaped string representation of a regex pattern",
    "2-0": "flags",
    "2-2": "optional, default none. \n\nFlags to apply to the regex (typically `i` for case-insensitive)",
    "2-1": "regex flags, for example: `\"i\"`, `\"g\"`, `\"m\"`",
    "3-0": "stop",
    "3-2": "optional, default none. \n\nA `Matcher` to stop extraction",
    "3-1": "[Matcher](ref:matcher)"
  },
  "cols": 3,
  "rows": 4
}
[/block]