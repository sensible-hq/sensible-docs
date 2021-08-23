---
title: "Fixed Table"
hidden: false
---
Matches tables with a fixed number of columns and returns their collated column contents. 

**Use**

- Use the Fixed Table method for tables in the same document type that always have the same column layout (same headings, same number of columns).  

**Requirements**

- The anchor text must be a line that precedes the table.  Do not chose a line that is a part of the table. For example, do not anchor on a table title that is inside the table borders. 

[**Parameters**](doc:fixed-table#section-parameters)
[**Examples**](doc:fixed-table#section-examples)
[**Notes**](doc:fixed-table#section-notes)



Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                        | value                       | description                                                  |
| :------------------------- | :-------------------------- | :----------------------------------------------------------- |
| id (**required**)          | `fixedTable`                | When you specify the Fixed Table method in a Field query object, you must also specify `"type": "table"` in the field's parameters. |
| columnCount (**required**) | integer                     | The number of columns the tables must have.                  |
| columns (**required**)     | array                       | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output <br/> - `index` (**required**): A zero-based column index <br/>-`type` : The type of the value in the table cell. See a list of possible types in [Field query object](doc:field-query-object) <br/> -`isRequired` (default: false): If true, Sensible does not return rows in which a value is not present in this column. If false, Sensible returns nulls for rows in which a value is not present. Bear in mind that if you set this parameter to true for an empty row in one column, Sensible leaves out that row for all other columns as well, even if that row had content under a different column. |
| stop                       | Match object. default: none | (**Recommended**)  [Match object](doc:match)  to stop table recognition. This method uses OCR  to recognize a table. With a Stop parameter defined, Sensible OCRs only the pages from the starting anchor to the page with the stop match. Otherwise, Sensible OCRs all pages, which can impact performance. |

Examples
=====

The following image shows extracting two columns from a fixed table in the Sensible app. Notes:

- In order to filter out all column headings, the config specifies `"type": "number"` and `"isRequired": true` for the column `col4_rank_last_month` 
- To improve performance, the config specifies a Stop parameter. This ensures Sensible only OCRs the relevant page area while looking for a table. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/fixedtable_example.png)

You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for fixed table | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/fixed_table_example.pdf) |
| --------------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "agile_risks_table",
      "anchor": "agile software",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 4,
        "columns": [
          {
            "id": "col1_risk_description",
            "type": "string",
            "index": 0
          },
          {
            "id": "col4_rank_last_month",
            "type": "number",
            "isRequired": true,
            "index": 3
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "project managers"
        }
      }
    }
  ]
}
```





Notes
====
If  tables have variable column layout, use the [Table method](doc:table) instead. 

