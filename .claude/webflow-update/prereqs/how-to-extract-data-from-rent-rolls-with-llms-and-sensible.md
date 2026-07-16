# How to extract data from rent rolls with LLMs and Sensible

## What we'll cover

This blog post briefly walks you through configuring extractions for **rent rolls**. By the end, you’ll know a few methods for extracting document data using our query language, and you’ll be on your way to extracting any data you choose using our documentation or our prebuilt open-source [**configurations**](https://github.com/sensible-hq/sensible-configuration-library).‍

## Write document extraction queries with SenseML

Let's extract data from a rent roll. Here's an example of a rent roll PDF with redacted or dummy data:

Example rent roll

To extract from this document, take the following prerequisite steps:

  * Sign up for a [**Sensible account**](https://app.sensible.so/register/)
  * Add prebuilt extraction support for rent rolls to your Sensible account. To add support, follow the steps in [**Out-of-the-box extractions**](https://docs.sensible.so/docs/library-quickstart) for rent rolls.



Our [**configurations for rent rolls**](https://github.com/sensible-hq/sensible-configuration-library/tree/main/proptech) are comprehensive. To keep the example in this post simple, let's just extract:

  * Total units, total rent, and % occupied
  * Apartment complex name
  * Details about each apartment unit, such as the occupant’s name and their monthly rent



We’ll also write some logic to test the monthly rent amounts, to verify that the extraction is working properly.

## Extract clustered facts: total units and total rent

Since rent rolls are documents with highly variable layouts, let’s use LLM-based methods to extract the data. By asking the LLM questions such as  `grand total occupied units`, you’ll extract facts as structured data. To improve accuracy and performance, you’ll group together facts that always appear in a cluster together in documents. 

See the following screenshot for an overview of how to configure a group of LLM prompts that extract a cluster of co-located facts. In this case, they’re on page 18 of the example document: 

Extracted document data

You can also view this data in JSON view:

JSON view

To configure the LLM prompts as shown in the preceding screenshot:

  * Navigate to the [**prop tech document type you created**](https://app.sensible.so/document-types/detail/?d=proptech&t=configurations) in a previous step. This document type contains everything you need to extract from rent rolls.
  * For the purposes of this tutorial, you’ll create a blank test configuration in the document type. Click **Create configuration** and name it test_rents. 
  * Click the configuration you created to edit it.
  * Switch to the JSON editor view by clicking **Switch to SenseML**. The app displays an example rent roll in the middle pane and the empty configuration in the left pane.
  * Paste the following code into the left pane of the Sensible app.  


    
    
    {
      "fields": [
        {
          "method": {
            /* group queries if and only if the targeted
             facts are always co-located within a page or two 
             in the document grouping queries improves LLM performance and accuracy 
             */
            "id": "queryGroup",
            "queries": [
              {
                "id": "grand_total_sqft_percent",
                "description": "grand total occupied sqft percent",
                "type": "string"
              },
              {
                "id": "grand_total_units",
                "description": "grand total occupied units",
                "type": "string"
              },
              {
                "id": "grand_total_rent",
                "description": "grand total occupied monthly base rent",
                "type": "string"
              }
            ]
          }
        }
      ]
    }
    

You'll get this output in the right pane:
    
    
    {
      "grand_total_sqft_percent": {
        "value": "94.8%",
        "type": "string",
        "confidenceSignal": "confident_answer"
      },
      "grand_total_units": {
        "value": "168",
        "type": "string",
        "confidenceSignal": "confident_answer"
      },
      "grand_total_rent": {
        "value": "140,379.00",
        "type": "string",
        "confidenceSignal": "confident_answer"
      }
    

In the preceding output, the confidenceSignal is a more nuanced [alternative](https://docs.sensible.so/docs/confidence) to confidence scores that indicates whether the LLM judges its own answer to be correct.
