---
title: "Advanced: nested table example"
hidden: false
---

The following example:

- Uses the Column Selection parameter in a vertical sections group to make sections out of table "slices". For more information about the Column Selection parameter, see [Section nuances](doc:section-nuances#column-selection).
- Uses relative column coordinates to find nested tables in each column table. (`"columnsRelativeToAnchor":"true"`).

**Config**



```json
{
  "preprocessors": [
    {
      "type": "splitLines",
      "minSpaces": 3
    }
  ],
  "fields": [
    {
      "id": "table_columns",
      "type": "sections",
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
          "id": "employee_category",
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
          "id": "employee_benefit",
          "anchor": "Employee benefit",
          "method": {
            "id": "row",
            "position": "right",
            "tiebreaker": "first"
          }
        },
        {
          "id": "reduction_subtable",
          "type": "table",
          "method": {
            "id": "textTable",
            "columnsRelativeToAnchor": true,
            "offsetY": -0.3,
            "columns": [
              {
                "id": "col1_age",
                "minX": -0.1,
                "maxX": 0.5,
                "type": "number"
              },
              {
                "id": "col2_reduction",
                "minX": 0.5,
                "maxX": 2.4,
                "type": "percentage",
                "isRequired": true
              }
            ],
            "stop": {
              "type": "startsWith",
              "text": "for more details about coverage"
            }
          },
          "anchor": {
            "match": {
              "type": "startsWith",
              "text": "age"
            }
          }
        },
        {
          "id": "everything_in_this_vertical_section",
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
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_table_in_table.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_section_table_in_table.pdf) |
| ----------- | ------------------------------------------------------------ |



**Output**

```json
{
  "table_columns": [
    {
      "employee_category": {
        "type": "string",
        "value": "Employees paid \u0000100k"
      },
      "employee_benefit": {
        "value": "100% of salary, max $100k",
        "type": "string"
      },
      "reduction_subtable": {
        "columns": [
          {
            "id": "col1_age",
            "values": [
              {
                "source": "65",
                "value": 65,
                "type": "number"
              },
              {
                "source": "70",
                "value": 70,
                "type": "number"
              },
              {
                "source": "75",
                "value": 75,
                "type": "number"
              }
            ]
          },
          {
            "id": "col2_reduction",
            "values": [
              {
                "source": "35%",
                "value": 35,
                "type": "percentage"
              },
              {
                "source": "60%",
                "value": 60,
                "type": "percentage"
              },
              {
                "source": "75%",
                "value": 75,
                "type": "percentage"
              }
            ]
          }
        ]
      },
      "everything_in_this_vertical_section": {
        "type": "string",
        "value": "Employees paid \u0000100k  Notes Employee benefit 100% of salary, max $100k  After a 3 month waiting period Common carrier Not included  Benefit reduction Age Reduction   Not adjusted for 65 35%   inflation 70 60%   75 75%   For more details about coverage and benefits, see the following sections."
      }
    },
    {
      "employee_category": {
        "type": "string",
        "value": "All other employees"
      },
      "employee_benefit": {
        "value": "50% of salary, max $50k",
        "type": "string"
      },
      "reduction_subtable": {
        "columns": [
          {
            "id": "col1_age",
            "values": [
              {
                "source": "65",
                "value": 65,
                "type": "number"
              },
              {
                "source": "70",
                "value": 70,
                "type": "number"
              },
              {
                "source": "75",
                "value": 75,
                "type": "number"
              }
            ]
          },
          {
            "id": "col2_reduction",
            "values": [
              {
                "source": "35%",
                "value": 35,
                "type": "percentage"
              },
              {
                "source": "60%",
                "value": 60,
                "type": "percentage"
              },
              {
                "source": "75%",
                "value": 75,
                "type": "percentage"
              }
            ]
          }
        ]
      },
      "everything_in_this_vertical_section": {
        "type": "string",
        "value": "All other employees Notes Employee benefit  50% of salary, max $50k After a 3 month waiting period Common carrier  Not included Benefit reduction   Age Reduction Not adjusted for   65 35% inflation   70 60%   75 75% For more details about coverage and benefits, see the following sections."
      }
    }
  ]
}
```
