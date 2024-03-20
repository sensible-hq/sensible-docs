---
title: "Topic"
hidden: false

---

Finds a range of lines in a document that best match a topic as determined by a [bag of words](doc:bag-of-words) scoring approach. Most useful in long, unstructured documents. For example, this method in conjunction with the [Summarizer method](doc:summarizer) can extract key-value pairs from free text using ML (machine learning).

[**Parameters**](doc:topic#parameters)
[**Examples**](doc:topic#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                                       | value        | description                                                  |
| :---------------------------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)                         | `topic`      | The Anchor parameter is optional for fields that use this method. If you specify an anchor, Sensible searches from the anchor match to the end of the document for the topic. |
| numParagraphs  or numLines (**required**) | number       | The number of  paragraphs or consecutive lines to extract, respectively. <br/><br/><br/> If you set the Num Paragraphs parameter, Sensible scores every paragraph in the document and returns the highest-scoring paragraph.  For more information about paragraph recognition, see the [Paragraph method](doc:paragraph) .<br/><br/>If you set the Num Lines parameter, Sensible scores every group of consecutive lines in the document and returns the highest-scoring group. For information about the definition of "consecutive", see [line sorting](doc:lines#line-sorting).<br/><br/>If line groups or paragraphs have equal scores, then Sensible returns the last one.<br/> |
| terms (**required**)                      | string array | An array of terms to score positively during topic recognition. For more information about scoring, see [bag of words](doc:bag-of-words). |
| stopTerms                                 | string array | An array of terms to score negatively during topic recognition. For more information about scoring, see [bag of words](doc:bag-of-words). |

Examples
====



The following example shows finding a  topic in a licensing legal code.

**Config**

```json
{
  "fields": [
    {
      "id": "liability_limitation_topic",
      /* anchor is optional for Topic method */
      "method": {
        "id": "topic",
        "numParagraphs": 1,
        "terms": [
          "limitation",
          "liability",
          "extent"
        ],
        "stopTerms": [
          "warranty"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/topic.png)

| Example document | [Download link](https://creativecommons.org/licenses/by-nc-sa/2.5/legalcode) |
| ----------- | ------------------------------------------------------------ |


**Output**

```json
{
  "liability_limitation_topic": {
    "type": "string",
    "value": "6. Limitation on Liability. EXCEPT TO THE EXTENT REQUIRED BY APPLICABLE LAW, IN NO EVENT WILL LICENSOR BE LIABLE TO YOU ON ANY LEGAL THEORY FOR ANY SPECIAL, INCIDENTAL, CONSEQUENTIAL, PUNITIVE OR EXEMPLARY DAMAGES ARISING OUT OF THIS LICENSE OR THE USE OF THE WORK, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES."
  }
}
```
