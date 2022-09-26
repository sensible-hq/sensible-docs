---
title: "Advanced: Zip and flatten nested sections"
hidden: false

---



The following example shows using the Copy from Sections computed method to flatten the output of nested and zipped sections. 

In this example, the config uses paired section groups nested in a parent section group to extract complete vehicle insurance declarations:

1. A parent section group's range contains the entire vehicle declaration.

2. A child section group captures data such as the vehicle description and VIN.

3. A child section group captures data such as the coverages and premiums:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/copy_from_sections_2.png)

If you [zip the child sections together](doc:sections-example-zip), you can output something like the following, using abbreviated YML notation to give an overview of the more complex JSON API response:

```yaml
parent_section_group_declarations:
- _zipped_vehicle_description_and_coverages:
  - vehicle_description:
      value: 2003 Mits Lancer Es
    bodily_liability_premium:
      value: 89.7
  - vehicle_description:
      value: 2019 Nissan Pathfinder
    bodily_liability_premium:
      value: 138.66
- _zipped_vehicle_description_and_coverages:
  - vehicle_description:
      value: 2010 Toyota Corolla
    bodily_liability_premium:
      value: 100.1
  - vehicle_description:
      value: 2012 Honda Accord
    bodily_liability_premium:
      value: 140.8
```

This example shows flattening the repeated `_zipped_vehicle_description_and_coverages` arrays, using the Copy From Sections method to produce something like the following:

```json
flattened_declarations:
  - vehicle_description:
      value: 2003 Mits Lancer Es
    bodily_liability_premium:
      value: 89.7
  - vehicle_description:
      value: 2019 Nissan Pathfinder
    bodily_liability_premium:
      value: 138.66
  - vehicle_description:
      value: 2010 Toyota Corolla
    bodily_liability_premium:
      value: 100.1
  - vehicle_description:
      value: 2012 Honda Accord
    bodily_liability_premium:
      value: 140.8
```



Details
----

The following elaborates on the preceding overview using JSON instead of YML.



**Config**

```json
{
  "fields": [
    {
      "type": "sections",
      /*  parent section group finds repeated pairs of Covered vehicles (nested horizontal section group)
          and Schedule of coverages (nested vertical section group). */
      "id": "parent_section_group_declarations",
      "range": {
        "anchor": {
          "match": "covered vehicles"
        }
      },
      "fields": [
        {
          /* nested section group for Covered vehicles*/
          "id": "_covered_vehicles",
          "type": "sections",
          "range": {
            /* each section in group starts with "Vehicle VIN" */
            "anchor": {
              "match": {
                "text": "Vehicle VIN",
                "type": "startsWith",
                "isCaseSensitive": true
              },
            },
            /* each section in group ends after "vehicle no." line */
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
              "anchor": "description:"
            },
            /* to illustrate section range, print out all text in this section */
            {
              "id": "_everything_in_this_covered_vehicle_section",
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
          /* nested section group for Schedule of coverages */
          "id": "_coverages_per_vehicle",
          "type": "sections",
          "range": {
            "direction": "vertical",
            /* columnSelection specifies that each vertical section is a table slice that
               combines the first two columns with one of the
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
                /* each coverages table starts with "Schedule of coverages" */
                "text": "Schedule of coverages",
                "isCaseSensitive": true
              },
            },
            /* exclude "Schedule of coverages" heading from section group range 
           to avoid breaking column recognition */
            "offsetY": 0.3
          },
          "fields": [
            {
              /* In each vertical section, the injury premium for each vehicle is always the 2nd cell to the right
                 of the cell containing "bodily injury liability",
                 as configured by columnSelection */
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
              "id": "_everything_in_this_coverage_section",
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
        /* combine Covered Vehicles and Schedule of Coverages section groups' output into a zipped field */
        {
          "id": "_zipped_vehicle_description_and_coverages",
          "method": {
            "id": "zip",
            "source_ids": [
              "_covered_vehicles",
              "_coverages_per_vehicle"
            ]
          }
        },
        /* for cleaner output, remove the source
       section groups. illustrates configurable field execution order nuances
       optional: add "_zipped_vehicle_description_and_coverages" to this field to further clean up output */
        {
          "id": "clean_up_output",
          "method": {
            "id": "suppressOutput",
            "source_ids": [
              "_coverages_per_vehicle",
              "_covered_vehicles",
            ]
          }
        }
      ]
    },
    /* outputs same data as "parent_section_group_declarations",
      but flattens "_zipped_vehicle_descriptions_and_coverages" into a single array  */
    {
      "id": "flattened_declarations",
      "method": {
        "id": "copy_from_sections",
        "source_sections": "parent_section_group_declarations",
        "source_field": "_zipped_vehicle_description_and_coverages"
      }
    }
  ]
}
```

