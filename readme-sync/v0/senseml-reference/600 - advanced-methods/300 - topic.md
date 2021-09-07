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

| key                     | value        | description                                                  |
| :---------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)       | `topic`      |                                                              |
| numLines (**required**) | number       | The number of consecutive lines to extract. Sensible scores every group of consecutive lines in the document and returns the highest-scoring group. If multiple groups have an equal score, then Sensible returns the last group. Sensible does not support grouping lines in a document with a column layout because of Sensible's default line sorting. For more information, see [line sorting](doc:line#linee-sorting). |
| terms (**required**)    | string array | An array of terms to score positively during topic recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). |
| stopTerms               | string array | An array of terms to score negatively during topic recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). |

Examples
====



The following example shows finding a paragraph

**Config**

```json
{
  "fields": [
    {
      "id": "fringe_benefits_topic",
      "anchor": "general instructions",
      "method": {
        "id": "topic",
        "numLines": 23,
        "terms": [
          "fringe",
          "benefits"
        ],
        "stopTerms": [
          "see",
          "qsehra"
        ]
      }
    }
  ]
}
```

**PDF**
The following image visually represents the output of this config for the following example PDF:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/TBD_example.png)



| Example PDF | [Download link](https://creativecommons.org/licenses/by-nc-sa/2.5/legalcode) |
| ----------- | ------------------------------------------------------------ |


**Output**

```json
{
  "fringe_benefits_topic": {
    "type": "string",
    "value": "Fringe benefits. Include all taxable fringe benefits in cost of group-term life insurance that is more than the cost box 1 of Form W-2 as wages, tips, and other of $50,000 of coverage, reduced by the amount the compensation and, if applicable, in boxes 3 and 5 as employee paid toward the insurance. Use Table 2-2 in social security and Medicare wages. Although not Pub. 15-B to determine the cost of the insurance. Also required, you may include the total value of fringe benefits show the amount in box 12 with code C. For employees, in box 14 (or on a separate statement). However, if you you must withhold social security and Medicare taxes, but provided your employee a vehicle, you must include the not federal income tax. For coverage provided to former value of any personal use in boxes 1, 3, and 5 of Form employees, the former employees must pay the employee W-2. You must withhold social security and Medicare tax, part of social security and Medicare taxes (or railroad but you have the option not to withhold federal income tax retirement taxes, if applicable) on the taxable cost of if you notify the employee and include the value of the group-term life insurance over $50,000 on Form 1040 or benefit in boxes 1, 3, 5, and 14. See Pub. 15-B for more"
  }
}
```
