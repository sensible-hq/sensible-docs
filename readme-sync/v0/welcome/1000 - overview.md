---
title: "Overview"
hidden: false
---



Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Use Sensible to build document-automation features into your vertical SaaS products. 

With Sensible's SenseML language, you can write extraction queries for any type of document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intro_SDK_3.png)

And get back key facts as JSON:

```json
{
    "street_address": {
        "value": "1234 ABC COURT",
        "type": "address"
    },
    "included_appliances": [
        {
            "value": "washers",
            "type": "string"
        },
        {
            "value": "dryers",
            "type": "string"
        },
        {
            "value": "refrigerators",
            "type": "string"
        }
    ]
}
```

Sensible is highly configurable. You can extract data in minutes by leveraging GPT-4 and other large language models (LLMs), or you can get fine-grained control with Sensible's visual, layout-based rules. By combining layout- and LLM-based extraction methods, Sensible supports the entire document landscape, from consistently laid-out, highly structured business forms to free-form, variable legal contracts :

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/document_landscape.png)

## Configurable data extraction

Configure your extractions using _SenseML_, Sensible's document-specific query language. SenseML combines the latest LLM techniques with visual layout-based rules to extract document primitives like rows, tables, checkboxes, sections, and more as JSON. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform_senseml.png)



With SenseML, you can:

- Preprocess documents by correcting layout metadata problems, removing unwanted pages, and more, so that Sensible has a clean, standardized text representation of the document from which to extract structured data in a later step. For more information, see [Preprocessors](doc:preprocessors). 
- Use "methods" to extract document primitives, like rows, columns, tables, boxes, checkbox status, and more. You can also parse extracted data types like currencies, dates, addresses, or your custom types. For more information, see [Layout-based methods](doc:layout-based-methods). 
- [Handle document variations](doc:document-variations)  in a set of similar documents (a "document type") by conditionally executing SenseML methods based on the document's contents.
- Post-process extracted document data. For example:
  - Write logical [validations](doc:validate-extractions)  like `customer ID is 9 digits` to throw custom errors and warnings about your extracted data. 
  - Manipulate the extracted data schema with [computed methods](doc:computed-field-methods)  like concat, split, and [custom logic](doc:custom-computation). Or, completely transform Sensible's standardized `parsed_document` output into any schema to fit your data consupmtion needs using a [JsonLogic postprocessor](doc:postprocessor). 
  - Get measures of accuracy for LLMs with [confidence scores](doc:confidence), and get overall measures of extraction completeness with [extraction coverage scores](doc:metrics#extraction-coverage). 

A [field](doc:field-query-object) is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data. SenseML is the basis for Sensible's extraction workflow.

Here's an example of a field that extracts a table:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/senseml_intro_1.png)

For more information about SenseML, see [SenseML reference introduction](doc:senseml-reference-introduction).

## Devops platform for document data extraction

See the following image for a high-level overview of Sensible's document data extraction workflow:

[![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform_devops.png)](doc:devops-platform)



For more information about this diagram, see [Devops platform](doc:devops-platform).

## Learn more

To use the Sensible platform, you'll:

- Learn  to extract data, or use out-of-the-box supported document types. See [Getting started](doc:getting-started-ai) and [Getting started with layout-based extractions](doc:getting-started).
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Validate**](doc:validate-extractions) extracted data by writing rules for custom errors like `extracted zip code is invalid format` 
- [**Monitor**](doc:metrics) extraction metrics in production
- [**Review**](doc:human-review) and correct extracted data at the field level using the review UI











