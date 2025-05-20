---
title: "Getting started"
hidden: true
---

## Introduction

See the following list for an overview of how to automate your document processing with Sensible:

- **Learn** to extract data from documents, or use out-of-the-box extraction support
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Quality control**](doc:validate-extractions) extracted data
-  [**Monitor**](doc:metrics) and [**review**](doc:human-review)  extracted data in production 

This guide gets you started with the first step, extracting data.

## Learn to extract data

Let's get started with extracting document data from an example bank statement. We'll author a prompt for a large language model (LLM) to extract a checking account number in minutes.

 In this guide, you'll:

- Extract data from an example document using a natural-language description of your target data, for example, a checking bank account number. 
- Publish your prompt as part of a "config."
- Test your config against a second, similar document to ensure it extracts the same target data.

## Get an account

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/). 

3. As a new user, you complete onboarding steps.

## View an example

1. After you complete Sensible's onboarding steps as a new user, navigate to a prebuilt example bank extraction at <https://app.sensible.so/editor/?d=llm_basics&c=bank_statement_2&g=bank_statement&om=1>. 

   Sensible displays an example document in the left pane, and fields of extracted data in the right pane. 



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_ui_llm_1.png)

## Extract more data 

Take the following steps to create prompts to extract more data from the document.

###  Extract facts

To extract short, simple facts, author queries.  Group them in a Query Group method if they're clustered within 1-2 pages of each other in the document. For example, append the following code to the array of fields in the left pane to extract two more facts:

```json
{
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "bank_name",
            "description": "What is the name of the bank?",
            "type": "string"
          },
          {
            "id": "bank_website",
            "description": "What is the banks website URL?",
            "type": "string"
          }
        ]
      }
    },
```

You should see additional extracted data as a result:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_1.png)



### Extract a table

The example already extracts the transaction history for the checking account. To extract the transaction history for the savings account,  copy the checking transactions field in the left pane, then modify it to extract your target data. For example, append the following field to the fields array in the left pane:

```json
{
      "id": "savings_transaction_history",
      "method": {
        "id": "nlpTable",
        "description": "savings transaction history, not checkings",
        "columns": [
          {
            "id": "date",
            "description": "date",
            "type": "date"
          },
          {
            "id": "description",
            "description": "description without totals",
            "type": "string"
          },
          {
            "id": "amount",
            "description": "amount",
            "type": "currency"
          }
        ]
      }
    }
```

You should see additional extracted data as a result.

## Publish the prompt

To extract similar data from other bank statements in production,  publish the "config" containing your prompt.

 Click **Publish configuration**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

Now you've published your config to the endpoint `https://api.sensible.so/v0/extract/llm_basics` document type, you can get document data at scale using Sensible's APIs, SDKs, or bulk-upload UI. Put the extracted data to work in Excel files, databases, and other destinations. For more information, see [Integrating](doc:integrate).

## Test the prompt

Let's see if the config containing your prompt works with other bank statements. To test the prompt, take the following steps:

1. Navigate to <https://app.sensible.so/editor/?d=llm_basics&c=bank_statement&g=bank_statement&om=1>. Notice that the middle pane now displays a statement for a different customer.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_1.png)

 Verify that the extracted data in the right pane also automatically updated to reflect the second example document.

## (Optional) Extract from your own documents

Sensible recommends grouping similar documents, for example, bank statements, into a *document type*. To extract data from your documents, first check if they're on Sensible's list of out-of-the-box [supported document types](doc:library-quickstart). If not, create document types and configure your custom extractions by using the interactive [tutorial](https://app.sensible.so/tutorial/) or taking the following steps:

1. To exit the visual editor, click **Sensible** in the upper left corner.
2. Click the **Document types** tab. Create a new document type using the dialog, then write prompts in the configuration editor to extract data using what you learned in previous steps.

## Next

### Learn more about extraction

For advanced extraction strategies, see [Choosing an extraction approach](doc:author).


### Integrate

Get extracted document data out of Sensible and put it to work in Excel files, databases, and other destinations. See [Integrating](doc:integrate).



