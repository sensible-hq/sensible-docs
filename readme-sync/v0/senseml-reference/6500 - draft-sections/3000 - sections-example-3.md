---
title: "Sections example 3"
hidden: true

---

Vertical sections: sections and columns
===

Overview
-----

To give a brief overview of using vertical sections for columns, the following image shows capturing numbered sections and their columns with these steps:

1. define a section group
2. define a nested vertical section  group

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_col_sect.png)

The following config uses abbreviated YML notation to give an overview of the more complex SenseML JSON: 

```yml
sections:
  - id: parentSections
    range:
      anchor: Section
    fields:
      - id: sectionTitle
        anchor: Section
        method:
          id: passthrough
   sections:
     - id: nestedColumns
       range:
         direction: vertical
         anchor: column
       fields:
         - id: columnTitle
           anchor: column
           method:
             id: passthrough    
      
```

With this approach, you can output something like the following, using abbreviated YML notation to give an overview of the more complex JSON API response:

```yml
parentSections:
  - sectionTitle: Section 1
    nestedColumns:
      columnTitle: Column A
      columnTitle: Column B
      columnTitle: Column C
 - sectionTitle: Section 2
    nestedColumns:
      columnTitle: Column A
      columnTitle: Column B
      columnTitle: Column C  
   
```

Details
----
The following elaborates on the preceding overview using JSON instead of YML.

**Config**

```json
{
  "fields": [],
  "sections": [
    {
      "id": "parentSections",
      "range": {
        "anchor": {
          "match": {
            "type": "startsWith",
            "text": "Section"
          }
        }
      },
      "fields": [
        {
          "id": "sectionNumber",
          "type": "number",
          "method": {
            "id": "label",
            "position": "right"
          },
          "anchor": {
            "match": {
              "type": "startsWith",
              "text": "Section"
            }
          }
        }
      ],
      "sections": [
        {
          "id": "nestedColumns",
          "range": {
            "direction": "vertical",
            "offsetY": 0,
            "anchor": {
              "match": {
                "type": "startsWith",
                "text": "Column"
              }
            }
          },
          "fields": [
            {
              "id": "columnLetter",
              "method": {
                "id": "label",
                "position": "right"
              },
              "anchor": {
                "match": {
                  "type": "startsWith",
                  "text": "Column"
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

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_col_sect_1.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_sections_col_section.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "parentSections": [
    {
      "sectionNumber": {
        "source": "1",
        "value": 1,
        "type": "number"
      },
      "nestedColumns": [
        {
          "columnLetter": {
            "type": "string",
            "value": "A"
          }
        },
        {
          "columnLetter": {
            "type": "string",
            "value": "B"
          }
        },
        {
          "columnLetter": {
            "type": "string",
            "value": "C"
          }
        }
      ]
    },
    {
      "sectionNumber": {
        "source": "2",
        "value": 2,
        "type": "number"
      },
      "nestedColumns": [
        {
          "columnLetter": {
            "type": "string",
            "value": "A"
          }
        },
        {
          "columnLetter": {
            "type": "string",
            "value": "B"
          }
        },
        {
          "columnLetter": {
            "type": "string",
            "value": "C"
          }
        }
      ]
    },
    {
      "sectionNumber": {
        "source": "3",
        "value": 3,
        "type": "number"
      },
      "nestedColumns": [
        {
          "columnLetter": {
            "type": "string",
            "value": "A"
          }
        },
        {
          "columnLetter": {
            "type": "string",
            "value": "B"
          }
        },
        {
          "columnLetter": {
            "type": "string",
            "value": "C"
          }
        }
      ]
    }
  ]
}
```

