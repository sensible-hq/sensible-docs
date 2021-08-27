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
| id (**required**)          | `fixedTable`                | When you specify the Fixed Table method, you must also specify `"type": "table"` in the field's parameters. |
| columnCount (**required**) | integer                     | The number of columns the tables must have.                  |
| columns (**required**)     | array                       | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output <br/> - `index` (**required**): A zero-based column index <br/>-`type` : The type of the value in the table cell. For more information, see  [types](doc:types) <br/> -`isRequired` (default: false): If true, Sensible omits a row if its cell is empty in this column. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |
| stop                       | Match object. default: none | (**Recommended**)  [Match object](doc:match)  to stop table recognition. Otherwise, Sensible searches all pages for tables, which can impact performance. |

Examples
=====

The following image shows extracting two columns from a fixed table in the Sensible app.

- In order to filter out all column headings, the config specifies `"type": "number"` and `"isRequired": true` for the column `col4_rank_last_month` 
- To improve performance, the config specifies a Stop parameter. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/fixedtable_example.png)

Try out this example in the Sensible app using the following PDF and config:

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/fixed_table_example.pdf) |
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

