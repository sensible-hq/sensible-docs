---
title: "Table"
slug: "table-1"
hidden: false
createdAt: "2021-05-05T20:45:21.536Z"
updatedAt: "2021-05-05T20:45:21.536Z"
---
Matches tables based on bag-of-words scoring and returns their collated column contents
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`table`",
    "1-0": "columns",
    "1-2": "An array of objects with the following shape:\n  * `id`: The id for the column in the extraction output\n  * `terms`: An array of strings with terms to score positively.\n  * `stopTerms`:  optional. An array of strings with terms to score negatively.\n  * `isRequired`: optional, default false. If true, the extraction will not return rows where a value is not present in this column",
    "2-0": "stop",
    "2-1": "[Matcher](ref:matcher)",
    "2-2": "optional, default: none. A [Matcher](ref:matcher) to stop extraction. With `stop` defined, the engine will selectively OCR the pages from the starting anchor to the page with the stop match. Otherwise the engine will OCR all pages",
    "1-1": "array"
  },
  "cols": 3,
  "rows": 3
}
[/block]