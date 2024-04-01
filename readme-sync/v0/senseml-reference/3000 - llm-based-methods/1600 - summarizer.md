---
title: "Summarizer"
hidden: false
---
TODO: remove 'alternative to list' links wherever you find them.

Automatically extracts key/value pairs from short snippets of free text using an LLM (GPT-3.5 Turbo). The Summarizer computed field method takes as input another extracted field's output, and transforms the text based on prompts or short samples of extracted values you provide. For example, use this method to transform another method's output when you can't use [types](doc:types) or other [computed field methods](doc:computed-field-methods). For example, if you use the [Row](doc:row) method to return an inconsistently formatted ranking (`first`, `1st`,  `1`), then you can use this method to consistently format the ranking. You can reformat with instructions like `the following snippet is a ranking. Return it formatted liked \"1st\", \"2nd\", \"3rd\" and so forth, not written out like \"first\" or in digit-only format like \"1\" `. 

TODO: add this example:

https://dev.sensible.so/editor/?d=frances_playground&c=summarizer_tests_senseml&g=summarizer_senseml_test___google_docs



Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value        | description                                                  |
| :----------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)        | `summarizer` | The Anchor parameter is optional for fields that use this method. If you omit an anchor, Sensible searches the entire document for the data you want to extract. |
| source_id (**required**) | field ID     | Specifies a field whose output is a snippet of text with the key/value information you want to extract. If the snippet doesn't occur at a predictable location in the document, then you can use the [Topic](doc:topic) method to find it. |
| fields (**required**)    | string array | Names of the keys you want to extract. These names have an impact on the free-text extraction, so choose names that have a meaningful relationship to the target data to extract. For example, for a dollar amount of rent to extract,  `rent`, `rents`, and `rent_in_dollars` are good naming choices. |
| instructions             | string       | Prompt for the LLM, describing how to extract information from the text in the Source ID parameter.<br/>For more information about how to write prompts, see [Query Group](doc:query-group-tips) tips.<br/>For an example of using this parameter, see the Examples section. |
| samples                  | object array | Short snippets of text similar to the text in the Source ID parameter, with examples of the information to extract. <br/>Use in addition to the Instructions parameter to increase the LLM's accuracy. <br/>Contains these parameters:<br/>`prompt` (string): An example of the sort of free text from which you want to extract data.<br/>`values` (string array):  The target information to extract from this prompt. This array is a parallel array to the Fields parameter's array. Parallel arrays are the same length and same sequence. If the LLM can't find the target information in the Source ID parameter, it can generate an arbitrary value. To override this behavior, specify a Sample parameter whose Prompt parameter has a text snippet that's missing the target data, and whose Values array indicates the data is missing (for example, "N/A" or "not found").<br/>For an example of using this parameter, see the Examples section. |

Examples
====

Example 1
---

The following example shows using the Summarizer method with the Topic method to extract agricultural data from a government report.

**Config**

