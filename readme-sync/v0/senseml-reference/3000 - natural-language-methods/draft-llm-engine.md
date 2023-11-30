---
title: 'draft llm'
hidden: true
---





(GPT-3)



| key               | value                               | description                                                  |
| :---------------- | :---------------------------------- | :----------------------------------------------------------- |
| id (**required**) | `list`                              | The Anchor parameter is optional for fields that use this method. If you specify an anchor, Sensible ignores it. |
| llm_engine        | `fast`, `thorough`. default: `fast` | Specifices the LLM model to which Sensible submits the full prompt. <br/>fast: GPT-3.5 Turbo<br/>thorough:GPT-4 |

Notes
===

For an overview of how the List method works, see the following steps:

1. Sensible finds the chunks of the document that most likely contain your target data: 

  - Sensible concatenates all your property descriptions with your overall list description. 
  - Sensible splits the document into equal-sized chunks. 
  - Sensible scores your concatenated list descriptions against each chunk.

2. Sensible selects a number of the top-scoring chunks, where the number is determined by the Chunk Count parameter. Sensible re-scores the top-scoring chunks to select a smaller list of page numbers containing the most relevant chunks, where the list size is determined by the re-scoring process. The  maximum list size is 20 page numbers.
3. To avoid large-language model (LLM)'s token limits, Sensible batches the page numbers into groups. The chunks in each page group can be non-consecutive in the document.
4. For each page group, Sensible submits a full prompt to the LLM that includes the pages' chunks as context, page-hinting data, and your prompts. For information about the LLM, see the LLM Engine parameter. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt). The full prompt instructs the LLM to create a list formatted as a table, based on the context.
5. Sensible concatenates the results from the LLM for each page group and returns a list, formatted as a table.