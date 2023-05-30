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
- Sensible returns an answer and any uncertainties about the answer. Uncertainties are an alternative to confidence scores. For tips about troubleshooting uncertainties, see [Query extraction tips](doc:query-tips).



Measures of confidence
---

Sensible returns the following measure of confidence:

- JsonLogic validations: For deterministic asnwers (TODO look up old wording on this)
- OCR confidence scores: For scanned text
- Uncertainties: Sensible asks the LLM to report any issues with its answer. These reports are generative and not 100% accurate, but they tend to be more useful than confidence scores, which in Sensible's experience often fall into either buckets of 100% uncertainty or 0% uncertainty and are therefore not useful for the sort of nuance that is helpul in troubleshooting. Uncertainties provide more nuanced ground for troubleshooting. As the research paper [Teaching models to express their uncertainties in words](https://arxiv.org/pdf/2205.14334.pdf) suggests, Uncertainties may arise from but not limited to: multiple answers, answer not solving the question, answer not in the context, and ambiguous question. Sensible prompts the LLM to return uncertainties as follows. 

**Troubleshooting prompts for the Query method**

| Error message                              | What's going on                                              | Tips and troubleshooting                                     |
| ------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Multiple Possible Answers                  | The context that Sensible provides to the LLM has multiple possible answers. | - If you want multiple answers returned, consider using the [List method](doc:list-tips) instead.<br/>- If you want a single answer, tweak the context that Sensible provides to the LLM using  [chunk parameters](doc:question#parameters) so that it contains a single answer. |
| Answer might not fully answer the question |                                                              |                                                              |
| Answer not found in the context            |                                                              |                                                              |
| Ambiguous query                            |                                                              |                                                              |

