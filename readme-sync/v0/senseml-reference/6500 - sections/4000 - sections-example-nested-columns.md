---
title: "Advanced: nested columns example"
hidden: false

---

This example shows using nested sections to extract repeating vertical section groups.

Overview
-----

To give a brief overview of using vertical sections for columns, the following image shows extracting numbered headings and their columns with these steps:

1. define a section group
2. define a nested vertical section  group

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_col_sect.png)

The following config uses abbreviated YML notation to give an overview of the more complex SenseML JSON: 

```yml
fields: []
sections:
- id: parentSections
  range:
    anchor:
      match:
        type: startsWith
        text: heading
  fields:
  - id: sectionTitle
    method:
      id: passthrough
    anchor:
      match:
        type: startsWith
        text: heading
  sections:
  - id: nestedColumns
    range:
      direction: vertical
      anchor:
        match:
          type: startsWith
          text: column
    fields:
    - id: columnTitle
      method:
        id: passthrough
      anchor:
        match:
          type: startsWith
          text: column

```

With this approach, you can output something like the following, using abbreviated YML notation to give an overview of the more complex JSON extraction response:

```yml
---
parentSections:
- sectionTitle:
    type: string
    value: Heading 1
  nestedColumns:
  - columnTitle:
      type: string
      value: Column A
  - columnTitle:
      type: string
      value: Column B
  - columnTitle:
      type: string
      value: Column C
- sectionTitle:
    type: string
    value: Heading 2
  nestedColumns:
  - columnTitle:
      type: string
      value: Column D
  - columnTitle:
      type: string
      value: Column E
  - columnTitle:
      type: string
      value: Column F

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
            "text": "heading"
          }
        }
      },
      "fields": [
        {
          "id": "sectionTitle",
          "method": {
            "id": "passthrough"
          },
          "anchor": {
            "match": {
              "type": "startsWith",
              "text": "heading"
            }
          }
        }
      ],
      "sections": [
        {
          "id": "nestedColumns",
          "range": {
            "direction": "vertical",
            "anchor": {
              "match": {
                "type": "startsWith",
                "text": "column"
              }
            }
          },
          "fields": [
            {
              "id": "columnTitle",
              "method": {
                "id": "passthrough"
              },
              "anchor": {
                "match": {
                  "type": "startsWith",
                  "text": "column"
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

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_col_sect_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_sections_col_section.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "parentSections": [
    {
      "sectionTitle": {
        "type": "string",
        "value": "Heading 1"
      },
      "nestedColumns": [
        {
          "columnTitle": {
            "type": "string",
            "value": "Column A"
          }
        },
        {
          "columnTitle": {
            "type": "string",
            "value": "Column B"
          }
        },
        {
          "columnTitle": {
            "type": "string",
            "value": "Column C"
          }
        }
      ]
    },
    {
      "sectionTitle": {
        "type": "string",
        "value": "Heading 2"
      },
      "nestedColumns": [
        {
          "columnTitle": {
            "type": "string",
            "value": "Column D"
          }
        },
        {
          "columnTitle": {
            "type": "string",
            "value": "Column E"
          }
        },
        {
          "columnTitle": {
            "type": "string",
            "value": "Column F"
          }
        }
      ]
    }
  ]
}
```

