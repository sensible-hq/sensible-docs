---
title: "Fixed Table"
slug: "fixedtable"
hidden: false
createdAt: "2021-03-24T00:19:53.251Z"
updatedAt: "2021-04-05T23:46:15.853Z"
---
Matches tables with a fixed number of columns and returns their collated column contents
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`fixedTable`",
    "1-0": "columnCount",
    "1-2": "The number of columns matched tables must have",
    "1-1": "integer",
    "2-0": "columns",
    "2-2": "An array of objects with the following shape:\n - `id`: The id for the column in the extraction output\n- `type`: A type for eduction (see a list of possible types in [Fields](ref:fields))\n- `index`: A zero based column index\n - `isRequired` (optional, default false). If true, the extraction will not return rows where a value is not present in this column",
    "2-1": "array",
    "3-0": "stop",
    "3-2": "optional, default: none. A [Matcher](ref:matcher) to stop extraction. With `stop` defined, the engine will selectively OCR the pages from the starting anchor to the page with the stop match. Otherwise the engine will OCR all pages.",
    "3-1": "[Matcher](ref:matcher)"
  },
  "cols": 3,
  "rows": 4
}
[/block]