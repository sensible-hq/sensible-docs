---
title: "search summary"
hidden: true
---


|                       |                         |                                                              |
| --------------------: | ----------------------- | ------------------------------------------------------------ |
| searchBySummarization | boolean. default: false | Set this to true to troubleshoot situations in which Sensible returns false positives for your prompts by misidentifying the part of the document that contains the answers to your prompts. <br/>This parameter is compatible with documents up to 1,280 pages long.<br/><br/>When true, Sensible bypasses the steps described in the Notes section and takes the following steps to implement a [completion-only RAG strategy](https://www.sensible.so/blog/embeddings-vs-completions-only-rag): <br/>1. Sensible prompts an LLM (as configured by the LLM Engine parameter) to summarize each page in the document. <br/> 2. Sensible prompts an LLM (GPT-4o) with all the indexed page summaries as context, and asks it to return a number of page indices that are most relevant to your concatenated Description parameters. The Chunk Count parameter configures the number of page indices that the LLM returns. <br/>3. Sensible prompts an LLM (as configured by the LLM Engine parameter) to answer your prompts, with the full text of the relevant pages as context.<br/><br/>If you set this parameter to true, then Sensible recommends the following for chunk-related parameters:<br/>- Chunk Count parameter: Set this to no larger than 10. <br/>-  Chunk Size parameter: Set this to 1<br/>- Chunk Overlap Percentage parameter: Set this to 0<br/><br/>If you set this parameter to true, it has the following effects on other parameters:<br/>- Sensible ignores the Chunk Scoring Text parameter.<br/>- If you configure the Multimodal Engine parameter, it takes effect in step 3 in the preceding list.<br/>- If you configure the Page Hinting parameter, it takes effect in step 2 and step 3.<br/> |
|             llmEngine | object                  | Where applicable, configures the LLM engine Sensible  that uses to answer your prompts. For situations where this parameter is applicable, see mentions of the LLM Engine parameter in this topic.  <br/>Contains the following parameters:<br/>`provider`:  <br/>- If set to `open-ai`, Sensible uses GPT-3 Turbo.  <br/> - If set to `anthropic`, Sensible uses TODO/TBD. |
|                       |                         |                                                              |



## Notes

For an overview of how this method works when `"searchBySummarization": false`, see the following steps.   

- To meet the LLM's token limit for input, Sensible splits the document into equal-sized, overlapping chunks.
- Sensible scores each chunk by its similarity to either the concatenated Description parameters for the queries in the group, or by the `chunkScoringText` parameter. Sensible scores each chunk using the OpenAPI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks. If you set chunk-related parameters that cause the context to exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.
- Sensible creates a full prompt for the LLM (as determined by the LLM Engine parameter) that includes the chunks, page hinting data, and your Description parameters. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt).





