---
title: "Advanced LLM prompt configuration"
hidden: true
---

You can configure the prompt that Sensible inputs to a large-language model (LLM) for a single field or for all fields in a config.

Sensible inputs a prompt to a large-language model (LLM) by combining:

- a prompt introduction
- "context", or formatted text chunks excerpted from the document and information about their page locations. For more information about chunks, see the notes section for each Sensible Instruct method, for example, the [Notes](doc:nlp-table#notes) section for the NLP Table method.
- the descriptive prompts you configure in a Sensible Instruct method, such as the [List](doc:list) or [Query](doc:question) methods

See the following image for an example of a full prompt that Sensible inputs to an LLM for the [Query](doc:question) method: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/prompt.png)

