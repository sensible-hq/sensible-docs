---
hidden: true
title: "LLM features overview"
---

Sensible supports large language model (LLM)-based document automation workflows. With LLMs, you can:

- extract data from documents
- classify documents by the document types you define in your Sensible account

#### Document data extraction  features

With LLMs, you can extract structured data as [lists](doc:list), [tables](doc:nlp-table), and [short facts](doc:query-group) from documents. Use Sensible's LLM configuration options and features to:

- Extract mulitmodal data from non-text data, such as photographs, charts, or illustrations embedded in documents. Using multimodal LLMs, you can also extract from poor-quality text, such as handwritten notes on top of typed text or crossed-out text. For more information, see the Query Group method's [Multimodal Engine parameter](doc:query-group#parameters)
- Chain LLM prompts.  You can specify an agentic workflow to extract document data, then specify subsequent prompts to transform the data. You can include conditional execution in the workflows. For more information, see TODO and TODO.

- Qualify LLM accuracy with confidence signals. Get feedback from the LLM if it's uncertain about its answer. For more information, see [Qualifying LLM accuracy](doc:confidence).
- Auto-extract from a new document when you upload it to the Sensible app. Sensible auto-generates a config to extract a few salient facts. Modify the config to extract more information.
- Advanced configuration options for troubleshooting. For more information, see draft-llms TODO.

#### Document classification features

With LLMs, you can automate document classification:

- Classify any document that belongs to one of the types you've defined in your account. you can configure LLM classification w/ a document type description, or leave it as-is. TODO link
- Segment a portfolio document into multiple document types complete w page ranges and then treat each document in the portfolio separately. TODO LINK



