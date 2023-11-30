---
title: 'draft llm'
hidden: true
---



**Tash**[1 day ago](https://sensiblehq.slack.com/archives/C0215T9K86P/p1701285302336219?thread_ts=1701284927.461799&cid=C0215T9K86P)

`fast` : Using a fast LLM model and applying auto-chunking (Determining which chunks are relevant: It doesn't change the chunk scoring itself but auto removing chunks that seem to be irrelevant, and only feeding those relevant ones to the model)



**Tash**[1 day ago](https://sensiblehq.slack.com/archives/C0215T9K86P/p1701285341991449?thread_ts=1701284927.461799&cid=C0215T9K86P)

`thorough` : Using a slower but more thorough LLM model and feeding all of the topChunks to the model.





(GPT-3)

TODO: remember to add to document type-level param??

| key               | value                               | description                                                  |
| :---------------- | :---------------------------------- | :----------------------------------------------------------- |
| id (**required**) | `list`                              | The Anchor parameter is optional for fields that use this method. If you specify an anchor, Sensible ignores it. |
| llm_engine        | `fast`, `thorough`. default: `fast` | Specifices the LLM model to which Sensible submits the full prompt, and affects the number of chunks that Sensible submits to the LLM. use thorough if you find that fast is partially extracting a multi-page list, ie skipping list items.<br/>fast: GPT-3.5 Turbo Uses a faster LLM model and potentially fewer chunks than those specified by the Chunk Count parameter<br/>thorough:GPT-4 - Uses a slower LLM model and exactly the number of chunks specified inth Chunk Count parameter. Use this if you find that the List method is skipping pages within a list/ failing to fully extract the List. QUESTION: is it slower? |

Notes
===

For an overview of how the List method works, see the following steps:

1. Sensible finds the chunks of the document that most likely contain your target data: 

  - Sensible concatenates all your property descriptions with your overall list description. 
  - Sensible splits the document into equal-sized chunks. 
  - Sensible scores your concatenated list descriptions against each chunk.

2. Sensible selects a number of the top-scoring chunks: 
   1. If you select `llm_engine: thorough`, the Chunk Count parameter determines the number of  top-scoring chunks Sensible selects.
   2. If you select `llm_engine: fast`,   Sensible 1. selects top-scoring chunks as determined by the Chunk Count parameters 2. Sensible selects a smaller list of page numbers by removing chunks that are significantly less relevant.
3. To avoid large-language model (LLM)'s token limits, Sensible batches the chunks into groups by page numbers, **up to a maximum of 20 page numbers TODO right place for it?** The chunks in each page group can be non-consecutive in the document.
4. For each page group, Sensible submits a full prompt to the LLM that includes the pages' chunks as context, page-hinting data, and your prompts. For information about the LLM model, see the LLM Engine parameter. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt). The full prompt instructs the LLM to create a list formatted as a table, based on the context.
5. Sensible concatenates the results from the LLM for each page group and returns a list, formatted as a table.