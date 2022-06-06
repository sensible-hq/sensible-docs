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

**Config**

The following example shows using an Offset Y parameter with the Document Range method to extract multiline rows. Since the target cell precedes the anchor, the example uses a negative offset to capture the cell contents. 

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
            "text": "claim number"
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
            "offsetY": -0.3,
            "typeFilters": ["date"]
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

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/document_range_yoffset.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/document_range_yoffset.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "injuries": [
    {
      "injury_multiline": {
        "type": "string",
        "value": "Slip and fall, from threshold of foyer"
      }
    },
    {
      "injury_multiline": {
        "type": "string",
        "value": "Slip and fall"
      }
    },
    {
      "injury_multiline": {
        "type": "string",
        "value": "Slip and fall, on wet breakroom tile"
      }
    }
  ]
}
```
