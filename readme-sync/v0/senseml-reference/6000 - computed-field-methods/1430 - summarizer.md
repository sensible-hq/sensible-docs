---
title: "Summarizer"
hidden: true
---
Automatically extracts key/value pairs from short snippets of free text using [OpenAI](https://openai.com/) machine learning (ML). The Summarizer compute field method takes a snippet of text extracted using the [Topic](doc:topic) method as input, and extracts key/value pairs informed by a few short samples of extracted values. 

Parameters
====

The following parameters are contained in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value        | description                                                  |
| :----------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)        | `summarizer` |                                                              |
| source_id (**required**) | field ID     | Specifies a field that uses a [Topic](doc:topic) method, and whose output which contains the relevant snippet of text containing the key/value information you want to extract. |
| fields                   | string array | Names of the keys you want to extract. These names have an impact on the free-text extraction, so choose names that have a meaningful semantic relationship to the target data to extract. For example, for a dollar amount of rent to extract,  `rent`, `rents`, and `rent_in_dollars` are all good naming choices. |
| samples                  | object       | Short snippets of text containing examples of how to extract information. Contains these parameters:<br/>`prompt`: a string up to XX characters long with a free text example containing the information you want to extract.<br/>`values` The target information to extract from the prompt, generally a single word or number. List the values in the same order as you listed corresponding fields in the Fields parameter.<br/>If Sensible can't find the target information in the Source ID parameter, then the term can't be found, the method returns the value found in the prompt(?) |

Examples
====

The following example shows using the Summarizer method to extract the monthly rent and the payment frequency.

**Config**

```json
{
  "fields": [
    {
      "id": "rent_raw",
      "anchor": {
        "match": {
          "type": "first"
        }
      },
      "method": {
        "id": "topic",
        "numLines": 3,
        "terms": [
          "per month",
          "pay",
          "leesee"
        ]
      }
    }
  ],
  "computed_fields": [
    {
      "id": "rent_computed",
      "method": {
        "id": "summarizer",
        "source_id": "rent_raw",
        "fields": [
          "rent_in_dollars",
          "payment_time_period"
        ],
        "samples": [
          {
            "prompt": "Rent 8. Subject to the provisions of this short-term Lease, the rent for the Property is $234.00 per week (the \"Rent\").",
            "values": [
              "$234.00",
              "week"
            ]
          },
          {
            "prompt": "Rent is due in advance on the ist day of each and every week, at $954.00 per week, beginning on November 15, 2015, payable to Owner/Agent at 123 Main Blvd., Sacramento, CA 95864. Payments made in person may be delivered to Owner/Agent between the hours of 24/Z.",
            "values": [
              "$954.00",
              "week"
            ]
          },
          
        ]
      }
    }
  ]
}
```

**PDF**



TODO: fill this out with a more permanent example. for now see https://dev.sensible.so/editor/?d=frances_test_playground&c=summarizer&g=summarizer_lease_8



The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/summarizer.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer.pdf) |
| ---------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "rent_raw": {
    "type": "string",
    "value": "Lessee shall pay $895.00 per month for rent. The first month’s rent consider this notice that on occasion, Allstar Management may and/or prorated rent amount of"
  },
  "rent_computed": [
    {
      "rent_in_dollars": "$895.00",
      "payment_time_period": "month"
    }
  ]
}
```
