---
title: "Query group"
hidden: true

---

Extracts individual facts in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery. 

- When you configure the Multimodal Engine parameter, this method can extra data from non-text images, such as photographs, charts, or illustrations. For an example, see [Example: Extract from images](doc:query-group#example-extract-from-images).
- When you configure the Source Fields parameter, you can use an LLM prompt to transform the extracted facts. For example, TBD/TODO take from summarizer lanugage

#### Prompt Tips

Sensible recommends grouping queries together if they share [context](doc:query-group#notes).  Queries share context when data exists in the same location or region of a document, for example, on the same page.

For example, contact information can usually be found in the same location of a document:

```json
Janelle Smith
New York City, NY
(123) 456-7890
jsmith@email.com 
```

Combining queries for the custom name, location, phone number, and email into the same group will help you maximize the accuracy and speed of your extractions. Frame each query, or prompt, in the group so that it has a single, short answer. Sensible recommends a maximum group size of 10 queries.

- Try framing each query, or prompt, so that it has a single, short answer such as:

  - "company address"
  - "name of recipient"
  - "document date"
- See the following resources for creating prompts:

  -  [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering)
  -  [Introduction to prompt engineering](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/prompt-engineering)
  -  [Short course: Building systems with the ChatGPT API](https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/) and [Short course: ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/). 

For information about how this method works, see [Notes](doc:query-group#notes).

[**Parameters**](doc:query-group#parameters)
[**Examples**](doc:query-group#examples)
[**Notes**](doc:query-group#examples)

Parameters
=====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method. 

**Note** You can configure some of the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrides the NLP preprocessor's parameter.

## Parameters

| key                   | value  | description                                                  |
| :-------------------- | :----- | :----------------------------------------------------------- |
| method (**required**) | object | For this object's parameters, see the following table.       |
| anchor                |        | The Anchor parameter is optional for fields that use this method.<br/><br/>If you specify an anchor and leave the Multimodal Engine unconfigured or configured with `"region": "automatic`" then:<br/>- Sensible ignores the anchor if it's present in the document.<br/>- Sensible returns nulls for the fields in this query group if the anchor isn't present in the document.<br/><br/>If you specify an anchor and configure the Multimodal Engine parameter's region manually, then Sensible creates the prompt's [context](doc:query-group#notes) relative to the anchor. |

## Query group parameters



| key                    | value            | description                                                  | interactions                                                 |
| :--------------------- | :--------------- | :----------------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)      | `queryGroup`     |                                                              |                                                              |
| queries                | array of objects | An array of query objects, where each extracts a single fact and outputs a single field. Each query contains the following parameters:<br/>`id` (**required**) - The ID for the extracted field. <br/>`description`  (**required**) - A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`. For more information about how to write questions (or "prompts"), see [Query Group](https://docs.sensible.so/docs/query-group-tips) extraction tips. |                                                              |
| chunkScoringText       | string           | Use this parameter to narrow down the page location of the answer to your prompt. For details about context and chunks, see the Notes section.<br/>A representative snippet of text from the part of the document where you expect to find the answer to your prompt.  For example, if your prompt has multiple candidate answers, and the correct answer is located near unique or distinctive text that's difficult to incorporate into your question, then specify the distinctive text in this parameter.<br/>If specified, Sensible uses this text to score chunks' relevancy. If unspecified, Sensible uses the prompt to score chunks.<br/>Sensible recommends that the snippet is specific to the target chunk, semantically similar to the chunk, and structurally similar to the chunk. <br/>For example,  if the chunk contains a street address formatted with newlines, then provide a snippet with an example street address that contains newlines, like `123 Main Street\nLondon, England`. If the chunk contains a street address in a free-text paragraph, then provide an unformatted street address in the snippet. | If you set the Search By Summarization parameter to true, Sensible ignores any configured value for this parameter. |
| multimodalEngine       | object           | Configure this parameter to:<br/>- Extract data from images embedded in a document, for example, photos, charts, or illustrations.<br/>- Troubleshoot extracting from complex text layouts, such as overlapping lines, lines between lines, and handwriting. For example, use this as an alternative to the [Signature](doc:signature) method, the [Nearest Checkbox](doc:nearest-checkbox) method, the [OCR engine](doc:ocr-engine), and line [preprocessors](doc:preprocessors).<br/><br/>This parameter sends an image of the document region containing the target data to a multimodal LLM (GPT-4o mini), so that you can ask questions about text and non-text images. This bypasses Sensible's [OCR](doc:ocr) and direct-text extraction processes for the region. <br/>This parameter has the following parameters:<br/><br/>`region`: The document region to send as an image to the multimodal LLM. Configurable with the following options :<br/><br/>- To automatically select the [context](doc:query-group#notes) as the region, specify `"region": "automatic"`. If you configure this option for a non-text image, then help Sensible locate the context by including queries in the group that target text near the image, or by specifying the nearby text in the Chunk Scoring Text parameter. <br/><br/>- To manually specify a region, specify an [anchor](doc:anchor) close to the region you want to capture. Specify the region's dimensions in inches relative to the anchor using the [Region](doc:region) method's parameters, for example:<br/>`"region": { `<br/>          `"start": "below",`<br/>          `"width": 8,`<br/>          `"height": 1.2,`<br/>          `"offsetX": -2.5,`<br/>         `"offsetY": -0.25`<br/>          `}` | If you configure this parameter, Sensible doesn't support confidence signals for the multimodal output. |
| llmEngine              | object           | Where applicable, configures the LLM engine Sensible uses to answer your prompts. <br/>Configure this parameter to troubleshoot situations in which Sensible correctly identifies the part of the document that contains the answers to your prompts, but the LLM's answer contains problems. For example, Sensible returns an LLM error because the answer isn't properly formatted, or the LLM doesn't follow instructions in your prompt.<br/><br/>Contains the following parameters:<br/>`provider`:  <br/>- If set to `open-ai` (default), Sensible uses GPT-4o mini  where not hard coded. See the Notes section for more information.  <br/> - If set to `anthropic`, Sensible uses Claude 3 Haiku where not hard coded. See the Notes section for more information. |                                                              |
| searchBySummarization  |                  | or information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters). |                                                              |
| confidenceSignals      |                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt). |                                                              |
| contextDescription     |                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters). |                                                              |
| pageHinting            |                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters). |                                                              |
| chunkCount             |                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters). |                                                              |
| chunkSize              |                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters). |                                                              |
| chunkOverlapPercentage |                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters). |                                                              |
| pageRange              |                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters). |                                                              |

## Examples

### Example: Extract from images

**Config**

The following example shows extracting structured data from real estate photographs embedded in an offering memorandum document using the Multimodal Engine parameter. It also shows extracting data from text.

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        /* send 2 pages as context to the LLM */
        "chunkSize": 1,
        "chunkCount": 2,
        /* Use a multimodal LLM to extract data about a photograph embedded in a document, 
          for example the presence or absence of trees in the photo. */
        "multimodalEngine": {
          /* Sends the "context", or relevant document excerpt, as an image to the multimodal LLM.
           If you configure "region":"automatic" for a non-text image, 
           then help Sensible locate the context by including queries 
           in the group that target text near the image, or by specifying 
           the nearby text in the Chunk Scoring Text parameter */
          "region": "automatic"
        },
        "queries": [
          {
            "id": "trees_present",
            "description": "are there trees on the property? respond true or false",
            "type": "string"
          },
          {
            "id": "multistory",
            "description": "are the buildings multistory? return true or false",
            "type": "string"
          },
          {
            "id": "community_amenities",
            "description": "give one example of a community amenity listed",
            "type": "string"
          },
          {
            "id": "ownership_upgrades",
            "description": "give one example of an existing upgrade that current ownership made",
            "type": "string"
          },
          {
            "id": "exterior",
            "description": "what is the exterior of the building made of (walls, not roof)?",
            "type": "string"
          },
        ]
      }
    },
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/multimodal_photo.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/multimodal_photo.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "trees_present": {
    "value": "true",
    "type": "string",
    "confidenceSignal": "not_supported"
  },
  "multistory": {
    "value": "true",
    "type": "string",
    "confidenceSignal": "not_supported"
  },
  "community_amenities": {
    "value": "Gated perimeter with key card access",
    "type": "string",
    "confidenceSignal": "not_supported"
  },
  "ownership_upgrades": {
    "value": "New Signage and Landscaping Enhancements",
    "type": "string",
    "confidenceSignal": "not_supported"
  },
  "exterior": {
    "value": "brick",
    "type": "string",
    "confidenceSignal": "not_supported"
  }
}
```

### Example: Extract handwriting

The following example shows using a multimodal LLM to extract from a scanned document containing handwriting. For an alternate approach to extracting from this document, see also the [Sort Lines](doc:method#sort-lines-example) example.

**Config**

```json
{
  "preprocessors": [
    /* Returns confidence signals, or LLM accuracy qualifications,
       for all supported fields. Note that confidence signals aren't supported
       for the Multimodal Engine parameter */
    {
      "type": "nlp",
      "confidenceSignals": true
    }
  ],
  "fields": [
    {
      /* use an anchor match to locate the 
         region, or relevant document excerpt,
          to send as an image to the multimodal LLM */
      "anchor": "ownership information",
      "method": {
        "id": "queryGroup",
        /* Use a multimodal LLM to troubleshoot
           problems with Sensible's default OCR engine and line merging.
           This 1-step option avoids advanced configuration of the defaults.
             */
        "multimodalEngine": {
          /* manually specify the region's dimensions in inches 
         relative to the anchor. Use the green region overlay in the
         rendered PDF to determine the dimensions */
          "region": {
            "start": "below",
            "width": 8,
            "height": 6,
            "offsetX": -1.5,
            "offsetY": 0.05
          }
        },
        "queries": [
          {
            "id": "ownership_type",
            "description": "What is type of ownership?",
            "type": "string"
          },
          {
            "id": "owner_name",
            "description": "What is the full name of the owner?",
            "type": "string"
          }
        ]
      }
    },
    /* Without the multimodal LLM engine, Sensible's default
       OCR, line sorting, and line merging options result 
      in incorrect answers. */
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "ownership_type_no_multimodal",
            "description": "What is the type of ownership?",
            "type": "string"
          },
          {
            "id": "owner_name_no_multimodal",
            "description": "What is the full name of the owner?",
            "type": "string"
          }
        ]
      }
    }
  ],
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/multimodal.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/xmajor_sort.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "ownership_type": {
    "value": "Natural Person(s)",
    "type": "string",
    "confidenceSignal": "not_supported"
  },
  "owner_name": {
    "value": "Kyle Murray",
    "type": "string",
    "confidenceSignal": "not_supported"
  },
  "ownership_type_no_multimodal": {
    "value": "Natural Person(s) UGMA/UTMACustodian Trust",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "owner_name_no_multimodal": {
    "value": "Mylic Cardinals Dr Glendale A2 85305",
    "type": "string",
    "confidenceSignal": "confident_answer"
  }
}
```




### Example: Extract from lease

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

- For an overview of how this method works when `"searchBySummarization": false`, see the following steps.   

  - To meet the LLM's token limit for input, Sensible splits the document into equal-sized, overlapping chunks.
  - Sensible scores each chunk by its similarity to either the concatenated Description parameters for the queries in the group, or by the `chunkScoringText` parameter. Sensible scores each chunk using the OpenAPI Embeddings API.
  - Sensible selects a number of the top-scoring chunks and combines them into "context". The chunks can be non-consecutive in the document. Sensible deduplicates overlapping text in consecutive chunks. If you set chunk-related parameters that cause the context to exceed the LLM's token limit, Sensible automatically reduces the chunk count until the context meets the token limit.
  - Sensible creates a full prompt for the LLM (as determined by the LLM Engine parameter) that includes the chunks, page hinting data, and your Description parameters. For more information about the full prompt, see [Advanced LLM prompt configuration](doc:prompt).

- For an overview of how this method works when `"searchBySummarization": true`, see the following steps.
  1. Sensible prompts an LLM (GPT-4o mini) to summarize each page in the document. Sensible ignores the Chunk Scoring Text parameter.
  
  2. Sensible prompts an LLM (GPT-4o) with all the indexed page summaries as context, and asks it to return a number of page indices that are most relevant to your concatenated Description parameters. The Chunk Count parameter configures the number of page indices that the LLM returns. Sensible recommends setting the Chunk Count parameter to less than 10.
  
  3. Sensible prompts an LLM (as configured by the LLM Engine parameter) to answer your prompts, with the full text of the relevant pages as context. If you configure the Page Hinting parameter, it takes effect in this and the preceding step. If you configure the Multimodal Engine parameter, it takes effect in this step. 

