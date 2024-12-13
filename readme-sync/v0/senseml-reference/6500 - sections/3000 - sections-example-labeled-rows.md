---
title: "Labeled rows example"
hidden: false
---

The following example shows using a vertical section group to capture a table that has both column labels and row labels. It also shows using the Column Selection parameter to create sections out of all but the last and first columns. For more information about the Column Selection parameter, see [Section nuances](doc:section-nuances#column-selection).



**Config**

```json
{
  "fields": [
    {
      "id": "nutrition_table",
      "type": "sections",
      "range": {
        "direction": "vertical",
        /* columnSelection specifies that each vertical section is a table slice that
           combines the first and last columns ("kept" columns) with one of the
           "fruit" columns (2rd through 2nd-to-last columns). */
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
        /* In each vertical section, the 1st
             cell to the right of "Nutrition"
             is always the name for that section's fruit,
             as configured by columnSelection */
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

The following image shows the data extracted by this config for the following example document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_labeled_rows.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_sections_labeled_rows.pdf) |
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
