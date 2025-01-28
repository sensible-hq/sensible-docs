---
hidden: true
title: "Configure/troubleshoot LLMs"
---

- see also: troubleshoot-llms

- prompt tips stuff in each LLM topic
- prompt tips in /prompt
- other stuff?
- BLOG post on chaining prompts?

## HOW IT WORKS







### prompt overview

The following is an overview of how Sensible's LLM-based methods work, to help you undersatnd your configuration options.

The most important constraint is that Sensible can't provide the text of a whole document to an LLM, unless the document is quite short. To meet the LLM's input token limit, Sensible must instead provide the LLM with a relevant extract from the document, or *context*. For example, for an insurance declaration document, the prompt might be `when does the coverage start?` and the (abbreviated) context might be something like:

````txt
Tel: 1-800-851-2000    Declarations Page
This is a description of you coverage
Please retain for your coverage.
Policy Number: 555-555-55-55
Coverage Period:
08-14-20 through 02-14-21
````

Note that context doesn't have to be limited to contiguous pages in the document; it can consist of extracts scattered across the document.

Most LLM-prompt troubleshooting has to do with context: locating it, making sure it's complete.

You can use a variety of configuration methods to locate the relevant and complete context in the document.  Let's go through them from least to most configurable:



// TODO: add a mermaid chart here??? https://docs.readme.com/main/docs/creating-mermaid-diagrams 

####  (most determinate) Use other extracted fields as context

You can extract data from other extracted fields using the Source Ids parameter for supported LLM-based methods. In this case, the context is predetermined: it's the output from the other fields. For example, say you use the Text Table method to extract the following data in a `snacks_rank` table (not shown in json for brevity): 

```json
snack       annual regional sales
apples      $100k
corn chips  $200k
bananas     $150k
```

If you create a Query Group method with the prompt `what is the best-selling snack?`, and specify `snacks_rank` as the context using the Source IDs parameter, then Sensible searches for answers to your question only in the extracted `snacks_rank` table. This can be useful for: 

- TBD prompt chaining etc

#### (TBD/TODO: most what?) Find context with page summaries

You can locate context using page summaries when you set the Search By Summarization parameter for supported LLM-based methods. Sensible uses a [completion-only retrieval-augmented generation (RAG) strategy](https://www.sensible.so/blog/embeddings-vs-completions-only-rag): Sensible prompts an LLM to summarize each page in the document, prompts a second LLM to return the pages most relevant to your prompt based on the summaries, and extracts the answers to your prompts from those pages' text.

#### (most configurable) Find context with chunk embeddings scores

Sensible's default method for locating context is as follows: 

1. To meet the LLM's input token limit, Sensible splits the document into chunks. These chunks are usually a fraction of a page and can overlap. Configurable parameters include:
   - Chunk Count
   - Chunk Size
   - Chunk Overlap Percentage
   - Page Range
   - MORE, depending on the method
2. Sensible selects the most relevant chunks and combines them with page-hinting data to create a "context".  Configurable parameters include:
   1. Context Description
   2. MORE depending on the method
3. Sensible creates a full prompt for the LLM that includes the context and the descriptive prompts you configure in the method. Configurable parameters include:
   1. Context Description

4. Sensible returns the LLM's response.

For specifics about how each LLM-based method works, see the Notes section for each method's SenseML reference topic, for example, [List](doc:list#notes) method.

You can configure a lot of the variables in the preceding steps:

In detail, when you write a prompt using an LLM-based method, Sensible creates a full prompt using the following:

- a prompt introduction
- "context", made up of chunks excerpted from the document and of page metadata. For more information about chunking configuration, see the Notes section.
- concatenated descriptive prompts you configure in an LLM-based method, such as in the [List](doc:list) or [Query Group](doc:query-group) methods.

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query Group](doc:query-group) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt.png)

The following table shows parameters that configure parts of the full prompt and that are global, or common to all LLM-based methods:

| key  | description                                                  | global parameters                                            |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| A    | Overall description of the chunks.<br/>The preceding image shows an example of a user-configured context description overriding the default. | Context Description                                          |
| B    | Page metadata for chunks.                                    | Page Hinting                                                 |
| C    | Chunks excerpted from document, concatenated into "context"  | Chunk Count<br/>Chunk Size<br/>Chunk Overlap Percentage<br/>Page Range |
| D    | Concatenation of all the descriptive prompts you configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:nlp-table) method. | Description fields                                           |
|      |                                                              |                                                              |





### list

For an overview of how this method works when `"searchBySummarization": false` and `source_ids` are unspecified, see the following steps:

1. Sensible finds the chunks of the document that most likely contain your target data: 

   - Sensible concatenates all your property descriptions with your overall list description. 

   - Sensible splits the document into equal-sized chunks. 

   - Sensible scores your concatenated list descriptions against each chunk.


2. Sensible selects a number of the top-scoring chunks: 

   1. If you specify Thorough or Long for the LLM Engine parameter, the Chunk Count parameter determines the number of top-scoring chunks Sensible selects to submit to the LLM.
   2. If you specify Fast for the LLM Engine parameter,  1. Sensible selects a number of top-scoring chunks as determined by the Chunk Count parameter. 2. To improve performance, Sensible removes chunks that are significantly less relevant from the list of top-scoring chunks. The number of chunks Sensible sumbits to the LLM can therefore be smaller than the number specified by the Chunk Count parameter.

3. To avoid large language model (LLM)'s input token limits, Sensible batches the chunks into groups. The chunks in each page group can come from non-consecutive pages in the document. If you set the Single LLM Completion parameter to True, then Sensible creates a single group that contains all the top-scoring chunks and sets a larger maximum token input limit for the single group (about 120k tokens) than it does for batched groups.

4. For each chunk group, Sensible submits a full prompt to the LLM that includes the chunks as context, page-hinting data, and your prompts. For information about the LLM model, see the LLM Engine parameter. For more information about the full prompt, see [Advanced LLM prompt configuration](doc:prompt). The full prompt instructs the LLM to create a list formatted as a table, based on the context.

5. Sensible concatenates the results from the LLM for each page group and returns a list, formatted as a table.

   ### NLP table

   For an overview of how the NLP Table method works, see the following steps:


   1. To optimize performance, Sensible makes a list of the pages that are most likely to contain your target table. To make the list:
      - Sensible concatenates all your column descriptions with your overall table description. 
      - Sensible splits the document into equal-sized, overlapping chunks. 
      - Sensible scores your concatenated table descriptions against each chunk using the OpenAI Embeddings API.
      - Sensible gets a list of page numbers from the top-scoring chunks.
   2. Sensible extracts all the tables on the pages most likely to contain your table, using the [OCR engine](doc:ocr-engine) specified by the document type. Sensible supports multi-page tables.
   3. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score:

      - Sensible concatenates all your column descriptions with your overall table description. 

      - Sensible concatenates a number of the first rows of the table with the table title.  Sensible uses the table title extracted by the table OCR provider, or falls back to using the text in a region above the table if the OCR provider doesn't find a title.

      - Sensible compares the two concatenations using the OpenAI Embeddings API. 
   4. Sensible creates a full prompt for the LLM (as specified by the LLM Engine parameter) that includes the top-scoring table, page hinting data, and your prompts. For more information about the full prompt, see [Advanced LLM prompt configuration](doc:prompt). The full prompt instructs the LLM to rewrite or restructure the best-scoring table based on your column descriptions and your overall table description. Note that if you select `rewriteTable: false`, Sensible uses an LLM (GPT-4) to rewrite the column headings' IDs, but doesn't otherwise restructure the table.
   5. Sensible returns the restructured table.

### query group



When you specify `source_ids` , Sensible uses the specified IDs as context. Otherwise, see the following notes:

- For an overview of how this method works when `"searchBySummarization": false`, see the following steps.   
  - To meet the LLM's token limit for input, Sensible splits the document into equal-sized, overlapping chunks.
  - Sensible scores each chunk by its similarity to either the concatenated Description parameters for the queries in the group, or by the `chunkScoringText` parameter. Sensible scores each chunk using the OpenAPI Embeddings API.
  - Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks. If you set chunk-related parameters that cause the context to exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.
  - Sensible creates a full prompt for the LLM (as determined by the LLM Engine parameter) that includes the chunks, page hinting data, and your Description parameters. For more information about the full prompt, see [Advanced LLM prompt configuration](doc:prompt).

- For an overview of how this method works when `"searchBySummarization": true`, see the following steps.
  1. Sensible prompts an LLM (GPT-4o mini) to summarize each page in the document. Sensible ignores the Chunk Scoring Text parameter.

  2. Sensible prompts an LLM (GPT-4o) with all the indexed page summaries as context, and asks it to return a number of page indices that are most relevant to your concatenated Description parameters. The Chunk Count parameter configures the number of page indices that the LLM returns. Sensible recommends setting the Chunk Count parameter to less than 10.

  3. Sensible prompts an LLM (as configured by the LLM Engine parameter) to answer your prompts, with the full text of the relevant pages as context. If you configure the Page Hinting parameter, it takes effect in this and the preceding step. If you configure the Multimodal Engine parameter, it takes effect in this step. 