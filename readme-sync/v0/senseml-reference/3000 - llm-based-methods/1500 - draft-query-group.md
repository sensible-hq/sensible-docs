---
title: "Query group"
hidden: true

---




Parameters
=====



|      |      |      |
| :--- | :--- | :--- |
|      |      |      |
|      |      |      |

## Query group parameters



| key                   | value                        | description | interactions |
| :-------------------- | :--------------------------- | :---------- | ------------ |
|                       |                              |             |              |
| searchBySummarization | WORDING IS IDENTICAL TO LIST |             |              |
|                       |                              |             |              |

## Examples

For an example of using `"searchBySummarization": "outline"`, see [Multicolumn](doc:multicolumn#examples).

## Notes

For an overview of this method's default approach to locating context, see the following steps. 

For alternate approaches, see [Advanced LLM prompt configuration](doc:prompt#full-prompt).

### How it works by default

- Sensible finds the chunks of the document that most likely contain your target data:

  - Sensible splits the document into equal-sized chunks.
  - Sensible scores each chunk by its similarity to either the concatenated Description parameters for the queries in the group. Sensible scores each chunk using a nonconfigurable OpenAPI Embeddings API.

- Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. 

  - You can configure the chunk count with the Chunk Count parameter. If the chunks exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.

- Sensible creates a full prompt for the LLM that includes the chunks, page-hinting data, and your Description parameters. For more information about the full prompt, see [Advanced LLM prompt configuration](doc:prompt#full-prompt).

  - You can configure the LLM engine using the LLM Engine parameter. 

  
