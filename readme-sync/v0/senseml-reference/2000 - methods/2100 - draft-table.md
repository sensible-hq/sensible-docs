---
title: "Table"
hidden: true
---
Matches tables based on bag-of-words scoring and returns their collated column contents.

**Use**

- Use the Table method for tables in the same document type that have a variable column formatting.

**Requirements**

- The anchor text must be a line that precedes the table. Do not choose a line that's a part of the table. For example, don't anchor on a table title that's inside the table borders. 

[**Parameters**](doc:table#parameters)
[**Examples**](doc:table#examples)


Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                    | value                     | description                                                  |
| :--------------------- | :------------------------ | :----------------------------------------------------------- |
| id (**required**)      | `table`                   | When you specify this method, you must also specify `"type": "table"` in the field's parameters. |
| columns (**required**) | array                     | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output. <br/>  -`terms` (**required**): An array of terms to score positively during column recognition. Usually, you include column heading terms in this array. For more information about the NLP approach, see [bag of words](doc:bag-of-words). <br/> -`stopTerms`: An array of terms to score negatively during column recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |
| stop                   | [Match object](doc:match) | (**Recommended**)  [Match object](doc:match)  to stop table recognition. Otherwise, Sensible searches all pages for tables, which can impact performance. |
| startOnRow             | integer. default: 0       | Zero-indexed row number at which to start table extraction. For example, use this to exclude column headings from the output. |



