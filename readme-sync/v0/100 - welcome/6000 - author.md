---
title: "Choosing an extraction approach"
hidden: false
---

TODO: new intro that lays out 'as you scale up, you'll encounter more document complexities and might need additional extraction strategies other than LLMs..."

*This topic describes how to choose between rules-based and large-language model (LLM)-based document extraction strategies.*

See the following diagram for an overview of document structure and variability, and how to determine when to use Sensible Instruct (LLMs) or SenseML (rules-based) query languages for extractions:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/document_landscape.png)

**Note:**  If your document types are listed in Sensible's [open-source configuration library](https://app.sensible.so/library), they come with out-of-the-box support. You can use these pre-authored configurations as-is, or tweak them as necessary to extract from your documents.

Sensible Instruct vs SenseML
---

You can author an extraction configuration, or "config", using SenseML, Sensible Instruct, or both. Use SenseML for advanced document extraction, for example, from complex document layouts. For simpler document extraction, author AI-powered extraction configurations using Sensible Instruct.

SenseML includes Sensible Instruct methods, as well as layout-based methods that use rules and heuristics to extract data. You can mix and match Sensible Instruct and SenseML in a config.

|                              | Sensible Instruct                                            | SenseML                                                      |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Powered by                   | LLMs                                                         | Rules-based                                                  |
| Technical expertise required | For nontechnical users. Describe what you want to extract using natural language.  For example, "the policy period" or "total amount invoiced". | Offers highly configurable JSON-based extraction configuration for technical users. For example, write instructions in JSON to grab the second cell in a column headed by "premium." |
| Workflow automation          | Suited to workflows that include human review or that are fault-tolerant. | Suited to automated workflows that require predictable results and validation. |
| Document variability         | Suited to documents that are unstructured or that have a large number of layout variations or revisions. | Offers faster performance for  structured documents with a finite number of variations, where you know the layout of the document in advance. |
| Deterministic                | No                                                           | Yes. Find the information in the document using anchoring text and layout data. |
| Handles complex layouts      | Limited ability                                              | Suited to documents with highly complex layouts or with complex repeating substructures (for example, loss runs). |



