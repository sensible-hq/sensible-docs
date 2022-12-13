---
title: "(Beta) Question"
hidden: false

---

Extracts the answer to a simple, free-text question. Best suited to questions that have a single-value, labeled answer in the document.  This method is in a beta release.



[**Parameters**](doc:question#parameters)
[**Examples**](doc:question#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key                     | value                                | description                                                  |
| :---------------------- | :----------------------------------- | :----------------------------------------------------------- |
| id (**required**)       | `question`                           | Powered by a fork of [LayoutLM](https://github.com/microsoft/unilm/tree/master/layoutlm).  Returns one answer per document. Generally the answer is one line or a substring in a line.<br/> Doesn't support anchors at granularity below the page level. For example, to improve performance,  anchor on text that's on the page containing the answer. If you specify `"match": { "type": "first" }`, Sensible searches the whole document for the answer. <br/>Doesn't support options that use multiple anchor match candidates. For example, doesn't support Sections, `"match":"all"` or `"match":"last"`. |
| question (**required**) | string                               | A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`. Best suited to simple questions that have one label and one answer in the document.<br/> |
| confidence              | number between 0 and 1. default: 0.6 | Return answer if confidence is equal to or greater than the specified value, else return null. |

Examples 
====

**Config**

```json
{
  "fields": [
    {
      /* ID for target data */
      "id": "policy_period_end_date",
      /* target data is a date */
      "type": "date",
      /* search whole document for answer */
      "anchor": {
        "match": {
          "type": "first"
        }
      },
      "method": {
        "id": "question",
        /* ask a free-text question.
          best suited to simple questions
          that have one label and one answer 
          in the document. */
        "question": "What are the policy period dates?",
        /* the question method returns a line containing two dates.
           return the larger (later) date.
           Or, remove the tiebreaker and ask,
           "when does the policy period end? */
        "tiebreaker": ">"
      }
    },
    {
      "id": "comprehensive_premium",
      "anchor": {
        "match": {
          "type": "first"
        }
      },
      /* target data is a currency, else return null */
      "type": "currency",
      "method": {
        "id": "question",
        "question": "in the table, what's the comprehensive premium"
      }
    },
    {
      "id": "policy_number",
      "type": "string",
      "anchor": {
        "match": {
          "type": "first"
        }
      },
      "method": {
        "id": "question",
        "question": "policy number"
      }
    },
    {
      "id": "driver_email",
      "type": "string",
      "anchor": {
        "match": {
          "type": "first"
        }
      },
      "method": {
        "id": "question",
        "question": "insured's email address"
      }
    },
  ]
}
```

**Example document**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |



**Output**

```json
{
  "policy_period_end_date": {
    "source": "Oct 14, 2021",
    "value": "2021-10-14T00:00:00.000Z",
    "type": "date"
  },
  "comprehensive_premium": {
    "source": "$150",
    "value": 150,
    "unit": "$",
    "type": "currency"
  },
  "policy_number": {
    "type": "string",
    "value": "123456789"
  },
  "driver_email": {
    "type": "string",
    "value": "petarpetrov@anyprovider.com"
  }
}
```



