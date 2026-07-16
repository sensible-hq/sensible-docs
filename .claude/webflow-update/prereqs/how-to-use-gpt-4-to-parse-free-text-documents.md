# How to use GPT-4 to parse free-text documents

## Introduction

Some documents, such as leases and other contracts, bury key information in paragraphs of legalese or other unstructured text. This historically represented a significant challenge for data extraction, since finding the target data required sophisticated natural language processing (NLP) techniques that, even at their best, weren't particularly reliable.

In 2020, OpenAI made a significant leap forward in generative language models (a subdiscipline of NLP) with their [**GPT-3**](https://openai.com/api/) model, which generates text that is difficult in many situations to distinguish from human-authored text. Most of the publicity around GPT has focused on its creative applications, such as completing stories, writing code, or finishing your emails.

At Sensible, we tackled the more mundane but still challenging task of using large-language models (LLMs) such as GPT-4 Vision, GPT-4, GPT-3, and GPT-3.5 Turbo to summarize unstructured free text into structured data in a business context. 

Sensible's free-text Query Group method is a great way to **apply LLMs to real-world business** uses. Let's dig into how to use this method  to pull structured rent data out of a lease, with no prior knowledge about the exact wording used in the lease.

Given paragraphs like these:

Lease example

Sensible can extract information like this:
    
    
    {
      "rent_computed": [
        {
          "rent_in_dollars": "$895.00",
          "payment_time_period": "month"
        }
      ]
    }
    

To get such slick output, you'd historically put in a lot of work training machine learning (ML) algorithms with sample documents. But not now! You get this extraction out of the box, because GPT-3 is already trained on a ton of documents – as much of the Internet as it could grab, including all of Wikipedia. 

So what, exactly, do you need to do to go from unstructured, natural-language documents to this structured data? You need to narrow down the document to just a snippet that contains the target information to avoid LLM token limits. Then, you need to prompt the LLM to extract the target information from the snippet.

 Fortunately, with the Sensible app, this multi-step process is easy. Sensible automatically scores chunks of the document based on your queries to find the most likely location, or context, for your data. Then the app can even automatically generate LLM prompts to extract the most interesting facts in the document page you’re currently viewing. All this in a few clicks. Let’s walk through it.

## Transforming unstructured into structured text with Sensible

### Prerequisites

To follow along:

  * Sign up for a [Sensible account](https://app.sensible.so/register/)
  * Download the example PDF: [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/blog_lease.pdf)



### Auto-extract data

Take the following steps to extract data from the lease:

  * Click **New document type.**
  * Select the example document you just downloaded.



Upload the example document

On upload, Sensible automatically extracts important information from the lease for you:

View extracted data

You can edit the automatically generated queries, auto-generate more queries, or manually author your own. For more information, see [Recommended Query Groups](https://www.sensible.so/blog/recommended-query-groups).

### Test the extraction template with a second document

The auto-generated queries, or extraction template, in the right pane in the preceding image can be used to extract from other lease documents.  To try it out:

  * Publish your template by selecting **Publish configuration > Publish to production**:



Publish the config

  * Download the second example document:[ Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/blog_lease_2.pdf)


  * Upload the second example document by clicking **Add file:**



Upload second example document

Note that the extracted data for the auto-generated queries updates to reflect the new document:

View extracted document data

Now that you’ve published the extraction template, you can [integrate](https://docs.sensible.so/docs/integrate) and extract these queries from lease documents in volume using the Sensible API, SDK, or bulk-upload UI.

## Advanced extractions

You’re not limited to auto-generated queries. You can author your own LLM prompts to extract not only short facts, but also tables and complex lists. You can extract from non-text images embedded in documents using multimodal LLMs such as GPT-4 Vision. And if an LLM can’t extract the data you’re looking for, you can always fall back to Sensible’s layout-based extraction [methods](https://docs.sensible.so/docs/methods).
