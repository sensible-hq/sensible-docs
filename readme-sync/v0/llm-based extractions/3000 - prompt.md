---
title: "Advanced prompt configuration"
hidden: false
---


You can configure the full prompt that Sensible inputs to a large language model (LLM). You can apply configurations to multiple fields in a config, and you can override them for individual fields.

When you write a prompt in a Sensible Instruct method, Sensible combines your prompt with other information to create the full prompt. The full prompt includes:

- a prompt introduction
- "context", made up of chunks excerpted from the document and of page metadata. For more information about chunks, see the Notes section.
- concatenated descriptive prompts you configure in a Sensible Instruct method, such as in the [List](doc:list-tips) or [Query Group](doc:query-group-tips) methods.

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query Group](doc:query-group-tips) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt.png)

The following table shows parameters that configure parts of the full prompt and that are global, or common to all Sensible Instruct methods:

| key  | description                                                  | global parameter name                                        |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| A    | Overall description of the chunks.<br/>The preceding image shows an example of a user-configured context description overriding the default. | Context Description                                          |
| B    | Page metadata for chunks.                                    | Page Hinting                                                 |
| C    | Chunks, or "context", excerpted from document.               | Chunk Count<br/>Chunk Size<br/>Chunk Overlap Percentage<br/>Page Range |
| D    | Concatenation of all the descriptive prompts you configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:table-tips) method. | Description                                                  |

You can configure all of these parameters in the SenseML editor and in the Sensible Instruct editor. For example, the following screenshots show prompt settings in Sensible Instruct for a Query Group field: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt_instruct_1.png)

The following screenshot shows prompt settings in Sensible Instruct for all fields in a config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt_instruct_2.png)



Global Sensible Instruct parameters
===

The following table shows global parameters, or parameters that are common to all Sensible Instruct methods. You can configure these parameters for all fields in a config, or on a field-by-field basis.

For parameters specific to a Sensible instruct method, see its reference topic, for example, the [Query Group](doc:query-group#parameters) method reference topic. Like global parameters, method-specific parameters can be set for all fields in a config, or on a field-by-field basis.


| SenseML parameter                   | value                                                        | config-level description:<br/>configure in [NLP preprocessor](doc:nlp) or in Sensible Instruct configuration settings | method-level description:<br/>configure in a field   |
| :---------------------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| confidenceSignals                   | boolean.<br/>defaults: true in  Sensible Instruct editor,<br/> false in SenseML editor | If specified, Sensible prompts the LLM to report any uncertainties it has about the accuracy of its response.  For more information, see [Qualifying LLM accuracy](doc:confidence).<br/>Applies to each supported method in the config. Sensible currently supports this parameter for the [Query Group](doc:query-group) method. | Overrides config-level parameter for a single field. |
| contextDescription                  | string. default: `The below context is an excerpt from a document.` | Configures context's metadata. For details about context and chunks, see the Notes section.<br/>Overwrites the default context description.<br/>Applies to each Sensible Instruct field in the config.<br/>For example:<br/>\- `The below context is an excerpt from a scanned index card that contains botanical information about a single plant species, including phenology information.`<br/>\- `The below context is an excerpt from an email. Assume the sender is always an automated system from an insurance broker.` | Overrides config-level parameter for a single field. |
| pageHinting                         | boolean. default: true                                       | Configures context's metadata. For details about context and chunks, see the Notes section. <br/>Includes or or removes page metadata for each chunk from the prompt Sensible inputs to an LLM.<br/>For example, if your PDF converter automatically applied page numbers to scanned ID cards, set this parameter to false to ignore the page numbers, since their relationship to the cards' text is arbitrary.<br/>Applies to each Sensible Instruct field in the config.<br/>For example, removes phrases like `The excerpt starts at the top of page 1 and ends at the bottom of page 1.` | Overrides config-level parameter for a single field. |
| chunkCount                          | number. default: see each method's [reference topic](doc:Query Group method-methods) | Configures context's size. For details about context and chunks, see the Notes section.<br/>The number of top-scoring chunks Sensible combines as context as part of the full prompt it submits to an LLM. <br/>Applies to each Sensible Instruct field in the config.<br/>Often, chunk count and chunk size are related. For example, if you know that your target data are spread over 7-10 pages, and occupy a small portion of those pages, you can specify a chunk count of 10 and a half-page  chunk size. | Overrides config-level parameter for a single field. |
| chunkSize                           | `0.5`, `1` default:  see each method's [reference topic](doc:llm-based-methods) | Configures context's size. For details about context and chunks, see the Notes section.<br/>The size of the chunks Sensible splits the document into, as a page fraction. For example, `0.5` specifies each chunk is half a page.<br/>Applies to each Sensible Instruct field in the config. <br/>Often, chunk count and chunk size are related. For example, if you know that the data you seek is contained in one cover page, you can set chunk size to 1 and a chunk count to 1. | Overrides config-level parameter for a single field. |
| chunkOverlapPercentage              | `0`, `0.25`, `0.5` default: see each method's [reference topic](doc:llm-based-methods) | Configures context's size. For details about context and chunks, see the Notes section.<br/>The extent to which chunks overlap, as a percentage of the chunks' height. For example, `0.5` specifies each chunk overlaps by half its height. <br/>Applies to each Sensible Instruct field in the config. <br/>Sensible recommends setting a non-zero overlap to avoid splitting data across chunks. Set overlap to 0 solely if you're confident that your document layout doesn't flow across page boundaries and you're using a one-page chunk size. | Overrides config-level parameter for a single field. |
| pageRange                           | object                                                       | Configures the context's range in the document. For details about context and chunks, see the Notes section.<br/>If specified, Sensible creates chunks in the page range and ignores other pages. For example, use this parameter to improve performance, or to avoid extracting unwanted data if your prompt has multiple candidate answers.<br/><br/>Contains the following parameters: <br/>`startPage`:  Zero-based index of the page at which Sensible starts creating chunks (inclusive). <br/>`endPage`: Zero-based index of the page at which Sensible stops creating chunks (exclusive).<br/><br/>**Note:** Sensible ignores this parameter when searching for a field's anchor. If you want to exclude the field's anchor from the page range, use the [Page Range](doc:page-range) preprocessor instead.<br/> | Overrides config-level parameter for a single field. |
| (**Deprecated**) promptIntroduction | string                                                       | Deprecated. Overwrites the introductory text at the beginning of the full prompt that Sensible submits to the LLM. |                                                      |


Notes
===
For an overview of how Sensible Instruct methods work, see the following steps. 

1. To meet the LLM's input token limit, Sensible splits the document into chunks.
2. Sensible selects the most relevant chunks and combines them with page-hinting data to create a "context".
3. Sensible creates a full prompt for the LLM that includes the context and the descriptive prompts you configure in the method. For an example of a full prompt, see the beginning of this topic.
4. Sensible returns the LLM's response.

For specifics about how each Sensible instruct method works, see the Notes section for each method's SenseML reference topic, for example, [List](doc:list#notes) method.

