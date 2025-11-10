---
title: "LLM models"
hidden: true
---



You can configure which LLM models Sensible uses to find answers in context for LLM-based methods. The following tables list your configuration options.

### List method TODO link to parameters table

| configuration                 | configuration       | LLM model         | Comments |
| ----------------------------- | ------------------- | ----------------- | -------- |
| LLM Engine<br/> mode: fast    | provider: anthropic | Claude 3.5 Haiku  |          |
|                               | provider: openapi   | GPT-4o mini       |          |
| LLM Engine<br/>mode: thorough | provider: anthropic | Claude 3.5 Sonnet |          |
|                               | provider: openapi   | GPT-4o            |          |
| LLM Engine<br/>  mode: long   | provider: anthropic | Claude 3.5 Haiku  |          |
|                               | provider: openapi   | GPT-4o mini       |          |

### Query Group method

| configuration                      | configuration                           | LLM model        |
| ---------------------------------- | --------------------------------------- | ---------------- |
| LLM Engine<br/>provider: anthropic |                                         | Claude 3.7 Haiku |
| LLM Engine<br/> provider openapi   |                                         | GPT 4.0 mini     |
| Multimodal Engine: true            | LLM Engine<br/>provider: <br/>anthropic | Claude 3.5 Haiku |
|                                    | LLM Engine<br/>provider:<br/> openapi   | GPT-4o mini      |

### NLP Table method

| configuration                      | LLM model      |
| ---------------------------------- | -------------- |
| LLM Engine<br/>provider: anthropic | Claude 3 Haiku |
| LLM Engine<br/> provider openapi   | GPT-4o         |

