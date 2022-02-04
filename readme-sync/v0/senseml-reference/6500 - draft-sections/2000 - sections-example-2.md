---
title: "Sections"
hidden: true
---



Vertical sections: complex tables
----

The following example shows:

- using a vertical section group to handle row labels in a table with the Column Selection parameter.
- extracting nested table using a nested section group. In the nested section group, each row of the nested table is its own section. (The regular expression to find these "row" sections also generates zero-height sections that Sensible ignores).

**Config**

TODO: test config works with regex change I made...

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
      "id": "sections",
      "range": {
        "direction": "vertical",
        "columnSelection": [
          1,
          2
        ],
        "minSpace": 0,
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
        }
      ],
      "sections": [
        {
          "id": "benefit_reduction",
          "range": {
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
  "sections": [
    {
      "employee_benefit": {
        "value": "100% of salary, max $100k",
        "type": "string"
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
          }
        }
      ]
    },
    {
      "employee_benefit": {
        "value": "50% of salary, max $50k",
        "type": "string"
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
          }
        }
      ]
    }
  ]
}
```



n-nuances.
