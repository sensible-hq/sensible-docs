---
title: "Computed Field"
hidden: false
---
A computed field is a field that takes in one or more [Fields](ref:fields) parsed from the document and applies transformations on them through a [Computed Field Method](ref:computed-field-method). 
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "0-0": "id",
    "0-1": "string",
    "0-2": "A string that identifies the field in the `parsed_document` output from the API",
    "h-2": "description",
    "1-0": "type",
    "1-2": "optional, default: `string`\n\nSee the eduction types in [Fields](ref:fields). Doesn't apply to the `summarizer` and `tfidf` computed field methods",
    "2-0": "method",
    "2-1": "[Computed Field Method](ref:computed-field-method)",
    "2-2": "The method used to create this field. See [Computed Field Method](ref:computed-field-method) for the full list of available methods.",
    "1-1": "string"
  },
  "cols": 3,
  "rows": 3
}
[/block]