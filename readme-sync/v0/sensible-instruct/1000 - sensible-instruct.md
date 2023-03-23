---
title: "Sensible Instruct introduction"
hidden: false
---

**Sensible instruct vs SenseML**

In general folks should first try capturing their data with Instruct. For structured documents with a finite number of variations, “traditional” SenseML (our layout-based rules & heuristics approach) is faster and gives more fine-grained control over the output than Instruct. For documents with complex repeating substructure (e.g., loss runs), customers should use sections and SenseML. SenseML also has all the Instruct methods, so it’s possible to blend Instruct methods with layout-based methods using SenseML

More fault-tolerant workflows work better with the Instruct methods. Similarly, if the workflow already contains a step where a human examines or touches the data, then that would be helpful too. 

 **when to use SenseML instead**

you can use both SenseML and Sensible Instruct together for different kinds of documents with different representations of data. You can mix these two in one document.

- The Sensible Instruct methods will currently have trouble with documents where you need to consider more than a page and a half of document context to answer a question or generate a list
- “traditional” SenseML (our layout-based rules & heuristics approach) is faster and gives more fine-grained control over the output than Instruct. For documents with complex repeating substructure (e.g., loss runs), customers should use sections and SenseML. SenseML also has all the Instruct methods, so it’s possible to blend Instruct methods with layout-based methods using SenseML

SenseML is a superset of Sensible Instruct. All the instruct methods are present in SenseML. In addition, SenseML has layout-based methods that use rules and heuristics to extract data, rather than NLP. The upside is that its behavior is predictable and reliable because it is essentially executing specific instructions that you’re writing about the structure of the document. The downside of these layout-based methods is that you need to know the layout ahead of time, and write a configuration per layout







