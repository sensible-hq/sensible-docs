---
title: "Advanced: Zip sections"
hidden: false

---



Advanced: Zip table sections
====



The following example shows zipping multiple tables together by treating each table as a section group and each row or column as a section.

**Note:** For an alternative to this example, see [Example 3: Zip tables](doc:zip).

As an overview, this example shows creating a  `zipped_vehicle_description_and_coverages` array, where each  object in the array contains information from the vehicles table and from the limitations table in the following image:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_zip.png)



 It also illustrates the following sections behavior:

- Splitting tables into sections, where each section is a row, agnostic of the text in the table.  For an illustration of this behavior, see [Section nuances](doc:section-nuances#multiple-anchors-in-section).
- Uses the Column Selection parameter in a vertical sections group to make sections out of table "slices". For more information about the Column Selection parameter, see [Section nuances](doc:section-nuances#column-selection).
- Using SenseML execution order to output the zipped section group and suppress the source section groups. See [Field extraction order](doc:field-order).



**Config**

```json
{
  "fields": [
    {
      /* section group for 1st table */  
      "id": "_vehicles",
      "type": "sections",
      /* to get each row in vehicle table as a section,
         use start and end to define the section group range
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
      /* section group for 2nd table */
      "id": "_coverages_per_vehicle",
      "type": "sections",
      "range": {
        "direction": "vertical",
        /* columnSelection specifies that each vertical section is a table slice that
           combines the first two columns ("kept" columns) with one of the
           numbered vehicle columns (3rd through last columns). */
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
        /* exclude "schedule of coverages" heading from section group 
           to avoid breaking column recognition */
        "offsetY": 0.3
      },
      "fields": [
        {
          /* In each vertical section, the 2nd
             cell to the right of "bodily injury liability"
             is always the injury premium for that section's vehicle,
             as configured by columnSelection */
          "id": "bodily_liability_premium",
          "type": "number",
          "method": {
            "id": "row",
            "tiebreaker": "second"
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
            /* remove these IDs to see section ranges displayed in the Sensible app */
          "_vehicles",
          "_coverages_per_vehicle"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_zip.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_sections_zip.pdf) |
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
