---
title: "Fixed Table"
hidden: false
---
Matches tables with a fixed number of columns and returns their collated column contents. Choose anchor text that precedes the table but is not inside the table, for example, a table title. 

Parameters
=====


| key                        | value                       | description                                                  |
| :------------------------- | :-------------------------- | :----------------------------------------------------------- |
| id (**required**)          | `fixedTable`                | When you specify the Fixed Table method in a Field query object, you must also specify `"type": "table"` in the field's parameters. |
| columnCount (**required**) | integer                     | The number of columns the tables must have.                  |
| columns (**required**)     | array                       | An array of objects with the following parameters: <br/> `id` (**required**): The id for the column in the extraction output <br/> `type` (**required**: See a list of possible types in [Field query object](doc:field-query-object)) <br/> `index` (**required**: A zero based column index <br/> `isRequired` (default: false): If true, the extraction does not return rows where a value is not present in this column. |
| stop                       | Match object. default: none | A [Match object](doc:anchor-object#section-match-object)  to stop extraction. With `stop` defined, the engine selectively OCRs the pages from the starting anchor to the page with the stop match. Otherwise the engine OCRs all pages. |

Examples
=====

The following image shows extracting 2 columns from a fixed table in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/review/readme-sync/assets/v0/images/fixedtable_example.png)

You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for box recognition | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/review/readme-sync/assets/v0/pdfs/example_table.pdf) |
| ------------------------------- | ------------------------------------------------------------ |

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
Use this method instead of the Table method or Text Table method when you are certain that the table always has the same number of columns in all the PDFs of the specified document type. 