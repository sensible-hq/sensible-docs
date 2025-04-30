---
title: "Qualifying LLM accuracy"
hidden: true
---

For data extracted by large language models (LLMs), Sensible asks the LLMs to report any uncertainties about the accuracy of the extracted data. For example, an LLM can report "multiple possible answers" or "ambiguous query".  These confidence *signals* offer more nuanced troubleshooting than numeric confidence *scores*.

Note that LLMs can inaccurately report confidence signals.  For more information about confidence signals, see the research paper [Teaching models to express their uncertainties in words](https://arxiv.org/pdf/2205.14334.pdf). 

Sensible support confidence signals for the Query Group method.

For more information about troubleshooting confidence signals, see the following table.

Query Group method confidence signals
---

For the Query Group method, Sensible returns the following messages, or "confidence signals",  to qualify the LLM's confidence in the accuracy of the extracted data.

| confidence signal                        | JSON output                 | description                                                  | troubleshooting                                              |
| ---------------------------------------- | --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Multiple possible answers                | `multiple_possible_answers` | The LLM answers the prompt, but identifies multiple possible answers in the context that Sensible provides to the LLM. | -  To return multiple answers, use the [List method](doc:list).<br/>- To return a single answer, ensure the context contains a single answer. |
| Answer might not fully answer the prompt | `answer_may_be_incomplete`  | The LLM answers the prompt, but is uncertain whether the context that Sensible provides to the LLM contains the full answer. | Simplify your prompt, for example, break it up into multiple prompts and chain the prompts together with the Source IDs parameter. |
| Answer not found in the context          | `answer_not_found`          | The LLM fails to answer the prompt, and can't find an answer to your prompt in the context that Sensible provides to the LLM. | For configuration options for locating the correct context, see TODO LINK LLM Context. |
| Ambiguous query                          | `ambiguous_query`           | The LLM either answers or fails to answer your prompt, and identifies ambiguities in your prompt. | Rephrase your prompt using the tips for each LLM-based method. For example, see [Query Group](doc:query-group) tips. |
| Incorrect answer                         | `incorrect_answer`          | The LLM judges the answer is incorrect given the context that Sensible provides to the LLM. |                                                              |
| Confident answer                         | `confident_answer`          | The LLM is confident about its answer to the prompt.         |                                                              |
| Not supported                            | `not_supported`             | Sensible doesn't support confidence signals for multimodal LLM prompts. It returns this message if you set the Multimodal Engine parameter to true. |                                                              |
| Unknown signal                           | `unknown_signal`            | The LLM returns a confidence signal other than the confidence signals Sensible prompts it to return. |                                                              |

 

