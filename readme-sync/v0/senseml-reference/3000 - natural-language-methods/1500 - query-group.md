---
title: "Query group"
hidden: true

---

Extracts individual facts in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery. Sensible uses a large-language model (LLM)  to find these facts in paragraphs of free text, or in more structured layouts, for example key/value pairs or tables. 

Sensible recommends grouping queries together if they share [context](doc:query-group#notes).  Queries share context when data exists in the same location or region of a document.

For example, contact information can usually be found in the same location of a document:

```
New York City, NY
(123) 456-7890
jsmith@email.com 
```



Combining queries for the location, phone number, and email into the same group will help you maximize the accuracy and speed of your extractions. Frame each query, or prompt, in the group so that it has a single, short answer.  For complex prompts with multi-part answers, use the [List method](doc:list) or the  [Summarizer](doc:summarizer) method. 

For tips and troubleshooting, see [Query tips](doc:query-tips).

For more information about how this method works, see [Notes](doc:query#notes).

[**Parameters**](doc:query#parameters)
[**Examples**](doc:query#examples)
[**Notes**](doc:query#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

**Note** You can configure some the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrrides the NLP preprocessor's parameter. For more information, see [Advanced prompt configuration](doc:prompt).

| key                                 | value            | description                                                  |
| :---------------------------------- | :--------------- | :----------------------------------------------------------- |
| id (**required**)                   | `queryGroup`     | The Anchor parameter is optional for fields that use this method. If you specify an anchor:<br/>- Sensible ignores the anchor if it's present in the document.<br/>- Sensible returns null for the field if the anchor isn't present in the document. |
| queries                             | array of objects | An array of query objects, where each extracts a single fact. Each query contains the following parameters:<br/>`id` (**required**) - The ID for the extracted field. <br/>`description`  (**required**) - A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`. For more information about how to write questions (or "prompts"), see [Query extraction tips](https://docs.sensible.so/docs/query-tips). |
| chunkScoringText                    | string           | Configures context's content. For details about context and chunks, see the Notes section.<br/>A representative snippet of text from the part of the document where you expect to find the answer to your prompt. Use this parameter to narrow down the page location of the answer to your prompt. For example, if your prompt has multiple candidate answers, and the correct answer is located near unique or distinctive text that's difficult to incorporate into your question, then specify the distinctive text in this parameter.<br/>If specified, Sensible uses this text to find top-scoring chunks. If unspecified, Sensible uses the prompt to score chunks.<br/>Sensible recommends that the snippet is specific to the target chunk, semantically similar to the chunk, and structurally similar to the chunk. <br/>For example,  if the chunk contains a street address formatted with newlines, then provide a snippet with an example street address that contains newlines, like `123 Main Street\nLondon, England`. If the chunk contains a street address in a free-text paragraph, then provide an unformatted street address in the snippet.<br/>For an example, see [Example 3](doc:query#example-3).<br/> |
| (**Deprecated**) promptIntroduction | string.          | **(Deprecated)**  overwrites the introductory text at the beginning of the [full prompt](https://docs.sensible.so/docs/prompt) that Sensible submits to the LLM for this field. |
| confidenceSignals                   |                  | For information about this parameter, see [Advanced prompt configuration](doc:prompt). |
| contextDescription                  |                  | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| pageHinting                         |                  | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkCount                          | default: 5       | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkSize                           | default: 0.5     | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkOverlapPercentage              | default: 0.5     | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| pageRange                           |                  | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |

## Notes

For an overview of how this method works, see the following steps:

- To meet the LLM's token limit for input, Sensible splits the document into equal-sized, overlapping chunks.
- Sensible scores each chunk by its similarity to either the concatenated Description parameters for the queries in the group, or by the `chunkScoringText` parameters. Sensible scores each chunk using the OpenAPI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks. If you set chunk-related parameters that cause the context to exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.
- Sensible creates a full prompt for the LLM (GPT-3.5 Turbo) that includes the chunks, page hinting data, and your prompts in the group. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt).

How location highlighting works
---

In the Sensible Instruct editor, you can click the output of a query field to view its source text in the document. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/changelog_August2023_location.png)

For an overview of how Sensible finds the source text in the document for the LLM's response, see the following steps:

- The LLM returns a response to your prompt.

- Sensible searches in the source document for a line that's a fuzzy match to the response.  For example, if the LLM returns `4387-09-22-33`, Sensible matches the line `Policy Number: 4387-09-22-33` in the document. Sensible implements fuzzy matching using [Levenshtien distance](https://en.wikipedia.org/wiki/Levenshtein_distance).

- Sensible selects the three lines in the document that contain the best fuzzy matches. For each line, Sensible concatenates the preceding and succeeding lines, in case the match spans multiple lines.
- Sensible searches for a fuzzy match in the concatenated lines for the text that the LLM returned.  Sensible returns the best match.
- Sensible highlights the best match in the document in the Sensible Instruct editor or in the SenseML editor.

**Limitations**

Sensible can highlight the incorrect location under the following circumstances:

- If you prompt the LLM to reformat the source text in the document or reformat the text using a [type](doc:types) , then Sensible can fail to find a match or can find an inaccurate match.

- If there are multiple candidates fuzzy matches in the document (for example, two instances of `April 7`), Sensible chooses the top-scoring match. If candidates have similar scores, Sensible uses page location as a tie breaker and chooses the earliest match in the document.

- If the LLM returns text that's not in the document, then location highlighting is inapplicable.