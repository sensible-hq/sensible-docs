---
title: "Advanced LLM prompt configuration"
hidden: true
---

TODO ON PUBLISH: link to this new topic from the troubleshooting Query table, from the "how it works" in the question method, and from the NLP preprocessor(?)



You can configure the prompt that Sensible inputs to a large-language model (LLM) for a single field or for all fields in a config.

Sensible inputs a prompt to a large-language model (LLM) by combining:

- a prompt introduction
- "context", or chunks excerpted from the document. For more information about chunks, see the notes section for each Sensible Instruct method, for example, the [Notes](doc:nlp-table#notes) section for the NLP Table method.
- the descriptive prompts you configure in a Sensible Instruct method, such as the [List](doc:list) or [Query](doc:question) methods

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query](doc:question) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/llm_prompt.png)





| key  | description                                                  | configurable for all fields in config? | configurable for each field?                       | parameter                                                    |
| ---- | ------------------------------------------------------------ | -------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| A    | prompt introduction. For example, ask for truthfulness or describe the shape of the data to extract, for example, query, table, or table | yes:<br/>[NLP preprocessor](doc:nlp)   |                                                    | Query Prompt  (and other Prompt intro-related methods -- queryIntro) TODO how to reword? |
| B    | overall description of the chunks, or "context"              | yes:<br/>[NLP preprocessor](doc:nlp)   |                                                    | Context Description                                          |
| C    | page metadata for chunk                                      | yes:<br/>[NLP preprocessor](doc:nlp)   |                                                    | Page Hinting                                                 |
| D    | chunk excerpted from document                                |                                        | yes:<br/>[Query method](doc:question)              | Chunk Scoring Text<br/>Chunk Count<br/>Chunk Size<br/>Chunk Overlap Percentage |
| E    | concatenation of all the descriptive prompts configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:nlp-table) method. |                                        | yes:<br/>[Sensible Instruct methods](doc:instruct) | Description                                                  |

