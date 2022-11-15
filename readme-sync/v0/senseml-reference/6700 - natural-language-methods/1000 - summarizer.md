---
title: "Summarizer draft"
hidden: true
---
Automatically extracts key/value pairs from short snippets of free text using [OpenAI's GPT-3 completion API](https://beta.openai.com/docs/). The Summarizer computed field method takes as input a snippet of free text, and extracts key/value pairs based on instructions or short samples of extracted values you provide. 

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value        | description                                                  |
| :----------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)        | `summarizer` |                                                              |
| source_id (**required**) | field ID     | Specifies a field whose output is a snippet of text with the key/value information you want to extract. If the snippet doesn't occur at a predictable location in the document, then you can use the [Topic](doc:topic) method to find it. |
| fields (**required**)    | string array | Names of the keys you want to extract. These names have an impact on the free-text extraction, so choose names that have a meaningful relationship to the target data to extract. For example, for a dollar amount of rent to extract,  `rent`, `rents`, and `rent_in_dollars` are good naming choices. |
| instructions             | string       | Natural-language instructions about how to extract information from the text in the Source ID parameter.<br/>For more information about how to write instructions, see [GPT-3 Completions documentation](https://beta.openai.com/docs/guides/completion/introduction).<br/>For an example of using this parameter, see the Examples section. |
| samples                  | object array | Short snippets of text containing examples of how to extract information from the text in the Source ID parameter. <br/>Use in addition to the Instructions parameter to increase GPT-3 accuracy. <br/>Contains these parameters:<br/>`prompt` (string): A free-text example of the information you want to extract.<br/>`values` (string array):  The target information to extract from this prompt. This array is a parallel array to the Fields parameter's array. Parallel arrays are the same length and same sequence. If GPT-3 can't find the target information in the Source ID parameter, it can generate an arbitrary value. To override this behavior, specify a Sample parameter whose Prompt parameter has a text snippet that's missing the target data, and whose Values array indicates the data is missing (for example, "N/A" or "not found").<br/>For an example of using this parameter, see the Examples section. |

Examples
====

Example 1
---

The following example shows using the Summarizer method with the Topic method to extract disease prevalence  information from a research article.

**Config**

```json
{
  "fields": [
    {
      "id": "_source_results_topic",
      "anchor": {
        "match": {
          "type": "first"
        }
      },
      "method": {
        "id": "topic",
        /* grab Results paragraph 
           as input for Summarizer method */
        "terms": [
          "prevalence",
          "per"
        ],
        "numLines": 10
      }
    }
  ],
  "computed_fields": [
    {
      "id": "summarized",
      "method": {
        "id": "summarizer",
        "source_id": "_source_results_topic",
        /* instructions for GPT3 for extracting data from source paragraph*/
        "instructions": "List all the diseases and disease subtypes mentioned below along with their population prevalence, country or region, and year, if applicable",
        /* the field IDs GPT3 must apply to the extracted data */
        "fields": [
          "disease",
          "prevalence",
          "region_or_country",
          "year"
        ],
        /* OPTIONAL SAMPLES:
          examples of which values to extract
          from a text snippet
          similar to _source_results_topic   */
        "samples": [
          {
            "prompt": "Prevelance of diabetes was 3 in 10,000, CHD was 10 in 10,000, and cancer was 7 in 10,000 across the population sampled in the United States, 2008-2010.",
            "values": [
              [
                "diabetes",
                "3 in 10,000",
                "United States",
                "2008-2010"
              ],
              [
                "CHD",
                "10 in 10,000",
                "United States",
                "2008-2010"
              ],
              [
                "cancer",
                "7 in 10,000",
                "United States",
                "2008-2010"
              ]
            ]
          }
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/summarizer_pubmed.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_pubmed.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "_source_results_topic": {
    "type": "string",
    "value": "NTDs per 10,000 births, including live and stillborn cases. Results: The meta-analysis included 20 studies consisting of 752,936 individuals. The pooled prevalence of all NTDs 2 per 10,000 births in Eastern Africa was 33.30 (95% CI: 21.58 to 51.34). Between-study heterogeneity was high (I = 97%, p < 0.0001), The rate was highest in Ethiopia (60 per 10,000). Birth prevalence of spina bifida (20 per 10,000) was higher than anencephaly (9 per 10,000) and encephalocele (2.33 per 10,000). No studies on NTDs were identified in 70% of the UN Eastern Africa region. Birth prevalence increased by 4% per year from 1983 to 2018. The level of evidence as qualified with GRADE was moderate. Conclusion: The birth prevalence of NTDs in the United Nations region of Eastern Africa is 5 times as high as observed in Western countries with mandatory folic acid supplementation in place. Therefore, mandatory folic acid"
  },
  "summarized": [
    {
      "disease": "NTDs",
      "prevalence": "2 per 10,000",
      "region_or_country": "Eastern Africa",
      "year": "1983-2018"
    },
    {
      "disease": "spina bifida",
      "prevalence": "20 per 10,000",
      "region_or_country": "Eastern Africa",
      "year": "1983-2018"
    },
    {
      "disease": "anencephaly",
      "prevalence": "9 per 10,000",
      "region_or_country": "Eastern Africa",
      "year": "1983-2018"
    },
    {
      "disease": "encephalocele",
      "prevalence": "2.33 per 10,000",
      "region_or_country": "Eastern Africa",
      "year": "1983-2018"
    }
  ]
}
```




Example 2
----

The following example shows using the Summarizer method and the Topic method to extract the following information from a lease:

- monthly rent
- payment frequency 
- payment due date

**Config**

```json
{
  "fields": [
    {
      /* grab Rents paragraph 
           as input for Summarizer method */
      "id": "_source_rent_topic_paragraphs",
      "anchor": {
        "match": {
          "type": "first"
        }
      },
      "method": {
        "id": "topic",
        "numParagraphs": 2,
        "terms": [
          "pay",
          "leesee",
          "rent",
          "dollars"
        ]
      }
    }
  ],
  "computed_fields": [
    {
      "id": "rent_computed",
      "method": {
        "id": "summarizer",
        "source_id": "_source_rent_topic_paragraphs",
        /* instructions for GPT3 for extracting data from source paragarph */
        "instructions": "list the rents, how often the rent must be paid, and when the rent is due",
        /* the field IDs GPT3 must apply to the extracted data */
        "fields": [
          "rent_in_dollars",
          "payment_time_period",
          "payment_due"
        ],
        /* OPTIONAL SAMPLES:
          examples of which values to extract
          from text snippets
          similar to _source_rent_topic_paragraphs   */
        "samples": [
          {
            "prompt": "Rent 8. Subject to the provisions of this short-term Lease, the rent for the Property is $234.00 on Monday each and every week (the \"Rent\").",
            "values": [
              "$234.00",
              "week",
              "Monday"
            ]
          },
          {
            "prompt": "Rent for this commerical property is due in advance on the first day of the quarter, at $20,125.00 per quarter, beginning on November 15, 2015, payable to Owner/Agent at 123 Main Blvd., Sacramento, CA 95864. Payments made in person may be delivered to Owner/Agent between the hours of 24/Z.",
            "values": [
              "$20,125.00",
              "quarter",
              "first day of the quarter"
            ]
          },
          {
            "prompt": "Leesee must pay rents biweekly. For the dollar amount due, see addendum A.",
            "values": [
              "not found",
              "biweekly",
              "not found"
            ]
          }
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/summarizer.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "_source_rent_topic_paragraphs": {
    "type": "string",
    "value": "Lessee shall pay 895.00 dollars per month for rent. The first month's rent and/or prorated rent amount shall be due prior to move-in. For any move in date that is after the 15th of the month, Tenant must pay a full month of rent in order to gain possession of the home. The prorated rent amount will be due the second month of lease. Every month thereafter, Lessee must pay rent on or before the 1st day of each month with 5 days of grace period. The following late fees will apply for payments made after the grace period:"
  },
  "rent_computed": [
    {
      "rent_in_dollars": "$895.00",
      "payment_time_period": "month",
      "payment_due": "on or before the 1st day of each month"
    }
  ]
}
```

