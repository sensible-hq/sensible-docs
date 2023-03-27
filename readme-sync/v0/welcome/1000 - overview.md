---
title: "Welcome"
hidden: false
---

Welcome to Sensible's documentation. Sensible extracts structured data from documents, for example PDFs of business forms. Sensible combines a variety of approaches to document extraction:

- **Low-code AI authoring**: You describe for an AI the document data that you want to extract, using Sensible's visual authoring tool, *Sensible Instruct*. Sensible uses GPT-3 and other large-language models (LLMs) to extract data from your example document. Save your description as an *extraction configuration*, then extract from documents you upload to Sensible that are similar to your example.  For more information, see [Getting started with AI extractions](doc:getting-started-ai).
- **Advanced authoring:**  To extract from complex document layouts, use *SenseML*, a JSON-formatted query language that combines layout-based queries with AI-powered queries. By combining layout and AI-powered queries, you can extract from a variety of documents, from highly structured business forms to unstructured legal or research papers. For more information, see [Getting started with SenseML](doc:getting-started).
-  **Out-of-the-box extraction for common business documents:**  No need to author document extraction configurations for common business and tax forms. Use Sensible's pre-built, open-source [configuration library] TODO link to sensible app to extract key information from  1099s, common carrier insurance declaration pages, and others documents. Then tweak the pre-built configurations for your custom data needs. For more information, see [Getting started with out-of-the-box extractions](doc:excel-quickstart).

See the following topics for resources:

- [No-code resources](doc:no-code)
- [Developer resources](doc:developer)



Choosing an authoring approach
----

If you're authoring your own custom document extraction configurations instead of using our out-of-the-box TODO LINK extraction configurations, use the following guidelines to choose your authoring approach:

You can author configuration using either SenseML or Sensible Instruct. Sensible Instruct methods are AI-powered. SenseML is a superset of Sensible Instruct. SenseML includes layout-based methods that use rules and heuristics to extract data, rather than NLP.  You can mix SenseML and Sensible Instruct in a single document extraction configuration, and fallback from one method to anther for any given piece of data you want to extract.

Sensible Instruct

- Offers low-code, visual authoring of document extraction configuration for nontechnical users.
- Suited to workflows that include human review or that are fault-tolerant.
- Suited to documents that are unstructured or that have a large number of layout variations or revisions.

SenseML

-  Offers highly configurable JSON-based extraction configuration for technical users.
-  Suited to automated workflows that require predictable results and validation.
-  Offers faster performance for  structured documents with a finite number of variations, where you know the layout of the document in advance.
-  Suited to documents with highly complex layouts or with complex repeating substructures (for example, loss runs).





