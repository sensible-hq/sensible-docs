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
| samples                  | object array | Short snippets of text containing examples of how to extract information from the text in the Source ID parameter. <br/>Use in addition to the Instructions parameter to increase GPT-3 accuracy. <br/>Contains these parameters:<br/>`prompt` (string): A free-text example of the information you want to extract.<br/>`values` (string array):  The target information to extract from this prompt. This array is a parallel array to the Fields parameter's array (the same length and same sequence). If GPT-3 can't find the target information in the Source ID parameter, it can generate an arbitrary value. To override this behavior, specify a Sample parameter whose Prompt parameter has a text snippet that's missing the target data, and whose Values array indicates the data is missing (for example, "N/A" or "not found").<br/>For an example of using this parameter, see the Examples section. |

Examples
====

Example 1
---




Example 2
----

The following example shows using the Summarizer method configured with the Instructions parameter to extract the following information from a lease:

- monthly rent
- payment frequency 
- payment due date

In a production scenario, you can use the Samples parameter in addition to the Instructions parameter if you want to increase GPT-3's accuracy.



**Config**

```json
{
  "fields": [
    {
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
        "fields": [
          "rent_in_dollars",
          "payment_time_period",
          "payment_due"
        ],
        "prompt": "list the rents, how often the rent must be paid, and when the rent is due"
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
      "rent_in_dollars": "895.00",
      "payment_time_period": "monthly",
      "payment_due": "1st of month"
    }
  ]
}
```

Example 3
----

The following example shows using the Summarizer method configured with the Samples parameter to extract the following information from a lease:

- monthly rent
- payment frequency 

In a production scenario, you can use the Samples parameter in addition to the Instructions parameter if you want to increase GPT-3's accuracy.

**Config**

```json
{
  "fields": [
    {
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
        "fields": [
          "rent_in_dollars",
          "payment_time_period"
        ],
        "samples": [
          {
            "prompt": "Rent 8. Subject to the provisions of this short-term Lease, the rent for the Property is $234.00 each and every week (the \"Rent\").",
            "values": [
              "$234.00",
              "week"
            ]
          },
          {
            "prompt": "Rent for this commerical property is due in advance on the ist day of the quarter, at $20,125.00 per quarter, beginning on November 15, 2015, payable to Owner/Agent at 123 Main Blvd., Sacramento, CA 95864. Payments made in person may be delivered to Owner/Agent between the hours of 24/Z.",
            "values": [
              "$20,125.00",
              "quarter"
            ]
          },
          {
            "prompt": "Leesee must pay rents biweekly. For the dollar amount due, see addendum A.",
            "values": [
              "not found",
              "biweekly"
            ]
          }
        ]
      }
    }
  ]
}
```

**Example document**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/summarizer.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer.pdf) |
| ---------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "_source_rent_topic_paragraphs": {
    "type": "string",
    "value": "Lessee shall pay 895.00 dollars per month for rent. The first month's rent and/or prorated rent amount shall be due prior to move-in. For any move in date that is after the 15th of the month, Tenant must pay a full month of rent in order to gain possession of the home. The prorated rent amount will be due the second month of lease. Every month thereafter, Lessee must pay rent on or before the 1st day of each month with 5 days of grace period. The following late fees will apply for payments made after the grace period:"
  },
  "rent_computed": [
    {
      "rent_in_dollars": "895.00",
      "payment_time_period": "month"
    }
  ]
}
```
