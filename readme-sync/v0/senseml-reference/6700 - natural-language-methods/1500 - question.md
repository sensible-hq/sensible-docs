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