**Example document**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/copy_from_sections.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/copy_from_sections.pdf) |
| ---------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "parent_section_group_declarations": [
    {
      "_zipped_vehicle_description_and_coverages": [
        {
          "vehicle_description": {
            "type": "string",
            "value": "2003 Mits Lancer Es"
          },
          "_everything_in_this_covered_vehicle_section": {
            "type": "string",
            "value": "Vehicle VIN\u0000 12345678901234 Vehicle no. 1 Description: 2003 Mits Lancer Es"
          },
          "bodily_liability_premium": {
            "source": "89.70",
            "value": 89.7,
            "type": "number"
          },
          "_everything_in_this_coverage_section": {
            "type": "string",
            "value": "Coverages Limits of Liability Vehicle 1 Bodily injury liability $300,000 per 89.70 person Property damage $200,000 per 61.69 liability person"
          }
        },
        {
          "vehicle_description": {
            "type": "string",
            "value": "2019 Nissan Pathfinder"
          },
          "_everything_in_this_covered_vehicle_section": {
            "type": "string",
            "value": "Vehicle VIN\u0000 01234567890123 Vehicle no. 2 Description:2019 Nissan Pathfinder"
          },
          "bodily_liability_premium": {
            "source": "138.66",
            "value": 138.66,
            "type": "number"
          },
          "_everything_in_this_coverage_section": {
            "type": "string",
            "value": "Coverages Limits of Liability Vehicle 2 Bodily injury liability $300,000 per 138.66 person Property damage $200,000 per 79.45 liability person"
          }
        }
      ]
    },
    {
      "_zipped_vehicle_description_and_coverages": [
        {
          "vehicle_description": {
            "type": "string",
            "value": "2010 Toyota Corolla"
          },
          "_everything_in_this_covered_vehicle_section": {
            "type": "string",
            "value": "Vehicle VIN\u0000 5555555555555 Vehicle no. 3 Description: 2010 Toyota Corolla"
          },
          "bodily_liability_premium": {
            "source": "100.10",
            "value": 100.1,
            "type": "number"
          },
          "_everything_in_this_coverage_section": {
            "type": "string",
            "value": "Coverages Limits of Liability Vehicle 3 Bodily injury liability $300,000 per 100.10 person Property damage $200,000 per 55.89 liability person"
          }
        },
        {
          "vehicle_description": {
            "type": "string",
            "value": "2012 Honda Accord"
          },
          "_everything_in_this_covered_vehicle_section": {
            "type": "string",
            "value": "Vehicle VIN\u0000 9999999999999 Vehicle no. 4 Description: 2012 Honda Accord"
          },
          "bodily_liability_premium": {
            "source": "140.80",
            "value": 140.8,
            "type": "number"
          },
          "_everything_in_this_coverage_section": {
            "type": "string",
            "value": "Coverages Limits of Liability Vehicle 4 Bodily injury liability $300,000 per 140.80 person Property damage $200,000 per 89.45 liability person"
          }
        }
      ]
    }
  ],
  "flattened_declarations": [
    {
      "vehicle_description": {
        "type": "string",
        "value": "2003 Mits Lancer Es"
      },
      "_everything_in_this_covered_vehicle_section": {
        "type": "string",
        "value": "Vehicle VIN\u0000 12345678901234 Vehicle no. 1 Description: 2003 Mits Lancer Es"
      },
      "bodily_liability_premium": {
        "source": "89.70",
        "value": 89.7,
        "type": "number"
      },
      "_everything_in_this_coverage_section": {
        "type": "string",
        "value": "Coverages Limits of Liability Vehicle 1 Bodily injury liability $300,000 per 89.70 person Property damage $200,000 per 61.69 liability person"
      }
    },
    {
      "vehicle_description": {
        "type": "string",
        "value": "2019 Nissan Pathfinder"
      },
      "_everything_in_this_covered_vehicle_section": {
        "type": "string",
        "value": "Vehicle VIN\u0000 01234567890123 Vehicle no. 2 Description:2019 Nissan Pathfinder"
      },
      "bodily_liability_premium": {
        "source": "138.66",
        "value": 138.66,
        "type": "number"
      },
      "_everything_in_this_coverage_section": {
        "type": "string",
        "value": "Coverages Limits of Liability Vehicle 2 Bodily injury liability $300,000 per 138.66 person Property damage $200,000 per 79.45 liability person"
      }
    },
    {
      "vehicle_description": {
        "type": "string",
        "value": "2010 Toyota Corolla"
      },
      "_everything_in_this_covered_vehicle_section": {
        "type": "string",
        "value": "Vehicle VIN\u0000 5555555555555 Vehicle no. 3 Description: 2010 Toyota Corolla"
      },
      "bodily_liability_premium": {
        "source": "100.10",
        "value": 100.1,
        "type": "number"
      },
      "_everything_in_this_coverage_section": {
        "type": "string",
        "value": "Coverages Limits of Liability Vehicle 3 Bodily injury liability $300,000 per 100.10 person Property damage $200,000 per 55.89 liability person"
      }
    },
    {
      "vehicle_description": {
        "type": "string",
        "value": "2012 Honda Accord"
      },
      "_everything_in_this_covered_vehicle_section": {
        "type": "string",
        "value": "Vehicle VIN\u0000 9999999999999 Vehicle no. 4 Description: 2012 Honda Accord"
      },
      "bodily_liability_premium": {
        "source": "140.80",
        "value": 140.8,
        "type": "number"
      },
      "_everything_in_this_coverage_section": {
        "type": "string",
        "value": "Coverages Limits of Liability Vehicle 4 Bodily injury liability $300,000 per 140.80 person Property damage $200,000 per 89.45 liability person"
      }
    }
  ]
}
```