---
title: "LLM models"
hidden: true
---



You can configure which LLMs Sensible uses to answer your prompts. The following tables list your configuration options.

**Note** 

Note there are several non-configurable LLM processes as well. For example, there's no option for configuring the LLMs that Sensible uses for locating context TODO or for classifying documents by type TODO. 

### List method

| configuration                 | configuration       | LLM model used for finding answer in context | Comments |
| ----------------------------- | ------------------- | -------------------------------------------- | -------- |
| LLM Engine<br/> mode: fast    | provider: anthropic | Claude 3.5 Haiku                             |          |
|                               | provider: openapi   | GPT-4o mini                                  |          |
| LLM Engine<br/>mode: thorough | provider: anthropic | Claude 3.5 Sonnet                            |          |
|                               | provider: openapi   | GPT-4o                                       |          |
| LLM Engine<br/>  mode: long   | provider: anthropic | Claude 3.5 Haiku                             |          |
|                               | provider: openapi   | GPT-4o mini                                  |          |

### Query Group method

| configuration                      | configuration                           | LLM model used for finding answer in context |
| ---------------------------------- | --------------------------------------- | -------------------------------------------- |
| LLM Engine<br/>provider: anthropic |                                         | Claude 3 Haiku                               |
| LLM Engine<br/> provider openapi   |                                         | GPT 4.0 mini                                 |
| Multimodal Engine: true            | LLM Engine<br/>provider: <br/>anthropic | Claude 3.5 Haiku                             |
|                                    | LLM Engine<br/>provider:<br/> openapi   | GPT-4o mini                                  |

### NLP Table method

| configuration                      | LLM model used for finding answer in context |
| ---------------------------------- | -------------------------------------------- |
| LLM Engine<br/>provider: anthropic | Claude 3 Haiku                               |
| LLM Engine<br/> provider openapi   | GPT-4o                                       |

