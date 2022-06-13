---
title: "draft Topic"
hidden: true
---



| key                                      | value   | description                                                  |
| :--------------------------------------- | :------ | :----------------------------------------------------------- |
| id (**required**)                        | `topic` |                                                              |
| numLines or numParagraphs (**required**) | number  | The number of consecutive lines or paragraphs to extract, respectively. <br/>If you set the Num Lines parameter, Sensible scores every group of consecutive lines in the document and returns the highest-scoring group (for information about the definition of "consecutive", see [line sorting](doc:lines#line-sorting). If you set the Num Paragraphs parameter, Sensible scores every group of paragraph lines in a document and returns the highest-scoring paragraph group.  For more information about paragraph recognition, see the [Paragraph method](doc:paragraph) .<br/>If groups have equal scores, then Sensible returns the last group.<br/> |
|                                          |         |                                                              |
|                                          |         |                                                              |

Examples
====



The following example shows finding a  topic in a licensing legal code.

**Config**

```json
{
  "fields": [
    {
      "id": "liability_limitation_topic",
      "anchor": {
        "match": {
          "type": "first"
        }
      },
        "method": {
          "id": "topic",
          "numParagraphs": 1,
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

**Example document**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/topic.png)

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
