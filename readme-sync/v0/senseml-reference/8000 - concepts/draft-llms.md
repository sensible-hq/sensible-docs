---
hidden: true
title: "Configure/troubleshoot LLMs"
---

- see also: troubleshoot-llms

- prompt tips stuff in each LLM topic
- prompt tips in /prompt
- other stuff?
- BLOG post on chaining prompts?



TO DOs: -- search by summarization is NOT global; NLP table don't support it.

## HOW IT WORKS





The following is an overview of how Sensible's LLM-based methods work. Use this overview to understand your configuration and troubleshooting options.

### Overview

Sensible supports LLM-based data extraction methods from documents. For example, for an insurance declaration document, you can submit the prompt `when does the insurance coverage start?`, and the LLM returns `08-14-24`. 

LLMs' input token limits are important constraints in this scenario. Because of these limits, Sensible must generally submit an excerpt of the document rather than the whole document to the LLM. This relevant excerpt is called *context*. For example, for the prompt  `when does the insurance coverage start?`, the abbreviated context can be something like:

````txt
Tel: 1-800-851-2000    Declarations Page
This is a description of you coverage
Please retain for your coverage.
Policy Number: 555-555-55-55
Coverage Period:
08-14-24 through 02-14-25
[etc]
````

Note that context doesn't have to be limited to contiguous pages in the document; it can consist of extracts scattered across the document.

### Example: Full prompt with context

See the following image for an example of a *full prompt* that Sensible inputs to an LLM for the [Query Group](doc:query-group) method using the default embeddings scoring approach (TODO link to that section).  When you write a prompt using an LLM-based method, Sensible creates a full prompt using the following:

- A prompt introduction
- "context", made up of chunks excerpted from the document and of page metadata. 
- concatenated descriptive prompts you configure in an LLM-based method, such as in the [List](doc:list) or [Query Group](doc:query-group) methods.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt.png)

| key  | description                                                  |
| ---- | ------------------------------------------------------------ |
| A    | Context description: an overall description of the chunks.<br/>Note that the preceding image shows an example of a user-configured context description overriding the default. |
| B    | Page metadata for chunks.                                    |
| C    | Chunks excerpted from document, concatenated into "context"  |
| D    | Concatenation of all the descriptive prompts you configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:nlp-table) method. |

Sensible provides configuration options for ensuring correct and complete contexts. For more information, see the following section.

// TODO: add a mermaid chart here??? https://docs.readme.com/main/docs/creating-mermaid-diagrams 

## Options for locating context

####  (Most determinate) Use other extracted fields as context

You can prompt an LLM to answer questions about other [fields](doc:field-query-object)' extracted data.  In this case, the context is predetermined: it's the output from the other fields. For example, say you use the Text Table method to extract the following data in a `snacks_rank` table: 

```json
snack       annual regional sales
apples      $100k
corn chips  $200k
bananas     $150k
```

If you create a Query Group method with the prompt `what is the best-selling snack?`, and specify `snacks_rank` as the context using the Source IDs parameter, then Sensible searches for answers to your question only in the extracted `snacks_rank` table rather than in the entire document. Use other fields as context to: 

