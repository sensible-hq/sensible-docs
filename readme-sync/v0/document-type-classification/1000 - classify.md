---
title: "Classifying documents by type"
hidden: false
---

You can classify a document by its similarity to each document type you define in your Sensible account.  For example,  if you define a [bank statements](https://github.com/sensible-hq/sensible-configuration-library/tree/main/bank_statements) type and a [tax_forms](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms) document in your account, you can classify 1040 forms,1099 forms, Bank of America statements, Chase statements, and other documents, into those two types. In this scenario, for a  `2023-1-1_bankofamerica_statement_jon_doe.pdf` document, Sensible: 

- Classifies this document into the `bank_statements` document type.
- Classifies the statement doc by its similarity to reference documents in the `bank_statements` document type. The highest score is for [a Bank of America sample PDF](https://github.com/sensible-hq/sensible-configuration-library/blob/main/bank_statements/bank_of_america/boa_sample.pdf).
- Provides metadata for the classification, including similarity scores for this document compared to each document type in your Sensible account and to each reference document in the `bank_statements` type.

Use document classification:

- In an extraction workflow. For example, determine which documents to extract prior to calling a Sensible extraction endpoint.

- Outside an extraction workflow. For example, determine where to route each document or to label each document in a system of record.

For best classification results, Sensible recommends that a document type includes a sample set of reference documents that represent the diversity you expect to see in the document type. To use a document type for classification, Sensible requires that the type contains at least one reference document.

For more information about classifying documents, see the [Sensible API reference](ref:classify-documents-async).
