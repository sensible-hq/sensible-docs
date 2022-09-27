---
title: "Labeled rows example"
hidden: false
---

The following example shows using a vertical section group to capture a table that has both column labels and row labels. It also shows:

- Using the Column Selection parameter to exclude the first and last columns from the output but make their text available as anchoring information for each outputted column.



**Config**

```json
{
  "fields": [],
  "sections": [
    {
      "id": "nutrition_table",
      "range": {
        "direction": "vertical",
        /* treat 1st and last columns as anchor candidates,
           output 2nd thru 2nd-to-last columns as sections */
        "columnSelection": [
          [
            1,
            -2
          ]
        ],
        "anchor": {
          "match": {
            "type": "equals",
            "text": "Nutrition",
            "isCaseSensitive": true
          }
        },
        /* section group ends below "protein" */
        "stop": "protein",
        /* since anchor match occurs in table, set offset to avoid 
           cutting off 1st row */
        "offsetY": -0.3
      },
      "fields": [
        /* each vertical section is a table slice determined
             by columnSelection that 
             combines the "anchoring" columns with one of the
             fruit columns. In each table slice, the 1st
             cell to the right of "Nutrition"
             is always the name for that section's fruit */
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
          /* to illustrate section range, output all text in this section */
          "id": "_everything_in_this_section",
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
  "nutrition_table": [
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
      "_everything_in_this_section": {
        "type": "string",
        "value": "Nutrition Apple Notes Calories 50 Per 100 g Fiber (g) 2.4 Skin on, if applicable Protein (g) 0.5"
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
      "_everything_in_this_section": {
        "type": "string",
        "value": "Nutrition Banana Notes Calories 90 Per 100 g Fiber (g) 3.1 Skin on, if applicable Protein (g) 1.3"
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
      "_everything_in_this_section": {
        "type": "string",
        "value": "Nutrition Cantelope Notes Calories 34 Per 100 g Fiber (g) 0.9 Skin on, if applicable Protein (g) 0.8"
      }
    }
  ]
}
```
