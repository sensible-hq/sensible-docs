---
title: "NLP"
hidden: true
---

TODO ON PUBLISH: do I want to link to the NLP preprocessor from the Question method -> SenseML only --> and other ref topics for instruct? from notes section?

Parameters
====

| key            | value                                                        | description                                                  |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
|                |                                                              |                                                              |
|                |                                                              |                                                              |
| pageHinting    | boolean. default: true                                       | Includes or or removes page metadata for each chunk from the [full prompt](doc:prompt) Sensible inputs to an LLM.  For example, removes phrases like ``The excerpt starts at the top of page 1 and ends at the bottom of page 1.`` <br/>If you set this parameter to `false` and specify page information in a method's prompts, the LLM ignores that information. For example, if you specify `What is the medical paid value on the last claim of the first page?`  in the Question method, the LLM ignores `of the first page`.<br/>TO QUESTION: TRUE? |
| queryPrompt    | QUESTION: I assume "\n\nContext:\n\n isn't configurable for all of these, so left it out...<br/>string. default: `Answer the question as truthfully and concisely as possible using the provided context, and if the answer is not contained within the text below, say \"I don't know.\"'` | Overwrites the default text at the beginning of the prompt that Sensible submits to the LLM for the Question method.<br/> For example:  `Answer the question as truthfully and concisely as possible using the provided context, and if the answer is not contained within the text below, say \"UNKNOWN\".",`<br/>**Note** Sensible returns null if the phrase `I don't know` is in the returned field value. If you alter this key phrase using this parameter, for example by asking the LLM to return a phrase like `UNKNOWN` , then Sensible returns a phrase like `UNKNWON` instead of null. |
| listPrompt     | string. default: `Using the provided context fill out the table below. If the context doesn't contain any of the described items, leave it empty.` | Overwrites the default text at the beginning of the prompt that Sensible submits to the LLM for the List method.<br/>For example:<br/>`Using the provided context fill out the table below. If the context doesn't contain any of the described items, return \"NONE FOUND\ in each cell"` |
| nlpTablePrompt | string. default: `Below is a sample table. Please transform the data from the sample table into the target table where the target table's column headers are provided. Please do not modify the target table's headers. If cells in the sample table don't contain data, leave the corresponding cell of the new table blank. Finally return the transformed table without the header and header seperator line.` | Overwrites the default text at the beginning of the prompt that Sensible submits to the LLM for the NLP Table method. <br/> For example, overwrite with:`"Below is a sample table. Please transform the data from the sample table into the target table where the target table's column headers are provided. Please do not modify the target table's headers. If the cells in the sample table don't contain data, populate the cell with \"NOT FOUND\". Finally return the transformed table without the header and header seperator line."` |



