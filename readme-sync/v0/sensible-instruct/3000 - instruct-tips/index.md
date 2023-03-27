---
title: "Sensible Instruct authoring tips"
hidden: false
---

See the following topics for tips on authoring the following methods using Sensible Instruct:

| Method                            | Example use case                                             | Notes                                                        |
| --------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [List](doc:list)                  | For each vehicle in an auto insurance declaration, extract the VIN, model, and year. | Extracts a list of data out of a document, where you don't know how the data are represented. |
| [NLP Table](doc:nlp-table) method | For each transaction in a bank statement table, extract the date and amount. | Extracts a list of data out of a document, where you know they're in a table. |
| [Question](doc:question) method   | "When does the policy period end?"<br/>"What are the last 4 numbers of the account?" | Extracts a single fact or data point.                        |
|                                   |                                                              |                                                              |

Notes
====

For layout-based extraction methods, see [methods](doc:methods).
