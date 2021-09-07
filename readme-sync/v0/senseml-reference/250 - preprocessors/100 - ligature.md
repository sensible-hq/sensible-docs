---
title: "Ligature"
hidden: false
---


Intelligently replaces Unicode [ligatures](doc:ligatures) in a PDF text extraction. 

Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)     | `ligature` |                                                    |
| `mappings` (**required**) | object | An object mapping ligature strings (e.g., `"\u0000"`) to an array of possible ligature replacements (e.g., `["ff", "ffi", "fi", "fl"]`). Sensible uses a dictionary in the target language to choose replacements that lead to known words. Sensible supports American English (en-us). This approach is conservative and may leave some Unicode characters in proper names or other non-word data. |

Examples
----

This config shows using a Ligature preprocessor and outputting the whole document in order to check the ligature replacement accuracy: 

```
{
  "preprocessors": [
    {
      "type": "ligature",
      "mappings": {
        "\u0013": [
          "gg"
        ],
        ",": [
          "fi"
        ]
      }
    }
  ],
  "fields": [
    {
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type": "first"
        }
      }
    }
  ]
}
```









