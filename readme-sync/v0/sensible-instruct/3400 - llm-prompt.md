---
title: "Advanced LLM prompt configuration"
hidden: true
---

TODO: link to this new topic from the troubleshooting Query table, from the "how it works" in the question method, and from ... the NLP preprocessor?



You can configure the prompt that Sensible inputs to a large-language model (LLM) for a single field or for all fields in a config.

Sensible inputs a prompt to a large-language model (LLM) by combining:

- a prompt introduction
- the descriptive prompts you configure in a method such as the [List](doc:list) or [Query](doc:question) methods.
- the excerpts, or "context", extracted from the document. 

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query](doc:question) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/llm_prompt.png)





| key  | description                                                  | configurable for all fields in config? | configurable for one field?                        | parameter                                                    |
| ---- | ------------------------------------------------------------ | -------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| A    | prompt introduction. For example, ask for truthfulness or describe the shape of the data to extract, for example, query, table, or table | yes:<br/>[NLP preprocessor](doc:nlp).  |                                                    | queryPrompt  (and other Prompt intro-related methods -- queryIntro) TODO how to reword? |
| B    | overall description of the chunks                            | yes:<br/>[NLP preprocessor](doc:nlp).  |                                                    | contextDescription                                           |
| C    | page metadata                                                | yes:<br/>[NLP preprocessor](doc:nlp).  |                                                    | pageHinting                                                  |
| D    | chunk excerpted from document                                |                                        | yes:<br/>[Query method](doc:question)              | chunkScoringText<br/>chunkCount<br/>chunkSize<br/>chunkoverlapPercentage |
| E    | concatenation of all the descriptive prompts configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:nlp-table) method. |                                        | yes:<br/>[Sensible Instruct methods](doc:instruct) | description                                                  |

