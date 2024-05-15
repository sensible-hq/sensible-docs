---
title: "Combining LLM- and layout-based extractions"
hidden: true
---



## Capture the longtail

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
