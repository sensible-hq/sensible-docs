---
title: "Labled rows example"
hidden: true
---

The following examples shows using a vertical section to capture a table that has both column labels and row labels. It also shows:

- Using the Column Selection parameter to output the second through second-to-last columns and make other columns available as anchoring information for each output column.
- To aid column recognition, excluding the anchor from the vertical section using the Offset Y parameter.



**Config**

```json
{
  "fields": [],
  "sections": [
    {
      "id": "nutrition_per_fruit",
      "range": {
        "direction": "vertical",
        "columnSelection": [
          [1, -1]
        ],
        "anchor": {
          "match": {
            "type": "equals",
            "text": "Nutrition info",
            "isCaseSensitive": true
          }
        },
        "offsetY": 0.3
      },
      "fields": [
        {
          "id": "fruit_name",
          "anchor": {
            "match": {
              "text": "nutrition",
              "type": "equals"
            }
          },
          "method": {
            "id": "row",
            "tiebreaker": "first"
          }
        },
        {
          "id": "fiber",
          "type":"number",
          "anchor": {
            "match": {
              "text": "fiber",
              "type": "startsWith"
            }
          },
          "method": {
            "id": "row",
            "tiebreaker": "first"
          }
        }
      ]
    }
  ]
}
```

**PDF**

The following image shows the data extracted by this config for the following example PDF:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_labeled_rows.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_sections_labeled_rows.pdf) |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "nutrition_per_fruit": [
    {
      "fruit_name": {
        "value": "Apple",
        "type": "string"
      },
      "fiber": {
        "source": "2.4",
        "value": 2.4,
        "type": "number"
      }
    },
    {
      "fruit_name": {
        "value": "Banana",
        "type": "string"
      },
      "fiber": {
        "source": "3.1",
        "value": 3.1,
        "type": "number"
      }
    },
    {
      "fruit_name": {
        "value": "Cantelope",
        "type": "string"
      },
      "fiber": {
        "source": "0.9",
        "value": 0.9,
        "type": "number"
      }
    }
  ]
}
```
