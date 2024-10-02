---
title: "Text table"
hidden: true
---


| key                  | value   | description                                                  |
| :------------------- | :------ | :----------------------------------------------------------- |
| id **required**      | `table` | When you specify this method, you must also specify `"type": "table"` in the field's parameters. |
| columns **required** | array   | An array of objects with the following parameters:<br/> -`id` (**required**): The id for the column in the extraction output. <br/>**To specify fallbacks, use the same ID for multiple columns. Succeeding columns act as fallbacks if the first returns null.** <br/> |
|                      |         |                                                              |
|                      |         |                                                              |
|                      |         |                                                              |
|                      |         |                                                              |
|                      |         |                                                              |

You can output the issuing financial institution and the displayed account number as separate columns, with a configuration like the following configuration.

Notes
====

- To extract complex tables, for example tables inside tables or tables with labeled rows and columns, see [Sections](doc:sections#examples).





  

  

  

  







