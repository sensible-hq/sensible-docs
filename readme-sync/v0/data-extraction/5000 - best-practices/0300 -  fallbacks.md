---
title: "Fallback strategies"
hidden: false
---

Use Sensible's fallback mechanisms to solve missing or inaccurately extracted data. You can set fallbacks at different levels of granularity:

- You can fall back from one field to another, allowing you to try multiple methods or prompts to extract a target piece of data from a single document.
- You can fall back from one config to another, allowing you to try multiple configs on a single document and pick the winning config. Specify fallback configs using [fingerprints](https://docs.sensible.so/docs/fingerprint).

For more information, see the following sections.

## Fallback fields

If a field fails to extract data, you can specify a backup, or fallback field to target the same data with a different method. To specify fallbacks between fields, specify consecutive fields that use the same ID. 

Use fallback fields to define alternate methods of extracting the same target data. This enables you to use a single configuration to extract data from similar documents whose formatting can vary. For example, say you want to extract a "total amount" field which appears in a table in document revision A and in a free-text paragraph in document revision B. You can define two fields in one configuration with the same ID (`total_amount`), which use the Row method and the Query Group method, respectively. 

A field evaluates as "failed" and falls back if it returns an empty array, null, or undefined. A field evaluates to "passed" and doesn't fall back if it returns an empty string or 0. Fallback fields can be of any kind. For example, you can fallback from a field, to a computed field, to a section group.<br/>

**Limitations:**<br/>- Fallbacks don't work across nested structures. For example, you can't fall back from a parent section group's field to a child section group's field.<br/>- Fallbacks don't work within a Query Group method. To specify fallback fields, define each one in a separate query group.



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

   - Define  [fingerprints](doc:fingerprint) for each auto shop's config. For example, if Andy and Son's is one of your top 5 shops, then include fingerprints for phrases that occur in those invoices:

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
   
    - Leverage the consistent formatting in each of the top vendors to extract data. For example, if Andy and Son's always labels the repaired vehicle's VIN number with the text `VIN #:`, then define a field similar to the following:
   
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

