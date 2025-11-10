---
title: "LLM models"
hidden: false
---



You can configure which LLM models Sensible uses to find answers in [context](doc:prompt) for LLM-based methods. The following tables list your configuration options.

### List method

| configuration                      | LLM Engine:<br/>provider: **openai** | LLM Engine:<br/>provider: **anthropic** |
| ---------------------------------- | ------------------------------------ | --------------------------------------- |
| LLM Engine:<br/> mode: **fast**    | GPT-4o mini                          | Claude 3.5 Haiku                        |
| LLM Engine:<br/>mode: **thorough** | GPT-4o                               | Claude 3.7 Sonnet                       |
| LLM Engine:<br/>  mode: **long**   | GPT-4o mini                          | Claude 3.5 Haiku                        |

### Query Group method

| configuration                     | LLM Engine:<br/> provider: **openai** | LLM Engine:<br/>provider: **anthropic** |
| --------------------------------- | ------------------------------------- | --------------------------------------- |
|                                   | GPT-4o mini                           | Claude 3 Haiku                          |
| Multimodal Engine: **true**       | GPT-4o mini                           | Claude 3 Haiku                          |
| Source Ids parameter is specified | GPT-4o mini                           | Claude 3.7 Sonnet                       |

### NLP Table method

| configuration                          | LLM model      |
| -------------------------------------- | -------------- |
| LLM Engine:<br/> provider: **openai** | GPT-4o         |
| LLM Engine<br/>provider: **anthropic** | Claude 3 Haiku |

