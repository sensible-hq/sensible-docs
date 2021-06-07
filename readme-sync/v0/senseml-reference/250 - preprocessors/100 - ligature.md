---
title: "Ligature"
hidden: false
---


Intelligently replaces Unicode ligatures in PDF text extraction.  For more information about ligatures, see the Notes section.

Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)     | `ligature` |                                                    |
| `mappings` (**required**) | object | An object mapping ligature strings (e.g., `"\u0000"`) to an array of possible ligature replacements (e.g., `["ff", "ffi", "fi", "fl"]`). Sensible uses a dictionary in the target language to choose replacements that lead to known words. Currently Sensible supports American English (en-us). This approach is conservative and may leave some Unicode characters in proper names or other non-word data. |

Examples
----

This config  includes a ligature mapping preprocessor and shows the output of the whole document in order to check the ligature replacement accuracy: 

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





Notes
----

*Ligatures* are two or more letters joined together into a sign glyph. They appear to be garbage Unicode characters in your direct text extraction, like this:

```json
….incinerating or composting toilets; \u0000re suppression systems; water softeners, conditioners or \u0000ltering systems; over\u0000ow drains for tubs and sinks; back\u0000ow prevention devices...
```

Even if the PDF rendering looks fine, ligatures can still exist in the extracted text. In the preceding example, `fi`, `fl` and others are joined together and appear as `\u0000` in the raw text, so that you see `\u0000re` instead of `fire` and `over\u0000ow` instead of `overflow`.

To find out if ligatures exist in the extracted text for your PDF, you can extract all the lines in the PDF and search for unicode characters. To extract all lines into one key-value pair, you can use a config like:

```
{
  "fields": [
     
    {
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type":"first"
        }
      }
    }
  ],
}
```

The following image shows an example of capturing all the lines of text in a W-9 form:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/all_lines.png)




