---
title: "Choosing an extraction approach"
hidden: false
---

TODO rewrite

As you scale up, you'll need to balance extraction performance versus the effort you put into writing extraction configurations.  As part of this optimization, choose between LLMs or rules-based extraction methods.

See the following diagram for an overview of document structure and variability, and when to use Sensible Instruct (LLMs) or SenseML (rules-based) for extractions:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/document_landscape.png)

TODO rewrite this or remove it? Sensible recommends using large-language model (LLM) extraction prompts for free-form, highly variable documents, and layout-based, or "rule-based", extraction queries for structured, less-variable documents.  You can mix and match both strategies, since they're fully compatible with each other. When either strategy can work, Sensible recommends layout-based queries for the sake of fast performance and deterministic output. 

Sensible uses an extraction configuration to extract data from a collection of similar documents that you send to Sensible. You can configure extractions from a variety of documents, from highly structured business forms to unstructured legal or research papers. You have the following options for configuring your extractions:

| document category          | document example   | notes                                                        | get started                                                  |
| -------------------------- | ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **unstructured documents** | research papers    | You describe the document data that you want to extract, using Sensible's visual authoring tool, *Sensible Instruct*. Sensible uses GPT-4 and other large-language models (LLMs) to extract data from your documents. | [Getting started with AI extractions](doc:getting-started-ai) |
| **forms**                  | utility statements | To extract from complex document layouts, use *SenseML*, a superset of Sensible Instruct. SenseML is a JSON-formatted query language that combines layout-based queries with AI-powered queries. | [Getting started with SenseML](doc:getting-started)          |
| **common business forms**  | 1099 tax forms     | Sensible provides out-of-the-box extraction configurations for common business and tax forms. Use Sensible's pre-built, open-source [configuration library](https://github.com/sensible-hq/sensible-configuration-library/) to extract key information from tax forms such as 1099s, major carrier insurance declaration pages, and other documents. Then tweak the pre-built configurations for your custom data needs. | [Getting started with out-of-the-box extractions](doc:excel-quickstart) |

For more information about choosing between SenseML and Sensible Instruct, see [Choosing an extraction approach](doc:author).

See the following table for an overview of the pros and cons of LLMs versus layout-based extraction:

|                              | LLM (Sensible Instruct)                                      | Layout-based (SenseML)                                       |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Technical expertise required | For nontechnical users. Describe what you want to extract using natural language.  For example, "the policy period" or "total amount invoiced". | Offers highly configurable JSON-based extraction configuration for technical users. For example, write instructions in JSON to grab the second cell in a column headed by "premium." |
| Workflow automation          | Suited to workflows that include human review or that are fault-tolerant. | Suited to automated workflows that require predictable results and validation. |
| Document variability         | Suited to documents that are unstructured or that have a large number of layout variations or revisions. | Offers faster performance for  structured documents with a finite number of variations, where you know the layout of the document in advance. |
| Deterministic                | No                                                           | Yes. Find the information in the document using anchoring text and layout data. |
| Handles complex layouts      | Limited ability                                              | Suited to documents with highly complex layouts or with complex repeating substructures (for example, loss runs). |

**Note:**  If your document types are listed in Sensible's [open-source configuration library](https://app.sensible.so/library), they come with out-of-the-box support. You can use these pre-authored configurations as-is, or tweak them as necessary to extract from your documents.

