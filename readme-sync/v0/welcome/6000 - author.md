---
title: "Choosing an extraction approach"
hidden: false
---

This topic describes how to choose between several strategies for you to author an extraction configuration that you can use for all documents of a given type. 

Summary:

- If the documents you want to extract from are listed in the Sensible configuration library, you can use our out-of-the-box support and author tweaks as necessary . TODO LINKS
- If the data you want to extract is relatively simple and you want an AI-powered solution, use Sensible Instruct to author the extraction configuration.
- For mroe advanced data extraction scenarios, use SenseML.



Sensible Instruct vs SenseML
---


You can author an extraction configuration using either SenseML or Sensible Instruct. Sensible Instruct methods are AI-powered. SenseML is a superset of Sensible Instruct. SenseML includes document layout-based methods that use rules and heuristics to extract data, rather than NLP.  You can mix SenseML and Sensible Instruct in a single document extraction configuration, and fallback from one method to anther for any given piece of data you want to extract.

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



