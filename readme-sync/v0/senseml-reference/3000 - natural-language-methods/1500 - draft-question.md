---
title: "Question"
hidden: true
---



Notes
===

For an overview of how this method works, see the following steps:

- To meet GPT-3's character limit for input, Sensible splits the document into equal-sized, overlapping chunks.
- Sensible scores each chunk by its similarity to either the `question` or the `chunkScoringText` parameters. Sensible scores each chunk using the OpenAPI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them. The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks.
- Sensible inputs the combined chunks to GPT-3 as one context, and instructs it to answer the question based on the context.
- **TODO: move this?** 
- Sensible returns an answer and any uncertainties about the answer. Uncertainties are an alternative to confidence scores. For tips about troubleshooting uncertainties, see [Query extraction tips](doc:query-tips). 



