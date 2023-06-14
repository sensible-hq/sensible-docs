---
title: "Ligature"
hidden: false
---


Intelligently replaces Unicode [ligatures](doc:ligatures) in a PDF text extraction. 

Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| type (**required**)     | `ligature` |                                                    |
| mappings (**required**) | object | An object mapping ligature strings (for example, `"\u0000"`) to an array of possible ligature replacements (for example, `["ff", "ffi", "fi", "fl"]`). Sensible uses a dictionary in the target language to choose replacements that lead to known words. Sensible supports American English (en-us). This approach is conservative and may leave some Unicode characters in proper names or other non-word data. |
| forceReplaceAll | false | If true, specifies to bypass the dictionary lookup and to replace each ligature with the first replacement listed in the mappings array. This is useful in situations where words containing ligatures are not in the supported dictionary. For example, they are in an unsupported language or are proper nouns. |

Examples
----

This config shows using a Ligature preprocessor and outputting the whole document to check the ligature replacement accuracy: 

```json
{
  "preprocessors": [
    {
      "type": "ligature",
      "mappings": {
        "\u0000": [
          "ff",
          "fi",
          "fl"
        ],
        "\u0001": [
          "ti",
          "tl"
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









