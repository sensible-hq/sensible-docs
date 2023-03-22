---
title: "Question"
hidden: false

---



Best practices/tips

- Best suited for labeled data

- When extracting non-labelled data, using layout based language helps (for example, what is the company name in the top left of the document)

- Being as specific as possible will give the best results (including location, section of the document, type of data, page number, etc.)

- “Positional” directions work (i.e. what is the name in the top left)

- Capable of manipulating output in the question. For example, asking a question and following that with “where unchecked boxes mean no” will output no for unchecked boxes

**how to author this method**

See - resources TBD TODO (video, getting started, etc)

Examples
===

![image-20230322130112047](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230322130112047.png)

**try it out**

TODO provide PDF download link

provide list of questions:


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