---
title: "SenseML reference introduction"
hidden: false
---

*SenseML* is a document-specific query language that lets you extract structured data from documents, for example, from PDFs. A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data. SenseML is a key part of the Sensible devops platform TODO link to overview.

Here's a example of a field that extracts a table:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/senseml_intro_1.png)

SOURCE 2do delete: https://dev.sensible.so/editor/?d=frances_playground&c=table_demo&g=compose_type



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform.png)

With SenseML, you can:

- Preprocess documents by correcting layout metadata problems, removing unwanted pages, and more, so that Sensible has a clean, standardized text representation of the document from which to extract structured data in a later step.

- Use "methods" in fields to extract document primitives, like rows, columns, tables, boxes, checkbox status, and more. You can also can parse extracted data types like currencies, dates, addresses, or your custom types.

-  Post-process extracted document data with logical validations you write like `extracted zip code is 5 digits`, computations like concat/split, and more.

  

  See the following topics for reference documentation for the SenseML query language:

  **Preprocessors**

  - [Preprocessors](doc:preprocessors)
  - [Classify with fingerprints](doc:fingerprint)
  - [OCR](doc:ocr)

  **Document primitives**
  
  - [Field query object](doc:field-query-object)
  - [Methods](doc:methods)
  - [LLM-based methods](doc:llm-based-methods), including LLM-based Sensible Instruct methods. For more information about choosing whether to author configs in either SenseML or Sensible Instruct, see [Choosing an extraction approach](doc:author).
  - [Sections](doc:sections)
  - [Configuration settings](doc:config-settings) TODO remove?
  - [Document type settings](doc:document-type-settings) TODO remove?
  
  **Post-processing**
  
  - [Computed Field methods](doc:computed-field-methods)
  
  - [Verbosity](doc:verbosity)
  - [Confidence signals](doc:confidence)
  
  

Examples
====

 The following image shows a "config". A "config" is a collection of SenseML preprocessors, fields, and other configurations that you use for extracting from a group of similar documents in bulk.  Configs can be highly specific to a type of document, in which case you genearlly use layout-based extraction methods, or LLM-based and generalized for a long tail of documents. For example you could write a, `boa_consolidated_statements`  config using layout based methods like Row, Region, and Checkbox, or you could write a  `generalized_bank_statements` config that uses LLM-based methods like Table and List . 

For an overview of the elements of a config, see the following example:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/senseml_intro.png)

Try out this example in the Sensible app using the following document and config:

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split.pdf) |
| ---------------------------- | ------------------------------------------------------------ |

This example uses the following config:


```json
{
  "fingerprint": { // preferentially run this config if doc contains the test strings
    "tests": [
      "anyco",
      "quoted coverage changes"
    ]
  },
  "preprocessors": [
    {
      "type": "pageRange", // cuts out irrelevant doc pages before extraction
      "startPage": 0,
      "endPage": 2
    }
  ],
  "fields": [
    /* LAYOUT-BASED EXAMPLE */
    {
      "id": "_driver_name_raw", // ID for extracted target data
      "anchor": "name of driver", // search for target data near text "name of driver" in doc
      "method": {
        "id": "label", // target to extract is a single line near anchor line
        "position": "below" // target is below anchor line ("name of driver")
      }
    },
    /* LLM-BASED EXAMPLE */
    {
      "method": {
        /* to improve performance, group facts to extract if 
           they're co-located in the document  */
        "id": "queryGroup",
        "queries": [
          {
            "id": "policy_period",
            /* described each data point you want to extract
               with simple, short language */
            "description": "policy period",
            "type": "string"
          },
          {
            "id": "policy_number",
            "description": "policy number",
            "type": "string"
          }
        ]
      }
    },
  ],
  "computed_fields": [
    { // target data is a transformation of already extracted data
      "id": "driver_name_last", // ID for transformed target data
      "method": {
        "source_id": "_driver_name_raw", // extracted data to transform
        "id": "split", // target data is substring in extracted data
        "separator": " ", // use a whitespace space to split the extracted data into substring array
        "index": 1 // target is 2nd element in substring array
      }
    }
  ]
}
```

The output of this example config is as follows:

```json
{
  "_driver_name_raw": {
    "type": "string",
    "value": "Petar Petrov"
  },
  "policy_period": {
    "value": "April 14, 2021 - Oct 14, 2021",
    "type": "string"
  },
  "policy_number": {
    "value": "123456789",
    "type": "string"
  },
  "driver_name_last": {
    "value": "Petrov",
    "type": "string"
  }
}
```

This example config has the following elements:

- The **field** `_driver_name_raw` is a query that extracts a driver's name by searching below some matched text (`"position": "below"`). Its ID is the key for the extracted data. For more information, see [Field query object](doc:field-query-object).

- (not applicable for LLM methods) an **anchor** is matched text that helps narrow down a location in the document from which to extract data. In the `"_driver_name_raw"` field, Sensible matches a string (`"name of driver"`). For information about more complex anchors, see [Anchor object](doc:anchor).

- A **method** defines how to extract data after the anchor narrows down the data's location. In this example field, the Label method tells Sensible to extract data that's below and close to the anchor.

  There are two broad categories of methods:

  |                         | [LLM-based methods](doc:llm-based-methods)     | Layout-based [methods](doc:methods)                          |
  | ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | Notes                   | Ask questions about info in the document, as you'd ask a human. For example, "what's the policy period"?  Uses large language models (LLMs). | Find the information in the document using anchoring text and layout data. For example, write instructions to grab the second cell in a column headed by "premium". |
  | Deterministic           | no                                                           | yes                                                          |
  | Handles complex layouts | no                                                           | yes                                                          |

- The **preprocessor**, `pageRange`, cuts out irrelevant pages of the document. For more information about using preprocessors to clean up documents before extracting data, see [Preprocessors](doc:preprocessors).

- The **fingerprint** tells Sensible to preferentially run this config if the document contains the terms "anyco" or "quoted coverage changes." For more information about using fingerprints to improve performance, and other configuration settings, see [Configuration Settings](doc:config-settings).

- The **computed field** `"driver_name_last"` extracts the last name from the raw output of the `_driver_name_raw` field. For more information about transforming field output, see [Computed field methods](doc:computed-field-methods).  You can also capture the full name as typed output. See [types](doc:types).

 

Using SenseML, you can extract just about any text, as well as image coordinates, from a document. Happy extracting!
