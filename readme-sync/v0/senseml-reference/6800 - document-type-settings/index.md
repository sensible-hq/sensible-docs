---
title: "Document type settings"
hidden: false

---

A document type is an API endpoint that you configure for extracting data from a general category of similar documents, for example, `bank_statments` or `1040s`.  You configure extraction templates or leverage Sensible's out-of-the-box [library](doc:library-quickstart). 

 In the endpoint, you configure *configs*, or templates that define how to extract data from subcategories of documents in the general document type category. The templates contain queries you write in Sensible's document-domain specific query language, [SenseML](doc:senseml-reference-introduction). For example, a `bank_statements` document type can contain a template for Bank of America statements, a template for Wells Fargo statements, and a template for Chase statements. 

For more information about creating and configuring document types, see [Getting started](doc:getting-started-ai).

See the following topics for options you can set in the **Settings** tab for each document type:

- [Fingerprint mode](doc:fingerprint-mode)

- [OCR engine](doc:ocr-engine)

  

See the following topics for other settings you can set for each document type:

- [Human review](doc:human-review) 
- [OCR level](doc:ocr-level) 
- [Validations](doc:validate-extractions)

