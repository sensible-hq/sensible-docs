---
title: "LLM-based methods"
hidden: false
---

Extract free text from unstructured documents using large language model (LLM)-based SenseML methods. For example, extract information from legal paragraphs in contracts and leases, or results from research papers.

The following LLM-based methods are alternatives to [layout-based methods](doc:layout-based-methods) for structured documents, for example, tax documents or insurance forms. 

| Method                                | Example use case                                             | Chained-prompt example<sup>1</sup>                           | Notes                                                        |
| ------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [List](doc:list) method               | "For each vehicle in an auto insurance declaration, extract the VIN, model, and year." | "For the extracted list of vehicles, sort them by year of manufacter " | Extracts a list of data out of a document, where you don't know how the data are represented. |
| [Query Group](doc:query-group) method | "When does the policy period end?"<br/>"What's the account number?" | "Redact the account number to only the last 4 digits"        | Extracts a single fact or data point.                        |
| [NLP Table](doc:nlp-table) method     | "For each transaction in a bank statement table, extract the date and amount." | N/A                                                          | Extracts a list of data out of a document, where you know they're in a table. |

Notes
====

- <sup>1</sup> For information about chained prompts, see [Computed field methods](doc:computed-field-methods).

- For layout-based extraction, see [Layout-based methods](doc:layout-based-methods).

  
