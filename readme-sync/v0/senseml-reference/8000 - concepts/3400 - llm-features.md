---
hidden: false
title: "LLM features overview"
---

Sensible supports large language model (LLM)-based document automation workflows. With LLMs, you can:

- extract data from documents
- classify documents by the document types you define in your Sensible account

## Document data extraction  features

With LLMs, you can extract data from documents structured as:

- [lists](doc:list)
-  [tables](doc:nlp-table)
- [short facts](doc:query-group) 

In addition, use Sensible's LLM configuration options and features to:

- Chain LLM prompts.  You can specify agentic workflows to extract document data, then specify subsequent prompts to transform the data. You can include conditional execution in the workflows. For more information, see Source Ids parameter for the Query Group and List methods and the [Conditional](doc:conditional) method. 
- Qualify LLM accuracy with confidence signals. Get feedback from the LLM if it's uncertain about its answer. For more information, see [Qualifying LLM accuracy](doc:confidence).
- Extract multimodal data from non-text data, such as photographs, charts, or illustrations embedded in documents. Using multimodal LLMs, you can also extract from poor-quality text, such as handwritten notes on top of typed text or crossed-out text. For more information, see the Query Group method's [Multimodal Engine parameter](doc:query-group#parameters).
- Auto-extract from a new document when you upload it to the Sensible app. Sensible auto-generates a config to extract a few salient facts. Modify the config to extract more information.
- [Advanced configuration options](doc:prompt) for troubleshooting. 

## Document classification features

With LLMs, you can automate document classification:

- Classify any document that belongs to one of the types you've defined in your account. You can optionally configure LLM classification with a document type [description](doc:descriptions).
- Segment a portfolio document into multiple document types by page ranges. Then extract from each document in the portfolio file separately. For more information, see [Multi-document extraction](doc:portfolio).