```json
{
  "fields": [
    {
      "id": "_source_ending_stock",
       /* if you don't specify an anchor, Sensible searches the whole doc*/
      "method": {
        "id": "topic",
        /* grab snippet as 
           input for Summarizer method */
        "terms": [
          "global ending stocks"
        ],
        "numLines": 15
      }
    }
  ],
  "computed_fields": [
    {
      "id": "ending_stocks_summarized",
      "method": {
        "id": "summarizer",
        /* field ID containing the source snippet */
        "source_id": "_source_ending_stock",
        /* instructions to the LLM for extracting data from source snippet*/
        "instructions": "list the ranges, in million metric tons (MMT), of changes in 2022/23 for ending stocks by countries mentioned in the following text excerpt. Don't list countries not mentioned in the excerpt.",
        /* the field IDs the LLM must apply to the extracted data */
        "fields": [
          "region_or_country",
          "range_of_change_in_ending_stock",
        ],
        "samples": [
          /* OPTIONAL SAMPLES:
          examples of what data to extract
          from text snippets
          similar to source snippet   */
          {
            "prompt": "Stocks in the USA are up 0.7 MMT to 3.8 MMT",
            "values": [
              [
                "USA",
                "0.7 MMT to 3.8 MMT",
              ],
            ]
          },
          {
            "prompt": "Stocks in Bangladesh remain unchanged, at 1.5 MMT",
            "values": [
              [
                "USA",
                "no change",
              ],
            ]
          },
          {
            "prompt": "Data are unavailable for ending stocks in Brazil",
            "values": [
              [
                "Brazil",
                "no data available",
              ],
            ]
          }
        ]
      }
    },
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/summarizer_crop.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_crop.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "_source_ending_stock": {
    "type": "string",
    "value": "Slight Relief for 2022/23 Global Ending Stocks 2022/23 global ending stocks are projected up 0.3 MMT to 267.8 MMT but remain the tightest since 2016/17 (figure 10). China accounts for more than 50 percent of 2022/23 global ending stocks but its stocks are largely not available to the public. When China is removed from the global picture, stocks are even tighter at 123.5 MMT, the lowest since 2007/08. Major exporters' stocks are forecasted down 0.1 MMT to 55.6 MMT. Stocks in Australia are raised 0.5 MMT to 3.7 MMT with higher domestic production. Despite a production decline Argentina's stocks are raised 0.2 MMT to 1.4 MMT as exports will be limited with restricted supplies. Higher exports for the European Union and Kazakhstan cut their ending stocks by 0.5 MMT to 9.5 MMT and 0.2 MMT to 1.2 MMT, respectively. Stronger food use in the United States results in lower ending stocks (-0.1 MMT to 15.5 MMT). Canada, Ukraine, and Russia's stocks remain anchored at 4.2 MMT, 4.7 MMT, and 15.4 MMT, respectively. Stocks for India are raised 0.5 MMT to 12.0 MMT as exports remain restricted, but this still would be the tightest in 6 years. Figure 10 Global ending stocks, 2016/17–2022/23"
  },
  "ending_stocks_summarized": [
    {
      "region_or_country": "Australia",
      "range_of_change_in_ending_stock": "0.5 MMT to 3.7 MMT"
    },
    {
      "region_or_country": "Argentina",
      "range_of_change_in_ending_stock": "0.2 MMT to 1.4 MMT"
    },
    {
      "region_or_country": "EU",
      "range_of_change_in_ending_stock": "-0.5 MMT to 9.5 MMT"
    },
    {
      "region_or_country": "Kazakhstan",
      "range_of_change_in_ending_stock": "-0.2 MMT to 1.2 MMT"
    },
    {
      "region_or_country": "USA",
      "range_of_change_in_ending_stock": "-0.1 MMT to 15.5 MMT"
    },
    {
      "region_or_country": "Canada",
      "range_of_change_in_ending_stock": "no change"
    },
    {
      "region_or_country": "Ukraine",
      "range_of_change_in_ending_stock": "no change"
    },
    {
      "region_or_country": "Russia",
      "range_of_change_in_ending_stock": "no change"
    },
    {
      "region_or_country": "India",
      "range_of_change_in_ending_stock": "0.5 MMT to 12.0 MMT"
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
      /* grab Rents snippet 
           as input for Summarizer method */
      "id": "_source_rent_topic_paragraphs",
      /* if you don't specify an anchor, Sensible searches the whole doc*/
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
        /* field ID containing the source snippet */
        "source_id": "_source_rent_topic_paragraphs",
        /* instructions for the LLM for extracting data from source snippet */
        "instructions": "list the rents, how often the rent must be paid, and when the rent is due",
        /* the field IDs the LLM must apply to the extracted data */
        "fields": [
          "rent_in_dollars",
          "payment_time_period",
          "payment_due"
        ],
        /* OPTIONAL SAMPLES:
          examples of what data to extract
          from text snippets
          similar to source snippet   */
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

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer.pdf) |
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

