---
title: February 2025
slug: february-2025
date: 2025-01-15
---

In the last month, Sensible released support for chaining large language model (LLM) prompts for the List method, Anthropic support for the List and NLP Table methods, UX improvements to the Sensible app, configurability for classifying documents by type, and advanced output schema manipulation features.

## Improvement: Chain LLM prompts for the List method

With the List's new [Source IDs](doc:list#parameters)  parameter, you can prompt a large language model (LLM) to extract or transform data from another field's extracted output. For example, if you extract a field `_checking_transactions` and specify it in this parameter, then Sensible answers the prompts `rank deposits by size` and `reformat withdrawals with a minus sign if they're formatted with parentheses` using `_checking_transactions` rather than searching the whole document to locate the [context](doc:prompt#notes).

Using the Source IDs parameter, you can prompt an LLM to:

* Reformat or otherwise transform the outputs of other fields.
* Compute or generate new data from the output of other fields.
* Narrow down the context for your prompts to a specific part of the document.
* Troubleshoot or simplify complex prompts that aren't performing reliably. Break the prompt into several simpler parts, and chain them together using successive Source ID parameters in the fields array.

Configure the List method's Source IDs parameter as an alternative to the Query Group's Source IDs parameter when you want to output repeating data from another extracted field.

## Improvement: Support for Anthropic LLMs for List and NLP Table methods

 With the [NLP Table](doc:nlp-table#parameters)  and [List](doc:list#parameters)  methods' new Provider parameter, you can specify to use Anthropic LLMs instead of OpenAI LLMs. Select Anthropic LLMs to troubleshoot situations in which Sensible correctly identifies the part of the document that contains the answers to your prompts, but the LLM's answer contains problems. For example, Sensible returns an LLM error because the answer isn't properly formatted, or the LLM doesn't follow instructions in your prompt.

## Improvement: Support for very large extractions

Previously, Sensible returned JSON extraction objects up to around 90 MB in size. Now, Sensible can return extractions up to about 500 MB in size. 

## Improvement: Classify a subset of document types

With the [classify](https://docs.sensible.so/reference/classify-document) endpoints' new `document_types` query parameter, you can classify a document against a subset of the document types defined in your Sensible account.

## Improvement: Advanced configurability for the Document Range method

With the [Document Range](doc:document-range#parameters) method's new Num Lines parameter, you can specify a number of lines to extract as an alternative to the Stop parameter.

## UX improvements: Filtering, viewing, and selecting

With new features in the Sensible app, you can select all extractions on all pages, copy configuration version IDs, and sort reference documents. 

* Previously, clicking the **Select all** checkbox selected extractions in the **Extraction history** tab for the current page. Now, you can click **Load all** to select all extractions on all pages:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_feb2025_selectall.png)

<br />

* You can now view and copy configurations' version IDs in the config version history dropdown in the SenseML editor. For example, use these IDs with the Sensible API's configuration endpoints: 

<br />

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_feb2025_versionid.png) 

<br />

* In a document type's **Reference documents** tab, you can now sort reference documents by name, associated configuration, and creation date:

<br />

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_feb2025_refdoc.png) 

<br />

## New feature: Support for extracting from XLS

Sensible now supports data extraction and classification for XLS documents, in addition to existing support for XLSX and CSV files. For more information, see [Supported file types](doc:file-types).

## New feature: Advanced JsonLogic operations

In addition to the base JsonLogic operators, Sensible released new extended JsonLogic operations:

* Use the Log operation to troubleshoot your JsonLogic.
* Use the Pick Fields operation to transform your output schema by copying a list of specified fields from one object to another.

For more information, see  [Log](https://docs.sensible.so/docs/jsonlogic#log) and  [Pick Fields](https://docs.sensible.so/docs/jsonlogic#pick-fields).

## New feature: Transform and output multiple fields with the new Custom Computation Group method

With the existing [Custom Computation](doc:custom-computation)  method, you can use custom JsonLogic rules to output a single field. With the new Custom Computation Group method, you can output multiple fields. 

For more information, see [Custom computation group](doc:custom-computation-group).
