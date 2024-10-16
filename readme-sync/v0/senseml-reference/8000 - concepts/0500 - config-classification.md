---
title: "Config classification"
hidden: true
---

Sensible supports two levels of document classification:

1. Classify a document by its similarity to each document type you define in your Sensible account.
2. Classify a document by its subtype, or "config", during the extraction workflow.  

This topic covers classifying a document by its subtype. You can configure the defaults for how this step is performed.

## Automatic classification

When you create a *document type*, or API endpoint, you configure it to extract data from a general category of similar documents, for example, `/extract/bank_statments` or `extract/drivers_license`. 

To handle subtypes in the general document type, you create *configs* to handle each subtype, for example, a  `chase_statements` config, a  `wells_fargo_statments`  config, and a `boa_statements` for the `bank_statements` document type. A config specifies how to extract data using queries, and how to populate a target output schema.  You should design each config so it can handle edge cases for each subtype, so that you can ultimately output the extraction for each subtype to a uniform `bank_statements` schema.

As a convenience, Sensible automatically classifies each document you upload to a document type into its subtype:

![image-20241016124414284](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20241016124414284.png)

Sensible classifies the document by its subtype as follows:

TODO talk about classification score

## Configuring classification

TODO talk about fingerprints
