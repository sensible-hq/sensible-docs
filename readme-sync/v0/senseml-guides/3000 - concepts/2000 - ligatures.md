---
title: "Ligatures"
hidden: false
---

*Ligatures* are two or more letters joined together into a single glyph. They appear to be garbage Unicode characters in your PDF direct text extraction, for example:

```json
….incinerating or composting toilets; \u0000re suppression systems; water softeners, conditioners or \u0000ltering systems; over\u0000ow drains for tubs and sinks; back\u0000ow prevention devices...
```

Even if the rendered PDF looks fine, ligatures can still exist in the extracted text. In the preceding example, a text extractor incorrectly joined `fi`, `fl` and others together so they appear as `\u0000` in the raw text. You see `\u0000re` instead of `fire` and `over\u0000ow` instead of `overflow`.

To find out if ligatures exist in the extracted text for your PDF, extract all the lines in the PDF and search for Unicode characters. To extract all lines into one key-value pair, use a config like:

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



