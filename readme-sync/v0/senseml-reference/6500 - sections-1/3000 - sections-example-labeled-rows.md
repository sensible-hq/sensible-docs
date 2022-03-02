---
title: "Labled rows example"
hidden: true
---

The following examples shows using a vertical section to capture a table that has both column labels and row labels. It also shows:

- Using the Column Selection parameter to exclude the first and last columns from the output but make their text available as anchoring information for each outputted column.
- To aid column recognition, excluding the anchor from the vertical section using the Offset Y parameter.
- To illustrate each section's range, the config includes a field that outputs the entire contents of each section.



**Config**

```json
{
  "fields": [],
  "sections": [
    {
      "id": "nutrition_per_fruit",
      "range": {
        "direction": "vertical",
        "columnSelection": [[1,-2]],
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
          "type": "number",
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
        },
        {
          "id": "everything_in_this_section",
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
  ]
}
```

**Example document**

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
      },
      "everything_in_this_section": {
        "type": "string",
        "value": "Nutrition Apple   Notes Calories 50   Per 100 g Fiber (g) 2.4   Skin on, if applicable Protein (g) 0.5  "
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
      },
      "everything_in_this_section": {
        "type": "string",
        "value": "Nutrition  Banana  Notes Calories  90  Per 100 g Fiber (g)  3.1  Skin on, if applicable Protein (g)  1.3 "
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
      },
      "everything_in_this_section": {
        "type": "string",
        "value": "Nutrition   Cantelope Notes Calories   34 Per 100 g Fiber (g)   0.9 Skin on, if applicable Protein (g)   0.8"
      }
    }
  ]
}
```
