---
title: "search summary"
hidden: true
---


|      |      |      |
| ---: | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |



## Notes

For an overview of how this method works when `"searchBySummarization": false`, see the following steps.   

- To meet the LLM's token limit for input, Sensible splits the document into equal-sized, overlapping chunks.
- Sensible scores each chunk by its similarity to either the concatenated Description parameters for the queries in the group, or by the `chunkScoringText` parameter. Sensible scores each chunk using the OpenAPI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks. If you set chunk-related parameters that cause the context to exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.
- Sensible creates a full prompt for the LLM (as determined by the LLM Engine parameter) that includes the chunks, page hinting data, and your Description parameters. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt).





