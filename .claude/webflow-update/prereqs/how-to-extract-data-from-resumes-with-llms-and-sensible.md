# How to extract data from resumes with LLMs and Sensible

## What we'll cover

This blog post briefly walks you through configuring extractions for resumes. By the end, you’ll know a few methods for extracting document data using our query language, and you’ll be on your way to extracting any data you choose using our documentation or our prebuilt open-source [configurations](https://github.com/sensible-hq/sensible-configuration-library).‍

## Write document extraction queries with SenseML

Let's extract data from a resume. Here's an example of a resume PDF with redacted or dummy data:

Example resume

To extract from this document, take the following prerequisite steps:

  * Sign up for a [Sensible account](https://app.sensible.so/register/)
  * Add prebuilt extraction support for resumes to your Sensible account. To add support, follow the steps in [Out-of-the-box extractions](https://docs.sensible.so/docs/library-quickstart) and select resumes.



Our [configurations for resumes](https://github.com/sensible-hq/sensible-configuration-library/) are comprehensive. To keep the example in this post simple, let's extract just the:

  * Candidate’s name
  * Candidate’s experiences



## Configure the LLM preprocessor

You’ll use LLM-based methods to extract from resumes since they’re documents with highly variable layouts. To improve accuracy and performance, you’ll first configure some global parameters for all the LLM prompts in the resume configuration.

See the following screenshot for an overview of how to configure the global LLM parameters: 

Global LLM prompt preprocessor

To configure the global LLM parameters as shown in the preceding screenshot:

  * Navigate to the [resume document type you created](https://app.sensible.so/document-types/detail/?d=resumes&t=configurations)  in a previous step.
  * Click **Create configuration** and create a new test configuration, named for example `test_resume`. 
  * Click the configuration you created to edit it.
  * Switch to the JSON editor view by clicking Switch to SenseML.
  * Paste the following code into the left pane of the Sensible app.  This preprocessor code will configure all the data extraction queries you author in succeeding steps in this tutorial:


    
    
    {
      "preprocessors": [
        {
          /* Sensible uses JSON5 to support code comments */
          "type": "nlp",
          /* describe the document to extract data from, in this case, resumes */
          "contextDescription": "the following context is an excerpt from a resume",
          /* For each field, submit a two-page excerpt to the LLM. The two-page limit improves performance.
             Sensible finds the most relevant document excerpts, or chunks, for each field. */
          /* each excerpt is 1 page long */
          "chunkSize": 1,
          /* submit a total of two excerpts to the LLM */
          "chunkCount": 2,
          /* don't overlap the excerpts */
          "chunkOverlapPercentage": 0
        }
      ],
      "fields": []
    }
    

The preceding code configures the prompts that Sensible submits to the LLMs for each field in the config. They describe the document to extract from (resumes) and configure the size of the document excerpts that Sensible submits to the LLMs as context for the prompts. For more information about these global parameters, see [Advanced prompt configuration](https://docs.sensible.so/docs/prompt#global-sensible-instruct-parameters).
