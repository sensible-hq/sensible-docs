---
title: "Table"
hidden: false
---
Matches tables based on bag-of-words scoring and returns their collated column contents.

| key     | value                                            | description                                                  |
| :------ | :----------------------------------------------- | :----------------------------------------------------------- |
| id      | `table`                                          | When you specify the Table method in a Field query object, you must also specify `"type": "table"` in the field's parameters. |
| columns | array                                            | An array of objects with the following shape: *`id`: The id for the column in the extraction output *`terms`: An array of strings with terms to score positively. *`stopTerms`: optional. An array of strings with terms to score negatively. *`isRequired`: optional, default false. If true, the extraction will not return rows where a value is not present in this column |
| stop    | [Matcher](https://docs.sensible.so/docs/matcher) | optional, default: none. A [Matcher](https://docs.sensible.so/docs/matcher) to stop extraction. With `stop` defined, the engine will selectively OCR the pages from the starting anchor to the page with the stop match. Otherwise the engine will OCR all pages |