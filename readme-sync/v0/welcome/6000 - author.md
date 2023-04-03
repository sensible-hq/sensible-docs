---
title: "Choosing an extraction approach"
hidden: false
---

This topic describes how to choose between SenseML and Sensible Instruct for authoring an extraction configuration that you can use to extract data from a set of similar documents.

**Note** If you If the documents you want to extract from are listed in the Sensible configuration library, you can use our out-of-the-box support and author tweaks as necessary TODO link.

Sensible Instruct vs SenseML
---

You can author an extraction configuration using either SenseML or Sensible Instruct. Sensible Instruct methods are AI-powered. SenseML is a superset of Sensible Instruct. SenseML includes document layout-based methods that use rules and heuristics to extract data, rather than NLP.  You can mix SenseML and Sensible Instruct in a single document extraction configuration, and fallback from one method to anther for any given piece of data you want to extract.



TODO reconcile these paragraphs:

*Note that you can mix and match SenseML methods with Sensible Instruct methods. SenseML is a a JSON-formatted, layout-based query language, and Sensible Instruct is an AI-powered subset of SenseML that you can author in the app, no JSON required. Use SenseML for advanced document extraction, for example, for complex document layouts. For simpler document extraction, author AI-powered extraction configurations using Sensible Instruct.* 

Sensible Instruct

- For nontechnical users: Describe what you want to extract in natural language terms.
- Suited to workflows that include human review or that are fault-tolerant.
- Suited to documents that are unstructured or that have a large number of layout variations or revisions.

SenseML

-  Offers highly configurable JSON-based extraction configuration for technical users.
-  Suited to automated workflows that require predictable results and validation.
-  Offers faster performance for  structured documents with a finite number of variations, where you know the layout of the document in advance.
-  Suited to documents with highly complex layouts or with complex repeating substructures (for example, loss runs).



|                         | [Natural language methods](doc:natural-language-methods)     | Layout-based [methods](doc:methods)                          |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
|                         | Ask a question about info in the document, as you'd ask a human or chatbot. For example, "what's the policy period"? | Find the information in the document using anchoring text and layout data. For example, write instructions in JSON to grab the second cell in a column headed by "premium". |
| Deterministic           | no                                                           | yes                                                          |
| Handles complex layouts | no                                                           | yes                                                          |



