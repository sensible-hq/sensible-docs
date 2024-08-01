---
title: replace type
hidden: true
---

Replace
====

Returns the

TODO: add more params to it?



EXAMPLE: see

`https://dev.sensible.so/editor/?d=frances_playground&c=replace_type_docs&g=replace_sample_acord_redacted`

Alternatives:

- custom computation method
- Compose type in combination with Custom type

**Config**

```json
{
  "fields": [
    {
      /* the source text has unexpected whitespaces
         use the Replace type to strip the whitespaces
         and the Compose method to convert the stripped output
         to a currency  */
      "id": "each_accident",
      "anchor": {
        "match": {
          "text": "EMPLOYER'S LIABILITY",
          "type": "includes"
        }
      },
      "type": {
        "id": "compose",
        "types": [
          {
            "id": "replace",
            /* find all capital letters and whitespaces */
            "pattern": "[A-Z\\s+]",
            /*  strip them from the output */
            "replaceWith": ""
          },
          /* convert the output of the Replace type to a currency */
          "currency"
        ]
      },
      "method": {
        "id": "region",
        "start": "left",
        "offsetX": 0,
        "offsetY": 0.1,
        "width": 3,
        "height": 0.2,
        "sortLines": "readingOrderLeftToRight",
      }
    },
    {
      /* without the regex type to strip out whitespaces,
         Sensible can't recognize the amount as a currency */
      "id": "_each_accident_raw",
      "anchor": {
        "match": {
          "text": "EMPLOYER'S LIABILITY",
          "type": "includes"
        }
      },
      "method": {
        "id": "region",
        "start": "left",
        "offsetX": 0,
        "offsetY": 0.1,
        "width": 3,
        "height": 0.2,
        "sortLines": "readingOrderLeftToRight",
      }
    },
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/replace_type.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/replace_type.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "each_accident": {
    "source": "$500,000",
    "value": 500000,
    "unit": "$",
    "type": "currency"
  },
  "_each_accident_raw": {
    "type": "string",
    "value": "$ 50 0 , 000 ACCIDEN EACH T"
  }
}
```
