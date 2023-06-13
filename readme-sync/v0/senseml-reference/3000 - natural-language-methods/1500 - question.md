---
title: "Question"
hidden: false

---

Extracts individual facts in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery. It can find these facts in paragraphs of free text or in more structured layouts, for example key/value pairs or tables.

Sensible recommends framing each question, or prompt, so that it has a single, short answer.  For complex prompts with multi-part answers, use the [List method](doc:list) or the  [Summarizer](doc:summarizer) method. 

For tips and troubleshooting, see [Query tips](doc:query-tips).

For more information about how this method works, see [Notes ](doc:question#notes).

[**Parameters**](doc:question#parameters)
[**Examples**](doc:question#examples)
[**Notes**](doc:question#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key                     | value                             | description                                                  |
| :---------------------- | :-------------------------------- | :----------------------------------------------------------- |
| id (**required**)       | `question`                        | The Anchor parameter is optional for fields that use the Question method. If you specify an anchor, Sensible ignores it. |
| question (**required**) | string                            | A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`.  For more information about how to write questions (or "prompts"), see [Best practices for prompt engineering with OpenAI](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api). |
| chunkScoringText        | string                            | Configures context's content.<br/>A representative snippet of text from the part of the document where you expect to find the answer to your prompt. Use this parameter to narrow down the page location of the answer to your prompt. For example, if your prompt has multiple candidate answers, and the correct answer is located near unique or distinctive text that's difficult to incorporate into your question, then specify the distinctive text in this parameter.<br/>If specified, Sensible uses this text to find top-scoring chunks. If unspecified, Sensible uses the prompt to score chunks.<br/>Sensible recommends that the snippet is specific to the target chunk, semantically similar to the chunk, and structurally similar to the chunk. <br/>For example,  if the chunk contains a street address formatted with newlines, then provide a snippet with an example street address that contains newlines, like `123 Main Street\nLondon, England`. If the chunk contains a street address in a free-text paragraph, then provide an unformatted street address in the snippet.<br/>For an example, see [Example 3](doc:question#example-3).<br/>For details about context and chunks, see the Notes section. |
| chunkCount              | number. default: `5`              | Configures context's size.<br/>The number of top-scoring chunks Sensible combines as context for the prompt it poses to a large-language model (LLM).<br/>For details about context and chunks, see the Notes section. |
| chunkSize               | `0.5`, `1` default: `0.5`         | Configures context's size.<br/>The size of the chunks Sensible splits the document into, as a page fraction. For example, `0.5` specifies each chunk is half a page. <br/>For details about context and chunks, see the Notes section. |
| chunkOverlapPercentage  | `0`, `0.25`, `0.5` default: `0.5` | Configures context's size.<br/>The extent to which chunks overlap, as a percentage of the chunks' height. For example, `0.5` specifies each chunk overlaps by half its height. <br/>For details about context and chunks, see the Notes section |

Examples
====

Example 1
---

The following example shows using the Question method to extract agricultural data from a government report.

**Config**

```json
{
	"fields": [{
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
		},
		{
			"id": "global_consumption_change",
			"method": {
				"id": "question",
				"question": "by what amount did global wheat production change this year, measured in MMT? look near the end of the document for the answer"
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
	},
	"global_consumption_change": {
		"type": "string",
		"value": "1.0 MMT"
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




Example 3
----

The following example shows using chunk-related parameters to narrow down the page location of an answer in a document.

```json
{
  "fields": [
    {
      "id": "reinsured",
      "method": {
        "id": "question",
        "question": "Return the reinsured company name for this policy?",
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

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/question_chunk.pdf) |
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

For an overview of how this method works, see the following steps:

- To meet GPT-3's character limit for input, Sensible splits the document into equal-sized, overlapping chunks.
- Sensible scores each chunk by its similarity to either the `question` or the `chunkScoringText` parameters. Sensible scores each chunk using the OpenAPI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them. The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks.
- Sensible inputs the combined chunks to GPT-3 as one context, and instructs it to answer the prompt based on the context.