- Reformat or otherwise transform the outputs of other fields.
- Compute or generate new data from the output of other fields
- Narrow down the [context](doc:prompt#notes) for your prompts to a specific part of the document.
- Troubleshoot or simplify complex prompts that aren't performing reliably. Break the prompt into several simpler parts, and chain them together using successive Source ID parameters in the fields array.

To use other fields as context, configure the Source Ids parameter for the [Query Group](doc:query-group) or [List](doc:list#parameters) methods.

#### (Best for legalese) Find context with page summaries

You can locate context using page summaries when you set the Search By Summarization parameter for supported LLM-based methods. Sensible uses a [completion-only retrieval-augmented generation (RAG) strategy](https://www.sensible.so/blog/embeddings-vs-completions-only-rag): Sensible prompts an LLM to summarize each page in the document, prompts a second LLM to return the pages most relevant to your prompt based on the summaries, and uses those pages' text as the context.  This strategy is can be useful for long documents in which multiple mentions of the same concept make finding relevant context difficult.

#### (Most configurable) Find context with embeddings scores

Sensible's default method for locating context is to split the document into fractional page chunks, score them for relevancy using embeddings, and then return the top-scoring chunks as context. 

The following steps provide details about the parameters you can use to configure this process:

1. To meet the LLM's input token limit, Sensible splits the document into chunks. These chunks are a fraction of a page and can overlap. Parameters that configure this step include:
   - Chunk Count
   - Chunk Size
   - Chunk Overlap Percentage
   - Page Range
2. Sensible selects the most relevant chunks and combines them with page-hinting data to create a "context".  Parameters that configure this step include:
   1. Page Hinting
   2. LLM Engine parameter

3. Sensible creates a *full prompt* for the LLM that includes the context and the descriptive prompts you configure in the method. Parameters that configure this step include:
   1. Context Description

4. Sensible returns the LLM's response.

For specifics about how each LLM-based method works, see the Notes section for each method's SenseML reference topic, for example, [List](doc:list#notes) method.

## Troubleshooting options

See the following tips for troubleshooting situations in which large language model (LLM)-based extraction methods return inaccurate responses, nulls, or errors.

### Fix error messages

**Error message**

```
ConfigurationError: LLM response format is invalid
```

**Description**

Sensible returns this error when the LLM doesn't return its response in the JSON format that Sensible specifies in the backend for [full prompts](doc:prompt). This can occur when your `description` parameters prompt the LLM to return data in a specific format that conflicts with the expected JSON format.

**Tips**

- Reword the prompt in simpler terms.
- Break a complex prompt into a sequence of simpler sub-prompts, or *chain* the prompt. Where supported, you can use the Source Ids parameter to chain prompts.
- Avoid specifying a format in the prompt for the extracted data.
- Where supported, select the non-default option for the method's LLM provider.
- Add a fallback field to bypass the error if the original query is working for most documents and you're only seeing the error intermittently. See the following section for more information about fallbacks.



### Interpret confidence signals

Confidence signals are an alternative to confidence scores and to error messages. For information about troubleshooting LLM confidence signals, such as `multiple_possible_answers` or `answer_maybe_be_incomplete`, see [Qualifying LLM accuracy](doc:confidence).

### Create fallbacks for null responses or false positives

Sometimes an LLM prompt works for the majority of documents in a document type, but returns null or an inaccurate response (a "false positive") for a minority of documents. Rather than rewrite the prompt, which can cause regressions, create fallbacks targeted at the failing documents. For more information, see [Fallback fields](doc:fallbacks).

### Trace source context

Tracing the document's source text, or [context](doc:prompt#notes), for an LLM's answer can help you determine if the LLM is misinterpreting the correct text, or targeting the wrong text.

You can view the source text for an LLM's answer highlighted in the document for the Query Group method:

- In the visual editor, click the **Location** button in the output of a query field to view its source text in the document.  For more information about how location highlighting works and its limitations, see [Location highlighting](doc:query-group#notes).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/location.png)

- In the JSON editor, Sensible displays location highlighting by outline the context with [blue boxes](doc:color). 

### Locate source context

Sometimes, an LLM fails to locate the relevant portion of the document that contains the answers to your prompts.  To troubleshoot targeting the wrong source text, or [context](doc:prompt#notes), in the document:

- For the Query Group method, add more prompts to the group that target information in the context, even if you don't care about the answer. For the List and NLP Table methods, add prompts to extract each item in the list or column in the table, respectively. 

- If the context occurs consistently in a page range in the document, use the Page Hinting or Page Range parameters to narrow down the context's possible location. For more  information about these parameters, see [Advanced LLM prompt configuration](doc:prompt).  (TODO: rename topic to "global parameters"? rm it entirely?)

