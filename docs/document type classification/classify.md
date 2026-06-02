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
Sensible "classifies" documents in the following senses:

1. When you extract data from a single document , you "classify" the document by specifying one of the high-level document types you defined in your account, for example `1040s` or `pay_stubs`. Sensible then automatically classifies the document by its subtype, or "config", in the document type, for example, the `1040s_2018` version or the `1040_20`  version of a `1040s` document. For more information, see [DevOps platform](doc:devops-platform).

2. When you extract data from multiple documents in a single request, you specify a list of possible document types, and Sensible "classifies" both high-level document types and subtypes automatically. For example:
   1. Sensible classifies, or "segments", each document in a multi-document file, or "portfolio".  For example, for a `loan_application_bundle.pdf` document containing  a  `pay_stubs`  document, a `1040` document, and a `bank_statements`  document, you can segment, each document by its page range in the file, and return its extracted data separately.  You can configure LLM- or fingerprint-based segmentation. For more information, see [Multi-document extractions](doc:portfolio).
   2. Classify each attached document in an email by document type, then return aeach document's extracted data separately. For more information, see [Getting started with email extraction](doc:getting-started-email)

3. Independently from extraction workflows, you can use the Sensible API to classify a document by its similarity to high-level document types you define in your Sensible account. For example, classify a document as a `1040s` document type or a `pay_stubs` document type. For more information, see the Sensible API's [Classify](reference:classify-document)  endpoint.

## Classification endpoints

This topic covers classifying a document by its high-level type using the Sensible API, independently from extraction workflows.

Sensible classifies a document by comparing it to the types you define in your account. For example, you can classify 1040 forms and bank statements if you define the following types in your account:

* a [bank statements](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Financial%20Services/Bank%20Statements) type

* a [1040s](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Tax%20Forms/1040s) type

Sensible uses a document type's name and its description for LLM-based classification:

* Sensible can classify documents into your document types even if the document type is empty (lacks a config or reference document). For example, if you lack a  `citibank` config or reference document in your `bank_statements` type, Sensible can still classify a  `2023-1-1_citbank_statement_jon_doe.pdf` document as a bank statement.
* If Sensible doesn't find an existing document type to which to match your document in your account, it returns an error.

To optionally improve classification results, describe each document type in your account in its **Settings** tab. For examples of descriptions, see [Document type descriptions](doc:descriptions).  By default, Sensible classifies a document using all the types you define in your account. You can optionally define a subset of document types for classifying a document.

## Use cases for classification endpoints

You can use Sensible's API to classify documents for your use cases, for example:

* Prior to an extraction workflow. Determine which documents to extract prior to calling a Sensible extraction endpoint.

* Independent from an extraction workflow. For example, determine where to route each document or to label each document in a system of record.
