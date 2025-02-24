---
title: "Handling document variations"
hidden: true
---

*Alt title: Conditional SenseML extraction*

*Handling variations in a document type*

*Handling document variations*



Sensible offers features for handling variations in a set of similar documents, or *document type*. For example, say you extract data from bank statements. Variations range in granularity:

-  Each major bank has its own distinctive layout and formatting for its statements. 
- Some major banks have differing layouts for each type of account. For example, the layout for a savings account statement differs from a checking account statement.
- You have a long tail of small regional credit unions you want to extract from, where it would be an overwhelming task to qualify all the minor variations.

For both layout-based and LLM-based extraction methods (TODO: Link) you can handle these variations by executing different types of SenseML queries to extract the same target data across the bank statements using different extraction methods. In the end, your goal with the differing SenseML queries is to produce a unified data output schema. By level of granularity, here are the features available to you:



| Feature               | granularity                               | how it works                                                 | example use case                                             | benefits | full example                                                 |
| --------------------- | ----------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
| fallback fields       | single field/query                        | If a field fails to extract data, fallback to another identically named field in a config that uses an alternate extraction method. | You want to extract a "total amount" field which appears in a table in document revision A and in a free-text paragraph in document revision B. You can define two fields in one configuration with the same ID (`total_amount`), which use the Row method and the Query Group method, respectively. |          | TODO link this topic?                                        |
| conditional execution | subset of fields/queries  in a config     | based on a pass/fail logical condition TODO LINK, execute alternate subsets of fields in a config file | You want to extract data from two affiliate banks' statements. The statements' layouts are so similar that you can reuse 90 percent of your SenseML queries to handle both. Rather than authoring two separate configs, you can handle the remaining 10 percent  with conditional field execution. |          | TODO link to conditional-execution                           |
| configs               | entire set of fields/queries in a config. | Based on matching characteristic text ("fingerprints")(TODO link), determine the best fitting config for a document. TODO word better | In a document type, you extract bank statements from Chase, Wells Fargo, Bank of America, and a long tail of small regional banks. Sensible uses a different collection of queries, or *config*,  to extract from each document based on whether it contains the text  `Chase` or `Wells Fargo` or `Bank of America`. If it doesn't contain the name of any major bank, Sensible uses a generalized, LLM-based config to extract from the long tail. |          | TODO: link to the config library and to the example on this page? |
|                       |                                           |                                                              |                                                              |          |                                                              |
|                       |                                           |                                                              |                                                              |          |                                                              |



These features range in granularity from  From small to large variations, these features range in granularity from single SenseML queries

 Handling variations between a set of similar documents 

Sensible offers a variety of methods for conditionally executing SenseML 



Different levels of granularity:

- execute one of a list of identically named fields, depending on which one first returns null, using fallbacks. Example use cases:
- execute one block of fields or another within a config, depending on a condition. Example use cases: TODO
- execute a config (group of fields) or another, depending on fingerprints. Example use cases: TODO



Sensible offers a couple of means of determining which SenseML :

- You can "fall back" from one failed field to another, to try alternate methods of extracting the same piece of target data. 
- You can "fall back" from one config to another. Sensible tests each config to find the "winning" config.
- You can conditionally execute lists of fields in a config based on a pass/fail condition. The condition can be similar to field fallbacks ("did a field fail?") or be unrelated to fallbacks ("Is this revision B of the document? ").



Use Sensible's fallback mechanisms to solve missing or inaccurately extracted data. You can set fallbacks at different levels of granularity:

