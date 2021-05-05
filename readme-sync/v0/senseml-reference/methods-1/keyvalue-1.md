---
title: "Key/Value"
slug: "keyvalue-1"
hidden: false
createdAt: "2021-05-05T20:41:43.840Z"
updatedAt: "2021-05-05T20:41:43.840Z"
---
Finds the most promising key/value pair (currently two-column tabular key/value representations only) in a single page of the source document. This single page and the winning key are those that score highest on the `terms` and `stopTerms`.
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`keyValue`",
    "1-0": "terms",
    "1-2": "An array of strings with terms to score positively",
    "1-1": "Array of strings",
    "2-0": "stopTerms",
    "2-2": "optional. An array of strings with terms to score negatively.",
    "2-1": "Array of strings"
  },
  "cols": 3,
  "rows": 3
}
[/block]