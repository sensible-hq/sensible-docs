---
title: "Query group"
hidden: true

---


====

Example 1 - WORKING
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




Example 2


Example 3
----

The following example shows using chunk-related parameters to narrow down the page location of an answer in a document.

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "chunkScoringText": "Retrocedant's Address: \n 10 Lime Street \n REINSURED: SCOR UK Company Limited ",
        "queries": [
          {
            "id": "reinsured_company_name",
            "description": "Return the reinsured company name for this policy?",
            "type": "string"
          }
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question_chunk.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/question_chunk.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "reinsured": {
    "type": "string",
    "value": "AB Sigorta Sirketi"
  }
}
```

Notes
===

How the Query Group method works
---

For an overview of how this method works, see the following steps:

- To meet the LLM's token limit for input, Sensible splits the document into equal-sized, overlapping chunks.
- Sensible scores each chunk by its similarity to either the `description` in the first query field in the group, or by or the `chunkScoringText` parameters. Sensible scores each chunk using the OpenAPI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks. If you set chunk-related parameters that cause the context to exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.
- Sensible creates a full prompt for the LLM (GPT-3.5 Turbo) that includes the chunks, page hinting data, and your prompts in the group. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt).

How location highlighting works
---

In the Sensible Instruct editor, you can click the output of a query field to view its source text in the document. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/changelog_August2023_location.png)

For an overview of how Sensible finds the source text in the document for the LLM's response, see the following steps:

- The LLM returns a response to your prompt.

- Sensible searches in the source document for a line that's a fuzzy match to the response.  For example, if the LLM returns `4387-09-22-33`, Sensible matches the line `Policy Number: 4387-09-22-33` in the document. Sensible implements fuzzy matching using [Levenshtien distance](https://en.wikipedia.org/wiki/Levenshtein_distance).

- Sensible selects the three lines in the document that contain the best fuzzy matches. For each line, Sensible concatenates the preceding and succeeding lines, in case the match spans multiple lines.
- Sensible searches for a fuzzy match in the concatenated lines for the text that the LLM returned.  Sensible returns the best match.
- Sensible highlights the best match in the document in the Sensible Instruct editor or in the SenseML editor.

**Limitations**

Sensible can highlight the incorrect location under the following circumstances:

- If you prompt the LLM to reformat the source text in the document or reformat the text using a [type](doc:types) , then Sensible can fail to find a match or can find an inaccurate match.

- If there are multiple candidates fuzzy matches in the document (for example, two instances of `April 7`), Sensible chooses the top-scoring match. If candidates have similar scores, Sensible uses page location as a tie breaker and chooses the earliest match in the document.

- If the LLM returns text that's not in the document, then location highlighting is inapplicable.
