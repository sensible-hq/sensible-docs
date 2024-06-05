---
title: "Overview"
hidden: true
---



Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. use Sensible to build document-automation features into your vertical SaaS products. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intro_SDK_2.png)

Sensible is highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful visual layout-based rules.  In this way, Sensible supports the entire document landscape, from consistently laid-out, highly structured business forms to free-text, highly variable legal documents :

![image-20240605094006233](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240605094006233.png)

Sensible offers devops for document automation:

**devops workflow for Extraction**

![image-20240604131029643](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240604131029643.png)



1. **Ingest** - In this step, you upload document files to Sensible, and Sensible converts them to a standardized text representation in preparation for extracting structured data. Features include:
   - **file types** supported [file types](doc:file-types) including PDFs, Microsoft Word and Excel, and image types such as JPEG.
   - **file upload methods** - Use our SDK, API, bulk upload UI ("manual upload"), or Zapier. For more information see [integrati]
   - **Optimized OCR** - Sensible optimizes performance by choosing between [OCR](doc:ocr) or direct extraction of embedded fonts. Sensible represents the whole document in a standarized format, as an array of text lines with metadata about their layout. 
2. **Classify**- In this step, Sensible automatically chooses which extraction processor best fits a document. Features include:
   - **multi-document files** Sensible segments files that combine multiple documents into one PDF [portfolio](doc:portfolio) (for example, a mortgage application package that contains tax forms, bank statements, and application forms into one file)  into separate documents using "[fingerprints](doc:fingerprint)", or text matches that characterize first and last pages.
   - **layout- and LLM-based extraction templates** You configure an extraction processor (or leverage our out-of-the-box processor [library](doc:library-quickstart)). Configure one processor for each general category of documents, for example, a `bank_statements` processor or a  `tax_documents` processor.  Each processor is an API endpoint. Inside the endpoint, you configure *templates* that define how to extract data from subcategories of documents in the general processor category. The templates contain queries you write in our document-domain specific query language, SenseML. For example, the `bank_statements` processor might have a template for bank of america statements, a template for wells fargo templates, and template for chase statements. Leverage our layout-based extraction SenseML methods (2do link) for fast and determinstic extractions for highly structured documents in the processor, and include an LLM-based, generalized template you can [fall back](doc:fallbacks#capture-long-tail-documents-with-fallback-configs) to if you have a long-tail of variable documents that you want to include in the processor.

3. **Extract** - In this step, Sensible returns the extracted document data. Features include:

   - 

   





To use the Sensible platform, you'll:

- **Learn** to extract data, or use out-of-the-box supported document types TODO
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Validate**](doc:validate-extractions) extracted data by writing rules for custom errors like `extracted zip code is invalid format` 
- [**Monitor**](doc:metrics) extracted data in production 
- 2do: HUMAN REVIEW

IS THERE A NICE GRAPHIC THAT's NOT COMPLICATED TO EXPRESS THIS?



As an overview, Sensible works like this:

- You create a processor. Each processor is an API endpoint that handles extractions for one broad document type, for example, bank statements, tax forms, or 2do. You can also use our out-of-the-box processors.
  - In the processor, you author extraction templates in SenseML to handle different vendors, form variations, etc, in the doc type. In the bank statements processor, maybe you have a `bank_of_america`, `chase`, and `wells_fargo` templates, for instance. The template specifies the JSON schema you want to populate with information from that vendor's bank statements for each extraction:
    - Sensible chooses the best-fitting template for each document automatically, or you can influence which template it chooses using fingerprints. 
    - You can manipulate the output schema to fit your data consumption needs (split, concat, etc) and even get data that's implied but not stated (eg sum the columns in a table with Custom Cmoputation method)

Here's a full example of a template:



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



For more information, see the SenseML reference topic

--> todo move 'shock and awe' to that topic







THIS NEEDS A REVAMP FOR MONITORING AND HUMAN REVIEW AND GOES IN INTRO REFERENCE TOPIC

![image-20240531150054816](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240531150054816.png)



- - 











