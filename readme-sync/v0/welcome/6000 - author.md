---
title: "Choosing an extraction approach"
hidden: false
---

As you scale up and encounter document complexity, you can optimize extraction performance by choosing between LLMs or layout-based extraction methods.

See the following diagram for an overview of when to use Sensible Instruct (LLMs) or SenseML (layout-based) for extractions: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/document_landscape.png)

Sensible recommends using large language model (LLM) prompts for free-form, highly variable documents, and layout-based, or "rule-based" queries for structured, less-variable documents.  You can combine both strategies since they're fully compatible with each other. 

See the following table to learn more about extraction strategies:

| extraction method | notes                                                        | get started                                                  |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| LLMs              | You describe the document data that you want to extract, using Sensible's visual authoring tool, *Sensible Instruct*. Sensible uses GPT-4 and other large language models (LLMs) to extract data from your documents. | [Getting started](doc:getting-started-ai)                    |
| layout-based      | To extract from complex document layouts, use *SenseML*, a superset of Sensible Instruct. SenseML is a JSON-formatted query language that combines layout-based queries with LLM-based queries. When either strategy can work, Sensible recommends layout-based queries for the sake of fast performance and deterministic output. | [Getting started with layout-based extractions](doc:getting-started) |
| out-of-the-box    | Sensible provides out-of-the-box extraction configurations for common business and tax forms. Use Sensible's pre-built, open-source [configuration library](https://github.com/sensible-hq/sensible-configuration-library/) to extract key information from tax forms such as 1099s, major carrier insurance declaration pages, and other documents. Then tweak the pre-built configurations for your custom data needs. | [Getting started with out-of-the-box extractions](doc:library-quickstart) |

See the following table for an overview of the pros and cons of LLMs versus layout-based extraction:

|                                                              | LLM (Sensible Instruct)                                      | layout-based (SenseML)                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Technical expertise required                                 | For nontechnical users. Describe what you want to extract in a prompt to an LLM.  For example, "the policy period" or "total amount invoiced". | Offers highly configurable JSON-based extraction configuration for technical users. For example, write instructions in JSON to grab the second cell in a column headed by "premium." |
| Workflow automation                                          | Suited to workflows that include human review or that are fault-tolerant. | Suited to automated workflows that require predictable results and validation. |
| Document variability                                         | Suited to documents that are unstructured or that have a large number of layout variations or revisions. | Suited to structured documents with a finite number of variations, where you know the layout of the document in advance. |
| Deterministic                                                | No                                                           | Yes. Find the information in the document using anchoring text and layout data. |
| Handles repeating layouts                                    | Use [List](doc:list-tips) method.                            | Use [sections](doc:sections) for highly complex repeating substructures, for example, [loss runs](doc:sections). |
| Handles non-text images (photos, illustrations, charts, etc) | To extract data about images (`"is the building in this picture multistory?"`, use [Query Group](doc:query-group) method with the Multimodal Engine parameter configured | No                                                           |
| Performance                                                  | Data extraction takes a few seconds for each Instruct method. | Offers faster performance in general. For more information, see [Optimizing extraction performance](doc:performance). |

