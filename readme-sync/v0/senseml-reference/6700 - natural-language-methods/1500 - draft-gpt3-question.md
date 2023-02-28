---
title: "Question"
hidden: true

---

Extracts the answer to a free-text question.  This method is a beta release.

Sensible recommends framing each question so that it has a single, short answer.  For more complex questions with multi-part answers, use the [Summarizer](doc:summarizer) method. For a comparsion of these methods, see the following table:

| Question method                                              | [Summarizer](doc:summarizer) method                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ✅ low-code authoring                                         | ❌  SenseML authoring                                         |
| ✅ finds the text snippet containing the answer automatically | ❌ Requires an input field to find the text snippet containing the answer. Typically, the input field uses the [Topic](doc:topic) or [Document Range](doc:document-range) methods. |
| ❌ returns a multiple-answer response as a natural-language string | ✅ returns a multiple-answer response structured as an object or list of objects |

For more information about how this method works, see [Notes ](doc:draft-nlp-table#notes).

TODO: update links

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
        "question": "did US wheat production estimate change this month, and if so, by how much"
      }
    },
    {
      "id": "seed_use",
      "method": {
        "id": "question",
        "question": "what was US wheat seed use this year in the US in millions of bushels? "
      }
    },
    {
      "id": "seed_use_change",
      "method": {
        "id": "question",
        "question": "did US wheat seed use change this year and if so, by how much (in million bushels)?"
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
    "value": "No, the US wheat production estimate is unchanged this month."
  },
  "seed_use": {
    "type": "string",
    "value": "66 million bushels."
  },
  "seed_use_change": {
    "type": "string",
    "value": "Seed use was revised down 2 million bushels to 66 million for the 2022/23 based on planting expectations for the 2023/24 wheat crop."
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
      "method": {
        "id": "question",
        "question": "list the rents, how often the rent must be paid, and when the rent is due. don't include details about prorated rents or late fees"
      }
    },
    {
      "id": "late_fees",
      "method": {
        "id": "question",
        "question": "list late fees for late payments or bounced checks"
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
    "type": "string",
    "value": "Lessee shall pay 895.00 dollars per month for rent. Rent must be paid on or before the 1st day of each month. The first month's rent must be paid prior to move-in."
  },
  "late_fees": {
    "type": "string",
    "value": "Late fee rule: 10 Percent of Recurring Rent Only. A charge of $50 will apply for every returned check or rejected electronic payment plus the amount of any fees charged to the Owner/Agent by any financial institution as a result of the check not being honored, plus any applicable late fee charges."
  }
}
```



Notes
===

For an overview of how this method works, see the following steps:

- To meet GPT-3's character limit for input, Sensible splits the document into equal-sized, overlapping chunks. 
- Sensible scores each chunk by how well it matches the question you pose about the data you want to extract. To create the score, Sensible compares your question against each chunk using the OpenAPI Embeddings API. 
- Sensible selects a number of the top-scoring chunks and combines them.
- Sensible inputs the combined chunks to GPT-3 as one context, and instructs it to answer the question based on the context.