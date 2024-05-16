---
title: "Using fallbacks"
hidden: true
---

Use Sensible's fallback mechanisms to solve missing or inaccurately extracted data. You can set fallbacks at different levels of granularity: 

- You can fall back from one field to another, allowing you to try multiple methods or prompts to extract a target piece of data from the same document. Define fallback fields in the fields array, where each fallback shares the same field ID.
- You can fall back from one config to another, allowing you to try multiple configs on the same document and pick the winning config. Define fallback configs using [fingerprints](doc:fingerprint).

For example, see the following sections.

## Fix nulls and false positives with field fallbacks

Sometimes an LLM prompt works for the majority of documents in a document type, but returns null or an inaccurate response (a "false positive") for a minority of documents. Rather than rewrite the prompt, which can cause regressions, create fallbacks targeted at the failing documents.

For example, you parse automotive repair invoices. For most auto shops' invoices, the prompt `total parts price` extracts a price listed in the repairs. For Andy & Son's car shop's invoices, this prompt returns `null` or it returns an inaccurate response, for example, a subtotal.  Through experimenting, you find a successful prompt:  `What is the 'total parts price'.  The total parts price will be labeled 'total parts' or something semantically similar. It's not a value that can be summed from the line items on the invoice.` To create a fallback field for Andy & Son's shop, create two fields with the same ID:

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

## Cover longtail documents with fallback configs

In this example, you extract data from automotive repair invoices. You have high volume from 5 auto shops, and a long tail of low-volume invoices from hundreds of other shops.  In this case:

1. Define a layout-based config for each of your top 5 auto shops to take advantage of layout-based method's speed and deterministic behavior:

   - Define  [fingerprints](doc:fingerprint) for each auto shop's config. For example, if Andy and Son's is one of your top 5 shops, then include fingerprints for phrases that occur in those invoices:

   ```json
   {
     "fingerprint": {
       "tests": [
         {
           "text": "ANDY AND SON'S",
           "type": "includes",
           "isCaseSensitive": true
         },
         {
           "text": "123 Main Street",
           "type": "equals",
           "isCaseSensitive": true,
           "xRangeFilter": {
             "minX": 3.3,
             "maxX": 5.1
           }
         }
       ]
     },
   ```

    - Leverage the consistent formatting in each of the top vendors to extract data. For example, if Andy and Son's always labels the repaired vehicle's VIN number with the text `VIN #:`, then define a field like

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

      

2. Define an LLM-based config for the long tail:

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

## Notes

This topic covers falling back at the document level using config-level fingerprints. To fall back at a more granular level (at the field level), use field fallbacks. For more information see (troubleshoot-llms) example and (field query object)
