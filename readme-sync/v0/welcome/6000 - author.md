---
title: "Choosing an extraction approach"
hidden: false
---

This topic describes how to choose between SenseML and Sensible Instruct for extracting data from a set of similar documents.

**Note:**  If your document types are listed in Sensible's [open-source configuration library](https://app.sensible.so/library), they come with out-of-the-box support. You can use these pre-authored configurations as-is, or tweak them as necessary to extract from your documents.

Sensible Instruct vs SenseML
---

You can author an extraction configuration, or "config", using SenseML, Sensible Instruct, or both. Use SenseML for advanced document extraction, for example, for complex document layouts. For simpler document extraction, author AI-powered extraction configurations using Sensible Instruct.

Sensible Instruct methods are AI-powered. SenseML includes Sensible Instruct methods, as well as document layout-based methods that use rules and heuristics to extract data.

You can mix and match Sensible Instruct and SenseML in a config . For example, for any individual piece of data you want to extract, you can fallback to a SenseML method if the Sensible Instruct method returns null.

|                              | Sensible Instruct                                            | SenseML                                                      |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Technical expertise required | For nontechnical users: Describe what you want to extract using natural language, as if chatting with an AI bot.  For example, "what's the policy period"? | Offers highly configurable JSON-based extraction configuration for technical users. For example, write instructions in JSON to grab the second cell in a column headed by "premium". |
| Workflow automation          | Suited to workflows that include human review or that are fault-tolerant. | Suited to automated workflows that require predictable results and validation. |
| Document variability         | Suited to documents that are unstructured or that have a large number of layout variations or revisions. | Offers faster performance for  structured documents with a finite number of variations, where you know the layout of the document in advance. |
| Deterministic                | No                                                           | Yes. Find the information in the document using anchoring text and layout data. |
| Handles complex layouts      | Limited ability                                              | Suited to documents with highly complex layouts or with complex repeating substructures (for example, loss runs). |



