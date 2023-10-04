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

| document category          | document example   | notes                                                        | get started                                                  |
| -------------------------- | ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **unstructured documents** | research papers    | You describe the document data that you want to extract, using Sensible's visual authoring tool, *Sensible Instruct*. Sensible uses GPT-4 and other large-language models (LLMs) to extract data from your documents. | [Getting started with AI extractions](doc:getting-started-ai) |
| **forms**                  | utility statements | To extract from complex document layouts, use *SenseML*, a superset of Sensible Instruct. SenseML is a JSON-formatted query language that combines layout-based queries with AI-powered queries. | [Getting started with SenseML](doc:getting-started)          |
| **common business forms**  | 1099 tax forms     | Sensible provides out-of-the-box extraction configurations for common business and tax forms. Use Sensible's pre-built, open-source [configuration library](https://github.com/sensible-hq/sensible-configuration-library/) to extract key information from tax forms such as 1099s, major carrier insurance declaration pages, and other documents. Then tweak the pre-built configurations for your custom data needs. | [Getting started with out-of-the-box extractions](doc:excel-quickstart) |

For more information about choosing between SenseML and Sensible Instruct, see [Choosing an extraction approach](doc:author).

Next
----

To learn how to extract document data, see [Getting Started](doc:getting-started-ai).
