---
title: "LLM models"
hidden: false
---



You can configure which LLM models Sensible uses to find answers in [context](doc:prompt) for LLM-based methods. The following tables list your configuration options.

### List method TODO link to parameters table

| configuration                      | configuration                           | LLM model         |
| ---------------------------------- | --------------------------------------- | ----------------- |
| LLM Engine:<br/> mode: **fast**    | LLM Engine:<br/>provider: **openai**   | GPT-4o mini       |
|                                    | LLM Engine:<br/>provider: **anthropic** | Claude 3.5 Haiku  |
| LLM Engine:<br/>mode: **thorough** | LLM Engine:<br/>provider: **openai**   | GPT-4o            |
|                                    | LLM Engine:<br/>provider: **anthropic** | Claude 3.7 Sonnet |
| LLM Engine:<br/>  mode: **long**   | LLM Engine:<br/>provider: **openai**   | GPT-4o mini       |
|                                    | LLM Engine:<br/>provider: **anthropic** | Claude 3.5 Haiku  |

### Query Group method

| configuration                           | configuration                           | LLM model         |
| --------------------------------------- | --------------------------------------- | ----------------- |
| LLM Engine:<br/> provider: **openai**  |                                         | GPT-4o mini       |
| LLM Engine:<br/>provider: **anthropic** |                                         | Claude 3.7 Sonnet |
| Multimodal Engine: **true**             | LLM Engine:<br/>provider: **openai**   | GPT-4o mini       |
|                                         | LLM Engine:<br/>provider: **anthropic** | Claude 3 Haiku    |

### NLP Table method

| configuration                          | LLM model      |
| -------------------------------------- | -------------- |
| LLM Engine:<br/> provider: **openai** | GPT-4o         |
| LLM Engine<br/>provider: **anthropic** | Claude 3 Haiku |

