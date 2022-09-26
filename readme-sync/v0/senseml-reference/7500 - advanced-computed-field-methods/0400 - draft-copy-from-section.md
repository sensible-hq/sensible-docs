---
title: "Copy FROM section"
hidden: true
---
https://dev.sensible.so/editor/?d=frances_test_playground&c=copy_from_section_final&g=copy_from_sections_final&v=

```
{
  "fields": [
    {
      "type": "sections",
      /* to find repeated instances of vertical sections (the "schedule of coverages"
         table),
         wrap the vertical sections in a parent section group
         also wrap the covered vehicles description talbe in the same parent
         TODO illustration of this... */
      "id": "parent_section_group_declarations",
      "range": {
        "anchor": {
          "match": "covered vehicles"
        }
      },
      "fields": [
        {
          /* section group for 1st table */
          "id": "_vehicles",
          "type": "sections",
          "range": {
            /* each section in group starts with "Vehicle VIN"
           todo: OFFSET?? */
            "anchor": {
              "match": {
                "text": "Vehicle VIN",
                "type": "startsWith",
                "isCaseSensitive": true
              },
            },
            /* each section in group ends after "vehicle no" line
          ( + offset)
        */
            "stop": {
              "type": "startsWith",
              "text": "Vehicle no",
              "isCaseSensitive": true
            }
          },
          "fields": [
            {
              "id": "vehicle_description",
              "method": {
                "id": "label",
                "position": "right"
              },
              "anchor": "Description"
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
          /* TODO LEFT OFF: hmmmm how to get the last schedule of coverages??? */
          /* section group for 2nd table */
          "id": "_coverages_per_vehicle",
          "type": "sections",
          "range": {
            "direction": "vertical",
            /* treat 1st two columns as row labels,
           output 3rd thru last columns as sections */
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
              },
            },
            /* exclude "schedule of coverages" heading from section group 
           to avoid breaking column recognition */
            "offsetY": 0.3,
            /* ignore "covered vehicles" text between two vertical column-style tables
           which would otherwise break column recognition */
            /* todo left off: hrrmm there are two 'rows' both with bodily injury liabitiliy
           which means you'd have to specify the # of tables which don't make sense...
          how did damon do it again? or better yet, choose an easier section, 
          maybe not a vertical one!!   */
            "stop": "total 12 month premium for all vehicles"
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
       section groups. illustrates configurable field execution order nuances
       TBD: add it in? which would we remove? */
      ]
    },
    {
      "id": "copy_from_sections_vehicles",
      "method": {
        "id": "copy_from_sections",
        "source_sections": "parent_section_group_declarations",
        "source_field": "zipped_vehicle_description_and_coverages"
      }
    }
  ]
}
```







Copies a field from a section group into a new field. This is useful for cleaning up the output of complex nested sections.





Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                 | description                                                  |
| :----------------------- | :------------------------------------ | :----------------------------------------------------------- |
| id (**required**)        | `copy_to_section`                     |                                                              |
| source_id (**required**) | source field ID in the current config | The source ID to copy must be in a field array or section that is one level up in the hierarchy relative to the destination section. For example, in a section, copy from the base fields array. In a subsection, copy from the parent section's field array. |
|                          |                                       |                                                              |

Examples
====

