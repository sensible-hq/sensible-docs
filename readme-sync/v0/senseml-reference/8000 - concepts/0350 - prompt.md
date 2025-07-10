---
title: "Advanced LLM prompt configuration"
hidden: false
---

To extract data from a document using [LLM-based methods](doc:llm-based-methods), Sensible submits a part of the document to the LLM.  Submitting a part of the document instead of the whole document improves performance and accuracy. This document excerpt is called a prompt's *context*.

To troubleshoot LLM-based methods, you can configure how Sensible locates a prompt's context using one of the following approaches:

1. (Default) Locate context with embeddings scores

2. Locate context by summarizing document content

3. Locate context by "chaining" or "pipelining" prompts

4. Locate non-text images as context

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/mermaid_llm_context.png)

For information about configuring each of these approaches, see the following sections.

## (Default) Locate context with embeddings scores

By default, Sensible locates context by splitting the document into equally sized chunks, scoring them for relevancy using [embeddings](https://www.sensible.so/blog/embeddings-vs-completions-only-rag), and then returning the top-scoring chunks as context:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/chunk_score.png)

The advantage of this approach is that it's fast. The disadvantage is that it can be brittle.

The following steps outline this default approach and provide configuration details:

1. Sensible splits the document into chunks. Parameters that configure this step include:
   - Chunk Count parameter.
   - Page Range parameter
   - **Note:** Defaults for these parameters vary by LLM-based method. For example, the default for the Chunk Count parameter is 5 for the [Query Group](doc:query-group#parameters) method and 20 for the [List](doc:list#parameters) method. Each method has a default chunk size, up to one page.
2. Sensible selects the most relevant chunks and combines them with page-number metadata to create a "context".  Parameters that configure this step include:
   - LLM Engine parameter 
3. Sensible creates a *full prompt* for the LLM that includes the context and the descriptive prompts you configure in the method. Sensible sends the full prompt to the LLM.
4. Sensible returns the LLM's response.

The details for this general process vary for each LLM-based method. For more information, see the Notes section for each method's SenseML reference topic, for example, [List](doc:list#notes) method.

## (Recommended) Locate context by summarizing document

When you configure the Search By Summarization parameter for supported LLM-based methods, Sensible finds context using LLM-generated summaries. Sensible uses a [completion-only retrieval-augmented generation (RAG) strategy](https://www.sensible.so/blog/embeddings-vs-completions-only-rag):

1. Sensible prompts an LLM to summarize chunks of the document. If you set `page`, a chunk is a page. If you set `outline`, an LLM generates a table of contents of the document, and each segment of the outline is a chunk.

2. Sensible prompts a second LLM to identify the most relevant chunks based on the summaries, then uses their text as the context.

The following image shows how an LLM can outline and summarize a document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/summary_scoring_powerpoint.png)

This strategy often outperforms the default approach to locating context. It's useful for long documents in which multiple mentions of the same concept make finding relevant context difficult, for example, long legal documents.

## Locate context by pipelining prompts

When you specify the Source IDs parameter for supported LLM-based methods, Sensible prompts an LLM to answer questions about other [fields](doc:field-query-object)' extracted data.  In this case, the context is predetermined: it's the output from the other fields. 

For example, you use the layout-based [Text Table](doc:text-table) method to extract the following data into a `snacks_rank`  field: 

```json
snack       annual regional sales
apples      $100k
corn chips  $200k
bananas     $150k
```

If you create a Query Group method with the prompt `what is the best-selling snack?`, and specify `snacks_rank` as the context using the Source IDs parameter, then Sensible searches for answers to your question (`corn chips`) only in the extracted `snacks_rank` table rather than in the entire document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/mermaid_chain_prompt.png)



 Use other fields as context to: 

- Reformat or otherwise transform the outputs of other fields.
- Compute or generate new data from the output of other fields
- Narrow down the context for your prompts to a specific part of the document.
- Troubleshoot or simplify complex prompts that aren't performing reliably. Break the prompt into several simpler parts, and chain them together using successive Source ID parameters in the fields array.

To use other fields as context, configure the Source Ids parameter for the [Query Group](doc:query-group) or [List](doc:list#parameters) methods.

## Locate multimodal (non-text) data

When you configure the Multimodal Engine parameter for the Query Group method, you can extract from non-text data, such as photographs, charts, or illustrations. 

For example, for the following image, you can prompt,  `"are the buildings multistory? return true or false"`.



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/multimodal_photo.png)

When you extract multimodal data, Sensible sends an image of the relevant document region as  context to the LLM. Using the Region parameter, you can configure to locate the context using a manually specified anchor  and region coordinates, or use the default page chunk scoring approach.  



## Troubleshooting

See the following tips for troubleshooting situations in which large language model (LLM)-based extraction methods return inaccurate responses, nulls, or errors.

### Fix error messages

**Error message**

```
ConfigurationError: LLM response format is invalid
```

**Notes**

Reword the prompt in simpler terms, chain the prompt using the Source Ids parameter, or avoid specifying a format in the prompt for the extracted data. Or, add a fallback field to bypass the error if the original query is working for most documents and you're only seeing the error intermittently. See the following section for more information about fallbacks.

Background: Sensible returns this error when the LLM doesn't return its response in the JSON format that Sensible specifies in the backend for full prompts. This can occur when your `description` parameters prompt the LLM to return data in a specific format that conflicts with the expected JSON format.

### Interpret confidence signals

Confidence signals are an alternative to confidence scores and to error messages. For information about troubleshooting LLM confidence signals, such as `multiple_possible_answers` or `answer_maybe_be_incomplete`, see [Qualifying LLM accuracy](doc:confidence).

### Create fallbacks for null responses or false positives

Sometimes an LLM prompt works for the majority of documents in a document type, but returns null or an inaccurate response (a "false positive") for a minority of documents. Rather than rewrite the prompt, which can cause regressions, create fallbacks targeted at the failing documents. For more information, see [Fallback strategies](doc:fallbacks).

### Trace source context

Tracing the document's source text, or *context*, for an LLM's answer can help you determine if the LLM is misinterpreting the correct text, or targeting the wrong text.

You can view the source text for an LLM's answer highlighted in the document:

- In the visual output pane, click the **Location** icon next to a field to view its source text in the document.  For more information about how location highlighting works and its limitations, see [Location highlighting](doc:color#location-highlighting).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_location.png)

 





