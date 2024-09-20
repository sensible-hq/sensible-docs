---
title: "Zip"
hidden: false
---
Zips one of the following:

- Zips the output of array source fields into an array of objects. Each source field must output an array, for example, as a result of configuring `"match": "all"` or `"type": "name"` for the field. 
- Zips the output of a single [table method](doc:table-methods) into row objects. Or, use this to zip multiple tables together.
- Zips the output of [sections](doc:sections) into an array of objects.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                        | value                                    | description                                                  |
| :------------------------- | :--------------------------------------- | :----------------------------------------------------------- |
| id (**required**)          | `zip`                                    |                                                              |
| source_ids  (**required**) | array of field IDs in the current config | One of the following: <br/><br/>- the IDs of the source fields to zip. Each source field must output an array.<br/><br/>- a single ID for a field that returns a table. Sensible returns an array of zipped row objects.<br/><br/>- the IDs of the section groups to zip together. Sensible returns a zipped section group containing all the fields from the source section groups. If there are identically named field IDs in the source section groups, Sensible falls back to outputting the IDs in the last section group listed in the `source_id` array.<br/><br/><br/>Zips operate with the following precedence for source IDs: <br/>- If at least one source field is a section group, Sensible outputs the section group and ignores all other types of sources.<br/><br/> - If at least one source is a table and there are no section group sources, Sensible outputs the first table ID and ignores all other sources.  <br/><br/>-  If the output of the source IDs are arrays, the Zip method joins them up to their maximum shared length. For example, if you zip arrays that have 4, 5, and 6 elements respectively, the zipped array has 4 elements. Examples of source IDs that output arrays include fields with `"match": "all"` configured, and section groups. To ensure the longest source array isn't shortened when using `"match": "all"`, instead use  `"match":"allWithNull"` for all source fields. For an example, see the Examples section. <br/> |

Examples
====

Sections zip
---

For an example of zipping sections together, see [Zip sections example](doc:sections-example-zip).

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

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zip.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/zip.pdf) |
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
    ],
    "title": {
      "type": "string",
      "value": "Insured vehicles"
    },
    "footer": {
      "type": "string",
      "value": "Please see your policy documents for details."
    }
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

All With Null zip
---

The following example shows using `"match":"allWithNull"` as an alternative to [sections](doc:sections) to return parallel arrays of phones and last names. If you used `"match":"all"` instead of `allWithNull`, the missing phone number for claimant Badawi would result in that claimant's omission from the zipped `name_and_phone` array.

**Config**

```json
{
  "preprocessors": [
    {
      "type": "splitLines",
      "minSpaces": 3
    }
  ],
  "fields": [
    {
      /* using `allWithNull` outputs a 5-element array
         with one null element (phone for Badawi).
         Using `all`  would output a 4-element array  */
      "id": "phone_number",
      "match": "allWithNull",
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "phone number"
        }
      },
      "method": {
        "id": "row"
      }
    },
    {
      /* using either `all` or
         `allWithNull` outputs a 5-element array, 
         because no last 
         names are missing in doc */
      "id": "last_name",
      "match": "allWithNull",
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "claimant last name"
        }
      },
      "method": {
        "id": "label",
        "position": "right"
      }
    }
  ],
  "computed_fields": [
    {
      /* if you used `all` instead of `allWithNull`,
         `name_and_phone` zipped output
         would omit claimant Bawadi, because Zip 
         method joins arrays up to 
         their maximum shared length. */
      "id": "name_and_phone",
      "method": {
        "id": "zip",
        "source_ids": [
          "phone_number",
          "last_name"
        ]
      }
    },
    {
      "id": "hide_unzipped_fields",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "phone_number",
          "last_name"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/all_with_null.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/all_with_null.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "name_and_phone": [
    {
      "phone_number": {
        "type": "string",
        "value": "512 409 8765"
      },
      "last_name": {
        "type": "string",
        "value": ": Diaz"
      }
    },
    {
      "phone_number": null,
      "last_name": {
        "type": "string",
        "value": ": Badawi"
      }
    },
    {
      "phone_number": {
        "type": "string",
        "value": "505 238 8765"
      },
      "last_name": {
        "type": "string",
        "value": ": Levy"
      }
    },
    {
      "phone_number": {
        "type": "string",
        "value": "860 231 8344"
      },
      "last_name": {
        "type": "string",
        "value": ": Zenfell"
      }
    },
    {
      "phone_number": {
        "type": "string",
        "value": "312 242 9856"
      },
      "last_name": {
        "type": "string",
        "value": ": Smith"
      }
    }
  ]
}
```