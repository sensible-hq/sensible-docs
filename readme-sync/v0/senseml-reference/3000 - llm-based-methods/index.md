---
title: "LLM-based methods"
hidden: false
---

Extract free text from unstructured documents using large language model (LLM)-based SenseML methods. For example, extract information from legal paragraphs in contracts and leases, or results from research papers.

These methods are alternatives to [layout-based methods](doc:methods) for structured documents, for example, tax documents or insurance forms.  


The following topics describe how to author LLM-based methods using the JSON editor. For information about authoring LLM-based methods using a visual editor, see [Prompt tips](doc:prompt-tips). 

| Method                                                       | Example use case                                             | Notes                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [List](doc:list) method                                      | "For each vehicle in an auto insurance declaration, extract the VIN, model, and year." | Extracts a list of data out of a document, where you don't know how the data are represented. |
| [NLP Table](doc:nlp-table) method                            | "For each transaction in a bank statement table, extract the date and amount." | Extracts a list of data out of a document, where you know they're in a table. |
| [Query Group](doc:query-group) method                              | "When does the policy period end?"<br/>"What are the last 4 numbers of the account?" | Extracts a single fact or data point.                        |
| [Summarizer](doc:summarizer) computed field method | transform extracted data using LLM prompts | Use this method to transform another method's output when you can't use [types](doc:types) or other [computed field methods](doc:computed-field-methods).            |



Notes
====



For layout-based extraction, see [Layout-based methods](doc:methods).
