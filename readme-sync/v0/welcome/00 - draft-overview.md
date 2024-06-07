---
title: "Overview"
hidden: true
---

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Use Sensible to build document-automation features into your vertical SaaS products. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intro_SDK_2.png)



Sensible is highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful visual layout-based rules.  Sensible supports the entire document landscape, from consistently laid-out, highly structured business forms to free-text, highly variable legal contracts :

![image-20240605094006233](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240605094006233.png)

## Devops for document extraction

See the following image steps for a high-level overivew of Sensible's document data extraction workflow:





![image-20240604131029643](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240604131029643.png)

As the preceding image shows, Sensible takes the following steps:

1. **Ingest:** Convert the document (PDF, Microsoft document, or image) to text.

2. **Classify**: Use a user-defined or out-of-the-box endpoint to classify the document according to the best-fitting extraction parser.

3. **Extract** Return the extraction. Optionally validate each extraction using user-configured logical rules.

   

Let’s look at each step in detail:



1. **Ingest** - In this step, you upload document files to Sensible, and Sensible converts them to a standardized text representation in preparation for extracting structured data. Features include:

   - **file types** supported [file types](doc:file-types) including PDFs, Microsoft Word and Excel, and image types such as JPEG.
   - **file upload methods** - Use our SDK, API, bulk upload UI ("manual upload"), or Zapier. For more information see [Integrate](doc:integrate).
   - **Optimized OCR** - Sensible optimizes performance by choosing between [OCR](doc:ocr) or direct extraction of embedded fonts. Sensible represents the whole document in a standarized format, as an array of text lines with metadata about their layout. 

2. **Classify**- In this step, Sensible automatically chooses which extraction parser best fits a document. Features include:

   - **multi-document files** Sensible segments files that combine multiple documents into one PDF [portfolio](doc:portfolio) (for example, a mortgage application package that contains tax forms, bank statements, and application forms into one file)  into separate documents using "[fingerprints](doc:fingerprint)", or text matches that characterize first and last pages.

   - **layout- and LLM-based extraction parsers, or "configs"** 

     ![image-20240607135147766](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240607135147766.png)

     

     You configure extraction templates (or leverage our out-of-the-box [library](doc:library-quickstart)). Configure one processor for each general category of documents, for example, a `bank_statements` processor or a  `tax_documents` processor.  Each processor is an API endpoint. Inside the endpoint, you configure *templates* that define how to extract data from subcategories of documents in the general processor category. The templates contain queries you write in our document-domain specific query language, [SenseML](doc:senseml-reference-introduction). For example, the `bank_statements` processor might have a template for bank of america statements, a template for wells fargo templates, and template for chase statements. Leverage our layout-based extraction SenseML methods (2do link) for fast and determinstic extractions for highly structured documents in the processor, and include an LLM-based, generalized template you can [fall back](doc:fallbacks#capture-long-tail-documents-with-fallback-configs) to if you have a long-tail of variable documents that you want to include in the processor. Here's an example of 2 different templates:

   - **layout-based template**

   - ````json
     {
       "fingerprint": {
         "tests": [
           {
             "text": "bankofamerica",
             "type": "endsWith",
           }
         ]
       },
         {
       "fields": [
             {
           "id": "customer_address",
           "type": "address",
           "method": {
             "id": "region",
             "start": "left",
             "offsetX": -5.5,
             "offsetY": 0.3,
             "width": 3.2,
             "height": 1.8
           },
           "anchor": {
             "match": {
               "type": "startsWith",
               "text": "customer service information"
             }
           }
         },
       ]
     }
         
     ````
     
   - **LLM-based template**

   - ```json
     {
       "fields": [
         {
           "method": {
             "id": "queryGroup",
             "queries": [
               {
                 "id": "customer_name",
                 "description": "what is the customer name",
                 "type": "string"
               }
             ]
           }
         }
       ]
     }
     ```
     
     

3. **Extract** - In this step, Sensible returns the extracted document data. Features include:

   - **structured data** Sensible returns data as key-value pairs. For example, for the previous templates, Sensible can return:

   - ```
       "customer_name": {
         "type": "string",
         "value": "JOHN SMITH",
         "confidenceSignal": "confident_answer"
       },
     ```

     Or it can return more complex data, like tables or sections. TODO links.

     **metadata for tracing source text** (bounding box stuff...todo check if this is true for LLM-based methods and link to location highlighting, maybe link to colors too) doc:validate-extractions and doc:metrics
     
     **validations** Quality control the data extractions in a document type by writing validations. For example, configure Sensible to throw an error if an extraction zip code is the wrong number of digits.
     
     **confidence scores**  - For LLM-based extractions, confidence *signals* offer more nuanced troubleshooting than confidence *scores*. They look like error messages like `multiple_possible_answers` and `answer_may_be_incomplete`.
     
     

4. **Monitor** -  

   1. You can monitor and filter in real-time your extractions at scale using the Sensible app's dashboard. For example, view the number of extractions in recent days or filter by which extractions are returning nulls for target data. TODO links

     ![image-20240607135835819](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240607135835819.png)

     

   

2. Human reivew: TODO add one it's released



## Learn more



To use the Sensible platform, you'll:

- **Learn** to extract data, or use out-of-the-box supported document types TODO link to the getting started guides and to SenseML reference
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Validate**](doc:validate-extractions) extracted data by writing rules for custom errors like `extracted zip code is invalid format` 
- [**Monitor**](doc:metrics) extracted data in production 
- 2do: HUMAN REVIEW





## throw out text?



As an overview, Sensible works like this:

- You create a processor. Each processor is an API endpoint that handles extractions for one broad document type, for example, bank statements, tax forms, or 2do. You can also use our out-of-the-box processors.
  - In the processor, you author extraction templates in SenseML to handle different vendors, form variations, etc, in the doc type. In the bank statements processor, maybe you have a `bank_of_america`, `chase`, and `wells_fargo` templates, for instance. The template specifies the JSON schema you want to populate with information from that vendor's bank statements for each extraction:
    - Sensible chooses the best-fitting template for each document automatically, or you can influence which template it chooses using fingerprints. 
    - You can manipulate the output schema to fit your data consumption needs (split, concat, etc) and even get data that's implied but not stated (eg sum the columns in a table with Custom Cmoputation method)









