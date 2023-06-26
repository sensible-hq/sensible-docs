---
title: "Advanced prompt configuration"
hidden: true
---

You can configure the prompt that Sensible inputs to a large-language model (LLM). You can apply configurations to multiple fields in a config, and you can override them for individual fields.

Sensible submits a full prompt to a large-language model (LLM) by combining:

- prompt introduction
- "context", made up of chunks excerpted from the document and of page metadata. For more information about chunks, see the Notes section.
- concatenated descriptive prompts you configure in a Sensible Instruct method, such as the [List](doc:list) or [Query](doc:query) methods.

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query](doc:query) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/llm_prompt.png)



| key  | description                                                  | configurable for all fields in config? | overridable for each field?        | parameter name                                               |
| ---- | ------------------------------------------------------------ | -------------------------------------- | ---------------------------------- | ------------------------------------------------------------ |
| A    | prompt introduction. Includes asking for truthfulness and describing the format of the data to extract, for example, query, table, or table. | yes:<br/>[NLP preprocessor](doc:nlp)   | yes:<br/>Sensible Instruct methods | Prompt Introduction                                          |
| B    | overall description of the chunks, or "context"              | yes:<br/>[NLP preprocessor](doc:nlp)   | yes:<br/>Sensible Instruct methods | Context Description                                          |
| C    | page metadata for chunks                                     | yes:<br/>[NLP preprocessor](doc:nlp)   | yes:<br/>Sensible Instruct methods | Page Hinting                                                 |
| D    | chunks excerpted from document                               | yes:<br/>[NLP preprocessor](doc:nlp)   | yes:<br/>Sensible Instruct methods | Chunk Count<br/>Chunk Size<br/>Chunk Overlap Percentage<br/>Chunk Scoring Text (Configurable solely in Query method)<br/> |
| E    | concatenation of all the descriptive prompts configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:nlp-table) method. | no                                     | yes:<br/>Sensible Instruct methods | Description                                                  |

See the following table for more information about the parameters in the preceding table.

Parameters
===

TODO: some note about how these parameters have different names in the UI??


| SenseML parameter name               | value                                                        | Config-level description ([NLP preprocessor](doc:nlp))       | Instruct Field-level description                             |
| :----------------------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ***prompt introduction parameters*** |                                                              |                                                              |                                                              |
| promptIntroduction                   | string.                                                      | Overwrites the default text at the beginning of the full prompt that Sensible submits to the LLM.  Each method has its own default prompt introduction, so you must specify which method's prompt introduction you want to override. <br/>For example, you can override the prompt introduction for each NLP Table field in the config, while leaving the defaults for other Sensible Instruct fields.<br/>For an example, see [NLP#examples](doc:nlp) preprocessor. | Overwrites the default text at the beginning of the full prompt that Sensible submits to the LLM for this field.  Applies to a single field. <br/>Each method has its own default prompt introduction. For more information, see each Sensible Instruct method reference topic, for example, [List](doc:list#parameters). <br/>TODO add links to examples?? |
| ***hinting parameters***             |                                                              |                                                              |                                                              |
| contextDescription                   | string. default: `The below context is an excerpt from a document.` | Configures context's metadata. For details about context and chunks, see the Notes section.<br/>Overwrites the default context description. Applies to each Sensible Instruct field in the config.<br/>For example:<br/>\- `The below context is an excerpt from an index card that contains botanical information about a single plant species, including phenology information.`<br/>\- `The below context is an excerpt from an email. Assume the sender is always an automated system from an insurance broker.` | Overwrites config-level parameter for a single field.        |
| pageHinting                          | boolean. default: true                                       | Configures context's metadata. For details about context and chunks, see the Notes section. <br/>Includes or or removes page metadata for each chunk from the prompt Sensible inputs to an LLM. Applies to each Sensible Instruct field in the config.<br/>For example, removes phrases like `The excerpt starts at the top of page 1 and ends at the bottom of page 1.` | Overwrites config-level parameter for a single field.        |
| ***chunking parameters***            |                                                              |                                                              |                                                              |
| chunkScoringText                     |                                                              | not available                                                | Available for the [Query](doc:query#parameters) method.      |
| chunkCount                           | number. default: `5`                                         | Configures context's size. For details about context and chunks, see the Notes section.<br/>The number of top-scoring chunks Sensible combines as context as part of the full prompt it submits to an LLM. Applies to each Sensible Instruct field in the config.<br/>Often, chunk count and chunk size are related. For example, if you know that your target data are spread over 7-10 pages, and occupy a small portion of those pages, you can specify a chunk count of 10 and a quarter- or half-page  chunk size. | Overwrites config-level parameter for a single field.        |
| chunkSize                            | `0.5`, `1` default: `0.5`                                    | Configures context's size. For details about context and chunks, see the Notes section.<br/>The size of the chunks Sensible splits the document into, as a page fraction. For example, `0.5` specifies each chunk is half a page. Applies to each Sensible Instruct field in the config. <br/>Often, chunk count and chunk size are related. For example, if you know that the data you seek is contained in one cover page, you can set chunk size to 1 and a chunk count to 1. | Overwrites config-level parameter for a single field.        |
| chunkOverlapPercentage               | `0`, `0.25`, `0.5` default: `0.5`                            | Configures context's size. For details about context and chunks, see the Notes section<br/>The extent to which chunks overlap, as a percentage of the chunks' height. For example, `0.5` specifies each chunk overlaps by half its height. <br/>Sensible recommends setting a non-zero overlap to avoid splitting data across chunks. Set overlap to 0 solely if you're confident that your document layout doesn't flow across page boundaries and you're using a one-page chunk size. | Overwrites config-level parameter for a single field.        |

Notes
===
TODO: edit 

Each Sensible Instruct method has a process that generally looks like the following. See the Notes section for each method for specifics, for example, [List](doc:list#notes) method:

1. To meet the LLM's input token limit, Sensible splits the document into chunks. For configuration, see the chunking parameters.
2. Sensible scores the chunks by relevance to your prompt, selects a number of top-scoring chunks, and combines them with page metadata. For configuration, see the chunking and hinting parameters.
3. Sensible creates a full prompt for GPT-3 that includes the chunks and the descriptive prompts you configure in the method. For an example of a full prompt, see the beginning of this topic.
4. Sensible returns the LLM's response.



