---
title: "Concatenate"
slug: "mapper"
hidden: false
createdAt: "2021-03-26T17:28:00.782Z"
updatedAt: "2021-03-26T17:40:30.151Z"
---
Concatenates the output of two or more fields. If the fields are all strings, the output will be a single string. If any are arrays, the output will be an array if the array lengths match, and a string if they don't (using the first element of each array). If a string is present in the fields amongst arrays, its value will be repeated for every element of the output.
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`concat`",
    "1-0": "source_ids",
    "1-1": "array of field ids on the current configuration",
    "1-2": "a list of field `id`s to concatenate",
    "2-0": "delimiter",
    "2-2": "optional, default: \" \"\n\nThe delimiter with which to join the output of the source fields",
    "2-1": "string"
  },
  "cols": 3,
  "rows": 3
}
[/block]