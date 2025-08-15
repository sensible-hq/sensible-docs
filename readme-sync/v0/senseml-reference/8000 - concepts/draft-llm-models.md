---
title: "LLM models"
hidden: true
---

| Feature                                                      | parameter configuration                                      | LLM model                  | Comments                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------- | ------------------------------------------------------------ |
| List method                                                  | mode: fast, provider: anthropic                              | Claude 3.5 Haiku           |                                                              |
| List method                                                  | mode: fast, provider: openai                                 | GPT-4o mini                |                                                              |
| List method                                                  | mode: thorough, provider: anthropic                          | Claude 3.5 Sonnet          |                                                              |
| List method                                                  | mode: thorough, provider: openai                             | GPT-4o                     |                                                              |
| List method                                                  | mode: long, provider: anthropic                              | Claude 3.5 Haiku           |                                                              |
| List method                                                  | mode: long, provider: openai                                 | GPT-4o mini                |                                                              |
| List method                                                  | searchBySummarization: page or outline<br/>and<br/>confidence signal: true |                            | Note that the LLM Engine parameter doesn't configure the LLMs Sensible uses for summarizing and locating context or for generating confidence signals when you set these parameters, respectively. TODO: list the models we use here...?? ALSO note that |
| Query Group method                                           | provider: open-ai                                            | GPT-4o mini                |                                                              |
| Query Group method                                           |                                                              | Anthropic's Claude 3 Haiku |                                                              |
| Query Group method                                           | searchBySummarization: page or outline<br/>and<br/>confidence signal: true |                            | same notes as for List method                                |
| NLP Table                                                    | provider: open-ai                                            | GPT-4o                     |                                                              |
| NLP Table                                                    | provider: anthropic                                          | Claude 3 Haiku             |                                                              |
| NLP Table                                                    | rewriteTable: false                                          | GPT-4                      | overrides provider parameter                                 |
|                                                              |                                                              |                            |                                                              |
| Classify single-document file by type                        |                                                              |                            |                                                              |
| Classify documents by type in a portfolio (multi-document file) |                                                              |                            |                                                              |
| any other LLM use I forgot? Embeddings AI for chunk scoring? (could be footnote) |                                                              |                            |                                                              |

