---
title: "SenseML versus Sensible Instruct"
hidden: false
---

For information about when to use Sensible Instruct or SenseML to extract document data, see the following sections:



SenseML is a superset of Sensible Instruct. All the instruct methods are present in SenseML.   Instruct methods are powered by LLMs.  SenseML includes layout-based methods that use rules and heuristics to extract data, rather than NLP.  You can mix SenseML and Sensible Instruct in a single document extraction configuration, and fallback from one method to anther for any given piece of data you want to extract.



Sensible Instruct

- Offers low-code, visual authoring of document extraction configuration for nontechnical users.
- Suited to workflows that include human review or that are fault-tolerant.
- Suited to documents that are unstructured or that have a large number of layout variations or revisions.



SenseML

-  Offers highly configurable JSON-based extraction configuration for technical users.
- Suited to automated workflows that require predictable results and validation.
- Offers faster performance for  structured documents with a finite number of variations, where you know the layout of the document in advance.
- Suited to documents with highly complex layouts or with complex repeating substructures (for example, loss runs).

