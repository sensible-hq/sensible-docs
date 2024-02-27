---
title: "Natural-language methods"
hidden: false
---

Use natural-language SenseML methods to extract free text from unstructured documents, or as low-code alternatives to [layout based methods](doc:methods). For example, extract information from legal paragraphs in contracts and leases, or results from research papers. 

SenseML natural-language methods are powered by machine learning and natural-language processing models, for example by the large-language model (LLM) GPT-4.

The following topics describe how to author natural-language methods using SenseML. 

| Method                                                       | Example use case                                             | Notes                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [List](doc:list) method                                      | "For each vehicle in an auto insurance declaration, extract the VIN, model, and year." | Extracts a list of data out of a document, where you don't know how the data are represented. |
| [NLP Table](doc:nlp-table) method                            | "For each transaction in a bank statement table, extract the date and amount." | Extracts a list of data out of a document, where you know they're in a table. |
| [Query Group](doc:query-group) method                              | "When does the policy period end?"<br/>"What are the last 4 numbers of the account?" | Extracts a single fact or data point.                        |
| [Summarizer](doc:summarizer) computed field method + [Topic](doc:topic) method | "list the rents, how often the rent must be paid, and when the rent is due" | More configurable alternative to the List method.            |



Notes
====

For information about authoring natural-language methods using a visual tool instead of JSON, see [Prompt tips](doc:instruct).

For layout-based extraction methods, see [methods](doc:methods).
