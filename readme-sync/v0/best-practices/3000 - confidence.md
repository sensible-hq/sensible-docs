---
title: "Qualifying LLM accuracy"
hidden: false
---

For data extracted by large language models (LLMs), Sensible asks the LLMs to report any uncertainties about the accuracy of the extracted data. For example, an LLM can report "multiple possible answers" or "ambiguous query".  These confidence *signals* offer more nuanced troubleshooting than confidence *scores*.

Note that LLMs can inaccurately report confidence signals.  For more information about confidence signals, see the research paper [Teaching models to express their uncertainties in words](https://arxiv.org/pdf/2205.14334.pdf). 

Sensible support confidence signals for the Query Group method. The **confidence signals** checkbox is enabled by default in the Sensible Instruct editor for new Query Group fields. To enable confidence signals for a field in SenseML, use the Query Group method's Confidence Signals parameter.

For more information about troubleshooting confidence signals, see the following table.

Query Group method confidence signals
---

For the Query Group method, Sensible returns the following messages, or "confidence signals",  to qualify the LLM's confidence in the accuracy of the extracted data.

| confidence signal                        | JSON output                 | description                                                  | troubleshooting                                              |
| ---------------------------------------- | --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Multiple possible answers                | `multiple_possible_answers` | The LLM answers the prompt, but identifies multiple possible answers in the context that Sensible provides to the LLM. | -  To return multiple answers, use the [List method](doc:list-tips).<br/>- To return a single answer, ensure the context contains a single answer. For more information, see [Advanced prompt configuration](doc:prompt). |
| Answer might not fully answer the prompt | `answer_may_be_incomplete`  | The LLM answers the prompt, but is uncertain whether the context that Sensible provides to the LLM contains the full answer. | - Simplify your prompt, for example, break it up into multiple prompts.<br/>- See [Advanced prompt configuration](doc:prompt). |
| Answer not found in the context          | `answer_not_found`          | The LLM fails to answer the prompt, and can't find an answer to your prompt in the context that Sensible provides to the LLM. | See [Advanced prompt configuration](doc:prompt).             |
| Ambiguous query                          | `ambiguous_query`           | The LLM either answers or fails to answer your prompt, and identifies ambiguities in your prompt. | - Rephrase your prompt using the tips for each Instruct method. For example, see [Query Group](doc:query-group-tips) tips.<br/>-  See [Advanced prompt configuration](doc:prompt). |
| Incorrect answer                         | `incorrect_answer`          | The LLM judges the answer is incorrect given the context that Sensible provides to the LLM. | See [Advanced prompt configuration](doc:prompt).             |
| Confident answer                         | `confident_answer`          | The LLM is confident about its answer to the prompt.         |                                                              |
| Unknown signal                           | `unknown_signal`            | The LLM returns a confidence signal other than the confidence signals Sensible instructs it to return. |                                                              |

 

