---
title: "List"
hidden: true
---
Extracts a table based on your natural-language description of the data you want to extract.

Use this method as a low-code alternative to layout-based Table methods, such as [Text Table](doc:text-table).

**Advantages**

- 

**Limitations**

- 

**Alternatives**

-   [NLP table] 
-   ?? question?
-  [Sections](doc:sections#examples).

**How it works**

For more information about how this method works, see [Notes ](doc:nlp-table#notes).

[**Parameters**](doc:nlp-table#parameters)  TODO THESE LINKS
[**Examples**](doc:nlp-table#examples)
[**Notes**](doc:nlp-table#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                 | value  | description                                                  |
| :------------------ | :----- | :----------------------------------------------------------- |
| id (**required**)   | `list` | TODO true?? The Anchor parameter is optional for fields that use this method. If you don't specify an anchor, Sensible searches the whole document for the table.<br/>If you specify an anchor, Sensible ignores any tables before the anchor and starts searching for candidate tables after the anchor. In detail, Sensible ignores a table if 1. it occurs on a page previous to the page containing the anchor, or 2. if on the same page, it ignores the table if the table's lower boundary is higher on the page than the lower boundary of the anchor line. |
| description         | string | A description of the list's subject matter as a whole.       |
| TODO (**required**) | array  | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the column in the extraction output. <br/>  -`description` (**required**):  A natural-language description of the data you want to extract from the column. The description can include instructions to reformat or filter the column's data. For example, provide descriptions like `" transaction amount. return the absolute value"` or `"vehicle make (not model)"`.  <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |


Examples
====

The following example shows using the NLP Table method to extract information from tables about insured vehicles and insurance transactions.

**Config**

```json

```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/TODO.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TODO.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json

```



Notes
===


4. For an overview of how the List method works, see the following steps:

   
   1. To optimize performance, Sensible makes a list of the pages that are most likely to contain your target table. To make the list:
      - Sensible concatenates all your column descriptions with your overall table description. 
      - Sensible splits the document into equal-sized, overlapping chunks. 
      - Sensible scores your concatenated table descriptions against each chunk using the OpenAI Embeddings API.
      - Sensible gets a list of page numbers from the top-scoring chunks.
   2. Sensible extracts all the tables on each page in the list of pages most likely to contain your table, using a Microsoft OCR provider. 
   
   3. For each extracted table, Sensible extracts the table title, if present.  In detail:
   
      -  Sensible extracts lines contained in a rectangular region immediately above each table, since that region is likely to contain the table title. 
      -  The height of that region equals the line height of the first non-empty cell of the table + 0.1 inches, and the region extends down to the top boundary of the table.
      -  For information about how Sensible determines if lines are "contained" in a region, see [Region](doc:region).
   
   4. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score:
   
      - Sensible concatenates all your column descriptions with your overall table description. 
   
      - Sensible concatenates the first two rows of the table with the table title.
   
      - Sensible compares the two concatenations using the OpenAI Embeddings API. 
   
   5. Sensible uses GPT-3 to restructure the best-scoring table based on your column descriptions and your overall table description. Sensible returns the restructured table.