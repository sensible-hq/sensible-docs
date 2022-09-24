---
title: "Copy FROM section"
hidden: true
---
https://dev.sensible.so/editor/?d=frances_test_playground&c=copy_from_section_final&g=copy_from_sections_final&v=

```
{
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
       section groups. illustrates configurable field execution order nuances */
  ]
}
```







Copies a field into each section in a section group, or from a parent section into each section in a nested section group. This is useful for cleaning up the output of complex nested sections.

TODO: examples of nested structure use cases?

For example you'll need a nested structure:

- to capture repeating verical sections
-  to capture groups that belong togethter, nest them inside a parent horizontal section then zip them together. 

These approaches can yield a complex output. For example: 

1. parent section that captures the entire vehicle declaration (2 tables )

2. child horizontal section that captures vehicle info like VIN

3. child vertical section that captures vehicle info like coverages:

   

![image-20220924101429584](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220924101429584.png)



If you zip the child sections together, the output for this type of nested sections will be:

```json
TODO VALIDATE
{
    // 1 in image above
	"parent_section": {
        // config uses zip computed method to zip 1 and 2 in image above
        // for an example config taht does this see /sections-example-zip
		"zipped_child_sections": {
			{
				"vin": "123",
				"bodily_injury_liability": "89.70"

			},
			{
				"vin": "0123",
				"bodily_injury_liability": "138.66"

			}
		},
{
			{
				"vin": "555",
				"bodily_injury_liability": "100.10"

			},
			{
				"vin": "9999",
				"bodily_injury_liability": "140.80"

			}
		}
	}
}
```

This isn't the greatest structured of output, because the parent gropu section (1) breaks the declarations up into two objects. use the copy_to_section to flatten the output like:

```json
"copied_from_zipped_child_sections": {
    			{
				"vin": "123",
				"bodily_injury_liability": "89.70"

			},
			{
				"vin": "0123",
				"bodily_injury_liability": "138.66"
                
                
                
                
```

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                 | description                                                  |
| :----------------------- | :------------------------------------ | :----------------------------------------------------------- |
| id (**required**)        | `copy_to_section`                     |                                                              |
| source_id (**required**) | source field ID in the current config | The source ID to copy must be in a field array or section that is one level up in the hierarchy relative to the destination section. For example, in a section, copy from the base fields array. In a subsection, copy from the parent section's field array. |

Examples
====

The following example shows using the Copy To Field method to add a policy number, which is listed once in the document and which is globally applicable, to every extracted claim. 

**Config**

```json
{
  "fields": [
    {
      /* capture raw policy # to copy into 
      each claim using copy_to_section */
      "id": "_raw_policy_number",
      "type": "number",
      "anchor": "policy number",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      /* get monthly claims totals 
      with match all (simpler alternative to sections) */
      "id": "monthly_total_unprocessed_claims",
      "match": "all",
      "anchor": {
        "match": {
          "type": "includes",
          "text": "unprocessed claims:",
          "isCaseSensitive": true
        },
        "end": {
          "text": "total claims",
          "type": "startsWith"
        }
      },
      "method": {
        "id": "row",
        "position": "right",
        "includeAnchor": true
      }
    }
  ],
  /* get first 2 claims sections in doc.  
     each claim starts with "claim number" and ends with 
     "unprocessed claims" */
  "sections": [
    {
      "id": "unprocessed_sept_oct_claims_sections",
      "range": {
        "anchor": {
          "start": {
            "text": "September",
            "type": "startsWith",
            "isCaseSensitive": true
          },
          "match": {
            "type": "includes",
            "text": "claim number"
          },
          "end": {
            "type": "startsWith",
            "text": "November",
            "isCaseSensitive": true
          }
        },
        "stop": {
          "type": "includes",
          "text": "unprocessed claims:",
          "isCaseSensitive": true
        }
      },
      /* return each claim as object containing claim # 
      and phone # fields */
      "fields": [
        {
          "id": "claim_number",
          "type": "number",
          "anchor": {
            "match": {
              "type": "startsWith",
              "text": "Claim number:",
              "isCaseSensitive": true
            }
          },
          "method": {
            "id": "label",
            "position": "right"
          }
        },
        {
          "id": "phone_number",
          "type": "phoneNumber",
          "anchor": {
            "match": {
              "type": "includes",
              "text": "Phone number",
              "isCaseSensitive": true
            }
          },
          "method": {
            "id": "row",
            "position": "right"
          }
        }
      ],
      /* copy policy number from outside sections
         into each claim */
      "computed_fields": [
        {
          "id": "policy_number",
          "method": {
            "id": "copy_to_section",
            "source_id": "_raw_policy_number"
          }
        }
      ]
    }
  ]
}
```

**Example document**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/copy_to_section.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections.pdf) |
| ---------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "_raw_policy_number": {
    "source": "5501234567",
    "value": 5501234567,
    "type": "number"
  },
  "monthly_total_unprocessed_claims": [
    {
      "type": "string",
      "value": "Sept unprocessed claims: 2"
    },
    {
      "type": "string",
      "value": "Oct unprocessed claims: 1"
    },
    {
      "type": "string",
      "value": "Nov unprocessed claims: 2"
    }
  ],
  "unprocessed_sept_oct_claims_sections": [
    {
      "claim_number": {
        "source": "1223456789",
        "value": 1223456789,
        "type": "number"
      },
      "phone_number": {
        "type": "phoneNumber",
        "source": "512 409 8765",
        "value": "+15124098765"
      },
      "policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      }
    },
    {
      "claim_number": {
        "source": "9876543211",
        "value": 9876543211,
        "type": "number"
      },
      "phone_number": null,
      "policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      }
    },
    {
      "claim_number": {
        "source": "6785439210",
        "value": 6785439210,
        "type": "number"
      },
      "phone_number": {
        "type": "phoneNumber",
        "source": "505 238 8765",
        "value": "+15052388765"
      },
      "policy_number": {
        "source": "5501234567",
        "value": 5501234567,
        "type": "number"
      }
    }
  ]
}
```
