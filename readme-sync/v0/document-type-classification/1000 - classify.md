---
title: "Classifying documents by type"
hidden: false
---

Sensible supports two levels of document classification:

1. Classify a document by its similarity to document types you define in your Sensible account. For example, classify a document as a `1040s` document type or a `pay_stubs` document type.

2. Classify a document by its subtype during the extraction workflow. By default, Sensible performs this step automatically.  For example, classify a document as a `1040_2018` or `1040_2019` subtype (or "config"). For more information, see [Devops platform](doc:devops-platform).

This topic covers classifying a document by its type.

Sensible classifies a document by comparing it to the types you define in your account. For example, you can classify 1040 forms and bank statements if you define the following types in your account:

- a [bank statements](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Financial%20Services/Bank%20Statements) type

- a [1040s](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Tax%20Forms/1040s) type

Sensible uses a document type's name and its description for LLM-based classification:

- If Sensible doesn't find an existing document type to which to match your document in your account, it returns an error.
- Since Sensible doesn't use configs or reference documents for classification, Sensible can classify documents into your document types even if the document type lacks a config or example. For example, if you lack a  `citibank` config or reference document in your `bank_statements` type, Sensible can still classify a  `2023-1-1_citbank_statement_jon_doe.pdf` document as a bank statement. 

 To improve classification results, describe each document type in your account in its **Settings** tab. For examples of descriptions, see [Document type descriptions](doc:descriptions).  By default, Sensible classifies a document using all the types you define in your account. You can optionally define a subset of document types for classifying a document.

Use document type classification:

- Prior to an extraction workflow. For example, determine which documents to extract prior to calling a Sensible extraction endpoint. 

- Independent from an extraction workflow. For example, determine where to route each document or to label each document in a system of record.

To classify documents, use the Sensible API or SDKs.

