---
title: "Fixed Table"
hidden: false
---
Extracts tables with a fixed number of columns and returns their collated column contents. Anchor either on the table title or on a table column heading.



Use the Fixed Table method for tables in the same document type that always have the same column layout (same headings in the same order, same number of columns).  This method can extract tables that span multiple pages and ignores repeated column titles on subsequent pages.

[**Parameters**](doc:fixed-table#parameters)
[**Examples**](doc:fixed-table#examples)
[**Notes**](doc:fixed-table#notes)



Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.


| key                        | value                                                        | description                                                  |
| :------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| id (**required**)          | `fixedTable`                                                 | When you specify this, you must also specify `"type": "table"` in the field's parameters. See the Stop parameter for details about how Sensible recognizes a table. |
| columnCount (**required**) | integer                                                      | The number of columns the tables must have.                  |
| columns (**required**)     | array                                                        | An array of objects with the following parameters: <br/> -`id` (**required**): The ID for the column in the extraction output <br/> - `index` (**required**): The zero-based column index <br/>-`type` : The table cell's type. For more information, see  [Types](doc:types) <br/> -`isRequired` (default: false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |
| stop                       | [Match object](doc:match) or array of Match objects. default: none | (**Recommended**)  Stops table recognition at the matched line. Otherwise, Sensible searches all pages for tables, which can impact performance.<br/>When you specify a stop, Sensible  uses an Amazon Web Service  provider to perform table recognition. When you omit a stop, Sensible uses a Microsoft OCR provider. |
| startOnRow                 | integer. default: 0                                          | Zero-indexed row number at which to start table extraction. For example, use this to exclude column headings from the output. As a stricter alternative, set the Is Required parameter on a column and set a type on the column (see example in Examples section). |

Examples
=====

The following example shows extracting two columns from a fixed table in the Sensible app.

- In order to omit column headings, the config specifies `"type": "number"` and `"isRequired": true` for the column `col4_rank_last_month` . You can also use `"startOnRow":1` to omit headings.
- To improve performance, the config specifies a Stop parameter. 

**Config**

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

**Example document**
The following image shows the example PDF used with this example config:


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/fixed_table.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/fixed_table.pdf) |
| --------------------------- | ------------------------------------------------------------ |


**Output**

```json
{
  "agile_risks_table": {
    "columns": [
      {
        "id": "col1_risk_description",
        "values": [
          {
            "value": "Poor task point estimation",
            "type": "string"
          },
          {
            "value": "Poor epic scope definition",
            "type": "string"
          },
          {
            "value": "Inadequate scrum master training",
            "type": "string"
          }
        ]
      },
      {
        "id": "col4_rank_last_month",
        "values": [
          {
            "source": "2",
            "value": 2,
            "type": "number"
          },
          {
            "source": "1",
            "value": 1,
            "type": "number"
          },
          {
            "source": "3",
            "value": 3,
            "type": "number"
          }
        ]
      }
    ]
  }
}
```


Notes
====
If  tables have variable column layout, use the [Table method](doc:table) instead. 

To extract complex tables, for example tables inside tables or tables with labeled rows and columns, see [Sections](doc:sections#examples).
