---
title: "Overview"
hidden: true
---


Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Use Sensible to build document-automation features into your vertical SaaS products. 

With Sensible, you can write extraction queries for any document:

![](https://files.readme.io/799bd47-image.png)

And get back key facts as JSON:

<br />

```json
{
    "street_address": {
        "value": "1234 ABC COURT",
        "type": "address"
    },
    "included_appliances": [
        {
            "value": "washers",Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Use Sensible to build document-automation features into your vertical SaaS products. 

With Sensible, you can write extraction queries for any document:

![](https://files.readme.io/799bd47-image.png)

And get back key facts as JSON:

<br />

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

Sensible is highly configurable. You can extract data in minutes by leveraging GPT-4 and other large language models (LLMs), or you can get fine-grained control with Sensible's powerful visual layout-based rules. By combining layout- and LLM-based extraction methods, Sensible supports the entire document landscape, from consistently laid-out, highly structured business forms to free-form, highly variable legal contracts :

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/document_landscape.png)

## Configurable data extraction

Configure your extractions using_SenseML_, Sensible's document-specific query language. SenseML combines the latest in LLM techniques with visual layout-based rules to extract document primitives like rows, tables, checkboxes, sections, and more as JSON. 

![](https://files.readme.io/ee7c021-image.png)

<br />

With SenseML, you can:

- Preprocess documents by correcting layout metadata problems, removing unwanted pages, and more, so that Sensible has a clean, standardized text representation of the document from which to extract structured data in a later step. For more information, see [Preprocessors](doc:preprocessors). 

- Use "methods" to extract document primitives, like rows, columns, tables, boxes, checkbox status, and more. You can also can parse extracted data types like currencies, dates, addresses, or your custom types. For more information, see [Methods](doc:methods). 

- Post-process extracted document data. For example:
  - Write logical [validations](doc:validate-extractions)  like `extracted zip code is 5 digits` in order to throw custom errors and warnings about your extracted data. 
  - Manipulate the extracted data schema with [computed methods](doc:computed-field-methods)  like concat, split, and [custom logic](doc:custom-computation) .
  - Get measures of accuracy for LLMs with [confidence scores](doc:confidence), and get overall measures of extraction completeness with [extraction coverage scores](doc:metrics#extraction-coverage)  . 

A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data. SenseML is a key part of the Sensible devops platform.

Here's a example of a field that extracts a table:

senseml_intro_1.png

![](https://files.readme.io/91ad1e2-image.png)

For more information about SenseML, see [SenseML reference introduction](doc:senseml-reference-introduction).

## Devops platform for document data extraction

See the following image for a high-level overview of Sensible's document data extraction workflow:

![](https://files.readme.io/e6320d9-image.png)

<br />

<br />

As the preceding image shows, Sensible's workflow contains the following steps: 

1. **Ingest:** Upload the document to Sensible. Sensible converts the document (PDF, Microsoft document, or image) to text. 

2. **Classify**:  You define an API endpoint, or _extraction processor_  for a general category of documents (for example, `bank statements`). In the processor, you define _templates_, or output extraction schemas, for document subtypes, for example,   one for `bank_of_america_combined_statements` and one for `chase_single_checking_statements`. This step automatically classifies each document you submit to the processor into the best-fitting template.  Classification optimizes performance for the next step, extraction.

3. **Extract** The processor returns the extraction using _SenseML_, a highly configurable document-specific query language that combines LLMs and layout-based extraction rules. Write the queries yourself in extraction _templates_, or leverage our open-source library of templates.  Use generalized queries for free-form documents like rental contracts, or in layout-specific queries for high-volume, standardized documents like 1040 tax forms.  Optionally validate each extraction using user-configured logical rules. 

4. **Monitor** -  Monitor real-time extraction metrics, for example document volume, validations, and percent of non-null extracted fields, using the [metrics](doc:metrics) dashboard. 

For more information, see [Devops platform overview](doc:devops-platform-overview)  

## Learn more

To use the Sensible platform, you'll:

- Learn  to extract data, or use out-of-the-box supported document types. See [Getting started](doc:draft-getting-started-ai) and [Getting started with layout-based extractions](doc:getting-started).
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Validate**](doc:validate-extractions) extracted data by writing rules for custom errors like `extracted zip code is invalid format` 
- [**Monitor**](doc:metrics) extracted data in production 
- 2do: link to HUMAN REVIEW once it's live











