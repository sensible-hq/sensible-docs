---
title: "Classifying documents by type"
hidden: true
---

You can classify a document by its similarity to each document type you define in your Sensible account. For example, if you import the [bank statements](https://github.com/sensible-hq/sensible-configuration-library/tree/main/bank_statements) type and the [tax_forms](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms) document type into your account from the open-source Sensible Configuration Library, and then ask Sensible to classify a Bank of America monthly bank statement, Sensible:

- Classifies the statement document into the `bank_statements` document type.
- Classifies the statement doc by its similarity to reference documents in the document type. In this case, the highest score is for [a Bank of America sample PDF](https://github.com/sensible-hq/sensible-configuration-library/blob/main/bank_statements/bank_of_america/boa_sample.pdf).
-  Provides metadata for the classification, including similarity scores for this document compared to each document type in your Sensible account and to each reference document in the highest-scoring document type.

Use document classification:

- In an extraction workflow. For example, determine which documents to extract prior to calling a Sensible extraction endpoint.

- Outside an extraction workflow. For example, determine where to route each document or to label each document in a system of record.

For more information about classifying documents, see the [Sensible API](ref:classify-documents).
