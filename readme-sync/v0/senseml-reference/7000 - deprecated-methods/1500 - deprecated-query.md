---
title: "(Deprecated) Query"
hidden: true

---

# Deprecated

The Query method is deprecated. The Query Group method replaces this method. See [Query Group](doc:query-group) for more information.

## Description

This method extracts individual facts in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery. Sensible uses a large-language model (LLM)  to find these facts in paragraphs of free text, or in more structured layouts, for example key/value pairs or tables.

Sensible recommends framing each query, or prompt, so that it has a single, short answer.  For complex prompts with multi-part answers, use the [List method](doc:list) or the  [Summarizer](doc:summarizer) method. 

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

**Note** You can configure some the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrrides the NLP preprocessor's parameter. For more information, see [Advanced prompt configuration](doc:prompt).

Parameters
=====



| key                                 | value        | description                                                  |
| :---------------------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)                   | `query`      | The Anchor parameter is optional for fields that use this method. If you specify an anchor:<br/>- Sensible ignores the anchor if it's present in the document.<br/>- Sensible returns null for the field if the anchor isn't present in the document. |
| description(**required**)           | string       | A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`.   |
| chunkScoringText                    | string       | Configures context's content. For details about context and chunks, see the Notes section.<br/>A representative snippet of text from the part of the document where you expect to find the answer to your prompt. Use this parameter to narrow down the page location of the answer to your prompt. For example, if your prompt has multiple candidate answers, and the correct answer is located near unique or distinctive text that's difficult to incorporate into your question, then specify the distinctive text in this parameter.<br/>If specified, Sensible uses this text to find top-scoring chunks. If unspecified, Sensible uses the prompt to score chunks.<br/>Sensible recommends that the snippet is specific to the target chunk, semantically similar to the chunk, and structurally similar to the chunk. <br/>For example,  if the chunk contains a street address formatted with newlines, then provide a snippet with an example street address that contains newlines, like `123 Main Street\nLondon, England`. If the chunk contains a street address in a free-text paragraph, then provide an unformatted street address in the snippet.<br/>For an example, see Example 3.<br/> |
| (**Deprecated**) promptIntroduction | string.      | **(Deprecated)**  overwrites the introductory text at the beginning of the [full prompt](https://docs.sensible.so/docs/prompt) that Sensible submits to the LLM for this field. |
| confidenceSignals                   |              | For information about this parameter, see [Advanced prompt configuration](doc:prompt). |
| contextDescription                  |              | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| pageHinting                         |              | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkCount                          | default: 5   | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkSize                           | default: 0.5 | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkOverlapPercentage              | default: 0.5 | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| pageRange                           |              | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |

Examples
====

Example 1
---

The following example shows using the Query Group method to extract agricultural data from a government report.

**Config**

```json
{
	"fields": [{
			"id": "report_date",
			"method": {
				"id": "query",
				"description": "for which month and year does this snippet describe wheat production"
			}
		},
		{
			"id": "change_in_production",
			"method": {
				"id": "query",
				"description": "by what amount did US wheat production estimate change this month? if it didn't change, respond with 'no change'"
			}
		},
		{
			"id": "seed_use",
			"method": {
				"id": "query",
				"description": "what was US wheat seed use this year in the US in millions of bushels?"
			}
		},
		{
			"id": "seed_use_change",
			"method": {
				"id": "query",
				"description": "by what amount did US wheat seed use change this year, in million bushels? Use a negative sign for negative change and a positive sign for positive change"
			}
		},
		{
			"id": "global_consumption_change",
			"method": {
				"id": "query",
				"description": "by what amount did global wheat production change this year, measured in MMT? look near the end of the document for the answer"
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
	},
	"global_consumption_change": {
		"type": "string",
		"value": "1.0 MMT"
	}
```




Example 2
----

The following example shows using the Query Group method to extract information from a lease.

**Config**

```json
{
  "fields": [
    {
      "id": "rents",
      "type": "currency",
      "method": {
        "id": "query",
        "description": "what's the rents amount in dollars? don't include details about when it's due"
      }
    },
    {
      "id": "rent_due",
      "method": {
        "id": "query",
        "description": "when is the rent due? don't include details about grace periods"
      }
    },
    {
      "id": "rent_frequency",
      "method": {
        "id": "query",
        "description": "how often must the rent be paid? return responses like 'monthly', 'quarterly', or 'biweekly'"
      }
    },
    /* if you ask a multi-part question, you get back
       a natural-language answer.
       As an alternative, use the Summarizer method to structure
       such multi-part responses  */
    {
      "id": "rents_multi_part_question",
      "method": {
        "id": "query",
        "description": "list the rents, how often the rent must be paid, and when the rent is due. don't include details about prorated rents or late fees"
      }
    },
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question_2.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer.pdf) |
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




Example 3
----

The following example shows using chunk-related parameters to narrow down the page location of an answer in a document.

```json
{
  "fields": [
    {
      "id": "reinsured",
      "method": {
        "id": "query",
        "description": "Return the reinsured company name for this policy?",
        /*   the document mentions the fictional
            "EF Signorta Sirketi" company as also reinsured. 
            chunkScoringText forces Sensible to 
            return the fictional company AB Signorta Sirketi instead */
        "chunkScoringText": "Retrocedant's Address: \n 10 Lime Street \n REINSURED: SCOR UK Company Limited ",
        
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
- Sensible scores each chunk by its similarity to either the `description` or the `chunkScoringText` parameters. Sensible scores each chunk using the OpenAPI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks. If you set chunk-related parameters that cause the context to exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.
- Sensible creates a full prompt for the LLM (GPT-3.5 Turbo) that includes the chunks, page hinting data, and your prompt. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt).

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
