---
title: November 2024
slug: november-2024
date: 2024-10-19
---

In the last month Sensible added support for extracting and classifying CSV files, made improvements to the LLM-based List method, added advanced support for extended JsonLogic operations, and added several advanced configuration options.

## New feature: Support for CSV documents

Sensible now supports data extraction and [classification](doc:classify)  for comma-separated value (CSV) documents. For more information, see [Supported file types](doc:file-types).

## Improvement: Troubleshoot duplicate or missing List contents

With the new Single LLM Completion parameter, you can troubleshoot incomplete or duplicate results in a multi-page list. When you set this parameter to true, Sensible submits the entire [context](doc:prompt), or relevant document extract for your prompt, to the LLM in one request rather than in batched calls. 

## Improvement:  Locate lists in documents using LLM page summaries

In addition to supporting the Search By Summarization parameter for the [Query Group](https://docs.sensible.so/changelog/july-2024#new-feature-llm-page-summaries-for-locating-target-data) method, Sensible now supports this parameter for the List method. Use this parameter to troubleshoot situations in which Sensible misidentifies the part of the document that contains the answers to your prompts. With this parameter, Sensible implements a completion-only retrieval-augmented generation (RAG) strategy. Sensible prompts an LLM to summarize each page in the document, prompts a second LLM to return the pages most relevant to your prompt based on the summaries, and extracts the answers to your prompts from those pages.

## Improvement: Advanced support for JsonLogic operations

In addition to the base JsonLogic [operators](https://jsonlogic.com/operations.html),  Sensible supports extended operations available in the [Json Logic Engine](https://json-logic.github.io/json-logic-engine/docs).  Newly supported operations include: 

* Array operations: `"length"`, `"get"`. 
* Miscellaneous operations: `"preserve"`, `"keys"`. 
* Higher order operations: `"every"`, `"eachKey"`.

With this improvement, Sensible recommends that you use the syntactically more concise `eachKey` operator instead of the [Object](doc:jsonlogic#object)  operator where possible.

## Improvement:  Advanced configuration for Row method and Sections

You can now troubleshoot unusual font sizes that cause the Row method or sections' Stop parameter to fail using the new Tolerance parameter. Use this parameter to adjust Sensible's criteria for recognizing when two lines are in the same "row," or distributed along the same x-axis. For more information, see [Row](doc:row#parameters)  and [Sections](doc:sections#range-parameters). 

## New feature: Define fallback types

With the new [Any](doc:types#any)  type, you can define an array of fallback types for a single field. Sensible uses the first-matching type in the array. Use the Any type as a more concise syntactical alternative to defining an array of [fallback](doc:fallbacks) fields of different types to capture variations in target data's formatting or type.

## UX improvement: Sort configurations in document types

In a document type's list of configs, you can now sort the configs by name, date created, and other attributes:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_nov2024_sort_config.png)
