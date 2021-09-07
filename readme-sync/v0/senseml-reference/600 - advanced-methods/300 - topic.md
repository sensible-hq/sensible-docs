---
title: "Topic"
hidden: true

---

Finds a range of lines in a document that most closely match a topic as determined by a bag of words NLP approach. Most useful in long, unstructured documents.

[**Parameters**](doc:text-table#section-parameters)
[**Examples**](doc:text-table#section-examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key                  | value        | description                                                  |
| :------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)    | `topic`      |                                                              |
| terms (**required**) | string array | An array of terms to score positively during topic recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). |
| stopTerms            | string array | An array of terms to score negatively during topic recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). |

Examples
====

