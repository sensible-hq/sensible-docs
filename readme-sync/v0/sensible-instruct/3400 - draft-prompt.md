---
title: "Advanced prompt configuration"
hidden: true
---

TODO ON PUBLISH: link to this new topic from the troubleshooting Query table, from the "how it works" in the question method, and from the NLP preprocessor(?)



You can configure the prompt that Sensible inputs to a large-language model (LLM) for a single field or for all fields in a config.

Sensible inputs a prompt to a large-language model (LLM) by combining:

- a prompt introduction
- "context", made up of chunks excerpted from the document and of page metadata. For more information about chunks, see the notes section for each Sensible Instruct method, for example, the [Notes](doc:nlp-table#notes) section for the NLP Table method.
- the descriptive prompts you configure in a Sensible Instruct method, such as the [List](doc:list) or [Query](doc:question) methods

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query](doc:question) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/llm_prompt.png)





| key  | description                                                  | configurable for all fields in config? | overridable for each field?                                  | parameter                                                    |
| ---- | ------------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| A    | prompt introduction. Includes asking for truthfulness and describing the format of the data to extract, for example, query, table, or table. | yes:<br/>[NLP preprocessor](doc:nlp)   | yes:<br/>[Sensible Instruct methods](doc:instruct)           | Prompt Introduction                                          |
| B    | overall description of the chunks, or "context"              | yes:<br/>[NLP preprocessor](doc:nlp)   | yes:<br/>[Sensible Instruct methods](doc:instruct)           | Context Description                                          |
| C    | page metadata for chunks                                     | yes:<br/>[NLP preprocessor](doc:nlp)   | yes:<br/>[Sensible Instruct methods](doc:instruct)           | Page Hinting                                                 |
| D    | chunks excerpted from document                               | yes                                    | yes:<br/>all [Sensible Instruct methods](doc:instruct) except that only the Query method has Chunk Scoring Text (TODO word better!) | Chunk Scoring Text (Query method only TODO WORD BETTER)<br/>Chunk Count<br/>Chunk Size<br/>Chunk Overlap Percentage |
| E    | concatenation of all the descriptive prompts configured in the method. For example, concatenation of all the column descriptions and the overall table description for the [NLP Table](doc:nlp-table) method. |                                        | yes:<br/>[Sensible Instruct methods](doc:instruct)           | Description                                                  |
