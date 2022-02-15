---
title: "Sections example 4"
hidden: true

---


Vertical sections: table grid
====

Overview
----

To give a broad overview using vertical sections for a table grid:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_table_grid.png)

In the preceding image, 1. define a section then 2.  define a nested vertical section.  The following abbreviated YML notation to give a brief idea of the more complex SenseML JSON, and shows:

- Using the Offset Y parameter in a vertical section to exclude non-columnar headings (for example, "2014 Toyota Camry") so as not to break column recognition.
- The parent section group, `car_model`, uses an offset to include the heading with car model and year. 
- The parent section demonstrates that without a Require Stop parameter, Sensible starts the next section on the first repeated instance of `trim` that follows the starting line vertically, but ignores repeats on the same horizontal line as the starting line. The nested section demonstrates the same behavior with the match-all regex `.+` . For more information, see TODO LINK section-nuances#multiple anchor matches.
- Configuring column recognition in a vertical section with the Min Column Gap parameter, so that column recognition doesn't break on the whitespace gaps within each trim specs column. 

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

With this approach, you can output something like the following, using abbreviated YML notation to give a brief idea of the more complex JSON API response:

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
        "offsetY": -1.1,
        "anchor": {
          "match": {
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
            "offsetY": 0.5,
            "minColumnGap": 0.5,
            "anchor": {
              "match": {
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

**PDF**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_section_table_grid_1.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_sections_table_grid.pdf) |
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
