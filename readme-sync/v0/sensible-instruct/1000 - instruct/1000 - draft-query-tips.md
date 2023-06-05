---
title: "Query extraction tips"
hidden: true

---



**Troubleshooting**

Sensible returns the following error messages when the LLM is uncertain about the accuracy of the extracted data. Note that LLMs can inaccurately report uncertainties. For more information, see [Accuracy measures](doc:accuracy-measures).

| error message                              | description                                                  | troubleshooting                                              |
| ------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Multiple possible answers                  | The context that Sensible provides to the LLM has multiple possible answers. | -  To return multiple answers, use the [List method](doc:list-tips).<br/>- To return a single answer, tweak the context that Sensible provides to the LLM using  [chunk parameters](doc:question#parameters) so that the context contains a single answer. |
| Answer might not fully answer the question | The context that Sensible provides to the LLM might not have the full answer. | - Tweak the context that Sensible provides to the LLM using  [chunk parameters](doc:question#parameters).<br/> - Simplify your question, for example, break it up into multiple questions. |
| Answer not found in the context            | The context that Sensible provides to the LLM doesn't contain the answer. | - Tweak the context that Sensible provides to the LLM using  [chunk parameters](doc:question#parameters).<br/> |
| Ambiguous query                            | The LLM identified ambiguities in your question.             | Rephrase your question using the tips in the tips section.   |

​    

