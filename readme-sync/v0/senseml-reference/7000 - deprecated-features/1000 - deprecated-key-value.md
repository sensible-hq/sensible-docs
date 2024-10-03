---
title: "(Deprecated) Key/Value"
hidden: true
---
## Deprecated

This method is deprecated. [LLM-based methods](doc:llm-based-methods) replace this method.

## Decription

Finds the most promising two-column tabular key/value pair in a single page of the source document. This single page and the winning key are those that score highest on the `terms` and `stopTerms`.

```
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-1": "`keyValue`",
    "1-0": "terms",
    "1-2": "An array of terms to score positively. For more information about scoring, see [bag of words](doc:deprecated-bag-of-words).",
    "1-1": "Array of strings",
    "2-0": "stopTerms",
    "2-2": "optional. An array of terms to score negatively. For more information about scoring, see [bag of words](doc:deprecated-bag-of-words).",
    "2-1": "Array of strings"
  },
  "cols": 3,
  "rows": 3
}
```

