---
title: "Question"
hidden: false

---

Extracts the answer to a free-text question.  This method is a beta release.

Sensible recommends framing each question so that it has a single, short answer.  For more complex questions with multi-part answers, use the [Summarizer](doc:summarizer) method. For a comparsion of these methods, see the following table:

| Question method                                              | [Summarizer](doc:summarizer) method                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ✅ finds the text snippet containing the answer automatically | ❌ Requires an input field to find the text snippet containing the answer. Typically, the input field uses the [Topic](doc:topic) or [Document Range](doc:document-range) methods. |
| ❌ returns a multiple-answer response as a natural-language string | ✅ returns a multiple-answer response structured as an object or list of objects |

For more information about how this method works, see [Notes ](doc:question#notes).

[**Parameters**](doc:question#parameters)
[**Examples**](doc:question#examples)
[**Notes**](doc:question#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key                     | value      | description                                                  |
| :---------------------- | :--------- | :----------------------------------------------------------- |
| id (**required**)       | `question` | The Anchor parameter is optional for fields that use the Question method. If you specify an anchor, Sensible ignores it. |
| question (**required**) | string     | A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`.  For more information about how to write questions (or "prompts"), see [GPT-3 Completions documentation](https://beta.openai.com/docs/guides/completion/introduction). |

Examples
====

Example 1
---

The following example shows using the Question method to extract agricultural data from a government report.

**Config**

```json
{
  "fields": [
    {
      "id": "report_date",
      "method": {
        "id": "question",
        "question": "for which month and year does this snippet describe wheat production"
      }
    },
    {
      "id": "change_in_production",
      "method": {
        "id": "question",
        "question": "by what amount did US wheat production estimate change this month? if it didn't change, respond with 'no change'"
      }
    },
    {
      "id": "seed_use",
      "method": {
        "id": "question",
        "question": "what was US wheat seed use this year in the US in millions of bushels?"
      }
    },
    {
      "id": "seed_use_change",
      "method": {
        "id": "question",
        "question": "by what amount did US wheat seed use change this year, in million bushels? Use a negative sign for negative change and a positive sign for positive change"
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question_1.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_crop.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "report_date": {
    "type": "string",
    "value": "November 2022"
  },
  "change_in_production": {
    "type": "string",
    "value": "No change."
  },
  "seed_use": {
    "type": "string",
    "value": "66 million bushels."
  },
  "seed_use_change": {
    "type": "string",
    "value": "-2 million bushels"
  }
}
```




Example 2
----

The following example shows using the Question method to extract information from a lease.

**Config**

```json
{
  "fields": [
    {
      "id": "rents",
      "type": "currency",
      "method": {
        "id": "question",
        "question": "what's the rents amount in dollars? don't include details about when it's due"
      }
    },
    {
      "id": "rent_due",
      "method": {
        "id": "question",
        "question": "when is the rent due? don't include details about grace periods"
      }
    },
    {
      "id": "rent_frequency",
      "method": {
        "id": "question",
        "question": "how often must the rent be paid? return responses like 'monthly', 'quarterly', or 'biweekly'"
      }
    },
    /* if you ask a multi-part question, you get back 
       a natural-language answer.
       As an alternative, use the Summarizer method to structure 
       such multi-part responses  */
    {
      "id": "rents_multi_part_question",
      "method": {
        "id": "question",
        "question": "list the rents, how often the rent must be paid, and when the rent is due. don't include details about prorated rents or late fees"
      }
    },
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question_2.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "rents": {
    "source": "895.00",
    "value": 895,
    "unit": "$",
    "type": "currency"
  },
  "rent_due": {
    "type": "string",
    "value": "On or before the 1st day of each month."
  },
  "rent_frequency": {
    "type": "string",
    "value": "Monthly"
  },
  "rents_multi_part_question": {
    "type": "string",
    "value": "Lessee shall pay 895.00 dollars per month for rent. Rent must be paid on or before the 1st day of each month. The first month's rent must be paid prior to move-in."
  }
}
```



Notes
===

For an overview of how this method works, see the following steps:

- To meet GPT-3's character limit for input, Sensible splits the document into equal-sized, overlapping chunks. 
- Sensible scores each chunk by how well it matches the question you pose about the data you want to extract. To create the score, Sensible compares your question against each chunk using the OpenAPI Embeddings API. 
- Sensible selects a number of the top-scoring chunks and combines them. The chunks can be non-consecutive in the document.
- Sensible inputs the combined chunks to GPT-3 as one context, and instructs it to answer the question based on the context.