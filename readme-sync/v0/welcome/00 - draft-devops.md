---
title: "Overview"
hidden: true
---

See the following image steps for a high-level overview of Sensible's document data extraction workflow:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform_devops.png)

<br />

Let’s look at each step in detail:

1. **Ingest** - In this step, you upload document files to Sensible, and Sensible converts them to a standardized text representation in preparation for extracting structured data. Features include:

   - **file types** supported [file types](doc:file-types) including PDFs, Microsoft Word and Excel, and image types such as JPEG.
   - **file upload methods** - Use our SDK, API, bulk upload UI ("manual upload"), or Zapier. For more information see [Integrate](doc:integrate).
   - **Optimized OCR** - Sensible represents the whole document in a standarized text format. Sensible optimizes performance by choosing between [OCR](doc:ocr) or direct extraction of embedded fonts. 

2. **Classify**- You upload the document to a _processor_, or API endpoint you configure . Each processor extracts data from a general category of similar documents, for example, `/extract/bank_statments` or `extract/tax_documents`.  From there, Sensible automatically classifies the document by  the highest-scoring extraction _template_  in the processor. A template defines how to extract data  using queries, and how to populate a target output schema. Features include:

   - **multi-document files** Sensible segments files that combine multiple documents into one PDF [portfolio](doc:portfolio). For example, Sensible splits a mortgage application package into tax forms, bank statements, and application forms. To configure segmentation, you define  "[fingerprints](doc:fingerprint)", or text that characterize first and last pages.
   - **out of the box templates** - Sensible provides an open-source [library](doc:library-quickstart)  of extraction templates with out-of-the-box support for common business forms, so you can get started extracting from balance sheets, drivers licenses, rent rolls, tax forms, resumes, and more in just minutes.
   - **Configurable classification** - You can let Sensible handle classification, or you can use _fingerprints_ to improve performance and accuracy. For example, you can leverage [fingerprints](doc:fallbacks#capture-long-tail-documents-with-fallback-configs)  to handle high-volume forms, and default to auto-scoring to handle a long-tail of more variable documents. TODO: move this image to the fallbacks topic.
   - **Classification granularity** By default, Sensible automatically classifies by document subtype in the processor during the extraction workflow. Prior to extraction , you can classify a document more broadly into processors using the [classify](doc:classify) endpoints.  In this case, the full devops worflow looks like the following:
   - ![](https://files.readme.io/7376b86-image.png)

     ![](https://files.readme.io/43e60bc-image.png)

     <br />

   <br />

   <br />

3. **Extract** - In this step, Sensible returns the extracted document data. Features include: 

   - **Highly configurable layout- and LLM-based extraction using SenseML** -  SenseML provides power and flexibility for your custom extraction needs.  You configure queries that return data. For example:

     ```
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
             /* to improve LLM  performance, group facts to extract if 
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
         }
         ]
         
         
         
         
         
     ```

   - For more information, see  [SenseML reference introduction](doc:senseml-reference-introduction).

   - **structured data** Sensible returns data as key-value pairs. For example:

   - ```json
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
       }
     }
     ```

     Or it can return more complex data, like [tables](doc:nlp-table)  or [sections](doc:repeat-layouts) . 

     **metadata for tracing source text** Sensible offers traceability from the extracted text to the source text in the document through visual overlays in the Sensible app and metadata in the retruned JSON. For more information, see [Color coding](doc:color) and [Verbosity](doc:verbosity).

     **validations** Quality control the data extractions in a document type by writing validations. For example, configure Sensible to throw an error if an extraction zip code is the wrong number of digits. For more information, see [Validating extractions](doc:validate-extractions).

     **confidence scores**  - For LLM-based extractions, confidence _signals_ offer more nuanced troubleshooting than confidence _scores_. They look like error messages like `multiple_possible_answers` and `answer_may_be_incomplete`. For more information, see [Qualifying LLM accuracy](doc:confidence).

4. **Monitor** -  

   1. You can monitor and filter in real-time your extractions at scale using the Sensible app's dashboard. For example, view the number of extractions in recent days or filter by which extractions are returning nulls for target data. For more information, see [Monitoring extractions](doc:metrics).

   ![](https://files.readme.io/f3936a3-image.png)

     ![image-20240607135835819](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240607135835819.png)

5. Human reivew: TODO add bullet point one it's released
