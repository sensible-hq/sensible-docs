---
title: "Zip"
hidden: true
---
Zips the following:

- zips the output of fields together into an array of objects
- zips the output of a single Table method into row objects
- zips the parallel array output of sections together into an array of objects. For example, use this to zip multiple tables together. 

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                        | value                                    | description                                                  |
| :------------------------- | :--------------------------------------- | :----------------------------------------------------------- |
| id (**required**)          | `zip`                                    |                                                              |
| source_ids  (**required**) | array of field IDs in the current config | Depending on the intended zip: <br/><br/>- the IDs of the fields to zip together. If you mix array source IDs with one or more table source IDs, the Zip method zips the first table and ignores everything else (tables take precedence over arrays for zipping).<br/><br/>- a single ID for a field that returns a table.<br/><br/>- the IDs of the sections to zip together. If you mix section source IDS with non-section IDs, the Zip method ignores the non-section IDs and outputs the sections.<br/><br/> If the output of the source IDs are arrays (for example, if you specify `"match: all"`, or if the source IDs are sections), the Zip method joins them up to their maximum shared length. For example, if you zip arrays that have 4, 5, and 6 elements respectively, the zipped array has 4 elements. |

Examples
====

Sections zip
---

For an example of zipping sections together, see TODO 



Table zip
----


The following example shows using the Zip method to extract each row from a table of vehicles as a vehicle object.

Notes:

- In order to filter out all column headings, the config specifies `"type": "number"` and `"isRequired": true` for the column `col3_year_made` .

- To improve performance, the config specifies a Stop parameter. This ensures Sensible restricts table recognition to the relevant page area.

**Config**

```json
{
  "fields": [
    {
      "id": "_insured_vehicles_table",
      "anchor": "insured vehicles",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 4,
        "columns": [
          {
            "id": "col2_model",
            "index": 1
          },
          {
            "id": "col3_year_made",
            "index": 2,
            "type": "number",
            "isRequired": true
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "please"
        }
      }
    }
  ],
  "computed_fields": [
    {
      "id": "computed_insured_vehicles",
      "method": {
        "id": "zip",
        "source_ids": [
          "_insured_vehicles_table"
        ]
      }
    }
  ]
}
```



**Example document**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zip.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/zip.pdf) |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "_insured_vehicles_table": {
    "columns": [
      {
        "id": "col2_model",
        "values": [
          {
            "value": "Camry",
            "type": "string"
          },
          {
            "value": "CR-V",
            "type": "string"
          },
          {
            "value": "Golf",
            "type": "string"
          }
        ]
      },
      {
        "id": "col3_year_made",
        "values": [
          {
            "source": "2010",
            "value": 2010,
            "type": "number"
          },
          {
            "source": "2015",
            "value": 2015,
            "type": "number"
          },
          {
            "source": "2020",
            "value": 2020,
            "type": "number"
          }
        ]
      }
    ]
  },
  "computed_insured_vehicles": [
    {
      "col2_model": {
        "value": "Camry",
        "type": "string"
      },
      "col3_year_made": {
        "source": "2010",
        "value": 2010,
        "type": "number"
      }
    },
    {
      "col2_model": {
        "value": "CR-V",
        "type": "string"
      },
      "col3_year_made": {
        "source": "2015",
        "value": 2015,
        "type": "number"
      }
    },
    {
      "col2_model": {
        "value": "Golf",
        "type": "string"
      },
      "col3_year_made": {
        "source": "2020",
        "value": 2020,
        "type": "number"
      }
    }
  ]
}
```

