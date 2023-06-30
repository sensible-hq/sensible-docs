---
title: "Advanced prompt configuration"
hidden: false
---

You can configure the full prompt that Sensible inputs to a large-language model (LLM). You can apply configurations to multiple fields in a config, and you can override them for individual fields.

Sensible submits a full prompt to a large-language model (LLM) by combining:

- a prompt introduction
- "context", made up of chunks excerpted from the document and of page metadata. For more information about chunks, see the Notes section.
- concatenated descriptive prompts you configure in a Sensible Instruct method, such as in the [List](doc:list) or [Query](doc:query) methods.

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query](doc:query) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt.png)

| key  | description                                                  | parameter name                                               |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| A    | Prompt introduction. Includes asking for truthfulness, asking for confidence signals, and describing the format of the data to extract, for example, query, table, or table. | Prompt Introduction<br/>Confidence Signals                   |
| B    | Overall description of the chunks.                           | Context Description                                          |
| C    | Page metadata for chunks.                                    | Page Hinting                                                 |
| D    | Chunks, or "context", excerpted from document.               | Chunk Count<br/>Chunk Size<br/>Chunk Overlap Percentage<br/>Chunk Scoring Text (currently supported for Query method)<br/> |
| E    | Concatenation of all the descriptive prompts you configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:nlp-table) method. | Description                                                  |

See the following table for more information about the parameters in the preceding table.

Parameters
===


| SenseML parameter        | value                                                        | config-level description:<br/>configure in [NLP preprocessor](doc:nlp) | method-level description:<br/>configure in a field           |
| :----------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ***introductions***      |                                                              |                                                              |                                                              |
| promptIntroduction       | string. default: the prompt introduction default varies for each Sensible Instruct method. | Overwrites the default text at the beginning of the full prompt that Sensible submits to the LLM. <br/> This parameter applies to each method of a specified type in a config.<br/>The default for the prompt introduction differs for each Sensible Instruct method. For more information and for an example, see [NLP](doc:nlp) preprocessor.<br/>**Note**: If you set the Confidence Signals parameter to true, you can't configure this parameter. For more information, see the Confidence Signals parameter. | Overrides config-level parameter for a single field.<br/> The default for the prompt introduction differs for each Sensible Instruct method. For more information, see the Sensible Instruct reference topic for the method you want to edit, for example, [List](doc:list#parameters). <br/>**Note**: If you set the Confidence Signals parameter to true, you can't configure this parameter. For more information, see the Confidence Signals parameter. |
| ***confidence signals*** |                                                              |                                                              |                                                              |
| confidenceSignals        | boolean. default: true                                       | For data extracted by large-language models (LLMs), Sensible asks the LLM to report any uncertainties it has about the accuracy of the extracted data.  For more information, see [Confidence signals](doc:confidence).<br/>**Note:** If you set this parameter to true, then you can't configure the Prompt Introduction parameter, and Sensible includes confidence signal instructions in the default prompt introduction.<br/>Applies to each supported method in the config. Sensible currently supports this parameter for the [Query](doc:list#query) method. For more information, see [NLP](doc:nlp) preprocessor. | Overrides config-level parameter for a single field.<br/>**Note:** If you set this parameter to true, then you can't configure the Prompt Introduction parameter, and Sensible includes confidence signal instructions in the default prompt introduction. <br/>Sensible currently supports this parameter for the [Query](doc:list#query) method. For more information, see the [Query](doc:list#query) method. |
| ***hints***              |                                                              |                                                              |                                                              |
| contextDescription       | string. default: `The below context is an excerpt from a document.` | Configures context's metadata. For details about context and chunks, see the Notes section.<br/>Overwrites the default context description.<br/>Applies to each Sensible Instruct field in the config.<br/>For example:<br/>\- `The below context is an excerpt from a scanned index card that contains botanical information about a single plant species, including phenology information.`<br/>\- `The below context is an excerpt from an email. Assume the sender is always an automated system from an insurance broker.` | Overrides config-level parameter for a single field.         |
| pageHinting              | boolean. default: true                                       | Configures context's metadata. For details about context and chunks, see the Notes section. <br/>Includes or or removes page metadata for each chunk from the prompt Sensible inputs to an LLM.<br/>Applies to each Sensible Instruct field in the config.<br/>For example, removes phrases like `The excerpt starts at the top of page 1 and ends at the bottom of page 1.` | Overrides config-level parameter for a single field.         |
| ***chunks***             |                                                              |                                                              |                                                              |
| chunkScoringText         |                                                              | not available                                                | Sensible currently supports this parameter for the [Query](doc:query#parameters) method. |
| chunkCount               | number. default: `5`                                         | Configures context's size. For details about context and chunks, see the Notes section.<br/>The number of top-scoring chunks Sensible combines as context as part of the full prompt it submits to an LLM. <br/>Applies to each Sensible Instruct field in the config.<br/>Often, chunk count and chunk size are related. For example, if you know that your target data are spread over 7-10 pages, and occupy a small portion of those pages, you can specify a chunk count of 10 and a half-page  chunk size. | Overrides config-level parameter for a single field.         |
| chunkSize                | `0.5`, `1` default: `0.5`                                    | Configures context's size. For details about context and chunks, see the Notes section.<br/>The size of the chunks Sensible splits the document into, as a page fraction. For example, `0.5` specifies each chunk is half a page.<br/>Applies to each Sensible Instruct field in the config. <br/>Often, chunk count and chunk size are related. For example, if you know that the data you seek is contained in one cover page, you can set chunk size to 1 and a chunk count to 1. | Overrides config-level parameter for a single field.         |
| chunkOverlapPercentage   | `0`, `0.25`, `0.5` default: `0.5`                            | Configures context's size. For details about context and chunks, see the Notes section.<br/>The extent to which chunks overlap, as a percentage of the chunks' height. For example, `0.5` specifies each chunk overlaps by half its height. <br/>Applies to each Sensible Instruct field in the config. <br/>Sensible recommends setting a non-zero overlap to avoid splitting data across chunks. Set overlap to 0 solely if you're confident that your document layout doesn't flow across page boundaries and you're using a one-page chunk size. | Overrides config-level parameter for a single field.         |


Notes
===
For an overview of how Sensible Instruct methods work, see the following steps. 

1. To meet the LLM's input token limit, Sensible splits the document into chunks.
2. Sensible selects the most relevant chunks and combines them with page hinting data to create a "context".
3. Sensible creates a full prompt for GPT-3 that includes the context and the descriptive prompts you configure in the method. For an example of a full prompt, see the beginning of this topic.
4. Sensible returns the LLM's response.

For specifics about how each Sensible instruct method works, see the Notes section for each method, for example, [List](doc:list#notes) method.

