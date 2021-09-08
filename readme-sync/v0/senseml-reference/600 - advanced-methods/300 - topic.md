---
title: "Topic"
hidden: false

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
| numLines (**required**) | number       | The number of consecutive lines to extract. Sensible scores every group of consecutive lines in the document and returns the highest-scoring group. If multiple groups have an equal score, then Sensible returns the last group. Sensible does not support grouping lines in a document with a column layout because of Sensible's default line sorting. For more information, see [line sorting](doc:lines#line-sorting). |
| terms (**required**)    | string array | An array of terms to score positively during topic recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). |
| stopTerms               | string array | An array of terms to score negatively during topic recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). |

Examples
====



The following example shows finding a  topic in a licensing legal code.

**Config**

```json
{
  "fields": [
    {
      "id": "liability_limitation_topic",
      "anchor": "creative commons corporation",
      "method": {
        "id": "topic",
        "numLines": 6,
        "terms": [
          "limitation",
          "liability",
          "extent"
        ],
        "stopTerms": [
          "warranty",
        ]
      }
    }
  ]
}
```

**PDF**
The following image visually represents the output of this config for the following example PDF:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/topic_example.png)



| Example PDF | [Download link](https://creativecommons.org/licenses/by-nc-sa/2.5/legalcode) |
| ----------- | ------------------------------------------------------------ |


**Output**

```json
{
  "liability_limitation_topic": {
    "type": "string",
    "value": "6. Limitation on Liability. EXCEPT TO THE EXTENT REQUIRED BY APPLICABLE LAW, IN NO EVENT WILL LICENSOR BE LIABLE TO YOU ON ANY LEGAL THEORY FOR ANY SPECIAL, INCIDENTAL, CONSEQUENTIAL, PUNITIVE OR EXEMPLARY DAMAGES ARISING OUT OF THIS LICENSE OR THE USE OF THE WORK, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. 7. Termination"
  }
}
```
