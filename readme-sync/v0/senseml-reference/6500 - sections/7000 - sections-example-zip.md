---
title: "Advanced: Zip sections"
hidden: false

---



Advanced: Zip table sections
====



The following example shows zipping multiple tables together by treating each table as a section group and each row or column as a section.

As an overview, this example shows creating a  `zipped_vehicle_description_and_coverages` array, where each  object in the array contains information from the vehicles table and from the limitations table in the following image:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_zip.png)



 It also illustrates the following sections behavior:

- Splitting tables into section group where each section is a row, agnostic of the text in the table.  For an illustration of this behavior, see [Section nuances](doc:section-nuances#multiple-anchors-in-section).
- Splitting tables into vertical section groups where each vertical section is a column, and treating "label" columns as anchoring data. For an illustration of this behavior, see  [Section nuances](docs/section-nuances#column-selection).
- Using SenseML execution order to output the zipped sections and suppress the source sections. See [Field extraction order](doc:field-order).



**Config**

```json
{
  "fields": [
    {
      "id": "_vehicles",
      "type": "sections",
      /* to get each row in vehicle table as a section,
         using start and end to define the section group range
         and .+ regex to match all rows as sections
         (last section in group continues to end of doc unless forced)
      */
      "range": {
        /* avoid including the column headings as a section
           using offsetY */
        "offsetY": 0.2,
        /* section group starts with 1st column heading in table */
        "anchor": {
          "start": {
            "text": "Vehicle",
            "type": "equals",
            "isCaseSensitive": true
          },
          "match": {
            /* Extract each row as a section. The underlying behavior is to 
              search for non-empty lines with regex ".+", then eliminate overlapping 
              horizontal sections and empty sections. */
            "type": "regex",
            "pattern": ".+"
          },
          /* to force the section group to end before "Schedule of coverages",
             define identical matches for end and stop
             (must define both to force the ".+" regex to end), 
             plus a stopOffsetY.
           */
          "end": {
            "type": "startsWith",
            "text": "Schedule of coverages",
            "isCaseSensitive": true
          }
        },
        "stopOffsetY": -1.0,
        "stop": {
          "type": "startsWith",
          "text": "Schedule of coverages",
          "isCaseSensitive": true
        },
      },
      "fields": [
        {
          "id": "vehicle_description",
          "method": {
            "id": "row",
            "tiebreaker": 0
          },
          "anchor": {
            "match": {
              "type": "first"
            }
          }
        },
        /* to illustrate section range, print out all text in this section */
        {
          "id": "_everything_in_this_vehicle_row_section",
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
    },
    {
      "id": "_coverages_per_vehicle",
      "type": "sections",
      "range": {
        "direction": "vertical",
        /* treat 1st two columns as row labels,
           output 2nd thru last columns as sections */
        "columnSelection": [
          [
            2,
            -1
          ]
        ],
        "anchor": {
          "match": {
            "type": "startsWith",
            "text": "Schedule of coverages",
            "isCaseSensitive": true
          }
        },
        /* don't include the "schedule of coverages" heading in section group */
        "offsetY": 0.3
      },
      "fields": [
        {
          /* each vertical section is a table slice determined
             by columnSelection that 
             combines the first two columns with one of the
             vehicle columns. In each table slice, the 2rd
             cell in the row that starts with "bodily injury liability"
             is always the injury premium for that section's vehicle */
          "id": "bodily_liability_premium",
          "type": "number",
          "method": {
            "id": "row",
            "tiebreaker": 1
          },
          "anchor": {
            "match": {
              "type": "includes",
              "text": "bodily injury liability"
            }
          }
        },
        {
          /* to illustrate section range, print out all text in this section */
          "id": "_everything_in_this_coverage_vertical_section",
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
    },
    /* output a zipped section group that combines vehicle
       info with coverage info */
    {
      "id": "zipped_vehicle_description_and_coverages",
      "method": {
        "id": "zip",
        "source_ids": [
          "_vehicles",
          "_coverages_per_vehicle"
        ]
      }
    },
    /* for cleaner output, remove the source
       section groups. illustrates configurable field execution order nuances */
    {
      "id": "cleanup_raw_source_sections",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "_vehicles",
          "_coverages_per_vehicle"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_zip.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections_zip.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "zipped_vehicle_description_and_coverages": [
    {
      "vehicle_description": {
        "value": "2003 Mits Lancer Es",
        "type": "string"
      },
      "_everything_in_this_vehicle_row_section": {
        "type": "string",
        "value": "1 2003 Mits Lancer Es 12345678901234"
      },
      "bodily_liability_premium": {
        "source": "89.70",
        "value": 89.7,
        "type": "number"
      },
      "_everything_in_this_coverage_vertical_section": {
        "type": "string",
        "value": "Coverages Limits of Liability Vehicle 1  Bodily injury liability $300,000 per 89.70  person Property damage $200,000 per 61.69  liability person"
      }
    },
    {
      "vehicle_description": {
        "value": "2019 Nissan pathfinder",
        "type": "string"
      },
      "_everything_in_this_vehicle_row_section": {
        "type": "string",
        "value": "2 2019 Nissan pathfinder 01234567890123"
      },
      "bodily_liability_premium": {
        "source": "138.66",
        "value": 138.66,
        "type": "number"
      },
      "_everything_in_this_coverage_vertical_section": {
        "type": "string",
        "value": "Coverages Limits of Liability  Vehicle 2 Bodily injury liability $300,000 per  138.66 person Property damage $200,000 per  79.45 liability person"
      }
    }
  ]
}
```
