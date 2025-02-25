---
title: "Handling document variations"
hidden: true
---

*Alt title: Conditional SenseML extraction*



Sensible offers features for handling variations in a set of similar documents (a *document type*). For example, say you extract data from bank statements. The statements all convey the same basic information, but vary in large and small ways:

-  Each major bank has its own distinctive layout and formatting for its statements.  Some combine checking and savings into one statement, and others separate them.
- Some affiliate banks have slightly different layouts but share major similarities.
- You have a long tail of small regional credit unions you want to extract from, where it would be an overwhelming task to qualify all the minor variations.

For both layout-based and LLM-based extraction methods (TODO: link) you can handle these variations by executing different types of SenseML queries to extract the same target data across the bank statements using different extraction methods. In the end, your goal is to produce a unified data output schema. To achieve this, you'll conditionally execute  data-extraction queries based on factors such as which bank issued a statement, whether a query is returning null, or on the shape of the extracted data. Here are the features available to you for conditionally executing data-extraction queries: 

## Handling document variations

| Feature               | granularity                                                 | how it works                                                 | example use case                                             | full example                                                 |
| --------------------- | ----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| configs               | entire set of fields in a *config* (collection of queries). | Determine the best-fitting config for a document, based either on:<br/>- Sensible's default scoring or<br/>- configurable "[fingerprints](doc:fingerprint)", or characteristic text in the document | In a document type, you extract bank statements from Chase, Wells Fargo, Bank of America, and a long tail of small regional banks. Sensible uses a different collection of queries, or *config*,  to extract from each document based on whether it contains the text  `Chase` or `Wells Fargo` or `Bank of America`. If it doesn't contain the name of any major bank, Sensible uses a generalized, LLM-based config to extract from the long tail. | TODO: link to the config library and/or to the example on fallbacks page? |
| conditional execution | subset of fields  in a config                               | based on a pass/fail logical [condition](doc:conditional), execute alternate subsets of fields in a config | You want to extract data from two affiliate banks' statements. The statements' layouts are so similar that you can reuse 90 percent of your SenseML queries to handle both. Rather than authoring two separate configs, you can handle the remaining 10 percent  with conditional field execution. | TODO link to conditional-execution topic                     |
| fallback fields       | single field                                                | If a field fails to extract data, fall back to another identically named field in a config that uses an alternate extraction method. | You want to extract a "total amount" field which appears in a table in document revision A and in a free-text paragraph in document revision B. You can define two fields in one configuration with the same ID (`total_amount`), which use the Row method and the Query Group method, respectively. | TODO link (fallback fields topic)                            |