- You can fall back from one failed field to another, allowing you to try multiple methods or prompts to extract a target piece of data from a single document.
- You can fall back from one config to another. In this scenario, Sensible tests multiple configs on a single document and pick the winning config. Specify fallback configs using [fingerprints](https://docs.sensible.so/docs/fingerprint).

For more information, see the following sections.

## Fallback fields

If a field fails to extract data, you can specify a backup, or fallback field to target the same data with a different method. To specify fallbacks between fields, specify consecutive fields that use the same ID. 

Use fallback fields to define alternate methods of extracting the same target data. This enables you to use a single configuration to extract data from similar documents whose formatting can vary. For example, say you want to extract a "total amount" field which appears in a table in document revision A and in a free-text paragraph in document revision B. You can define two fields in one configuration with the same ID (`total_amount`), which use the Row method and the Query Group method, respectively. 

A field evaluates as "failed" and falls back if it returns an empty array, null, or undefined. A field evaluates to "passed" and doesn't fall back if it returns an empty string or 0. Fallback fields can be of any kind. For example, you can fallback from a field, to a computed field, to a section group.<br/>

**Limitations:**<br/>- Fallbacks don't work across nested sections. Note fallbacks do work across nested [conditions](doc:conditional).<br/>- Fallbacks don't work within a Query Group method. To specify fallback fields, define each one in a separate query group.

### Example 1

If a company's explanation of benefits lists the patient name near the phrase "received for" in other cases and near the phrase "claimant" in others, you can write fallbacks like the following:

```json
{
  "fields": [
    {
      /* first look for patient name near phrase "recieved for" */
      "id": "patient_name",
      "anchor": "recieved for"
              "method": {
        "id": "label",
        "position": "right"
      }
    },
    /* if that fails, look for it in a row near the phrase "claimant" */
    {
      "id": "patient_name",
      "anchor": "claimant"
              "method": {
        "id": "row",
        "position": "right"
      }
    },
  ]
}
```


### Example 2: LLM prompt fallbacks

Sometimes a field works for the majority of documents in a document type, but returns null or an inaccurate response (a "false positive") for a minority of documents. This situation is most common with LLM-based methods. Rather than rewrite the LLM prompt, which can cause regressions, create fallbacks targeted at the failing documents.

For example, you parse automotive repair invoices. For most auto shops' invoices, the prompt `total parts price` extracts a total price. For Andy & Son's car shop's invoices, this prompt returns `null` or it returns an inaccurate response, for example, a subtotal.  Through experimenting, you find a successful prompt:  `What is the 'total parts price'. The total parts price will be labeled 'total parts' or something semantically similar. It's not a value that can be summed from the line items on the invoice.` To create a fallback field for Andy & Son's shop, create two fields with the same ID:

```json
{
  "fields": [
    /*
    fallback fields in query groups must be defined in
    separate groups, so define two single-member groups
     */
    {
      /* if Sensible doesn't find the anchor text 
          "Andy & Son's" in the invoice,
           it returns null for the parts_total_price field in this group
           and falls back to the parts_total_price in the next group.
           Use this fallback behavior to create a detailed prompt for 
           Andy & Son's invoices and more general prompt
           for all other invoices*/
      "anchor": "Andy & Son's",
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "parts_total_price",
            "description": "What is the 'total parts price'. The total parts price will be labeled 'total parts' or something semantically similar.  It's not a value that can be summed from the line items on the invoice",
            "type": "string"
          }
        ]
      }
    },
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            /* this field runs only if the previous
            parts_total_price field returns null */
            "id": "parts_total_price",
            "description": "total parts price",
            "type": "string"
          }
        ]
      }
    }
  ]
}
```

Fallback fields can be of any kind. For example, you can fallback from an LLM-based field to a layout-based field, or from a computed field to a section group. For more information, see [Field query object](doc:field-query-object).

## Fallback configs

Use fallback configs to capture long-tail document variations in a document type.

### Example 1

For example, say you extract data from automotive repair invoices. You have high volume from 5 auto shops, and a long tail of low-volume invoices from hundreds of other shops. In this case, define a layout-based config for each of your top 5 auto shops to take advantage of layout-based methods' speed and deterministic behavior, and define one catch-all LLM-based config for the long tail.

1. To define a layout-based config for each of your top 5 auto shops, take the following steps:

   - Define  [fingerprints](doc:fingerprint) for each auto shop's config. For example, if `Andy and Son`'s is one of your top 5 shops, then include fingerprints for phrases that occur in those invoices:

   ```json
   {
     "fingerprint": {
       "tests": [
         {
           "text": "ANDY AND SON'S",
           "type": "includes",
           "isCaseSensitive": true
         }
       ]
     },
   ```
   
    - Leverage the consistent formatting in each of the top vendors to extract data. For example, if `Andy and Son's` always labels the repaired vehicle's VIN number with the text `VIN #:`, then define a field similar to the following:
   
      ```json
      {
        "fields": [
          {
            "id": "vehicle_VIN",
            "anchor": "VIN #:",
            "method": {
              "id": "label",
              "position": "below"
            }
          }
        ]
      }
      ```
   
      
   
2. To define an LLM-based config for the long tail, take the following steps:

    - Don't define fingerprints.

    - Define the same field IDs as in previous configs using LLM-based methods. For example:

      ```json
      {
            "method": {
              "id": "queryGroup",
              "queries": [
                {
                  "id": "vehicle_VIN",
                  "description": "vehicle VIN"
                }
              ]
            }
          }
      ```

