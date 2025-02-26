---
title: "Fallback LLM configs"
hidden: true
---

TODO: see if I can find a good example in the config library, and link o it instead of using this example

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

