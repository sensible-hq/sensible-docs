---
title: "Overview"
hidden: false
---

Welcome! Use Sensible to extract structured data from documents, for example, business forms in PDF format. With the Sensible platform, you can:

-  upload documents for extraction using our drag-and-drop interface
-  pre-process document formatting to ensure clean extractions
-  extract data from tables, lists, checkboxes, and other document primitives
-  measure extraction accuracy during post-processing
-  Integrate with our API

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform.png)

TODO rewrite: Sensible uses an extraction configuration, or "config",  to extract data from a collection of similar documents that you send to Sensible. You can configure extractions from a variety of documents, from highly structured business forms to unstructured legal or research papers. You have the following options for configuring your extractions:

| document category                            | notes                                                        | get started                                                  |
| -------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **natural-language, unstructured documents** | You describe the document data that you want to extract, using Sensible's visual authoring tool, *Sensible Instruct*. Sensible uses GPT-4 and other large-language models (LLMs) to extract data from your documents. | [Getting started with AI extractions](doc:getting-started-ai) |
| **form-like documents **                     | To extract from complex document layouts, use *SenseML*, a superset of Sensible Instruct. SenseML is a JSON-formatted query language that combines layout-based queries with AI-powered queries. | [Getting started with SenseML](doc:getting-started)          |
| **common business documents**                | Sensible provides out-of-the-box extraction configurations for common business and tax forms. Use Sensible's pre-built, open-source [configuration library](https://github.com/sensible-hq/sensible-configuration-library/) to extract key information from tax forms such as 1099s, major carrier insurance declaration pages, and other documents. Then tweak the pre-built configurations for your custom data needs. | [Getting started with out-of-the-box extractions](doc:excel-quickstart) |

For more information about choosing between SenseML and Sensible Instruct, see [Choosing an extraction approach](doc:author).



Get started and integrate
---

- [Sign up for a free API key](https://app.sensible.so/register)
- Test the API with the  [Developer Quickstart](doc:quickstart)
- [Zapier integration](doc:zapier)
- [Code examples](doc:examples)

Reference docs
---

- [API reference](reference:choosing-an-endpoint) and [Postman collection](https://god.gw.postman.com/run-collection/16839934-45339059-3fec-4c31-a891-9a12a3e1c22b?action=collection%2Ffork&collection-url=entityId%3D16839934-45339059-3fec-4c31-a891-9a12a3e1c22b%26entityType%3Dcollection%26workspaceId%3Ddbde09dc-b7dd-487d-a68f-20d32b008f90)
- [SenseML reference introduction](doc:senseml-reference-introduction) 

Basic document extraction configuration
---

Write AI-powered extraction configurations in Sensible Instruct.

- [Getting started with AI-powered extractions](doc:getting-started-ai) or [interactive in-app tutorial](https://app.sensible.so/tutorial/)

Advanced extraction configuration: learn SenseML
---

Tweak existing doc extraction configurations or write new configurations for your custom documents.

- [Getting started with SenseML](doc:getting-started)
- Interactive tutorials: 
  - [extract_your_first_data](https://app.sensible.so/editor/?d=senseml_basics&c=1_extract_your_first_data&g=1_extract_your_first_data)
  - [tables and rows](https://app.sensible.so/editor/?d=senseml_basics&c=2_tables_and_rows&g=2_tables_and_rows)
  - [checkboxes, paragraphs, and regions](https://app.sensible.so/editor/?d=senseml_basics&c=3_checkboxes_paragraphs_and_regions&g=3_checkboxes_paragraphs_and_regions)
  - [blank-slate challenge](https://app.sensible.so/editor/?d=senseml_basics&c=4_extract_from_scratch&g=4_extract_from_scratch) 

Quality control and troubleshoot your extractions
---

  -   [Validate extractions](doc:validate-extractions)
  -   [Troubleshoot](doc:troubleshoot)

Test and go live
----

- [Test before integrating](doc:test-before-integrating-configs)

- [Go-live checklist](doc:go-live)

  

