---
title: "Query Group"
hidden: false

---

Extracts individual facts in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery. Sensible uses a large language model (LLM)  to find these facts in paragraphs of free text, or in more structured layouts, for example key/value pairs or tables. Create a query group to extract multiple facts that share a [context](doc:query-group#notes), or are co-located in the document.

For tips and troubleshooting, see [Query Group](doc:query-group-tips) extraction tips.

For more information about how this method works, see [Notes](doc:query-group#notes).

[**Parameters**](doc:query-group#parameters)
[**Examples**](doc:query-group#examples)
[**Notes**](doc:query-group#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

**Note** You can configure some of the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrides the NLP preprocessor's parameter. For more information, see [Advanced prompt configuration](doc:prompt).



## Parameters

| key                   | value  | description                                                  |
| :-------------------- | :----- | :----------------------------------------------------------- |
| method (**required**) | object | For this object's parameters, see the following table.       |
| anchor                |        | The Anchor parameter is optional for fields that use this method.<br/><br/>If you specify an anchor and leave the Multimodal Engine unconfigured or configured with `"region": "automatic`" then:<br/>- Sensible ignores the anchor if it's present in the document.<br/>- Sensible returns null for the field if the anchor isn't present in the document.<br/><br/>If you specify an anchor and configure the Multimodal Engine parameter's region manually, then Sensible creates the prompt's [context](doc:query-group#notes) relative to the anchor. |

## Query group parameters



| key                    | value            | description                                                  |
| :--------------------- | :--------------- | :----------------------------------------------------------- |
| id (**required**)      | `queryGroup`     |                                                              |
| queries                | array of objects | An array of query objects, where each extracts a single fact and outputs a single field. Each query contains the following parameters:<br/>`id` (**required**) - The ID for the extracted field. <br/>`description`  (**required**) - A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`. For more information about how to write questions (or "prompts"), see [Query Group](https://docs.sensible.so/docs/query-group-tips) extraction tips. |
| chunkScoringText       | string           | Configures context's content. For details about context and chunks, see the Notes section.<br/>A representative snippet of text from the part of the document where you expect to find the answer to your prompt. Use this parameter to narrow down the page location of the answer to your prompt. For example, if your prompt has multiple candidate answers, and the correct answer is located near unique or distinctive text that's difficult to incorporate into your question, then specify the distinctive text in this parameter.<br/>If specified, Sensible uses this text to find top-scoring chunks. If unspecified, Sensible uses the prompt to score chunks.<br/>Sensible recommends that the snippet is specific to the target chunk, semantically similar to the chunk, and structurally similar to the chunk. <br/>For example,  if the chunk contains a street address formatted with newlines, then provide a snippet with an example street address that contains newlines, like `123 Main Street\nLondon, England`. If the chunk contains a street address in a free-text paragraph, then provide an unformatted street address in the snippet.<br/>For an example, see [Example 3](doc:query-group#example-3). |
| multimodalEngine       | object           | Configure this parameter to:<br/>- Troubleshoot extracting from complex text layouts, such as overlapping lines and lines between lines. Many such layouts can occur as a consequence of handwritten text. For example, use this as an alternative to the [Signature](doc:signature) method. This parameter can also be an alternative to the [Nearest Checkbox](doc:nearest-checkbox) method, or as an alternative to configuring the [OCR engine](doc:ocr-engine) or line [preprocessors](doc:preprocessors).<br/>- Extract data from images embedded in a document, for example, photos or diagrams.<br/><br/>This parameter sends an image of the document region containing the target data to a multimodal LLM engine for extraction.  This bypasses Sensible's OCR and direct-text extraction processes. Note that this option doesn't support confidence signals.<br/><br/>This parameter has the following parameters:<br/>`region`: The document region to send as an image to the multimodal LLM. Configurable with the following options :<br/>- To automatically select the [context](doc:query-group#notes) as the region, specify `"region": "automatic"`. <br/>- To manually specify a region relative to the field's anchor, specify the region using the [Region](doc:region) method's parameters, for example:<br/>`"region": { `<br/>          `"start": "below",`<br/>          `"width": 8,`<br/>          `"height": 1.2,`<br/>          `"offsetX": -2.5,`<br/>         `"offsetY": -0.25`<br/>          `}` |
| confidenceSignals      |                  | For information about this parameter, see [Advanced prompt configuration](doc:prompt). |
| contextDescription     |                  | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| pageHinting            |                  | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkCount             | default: 5       | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkSize              | default: 0.5     | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| chunkOverlapPercentage | default: 0.5     | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |
| pageRange              |                  | For information about this parameter, see [Advanced prompt configuration](doc:prompt#parameters). |

## Examples

The following example shows using the Query Group method to extract information from a lease.

**Config**

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "tenancy_terms_start",
            "description": "tenancy terms start date",
            "type": "date"
          },
          {
            "id": "tenancy_terms_end",
            "description": "tenancy terms end date",
            "type": "date"
          },
          {
            "id": "notice_days_tenant_break",
            "description": "number of days notice for tenant must give to terminate lease",
            "type": "string"
          },
          {
            "id": "monthly_rents_dollars",
            "description": "monthly rents in dollars",
            "type": "currency"
          },
          {
            "id": "rent_due_in_month",
            "description": "when is the rent due in the month",
            "type": "string"
          },
          {
            "id": "grace_period_rent_due",
            "description": "grace period for the rent due",
            "type": "string"
          },
          {
            "id": "late_fee_amounts",
            "description": "late fee amount",
            "type": "string"
          },
          {
            "id": "fee_returned_checks",
            "description": "fee in dollars for returned checks or rejected payments",
            "type": "currency"
          }
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question_2.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "tenancy_terms_start": {
    "source": "01/01/2022",
    "value": "2022-01-01T00:00:00.000Z",
    "type": "date",
    "confidenceSignal": "confident_answer"
  },
  "tenancy_terms_end": {
    "source": "12/31/2023",
    "value": "2023-12-31T00:00:00.000Z",
    "type": "date",
    "confidenceSignal": "confident_answer"
  },
  "notice_days_tenant_break": {
    "value": "30 days",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "monthly_rents_dollars": {
    "source": "895.00",
    "value": 895,
    "unit": "$",
    "type": "currency",
    "confidenceSignal": "confident_answer"
  },
  "rent_due_in_month": {
    "value": "on or before the 1st day of each month",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "grace_period_rent_due": {
    "value": "5 days",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "late_fee_amounts": {
    "value": "10 Percent of Recurring Rent Only",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "fee_returned_checks": {
    "source": "$50",
    "value": 50,
    "unit": "$",
    "type": "currency",
    "confidenceSignal": "confident_answer"
  }
}
```

## Notes

For an overview of how this method works, see the following steps:

- To meet the LLM's token limit for input, Sensible splits the document into equal-sized, overlapping chunks.
- Sensible scores each chunk by its similarity to either the concatenated Description parameters for the queries in the group, or by the `chunkScoringText` parameter. Sensible scores each chunk using the OpenAPI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks. If you set chunk-related parameters that cause the context to exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.
- Sensible creates a full prompt for the LLM (GPT-3.5 Turbo) that includes the chunks, page hinting data, and your Description parameters. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt).

How location highlighting works
---

In the Sensible Instruct editor, you can click the search icon to the right of the output of a query field to view its source text in the document. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/location.png)

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
