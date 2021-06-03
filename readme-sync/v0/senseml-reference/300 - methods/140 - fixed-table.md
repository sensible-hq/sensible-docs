---
title: "Fixed Table"
hidden: false
---
Matches tables with a fixed number of columns and returns their collated column contents. Choose anchor text that precedes the table but is not inside the table, for example, a table title. 

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                        | value                       | description                                                  |
| :------------------------- | :-------------------------- | :----------------------------------------------------------- |
| id (**required**)          | `fixedTable`                | When you specify the Fixed Table method in a Field query object, you must also specify `"type": "table"` in the field's parameters. |
| columnCount (**required**) | integer                     | The number of columns the tables must have.                  |
| columns (**required**)     | array                       | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output <br/> - `index` (**required**): A zero-based column index <br/>-`type` : The type of the value in the table cell. See a list of possible types in [Field query object](doc:field-query-object)) <br/> -`isRequired` (default: false): If true, SenseML does not return rows in which a value is not present in this column. If false, SenseML returns nulls for rows in which a value is not present. |
| stop                       | Match object. default: none | **Recommended** [Match object](doc:anchor-object#section-match-object)  to stop table recognition. OCR is a prerequisite for table recognition. With a Stop parameter defined, the engine selectively OCRs the pages from the starting anchor to the page with the stop match. Otherwise, the engine OCRs all pages, which can impact performance. |

Examples
=====

The following image shows extracting 2 columns from a fixed table in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/review/readme-sync/assets/v0/images/fixedtable_example.png)

You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for fixed table | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/review/readme-sync/assets/v0/pdfs/example_fixed_table.pdf) |
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
Use this method instead of the Table method or Text Table method when you are certain that the table always has the same number of columns in all the PDFs of the specified document type. 