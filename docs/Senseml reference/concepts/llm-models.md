---
title: LLM models
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Available LLM models'
  robots: index
next:
  description: ''
---
You can configure which LLM models Sensible uses to find answers in [context](doc:prompt) for LLM-based methods. The following tables list your configuration options.

### List method

| configuration                                | LLM Engine parameter:<br/>provider: **openai** | LLM Engine parameter:<br/>provider: **anthropic** | LLM Engine parameter:<br/>provider: **google** |
| -------------------------------------------- | ---------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- |
| LLM Engine parameter:<br/> mode: **fast**    | GPT-4o mini                                    | Claude 4.5 Haiku                                  | Gemini 2.5 Flash-Lite                          |
| LLM Engine parameter:<br/>mode: **thorough** | GPT-4o                                         | Claude 4.5 Sonnet                                 | Gemini 2.5 Flash-Lite                          |
| LLM Engine parameter:<br/>  mode: **long**   | GPT-4o mini                                    | Claude 4.5 Haiku                                  | Gemini 2.5 Flash-Lite                          |



### Query Group method

| configuration                         | LLM Engine parameter:<br/> provider: **openai** | LLM Engine parameter:<br/>provider: **anthropic** | LLM Engine parameter:<br/>provider: **google** |
| ------------------------------------- | ----------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- |
| default                               | GPT-4o mini                                     | Claude 4.5 Haiku                                  | Gemini 2.5 Flash-Lite                          |
| Multimodal Engine parameter: **true** | GPT-4o mini                                     | Claude 4.5 Haiku                                  | Gemini 2.5 Flash-Lite                          |
| Source Ids parameter is specified     | GPT-4o mini                                     | Claude 4.5 Sonnet                                 | Gemini 2.5 Flash                               |

### Confidence Signals parameter

| configuration | Confidence Signals parameter:<br/>engine: **open-ai** | Confidence Signals parameter:<br/>engine: **anthropic** | Confidence Signals parameter:<br/>engine: **google** |
| ------------- | ----------------------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------- |
| default       | GPT-4o (fine-tuned)                                   | Claude 4.5 Haiku                                        | Gemini 2.5 Flash-Lite                                |

### NLP Table method

| configuration | LLM Engine parameter:<br/> provider: **openai** | LLM Engine parameter:<br/>provider: **anthropic** | LLM Engine parameter:<br/>provider: **google** |
| ------------- | ----------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- |
| default       | GPT-4o                                          | Claude 4.5 Haiku                                  | Gemini 2.5 Flash-Lite                          |
