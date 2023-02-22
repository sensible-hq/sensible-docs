---
title: "NLP Table"
hidden: true
---
Powered by GPT3

**limitations**

- It won't merge tables that span pages

- It works only (or at least best) on tables where the first row is a header

- It uses full doc OCR so it could time out on longer docs

- **future limitations**

- We should be able to support multi-page tables

- I’ve expanded it to check the first two rows, and we can likely look at the text directly preceding the table as well, but it will still mainly work with tables where the data elements are organized as rows (this is the typical case, but occasionally you run into data elements as columns)
- We can’t get around running table detection across the whole doc in the general case

**how it works**

1. Sensible uses a Microsoft OCR provider to find all the tables in the document. Sensible ignores any OCR settings you configure for the document type and uses Microsoft to OCR the entire document.
2. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score, Sensible compares your concatenated descriptions against the concatenated first two rows of the table using an OpenAPI embedding API. 
3. Sensible inputs the raw text of the highest-scoring table to GPT-3, and instructs GPT3 to output a new  table as follows:  `rearrange the below data into a tabular format where each row of the table answers the question posed in the header of the table. If the below data don't contain an answer to the question, just leave that cell of the table blank`
4. Sensible reformats the table returned by GPT3 to:
   1. format it in standard SenseML table format
   2.  remove the original table column headers 

- Sensible scores using embedding overlap (we turn raw text into vector and smaller angle means most similar...get thing pointing a direction in a high dimensional space representing smantics of text; if you see opposite vector pointing then you know they have very dissimilar meaning) ... IF the row headers have a lot of meaning, this works even better... so comparing vector of the 2 rows against the single vector of the concatenated descriptions ... ...the embedding engine is an openapi API thing... called an embedding b/c when you run gpt3, you give it the text context and words get tokenized into numeric representations and that transformation is similar to Topic taking bag of word and looking for overlap (with no relationship meaning)...but instead in the network, you transform the raw words into a bit of relationship meaning (arrangement in syntax)...taht intermediate internal rep of text is called an 'embedding ' ...just gives you back that internal representation (like a step of GPT3)...kinda like classification: which sample belongs to this category? or like clustering: whole bunch of docs, then organize them ... is embedding connoting these relationships? more a ref to taking data, embedding into a specific vector space (could come up in non-language use case w/ neural nets)...more about re-represenations of data in a meaningful space... we embed the rows, we embed the descriptions, and we do a similarity comparison and get a winning table ... then we stringify the table, give it to GPT3 and say re-represent it with these new column headings (the descriptions) ... should work for simple tables; no telling what GPT3 could do with complex tables...  

  -  the first two rows of each table using the descriptions you provide for the table's columns to find the best candidate table.

- Sensible creates a new, tabular representation of the best-candidate table by giving GPT3 this instruction, and we 

  `Please rearrange the below data into a tabular format where each row of the table answers the question posed in the header of the table. If the below data don't contain an answer to the question, just leave that cell of the table blank`

  - just transform that into SenseML table output and in post-process we remove the row headers



===

[@Josh Lewis](https://sensiblehq.slack.com/team/U0181MWQ8BV) so broadly, how does NLP table work? I have a rough guess:

- MS table finds all tables in doc (btw what engines do we use for Fixed Table and Table?)
  - Yes, and for fixedTable/table we use MS if there's no stop and Textract if there is... Stops table recognition at the matched line. Otherwise, Sensible searches all pages for tables, which can impact performance.<br/>When you specify a stop, Sensible  uses an Amazon Web Service  provider to perform table recognition. When you omit a stop, Sensible uses a Microsoft OCR provider.
- Score the MS tables (how? treating descriptions as questions and concatenating them then scoring 1st row against them?)
  - Yes, but first two rows
- feed highest scoring table to summarizer with prompt: "`Please rearrange the below data into a tabular format where each row of the table answers the question posed in the header of the table. If the below data don't contain an answer to the question, just leave that cell of the table blank."` -> it seems as if you're using summarizer to "recreate" the table? Are you doing so on a row-by-row basis, so each re-created table is just 1 row and 1 header? 
  - It recreates the whole table
- what's handling the question posed in `description` -- is it GPT3 summarizer or is it LayoutML? (I thought GPT3, but I did notice `question.ts` was modified)
  - GPT3



`Please rearrange the below data into a tabular format where each row of the table answers the question posed in the header of the table. If the below data don't contain an answer to the question, just leave that cell of the table blank.`



**Example tables**



These tables are good candidates:

| Snack | Ranking | Flavor profile | Regional sales |
| ----- | ------- | -------------- | -------------- |
|       |         |                |                |
|       |         |                |                |
|       |         |                |                |







These aren't:

| Risk type | january ranking | Feb ranking | This month ranking |
| --------- | --------------- | ----------- | ------------------ |
|           |                 |             |                    |
|           |                 |             |                    |
|           |                 |             |                    |

| Nutrition | Apple | Banana | Cantelope |
| --------- | ----- | ------ | --------- |
| calories  |       |        |           |
| fiber     |       |        |           |
| protein   |       |        |           |





also not a good candiate (might CHANGE if we add table title: same formatted table for different things like https://docs.google.com/document/d/13-Diiyds5-xa8KSVVMhQvNfjdwTbUe5EWc4kVp9MDrE/edit )





Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                    | value      | description                                                  |
| :--------------------- | :--------- | :----------------------------------------------------------- |
| id (**required**)      | `nlpTable` | The Anchor parameter is optional for fields that use this method. If you omit an anchor, Sensible searches the entire document for the data you want to extract. TODO: is that true |
| columns (**required**) | array      | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the column in the extraction output. <br/>  -`description` (**required**):  a natural-language description of the data you want to extract from the column. You can also provide instructions as you would with the [Summarizer method](doc:summarizer) to reformat or filter the column's data, for example, `the transaction amount. return the absolute values of the monetary amount` or `return the car make but not the model from this column`.  <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |
|                        |            |                                                              |
|                        |            |                                                              |
|                        |            |                                                              |

Examples
====

Example 1
---

The following example shows using the Summarizer method with the Topic method to extract agricultural data from a government report.

**Config**

```json

```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/tbd_.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/tbd_.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json

```



