---
title: "Advanced: nested table example"
hidden: true
---

The following example shows:

- using the Column Selection parameter in a vertical sections group to handle row labels in a table.
- Since table recognition works on the whole page, the example uses a nested section group to extract a nested table.  In the nested section group, each row of the nested table is its own section. For more information, see TODO LINK section-nuances#multiple anchor matches. 
- To illustrate each section's range, the config includes a field that outputs the entire contents of each section.

**Config**



```
{
  "preprocessors": [
    {
      "type": "splitLines",
      "minSpaces": 3
    }
  ],
  "fields": [],
  "sections": [
    {
      "id": "table_columns_w_row_labels",
      "range": {
        "direction": "vertical",
        "columnSelection": [
          1,
          2
        ],
        "offsetY": -0.5,
        "anchor": "Employee benefit",
        "stop": {
          "text": "for more details",
          "type": "includes"
        }
      },
      "fields": [
        {
          "id": "employee_benefit",
          "anchor": "Employee benefit",
          "method": {
            "id": "row",
            "position": "right",
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
      ],
      "sections": [
        {
          "id": "benefit_reduction",
          "range": {
            "offsetY": 0.1,
            "anchor": {
              "start": "Benefit reduction",
              "match": {
                "type": "regex",
                "pattern": ".+"
              }
            }
          },
          "fields": [
            {
              "id": "age",
              "type": "number",
              "anchor": {
                "match": {
                  "type": "first"
                }
              },
              "method": {
                "id": "passthrough"
              }
            },
            {
              "id": "reduction",
              "type": "percentage",
              "anchor": {
                "match": [
                  {
                    "type": "first"
                  },
                  {
                    "type": "first"
                  }
                ]
              },
              "method": {
                "id": "passthrough"
              }
            },
            {
              "id": "everything_in_this_subsection",
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
  ]
}
```

**PDF**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_table_in_table.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_section_table_in_table.pdf) |
| ----------- | ------------------------------------------------------------ |



**Output**

```json
{
  "table_columns_w_row_labels": [
    {
      "employee_benefit": {
        "value": "100% of salary, max $100k",
        "type": "string"
      },
      "everything_in_this_section": {
        "type": "string",
        "value": "Employees paid \u0000100k  Notes Employee benefit 100% of salary, max $100k  After a 3 month waiting period Common carrier Not included  Benefit reduction Age Reduction   Not adjusted for 65 35%   inflation 70 60%   75 75%  "
      },
      "benefit_reduction": [
        {
          "age": {
            "source": "65",
            "value": 65,
            "type": "number"
          },
          "reduction": {
            "source": "35%",
            "value": 35,
            "type": "percentage"
          },
          "everything_in_this_subsection": {
            "type": "string",
            "value": "65 35%   inflation    "
          }
        },
        {
          "age": {
            "source": "70",
            "value": 70,
            "type": "number"
          },
          "reduction": {
            "source": "60%",
            "value": 60,
            "type": "percentage"
          },
          "everything_in_this_subsection": {
            "type": "string",
            "value": "70 60%    "
          }
        },
        {
          "age": {
            "source": "75",
            "value": 75,
            "type": "number"
          },
          "reduction": {
            "source": "75%",
            "value": 75,
            "type": "percentage"
          },
          "everything_in_this_subsection": {
            "type": "string",
            "value": "75 75%  "
          }
        }
      ]
    },
    {
      "employee_benefit": {
        "value": "50% of salary, max $50k",
        "type": "string"
      },
      "everything_in_this_section": {
        "type": "string",
        "value": "All other employees Notes Employee benefit  50% of salary, max $50k After a 3 month waiting period Common carrier  Not included Benefit reduction   Age Reduction Not adjusted for   65 35% inflation   70 60%   75 75%"
      },
      "benefit_reduction": [
        {
          "age": {
            "source": "65",
            "value": 65,
            "type": "number"
          },
          "reduction": {
            "source": "35%",
            "value": 35,
            "type": "percentage"
          },
          "everything_in_this_subsection": {
            "type": "string",
            "value": "65 35% inflation    "
          }
        },
        {
          "age": {
            "source": "70",
            "value": 70,
            "type": "number"
          },
          "reduction": {
            "source": "60%",
            "value": 60,
            "type": "percentage"
          },
          "everything_in_this_subsection": {
            "type": "string",
            "value": "70 60%  "
          }
        },
        {
          "age": {
            "source": "75",
            "value": 75,
            "type": "number"
          },
          "reduction": {
            "source": "75%",
            "value": 75,
            "type": "percentage"
          },
          "everything_in_this_subsection": {
            "type": "string",
            "value": "75 75%"
          }
        }
      ]
    }
  ]
}
```
