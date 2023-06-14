---
title: "Advanced LLM prompt configuration"
hidden: true
---

You can configure the prompt that Sensible provides to a large-language model (LLM) to fine tune your results. You can configure some aspects of the prompt, such as the context description, for all fields in a config, and for others, you can configure them at the field level. Some you can configure at the config level, then override for individual fields

See the following image for an example of configuring a field that uses the [Query](doc:question) method. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/llm_prompt.png)

page hinting: yeah strips it out.



| key  | configurable at config level?             | configurable at field level?                                 | parameter name                                               |      |
| ---- | ----------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| A    | NLP preprocessor (config level) TODO link |                                                              | queryPrompt -- and other Prompt intro-related methods -- queryIntro |      |
| B    | NLP preprocessor (config level)           |                                                              | contextDescription                                           |      |
| C    | NLP preprocessor (config level)           |                                                              | pageHinting                                                  |      |
| D    |                                           | field's method.  For this example, [Question](doc:question) method | chunkScoringText<br/>chunkCount<br/>chunkSize<br/>chunkoverlapPercentage |      |
| E    |                                           | field's method                                               | description                                                  |      |

