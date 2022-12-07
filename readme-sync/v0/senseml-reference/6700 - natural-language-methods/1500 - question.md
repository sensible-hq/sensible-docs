---
title: "Question"
hidden: true

---

TODO: update index parent page topic link.



Finds the answer to a simple, free-text question. Best suited to questions that have a a single-value, labeled answer in the document. 



[**Parameters**](doc:topic#parameters)
[**Examples**](doc:topic#examples)

Parameters
=====

**Note:** This method doesn't support [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters specific to this method.

| key                     | value                                | description                                                  |
| :---------------------- | :----------------------------------- | :----------------------------------------------------------- |
| id (**required**)       | `question`                           | Powered by a fork of [LayoutLM](https://github.com/microsoft/unilm/tree/master/layoutlm).  Returns one answer per document. Generally the answer is one line or a substring in a line. Incompatible with configurations that return or filter lines arrays. For example, doesn't support Sections, `"match":"all"` or `"match":"last"`. |
| question (**required**) | string                               | To improve performance,  anchor on text that's on the page containing the answer. If you specify `"match": { "type": "first" }`, Sensible searches the whole document for the answer. A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`. Best suited to simple questions that have one label and one answer in the document. |
| confidence              | number between 0 and 1. default: 0.6 | Return answer if confidence is equal to or greater than the specified value, else return null. |

Examples
====



The following example shows TBD

https://dev.sensible.so/editor/?d=auto_insurance_quote&c=anyco_question&g=auto_insurance_anyco_golden_generic___style_updated___google_docs 

**Config**

```json
TODO
```

**Example document**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TB_D.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |



**Output**

```json
TDOO
```
---
title: "Question"
hidden: true

---

TODO: update index parent page topic link.



Finds the answer to a simple, free-text question. Best suited to questions that have a a single-value, labeled answer in the document. Powered by a fork of [LayoutLM](https://github.com/microsoft/unilm/tree/master/layoutlm).

[**Parameters**](doc:topic#parameters)
[**Examples**](doc:topic#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                     | value                                | description                                                  |
| :---------------------- | :----------------------------------- | :----------------------------------------------------------- |
| id (**required**)       | `question`                           |                                                              |
| question (**required**) | string                               | A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`. |
| confidence              | number between 0 and 1. default: 0.6 | Return answer if confidence is equal to or greater than the specified value, else return null. In practice, confidence is often either very low or above 0.6. |

Examples
====



The following example shows finding a  topic in a licensing legal code.

**Config**

```json
TODO
```

**Example document**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TB_D.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |



**Output**

```json
TDOO
```
