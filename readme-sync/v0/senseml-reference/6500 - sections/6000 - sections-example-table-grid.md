---
title: "Advanced: Table grid example"
hidden: false

---

This example shows:

- Finding repeating vertical sections by nesting them in parent sections.
- Ignoring repeated multiple anchor matches. For more information, see [Multiple anchors in section](doc:section-nuances#multiple-anchors-in-section).

Overview
----

To give a broad overview of using vertical sections for a table grid, see the following image:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_table_grid.png)

In the preceding image, the config uses sections as follows:

1. Defines sections for car models, including their trims.

2. Defines nested vertical sections for car trims.

The following abbreviated YML notation to give a brief idea of the more complex SenseML JSON:

```yml
sections:
  - id: car_model
    range:
      anchor: trim
      offsetY: -1.1
    fields:
      - id: car_heading
        anchor:
          match:
            type: first
        method:
          id: passthrough
   sections:
     - id: trim_specs
       range:
         direction: vertical
         offsetY: 0.5
         minColumnGap: 0.5
         anchor:
           match:
             type: regex
             pattern: .+
       fields:
         - id: trim_name
           anchor:
            match:
              type: first
           method:
             id: passthrough
         - id: engine
           anchor: engine
           method:
             id: row
             position: right
      
```

With this approach, you can output something like the following, using abbreviated YML notation to give a brief idea of the more complex JSON extraction response:

```yml
car_models:
  - car_heading: 2014 Toyota Camry
    trim_specs:
      - trim_name: LE trim
        engine: 178.0-hp, 2.5-liter, 4
      - trim_name: XLE trim
        engine: 268.0-hp, 3.5-liter, V6     
  - car_heading: 2022 Honda Civic
    trim_specs:
      - trim_name: EX trim
        engine: 180.0-hp, 1.5-liter, 4
      - trim_name: LX trim
        engine: 158.0-hp, 2.0-liter, 4 
   
```

Details
----

The following elaborates on the preceding brief overview using JSON instead of YML. To illustrate each section's range and for troubleshooting purposes, the config includes a field that outputs the entire contents of each section.

**Config**

```json
{
  "fields": [],
  "sections": [
    {
      "id": "car_models",
      "range": {
        /* uses an offset to include the heading with car model and year */
        "offsetY": -1.1,
        "anchor": {
          "match": {
            /* Sensible starts the next section on the first repeated instance of `trim` that 
            follows the starting line vertically. Sensible ignores repeated `trim` instances
            that occur on the same horizontal line as the starting line, so there's no need 
            to configure requireStop.
            */
            "type": "endsWith",
            "text": "trim"
          }
        }
      },
      "fields": [
        {
          "id": "car_heading",
          "method": {
            "id": "passthrough"
          },
          "anchor": {
            "match": {
              "type": "first"
            }
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
          "id": "trim_specs",
          "range": {
            "direction": "vertical",
            /* exclude non-columnar headings (for example, "2014 Toyota Camry") so as not to break column recognition.
               Sensible recognizes each trim table as one column */
            "offsetY": 0.5,
            /* use a large minColumnGap so column recognition doesn't break on the whitespace gaps in each trim specs column */
            "minColumnGap": 0.5,
            "anchor": {
              "match": {
                /* 
                  Since the parent section group defines the range for the child vertical section group,
                  you don't need to find specific text matches in the trim spec tables.
                  Match on all text with ".+" 
               */
                "type": "regex",
                "pattern": ".+"
              }
            }
          },
          "fields": [
            {
              "id": "everything_in_this_nested_section",
              "method": {
                "id": "documentRange",
                "includeAnchor": true
              },
              "anchor": {
                "match": {
                  "type": "first"
                }
              }
            },
            {
              "id": "trim_name",
              "method": {
                "id": "passthrough"
              },
              "anchor": {
                "match": {
                  "type": "first"
                }
              }
            },
            {
              "id": "engine",
              "method": {
                "id": "row",
                "position": "right"
              },
              "anchor": {
                "match": {
                  "type": "startsWith",
                  "text": "engine"
                }
              }
            },
          ]
        }
      ]
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_section_table_grid_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_sections_table_grid.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "car_models": [
    {
      "car_heading": {
        "type": "string",
        "value": "2014 Toyota Camry"
      },
      "everything_in_this_section": {
        "type": "string",
        "value": "2014 Toyota Camry LE trim XLE trim Engine 178.0-hp, 2.5-liter, 4 Engine 268.0-hp, 3.5-liter, V6 cylinder cylinder Transmission 6-speed A/T Transmission 6-speed A/T"
      },
      "trim_specs": [
        {
          "everything_in_this_nested_section": {
            "type": "string",
            "value": "LE trim  Engine 178.0-hp, 2.5-liter, 4   cylinder  Transmission 6-speed A/T  "
          },
          "trim_name": {
            "type": "string",
            "value": "LE trim"
          },
          "engine": {
            "type": "string",
            "value": "178.0-hp, 2.5-liter, 4"
          }
        },
        {
          "everything_in_this_nested_section": {
            "type": "string",
            "value": "XLE trim   Engine 268.0-hp, 3.5-liter, V6  cylinder   Transmission 6-speed A/T"
          },
          "trim_name": {
            "type": "string",
            "value": "XLE trim"
          },
          "engine": {
            "type": "string",
            "value": "268.0-hp, 3.5-liter, V6"
          }
        }
      ]
    },
    {
      "car_heading": {
        "type": "string",
        "value": "2022 Honda Civic"
      },
      "everything_in_this_section": {
        "type": "string",
        "value": "2022 Honda Civic EX trim LX trim Engine 180.0-hp, 1.5-liter, 4 Engine 158.0-hp, 2.0-liter, 4 cylinder cylinder Transmission CVT Transmission Transmission CVT Transmission"
      },
      "trim_specs": [
        {
          "everything_in_this_nested_section": {
            "type": "string",
            "value": "EX trim  Engine 180.0-hp, 1.5-liter, 4   cylinder  Transmission CVT Transmission  "
          },
          "trim_name": {
            "type": "string",
            "value": "EX trim"
          },
          "engine": {
            "type": "string",
            "value": "180.0-hp, 1.5-liter, 4"
          }
        },
        {
          "everything_in_this_nested_section": {
            "type": "string",
            "value": "LX trim   Engine 158.0-hp, 2.0-liter, 4  cylinder   Transmission CVT Transmission"
          },
          "trim_name": {
            "type": "string",
            "value": "LX trim"
          },
          "engine": {
            "type": "string",
            "value": "158.0-hp, 2.0-liter, 4"
          }
        }
      ]
    }
  ]
}
```
