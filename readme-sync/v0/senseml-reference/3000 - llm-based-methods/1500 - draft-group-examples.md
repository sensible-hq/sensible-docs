---
title: "Query group"
hidden: true

---


====

Example 1 - WORKING TODO add it to Query Group ref topic
---

The following example shows using the Query Group method to extract agricultural data from a government report.

**Config**

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            // all answers are co-located on pg 2
            "id": "us_wheat_prod_chg_mnth",
            "description": "by what amount did US wheat production estimate change this month? if it didn't change, respond with 'no change",
            "type": "string"
          },
          {
            "id": "us_wheat_seed_use_mil",
            "description": "what was US wheat seed use this year in the US in millions of bushels?",
            "type": "string"
          },
          {
            "id": "us_wheat_seed_chg_mil",
            "description": "by what amount did US wheat seed use change this year compared to last year, in million bushels? Use a negative sign for negative change and a positive sign for positive change, eg, -6 million bushels",
            "type": "string"
          },
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_crop.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "us_wheat_prod_chg_mnth": {
    "value": "no change",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "us_wheat_seed_use_mil": {
    "value": "66",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "us_wheat_seed_chg_mil": {
    "value": "8",
    "type": "string",
    "confidenceSignal": "confident_answer"
  }
}
```



