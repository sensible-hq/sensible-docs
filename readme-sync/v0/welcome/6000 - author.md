---
title: "Choosing an extraction approach"
hidden: false
---

This topic describes how to choose between SenseML and Sensible Instruct for extracting data from a set of similar documents.

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



See the following diagram for an overview of the document landscape, and where Sensible Instruct (LLMs) versus SenseML (rules-based) can determine your extraction approach:

