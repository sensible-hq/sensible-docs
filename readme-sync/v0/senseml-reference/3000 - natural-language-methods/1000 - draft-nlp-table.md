---
title: "NLP Table"
hidden: true
---
doc:nlp-table#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

**Note** You can configure some the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrides the NLP preprocessor's parameter. For more information, see [Advanced prompt configuration](doc:prompt).


| key               | value                  | description                                                  |
| :---------------- | :--------------------- | :----------------------------------------------------------- |
| id (**required**) | `nlpTable`             | The Anchor parameter is optional for fields that use this method. If you specify an anchor, Sensible ignores it. |
| restructureTable  | Boolean. default: true | If true, then you can prompt the LLM to split or merge columns or otherwise transform the table.<br/> Configure this to false to improve performance and to avoid LLM token overflow errors caused by tables that exceed 4,000 [tokens](https://platform.openai.com/tokenizer). If false, skips the full table restructure described in the Notes section and ignores the Prompt Introduction. As a result, the LLM returns the table body unchanged from the OCR extraction, and the only change you can make is to rename the column headings using the column descriptions you write in the prompt.<br/><br/> |
|                   |                        |                                                              |
|                   |                        |                                                              |
|                   |                        |                                                              |
|                   |                        |                                                              |
|                   |                        |                                                              |
|                   |                        |                                                              |
|                   |                        |                                                              |



Examples
====

Notes
===

For an overview of how the NLP Table method works, see the following steps:


1. To optimize performance, Sensible makes a list of the pages that are most likely to contain your target table. To make the list:
   - Sensible concatenates all your column descriptions with your overall table description. 
   - Sensible splits the document into equal-sized, overlapping chunks. 
   - Sensible scores your concatenated table descriptions against each chunk using the OpenAI Embeddings API.
   - Sensible gets a list of page numbers from the top-scoring chunks.
2. Sensible extracts all the tables on the pages most likely to contain your table, using an Amazon OCR provider. If a table spans a page break, Sensible extracts the full, multi-page table.

3. For each extracted table, Sensible extracts the table title, if present.  In detail:

   -  Sensible extracts lines contained in a rectangular region immediately above each table, since that region is likely to contain the table title. 
   -  The height of that region equals the line height of the first non-empty cell of the table + 0.1 inches, and the region extends down to the top boundary of the table.
   -  For information about how Sensible determines if lines are "contained" in a region, see [Region](doc:region).

4. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score:

   - Sensible concatenates all your column descriptions with your overall table description. 

   - Sensible concatenates the first two rows of the table with the table title.

   - Sensible compares the two concatenations using the OpenAI Embeddings API. 

5. Sensible creates a full prompt for GPT-4 that includes the top-scoring table, page hinting data, and your prompts. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt). The full prompt instructs GPT-4 to restructure the best-scoring table based on your column descriptions and your overall table description. 

6. Sensible returns the restructured table.