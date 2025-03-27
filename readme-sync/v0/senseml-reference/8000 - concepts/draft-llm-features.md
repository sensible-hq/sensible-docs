---
hidden: true
title: "LLM features overview"
---

Sensible supports large language model (LLM)-based document automation workflows. With LLMs, you can:

- extract data from documents
- classify documents by the document types you define in your Sensible account

#### Document data extraction  features

With LLMs, you can extract structured data as [lists](doc:list), [tables](doc:nlp-table), and [short facts](doc:query-group) from documents. Use Sensible's LLM configuration options and features to:

- Extract multimodal data from non-text data, such as photographs, charts, or illustrations embedded in documents. Using multimodal LLMs, you can also extract from poor-quality text, such as handwritten notes on top of typed text or crossed-out text. For more information, see the Query Group method's [Multimodal Engine parameter](doc:query-group#parameters).
- Chain LLM prompts.  You can specify an agentic workflow to extract document data, then specify subsequent prompts to transform the data. You can include conditional execution in the workflows. For more information, see the [Query Group](doc:query-group#parameters) method's Multimodal Engine parameter and the [Conditional](doc:conditional) method. 

- Qualify LLM accuracy with confidence signals. Get feedback from the LLM if it's uncertain about its answer. For more information, see [Qualifying LLM accuracy](doc:confidence).
- Auto-extract from a new document when you upload it to the Sensible app. Sensible auto-generates a config to extract a few salient facts. Modify the config to extract more information.
- Advanced configuration options for troubleshooting.
  -  *TODO LINK ON PUBLISH: For more information, see draft-llms*


#### Document classification features

With LLMs, you can automate document classification:

- Classify any document that belongs to one of the types you've defined in your account. You can optionally configure LLM classification with a document type [description](doc:descriptions).
- Segment a portfolio document into multiple document types by page ranges. Then extract from each document in the portfolio file separately. For more information, see [Multi-document extraction](doc:portfolio).

