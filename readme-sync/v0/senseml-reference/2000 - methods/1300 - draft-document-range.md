---
title: "Document Range"
hidden: true
---


|         |      |                                                              |
| ------- | ---- | ------------------------------------------------------------ |
|         |      |                                                              |
|         |      |                                                              |
|         |      |                                                              |
|         |      |                                                              |
| offsetY |      | Offsets the start of the document range. Positive values offset down the page, negative values offset up the page. For example, use this parameter as an alternative to the Row method to extract multiline cells from a table.<br/> |

Examples
====

The following example shows using an Offset Y parameter with the Document Range method

```json
{
  "fields": [],
  "sections": [
    {
      "id": "injuries",
      "range": {
        "anchor": {
          "match": {
            "type": "includes",
            "text": "Claim number"
          }
        }
      },
      "fields": [
        {
          "id": "injury_multiline",
          "method": {
            "id": "documentRange",
            "stop": {
              "text": "Claim date",
              "type": "startsWith"
            },
            "offsetY": -0.3
          },
          "anchor": {
            "match": {
              "type": "startsWith",
              "text": "Injury"
            }
          }
        }
      ]
    }
  ]
}
```

