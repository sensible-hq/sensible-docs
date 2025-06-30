---
title: "NLP"
hidden: true
---



LEFT OFF:  https://sensiblehq.slack.com/archives/C0215T9K86P/p1750789433364139 



Configures the full prompt for all [LLM-based](doc:llm-based-methods) methods in a config. For information about configuring the full prompt, see [Advanced LLM prompt configuration](doc:prompt#full-prompt).

[**Parameters**](doc:nlp#parameters)
[**Examples**](doc:nlp#examples)
[**Notes**](doc:nlp#notes)

Parameters
====

The following parameters are available both on the config level and for each individual field through the method's parameters. Setting a parameter at the method level overrides it at the config level.

| key                    | value  | description                                                  |
| ---------------------- | ------ | ------------------------------------------------------------ |
| type (**required**)    | `nlp`  |                                                              |
| nlpTable               | object | Parameters:<br/>- `rewriteTable`<br/>- `pageSpanThreshold`<br/>- `detectTableStructureOnly`<br/>-`annotateSuperscriptAndSubscript`<br/>- (**Deprecated**) `promptIntroduction`<br/>For information about these parameters, see [NLP Table](doc:nlp-table#parameters). |
| list                   | object | Parameters:<br/>- `llmEngine`<br/>For information about these parameters, see [List](doc:list#parameters). |
| (**Deprecated**) query | object | For information about this deprecated parameter see [Query](doc:deprecated-query). |
| pageRange              |        | For information about this parameter, see the reference topic for each LLM-based method. |

