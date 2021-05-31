---
title: "Table"
hidden: false
---
Matches tables based on bag-of-words scoring and returns their collated column contents.

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key                    | value        | description                                                  |
| :--------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)      | `table`      | When you specify the Table method in a Field query object, you must also specify `"type": "table"` in the field's parameters. |
| columns (**required**) | array        | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output <br/> -`terms` (**required**): An array of strings with terms to score positively. Usually, you include column headings in this array. <br/> -`stopTerms`: An array of strings with terms to score negatively. <br/> -`type`: The type of the value in the table cell. For more information about types, see [Field query object](doc:field-query-object). <br/>  -`isRequired` (default false): If true, the extraction does not return rows where a value is not present in this column |
| stop                   | Match object | **Recommended** [Match object](doc:anchor-object#section-match-object)  to stop table recognition. OCR is a prerequisite for table recognition. With `stop` defined, the engine selectively OCRs the pages from the starting anchor to the page with the stop match. Otherwise, the engine OCRs all pages, which can impact performance. |

Examples
====

The following example shows extracting two columns from a table that updates monthly with a variable number of columns in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/review/readme-sync/assets/v0/images/table_dynamic_example.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for table | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/example_table_dynamic.pdf) |
| --------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "agile_risks_table_updates_monthly",
      "anchor": "agile software",
      "type": "table",
      "method": {
        "id": "table",
        "columns": [
          {
            "id": "col1_risk_description",
            "terms": [
              "risk",
              "description"
            ],
          },
          {
            "id": "rank_this_month",
            "terms": [
              "this month"
            ],
            "type": "number"
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

The Table method is slower than the Fixed Table method, but is less sensitive to changes in table formatting. Use the Table method when dealing with tables in the same document type that have a variable number of columns. 