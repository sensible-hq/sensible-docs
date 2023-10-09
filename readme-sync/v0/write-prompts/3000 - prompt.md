---
title: "Advanced prompt configuration"
hidden: false
---


TEST You can configure the full prompt that Sensible inputs to a large-language model (LLM). You can apply configurations to multiple fields in a config, and you can override them for individual fields.

When you write a prompt in a Sensible Instruct method, Sensible combines your prompt with other information to create the full prompt it submits to a large-language model (LLM). The full prompt includes:

- a prompt introduction
- "context", made up of chunks excerpted from the document and of page metadata. For more information about chunks, see the Notes section.
- concatenated descriptive prompts you configure in a Sensible Instruct method, such as in the [List](doc:list-tips) or [Query](doc:query-tips) methods.

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query](doc:query-tips) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt.png)



| key  | description                                                  | parameter name                                               |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| A    | Prompt introduction. Includes asking for truthfulness and describing the format of the data to extract, for example, query, table, or table.<br/>The preceding image shows an example of a user-configured introduction overriding the default. | Prompt Introduction<br/>Confidence Signals                   |
| B    | Overall description of the chunks.<br/>The preceding image shows an example of a user-configured context description overriding the default. | Context Description                                          |
| C    | Page metadata for chunks.                                    | Page Hinting                                                 |
| D    | Chunks, or "context", excerpted from document.               | Chunk Count<br/>Chunk Size<br/>Chunk Overlap Percentage<br/>Chunk Scoring Text (currently supported for Query method)<br/> |
| E    | Concatenation of all the descriptive prompts you configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:table-tips) method. | Description                                                  |

You can configure all of these parameters in the SenseML editor and in the Sensible Instruct editor. For example, the following screenshots show prompt settings in Sensible Instruct for a Query field: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt_instruct_1.png)

The following screenshot shows prompt settings in Sensible Instruct for all fields in a config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt_instruct_2.png)



See the following table for more information about the parameters in the preceding table.

Parameters
===


| SenseML parameter      | value                                                        | config-level description:<br/>configure in [NLP preprocessor](doc:nlp) or in Sensible app | method-level description:<br/>configure in a field           |
| :--------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| promptIntroduction     | string. default: the prompt introduction default varies for each Sensible Instruct method. | Overwrites the default text at the beginning of the full prompt that Sensible submits to the LLM. <br/> This parameter applies to each method of a specified type in a config.<br/>The default for the prompt introduction differs for each Sensible Instruct method. For more information and for an example, see [NLP](doc:nlp) preprocessor.<br/>**Note**: If you set the Confidence Signals parameter to true, Sensible ignores this parameter and instead uses a nonconfigurable introduction that prompts for confidence signals. | Overrides config-level parameter for a single field.<br/> For more information, see the Sensible Instruct reference topic for the method you want to edit, for example, [List](doc:list#parameters). |
| confidenceSignals      | boolean.<br/>defaults: true in  Sensible Instruct editor,<br/> false in SenseML editor | If specified, Sensible prompts the LLM to report any uncertainties it has about the accuracy of its response.  For more information, see [Qualifying LLM accuracy](doc:confidence).<br/>Applies to each supported method in the config. Sensible currently supports this parameter for the [Query](doc:query) method. | Overrides config-level parameter for a single field.         |
| contextDescription     | string. default: `The below context is an excerpt from a document.` | Configures context's metadata. For details about context and chunks, see the Notes section.<br/>Overwrites the default context description.<br/>Applies to each Sensible Instruct field in the config.<br/>For example:<br/>\- `The below context is an excerpt from a scanned index card that contains botanical information about a single plant species, including phenology information.`<br/>\- `The below context is an excerpt from an email. Assume the sender is always an automated system from an insurance broker.` | Overrides config-level parameter for a single field.         |
| pageHinting            | boolean. default: true                                       | Configures context's metadata. For details about context and chunks, see the Notes section. <br/>Includes or or removes page metadata for each chunk from the prompt Sensible inputs to an LLM.<br/>For example, if a PDF converter automatically applied page numbers to scanned ID cards, set this parameter to false to ignore the page numbers, since their relationship to the cards' text is arbitrary.<br/>Applies to each Sensible Instruct field in the config.<br/>For example, removes phrases like `The excerpt starts at the top of page 1 and ends at the bottom of page 1.` | Overrides config-level parameter for a single field.         |
| chunkScoringText       |                                                              | not available                                                | Sensible currently supports this parameter for the Query method. For more information, see the [Query](doc:query#parameters) method. |
| chunkCount             | number. default: `5`                                         | Configures context's size. For details about context and chunks, see the Notes section.<br/>The number of top-scoring chunks Sensible combines as context as part of the full prompt it submits to an LLM. <br/>Applies to each Sensible Instruct field in the config.<br/>Often, chunk count and chunk size are related. For example, if you know that your target data are spread over 7-10 pages, and occupy a small portion of those pages, you can specify a chunk count of 10 and a half-page  chunk size. | Overrides config-level parameter for a single field.         |
| chunkSize              | `0.5`, `1` default: `0.5`                                    | Configures context's size. For details about context and chunks, see the Notes section.<br/>The size of the chunks Sensible splits the document into, as a page fraction. For example, `0.5` specifies each chunk is half a page.<br/>Applies to each Sensible Instruct field in the config. <br/>Often, chunk count and chunk size are related. For example, if you know that the data you seek is contained in one cover page, you can set chunk size to 1 and a chunk count to 1. | Overrides config-level parameter for a single field.         |
| chunkOverlapPercentage | `0`, `0.25`, `0.5` default: `0.5`                            | Configures context's size. For details about context and chunks, see the Notes section.<br/>The extent to which chunks overlap, as a percentage of the chunks' height. For example, `0.5` specifies each chunk overlaps by half its height. <br/>Applies to each Sensible Instruct field in the config. <br/>Sensible recommends setting a non-zero overlap to avoid splitting data across chunks. Set overlap to 0 solely if you're confident that your document layout doesn't flow across page boundaries and you're using a one-page chunk size. | Overrides config-level parameter for a single field.         |


Notes
===
For an overview of how Sensible Instruct methods work, see the following steps. 

1. To meet the LLM's input token limit, Sensible splits the document into chunks.
2. Sensible selects the most relevant chunks and combines them with page-hinting data to create a "context".
3. Sensible creates a full prompt for the LLM that includes the context and the descriptive prompts you configure in the method. For an example of a full prompt, see the beginning of this topic.
4. Sensible returns the LLM's response.

For specifics about how each Sensible instruct method works, see the Notes section for each method's SenseML reference topic, for example, [List](doc:list#notes) method.

