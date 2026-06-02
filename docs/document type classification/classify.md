---
title: Classifying documents by type
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: >-
    Automatically classify documents by type, for example, 'bank statment' or
    'driver's license
  robots: index
next:
  description: ''
---
Use Sensible to "classify" documents in the following ways:

1. Classify a document by its similarity to high-level document types you define in your Sensible account. For example, classify a document as a `1040s` document type or a `pay_stubs` document type. You can classify a document by type without extracting document data using the Sensible API's [Classify](reference:classify-document)  endpoint.  

2. Classify a document by its subtype during a single-document extraction workflow. By default, Sensible performs this step automatically.  For example, classify a document as a `1040_2018` or `1040_2019` subtype (or "config"). For more information, see [DevOps platform](doc:devops-platform).

3. Classify a document by its high-level type during a multi-document extraction workflow.  Sensible performs this step automatically. For example, TODO rework
   1. When you extract data from a single document, you manually specify the document type. When you extract data from multiple documents bundled together, you specify multiple possible document types, and Sensible automatically classifies documents by those specified type in the following circumstances: TODO: this list coudl be hard to maintain ... and could use a mermaid diagram for all of them maybe...
      1. attached documents in an email by type
      2. Classify, or "segment", a document in a multi-document file (a "portfolio").  For example, for a `loan_application_bundle.pdf` document containing  a  `pay_stubs`  document, a `1040` document, and a `bank_statements`  document, you can segment each document by its page range in the file, and return its extracted data separately.

<br />

## Classifying by document type

This topic covers classifying a document by its high-level type.

Sensible classifies a document by comparing it to the types you define in your account. For example, you can classify 1040 forms and bank statements if you define the following types in your account:

* a [bank statements](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Financial%20Services/Bank%20Statements) type

* a [1040s](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Tax%20Forms/1040s) type

Sensible uses a document type's name and its description for LLM-based classification:

* If Sensible doesn't find an existing document type to which to match your document in your account, it returns an error.
* Sensible can classify documents into your document types even if the document type lacks a config or reference document. For example, if you lack a  `citibank` config or reference document in your `bank_statements` type, Sensible can still classify a  `2023-1-1_citbank_statement_jon_doe.pdf` document as a bank statement.

To improve classification results, describe each document type in your account in its **Settings** tab. For examples of descriptions, see [Document type descriptions](doc:descriptions).  By default, Sensible classifies a document using all the types you define in your account. You can optionally define a subset of document types for classifying a document.

## Use cases for classification endpoints

You can use Sensible's API and SDK to classify documents for your use cases, for example:

* Prior to an extraction workflow. Determine which documents to extract prior to calling a Sensible extraction endpoint.

* Independent from an extraction workflow. For example, determine where to route each document or to label each document in a system of record.
