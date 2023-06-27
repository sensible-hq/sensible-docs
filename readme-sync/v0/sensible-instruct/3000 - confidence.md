---
title: "Confidence signals"
hidden: true
---

TODO: describe how to turn these on for prompt engineering phase, then turn off if you want ot edit promptIntro in prod? Or just always keep them on?

For data extracted by large-language models (LLMs), Sensible asks the LLM to report any uncertainties it has about the accuracy of the extracted data. For example, an LLM can report "multiple possible answers" or "ambiguous query".  These confidence *signals* are more useful for troubleshooting than confidence *scores*. This is because confidence scores tend to be oversimple: they fall into buckets of 0% or 100% accuracy.

Note that LLMs can inaccurately report confidence signals.  For more information about confidence signals, see the research paper [Teaching models to express their uncertainties in words](https://arxiv.org/pdf/2205.14334.pdf). 

Sensible support confidence signals for the [Query](doc:query-tips) method. For more information about troubleshooting confidence signals, see the following table.

Query method confidence signals
---

For the Query method, Sensible returns the following error messages, or "confidence signals", when the LLM is uncertain about the accuracy of the extracted data.

| confidence signal                        | json response               | description                                                  | troubleshooting                                              |
| ---------------------------------------- | --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Multiple possible answers                | `multiple_possible_answers` | The LLM answers the prompt, but identifies multiple possible answers in the context that Sensible provides to the LLM. | -  To return multiple answers, use the [List method](doc:list-tips).<br/>- To return a single answer, ensure the context contains a single answer. For more information, see [Advanced prompt configuration](doc:prompt). |
| Answer might not fully answer the prompt | TODO FIGURE THESE OUT       | The LLM answers the prompt, but is uncertain whether the context that Sensible provides to the LLM contains the full answer. | - Simplify your prompt, for example, break it up into multiple prompts.<br/>- See [Advanced prompt configuration](doc:prompt). |
| Answer not found in the context          |                             | The LLM fails to answer the prompt, and can't find an answer to your prompt in the context that Sensible provides to the LLM. | - See [Advanced prompt configuration](doc:prompt).           |
| Ambiguous query                          |                             | The LLM either answers or fails to answer your prompt, and identifies ambiguities in your prompt. | - Rephrase your prompt using the tips in the Tips section.<br/>-  See [Advanced prompt configuration](doc:prompt). |

 

