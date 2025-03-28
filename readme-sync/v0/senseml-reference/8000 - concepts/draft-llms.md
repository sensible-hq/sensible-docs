---
hidden: true
title: "Configure and troubleshoot LLMs"
---

- *TODO before publish:*
- *w/ Instruct going away, i can delete/replace the /prompt topic! And maybe just xlink btwn the NLP preprocessor in each method ...* 
- *prompt tips stuff in each LLM topic*
- *prompt tips in /prompt*

# Overview

To capture data from a document (e.g., a policy number or a list of transactions in a bank statement), Sensible has to submit a part of the document to the LLM.  Submitting a part of the document instead of the whole document improves performance and accuracy.

To troubleshoot, you can configure which part of the document (the *context*) to submit using one of the following approaches:

1. (Default) Locate context by scoring page chunks

2. Locate context by summarizing pages

3. Locate context by chaining prompts

4. Locate multimodal (non-text) data

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/mermaid_llm_context.png)

For information about configuring each of these approaches, see the following sections.

## (Default) Locate context by scoring page chunks

Sensible's default method for locating context is to split the document into fractional page chunks, score them for relevancy using embeddings, and then return the top-scoring chunks as context:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/chunk_score.png)

The advantage of this approach is that it's fast. The disadvantage is that it can be brittle.

The following steps outline this default approach and provides configuration details:

1. Sensible splits the document into chunks. These chunks are a fraction of a page and can overlap or be noncontiguous. Parameters that configure this step include:
   - Chunk Count parameter
   - Chunk Size parameter
   - Chunk Overlap Percentage parameter
   - Page Range parameter
2. Sensible selects the most relevant chunks and combines them with page-hinting data to create a "context".  Parameters that configure this step include:
   - Page Hinting parameter
   - LLM Engine parameter

3. Sensible creates a *full prompt* for the LLM that includes the context and the descriptive prompts you configure in the method. Parameters that configure this step include:
   - Context Description parameter

4. Sensible returns the LLM's response.

The details for this general process vary for each LLM-based method. For more information, see the Notes section for each method's SenseML reference topic, for example, [List](doc:list#notes) method.

See the following image for an example of a *full prompt* that Sensible inputs to an LLM for the [Query Group](doc:query-group) method using the default approach:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt.png)

| key  | description                                                  |
| ---- | ------------------------------------------------------------ |
| A    | Context description: an overall description of the chunks.<br/>Note that the preceding image shows an example of a user-configured context description overriding the default. |
| B    | Page metadata for chunks.                                    |
| C    | Chunks excerpted from document, concatenated into "context"  |
| D    | Concatenation of all the descriptive prompts you configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:nlp-table) method. |

## Locate context by summarizing pages

When you set the Search By Summarization parameter to true for supported LLM-based methods, Sensible finds context using LLM-generated page summaries. Sensible uses a [completion-only retrieval-augmented generation (RAG) strategy](https://www.sensible.so/blog/embeddings-vs-completions-only-rag):

1. Sensible prompts an LLM to summarize each page in the document.

   1.  TODO: what params are useful here??

2. Sensible prompts a second LLM to return the pages most relevant to your prompt based on the summaries.

3. Sensible uses those pages' text as the context. 

   

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/mermaid_page_summary.png)

This strategy is useful for long documents in which multiple mentions of the same concept make finding relevant context difficult, for example, long legal documents.

## Locate context by chaining prompts

When you specify the Source IDs parameter for supported LLM-based methods, Sensible prompts an LLM to answer questions about other [fields](doc:field-query-object)' extracted data.  In this case, the context is predetermined: it's the output from the other fields. 

For example, you use the [Text Table](doc:text-table) method to extract the following data into a `snacks_rank`  field: 

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
- Narrow down the [context](doc:prompt#notes) for your prompts to a specific part of the document.
- Troubleshoot or simplify complex prompts that aren't performing reliably. Break the prompt into several simpler parts, and chain them together using successive Source ID parameters in the fields array.

To use other fields as context, configure the Source Ids parameter for the [Query Group](doc:query-group) or [List](doc:list#parameters) methods.

## Locate multimodal (non-text) data

When you configure the Multimodal Engine parameter for the Query Group method, you can extract from non-text data, such as photographs, charts, or illustrations. 

For example, for the following image, you can prompt,  `"are the buildings multistory? return true or false"`.



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/multimodal_photo.png)

When you extract multimodal data, Sensible sends an image of the relevant document region as  context to the LLM. Using the Region parameter, you can configure to locate the context using a manually specified anchor  and region coordinates, or use the default page chunk scoring approach.  



 *TODO cross link to 'embeddings' approach from query group parameter table to here on publish.*



## Troubleshooting options

See the following tips for troubleshooting situations in which large language model (LLM)-based extraction methods return inaccurate responses, nulls, or errors.

### Fix error messages

**Error message**

```
ConfigurationError: LLM response format is invalid
```

**Notes**

Reword the prompt in simpler terms, chain the prompt using the Source Ids parameter, or avoid specifying a format in the prompt for the extracted data. Or, add a fallback field to bypass the error if the original query is working for most documents and you're only seeing the error intermittently. See the following section for more information about fallbacks.

Background: Sensible returns this error when the LLM doesn't return its response in the JSON format that Sensible specifies in the backend for [full prompts](doc:prompt). This can occur when your `description` parameters prompt the LLM to return data in a specific format that conflicts with the expected JSON format.

### Interpret confidence signals

Confidence signals are an alternative to confidence scores and to error messages. For information about troubleshooting LLM confidence signals, such as `multiple_possible_answers` or `answer_maybe_be_incomplete`, see [Qualifying LLM accuracy](doc:confidence).

### Create fallbacks for null responses or false positives

Sometimes an LLM prompt works for the majority of documents in a document type, but returns null or an inaccurate response (a "false positive") for a minority of documents. Rather than rewrite the prompt, which can cause regressions, create fallbacks targeted at the failing documents. For more information, see [Fallback strategies](doc:fallbacks).

### Trace source context

Tracing the document's source text, or [context](doc:prompt#notes), for an LLM's answer can help you determine if the LLM is misinterpreting the correct text, or targeting the wrong text.

You can view the source text for an LLM's answer highlighted in the document for the Query Group method:

- In the visual editor, click the **Location** button in the output of a query field to view its source text in the document.  For more information about how location highlighting works and its limitations, see [Location highlighting](doc:query-group#notes).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_location.png)

- In the JSON editor, Sensible displays location highlighting by outline the context with [blue boxes](doc:color). 

### Locate source context

Sometimes, an LLM fails to locate the relevant portion of the document that contains the answers to your prompts.  To troubleshoot targeting the wrong source text, or [context](doc:prompt#notes), in the document:

- For the Query Group method, add more prompts to the group that target information in the context, even if you don't care about the answer. For the List and NLP Table methods, add prompts to extract each item in the list or column in the table, respectively. 

- If the context occurs consistently in a page range in the document, use the Page Hinting or Page Range parameters to narrow down the context's possible location. For more  information about these parameters, see [Advanced LLM prompt configuration](doc:prompt).  (TODO: rename topic to "global parameters"? rm it entirely?)



