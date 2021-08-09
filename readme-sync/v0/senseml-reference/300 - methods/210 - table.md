---
title: "Table"
hidden: false
---
Matches tables based on bag-of-words scoring and returns their collated column contents.

**Use**

- Use the Table method for tables in the same document type that have a variable number of columns.  

**Requirements**

- The anchor text must be a line that precedes the table.  Do not chose a line that is a part of the table. For example, do not anchor on a table title that is inside the table borders. 

[**Parameters**](doc:table#section-parameters)
[**Examples**](doc:table#section-examples)


Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key                    | value        | description                                                  |
| :--------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)      | `table`      | When you specify the Table method in a Field query object, you must also specify `"type": "table"` in the field's parameters. |
| columns (**required**) | array        | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output. <br/>  -`terms` (**required**): An array of strings with terms to score positively. Sensible uses NLP techniques (such as tokenization and stemming) to score matches for the strings. Usually, you include column headings in this array. <br/> -`stopTerms`: An array of strings with terms to score negatively. Sensible uses NLP techniques (such as tokenization and stemming) to score matches for the strings. <br/> -`type`: The type of the value in the table cell. For more information about types, see [Field query object](doc:field-query-object). <br/>  -`isRequired` (default false): If true, Sensible does not return rows in which a value is not present in this column. If false, Sensible returns nulls for rows in which a value is not present. Bear in mind that if you set this parameter to true for an empty row in one column, Sensible leaves out that row for all other columns as well, even if that row had content under a different column. |
| stop                   | Match object | (**Recommended**) [Match object](doc:match)  to stop table recognition. This method uses OCR  to recognize a table. With a Stop parameter defined, Sensible OCRs only the pages from the starting anchor to the page with the stop match. Otherwise, Sensible OCRs all pages, which can impact performance. |

Examples
====

The following example shows extracting two columns from a table that updates monthly with a variable number of columns in the Sensible app. Notes:

- In order to filter out all column headings, the config specifies `"type": "number"` and `"isRequired": true` for the column `rank_this_month` .
- To improve performance, the config specifies a Stop parameter. This ensures Sensible only OCRs the relevant page area while looking for a table.

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/table_dynamic_example.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for table | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/table_dynamic_example.pdf) |
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
            "type": "number",
            "isRequired": true
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

If tables always have the same column layout (same column headings, same number of columns), use the [Fixed Table method](doc:fixed-table) instead. 

