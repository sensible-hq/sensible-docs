---
title: "Handling document variations"
hidden: false
---

## Overview

When you extract data from a set of similar documents (a *document type*), you encounter variations in layout, formatting, and content. Your goal is often to extract data across all these variations and output them into a unified data schema. To achieve this goal, you can take the following steps:

1. You can author data-extraction fields using a variety of SenseML  [methods](doc:methods) and [computed methods](doc:computed-field-methods) to extract the same target data from differing sources.
2. You can conditionally execute the fields you author depending on the variations you encounter in the source documents.

This topic covers conditional execution. 

## Example

 Say you extract data from bank statements. The statements all convey the same basic information, but vary in large and small ways:

-  Each major bank has its own distinctive layout and formatting for its statements. Some combine checking and savings into one statement, and others separate them.
- Some affiliate banks have slightly different layouts but share many similarities.
- You have a long tail of small regional credit unions you want to extract from, where it would be an overwhelming task to qualify all the minor variations.

To create a unified output schema for these banks, you can conditionally execute data-extraction fields based on which bank issued the statement, whether a SenseML field returns null, and other factors.

In order of granularity, here are the options for conditionally executing SenseML: 

## Handling document variations

| option                | granularity                  | how it works                                                 | example use case                                             | full example                                                 |
| --------------------- | ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| configs               | config                       | Sensible determines the best-fitting config for a document, based either on:<br/>- Sensible's default scoring<br/> or<br/>- configurable "[fingerprints](doc:fingerprint)" (characteristic text in the document) | In a `bank_statements` document type, you extract bank statements from Chase, Wells Fargo, Bank of America, and a long tail of small regional banks.<br/>1. For each major bank, you author a *config* (a collection of data-extraction fields). The `wells_fargo_config` extracts data if the document contains the text "Wells Fargo"; the `boa_config` extracts data if the document contains the text "Bank of America", and so on.<br/>2. For the long-tail regional banks, you author a fallback, generalized, [LLM-based](doc:llm-based-methods) config that runs if the names of the major banks are absent in the document. | Import Sensible out-of-the-box support for common [forms](doc:library-quickstart) and browse the configs in each document type in the Sensible app |
| conditional execution | subset of fields in a config | Based on a pass/fail logical [condition](doc:conditional), Sensible executes alternate subsets of fields in a config. | You want to extract data from two affiliate banks' statements. The statements' layouts are so similar that you can reuse 90 percent of your SenseML fields to handle both. Rather than authoring two separate configs, you can handle the remaining 10 percent with conditional field execution. | [Conditional execution](doc:conditional-execution)           |
| fallback fields       | single field                 | If a field fails to extract data, Sensible falls back to another identically named field in a config. The fallback field uses an alternate extraction method. TODO LINK to field-query-object | You want to extract a `total_amount` field which appears in a table in document revision A and in a free-text paragraph in document revision B. You define two fields in one config with the same ID (`total_amount`), which use the Row method and the Query Group method, respectively. | [Fallback fields](doc:fallbacks#fallback-fields)             |

