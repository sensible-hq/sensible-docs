---
title: draft Getting started
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This topic is a draft.

## Introduction

See the following list for an overview of how to automate your document processing with Sensible:

* **Learn** to extract data from documents, or use out-of-the-box extraction support
* [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
* [**Quality control**](doc:validate-extractions) extracted data
* [**Monitor**](doc:metrics) and [**review**](doc:human-review)  extracted data in production 

This guide gets you started with the first step, extracting data.

## Learn to extract data

Let's get started with extracting document data from an example bank statement. We'll author a prompt for a large language model (LLM) to extract data in a matter of minutes.

 In this guide, you'll:

* Extract data from an example document using a natural-language description of your target data, for example, "what's the customer service number?". 
* Publish your prompt as part of a "config."
* Test your config against a second, similar document to ensure it extracts the same target data.

## Get an account

<!-- test { "testId": "hello-world" } -->

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

<!-- step { "checkLink": { "url": "https://app.sensible.so/register" } } -->

2. Log into the [Sensible app](https://app.sensible.so/signin/). 

<!-- step { "checkLink": { "url": "https://app.sensible.so/signin/" } } -->

<!-- test end -->

3. As a new user, you complete onboarding steps.

## View an example

1. After you complete Sensible's onboarding steps as a new user, navigate to a prebuilt example bank extraction at [https://app.sensible.so/editor/?d=llm\_basics\&c=bank\_statement\&g=bank\_statement\_2\&om=1](https://app.sensible.so/editor/?d=llm_basics\&c=bank_statement\&g=bank_statement_2\&om=1). 

   Sensible displays an example document in the left pane, and fields of extracted data in the right pane. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickstart_llm_13.png) 

## Extract more data

Take the following steps to create prompts to extract more data from the document.

### Extract facts

To extract short, simple facts, author queries.  Group them in a Query Group method if they're clustered within 1-2 pages of each other in the document. For example, append the following code to the array of fields in the left pane to extract two more facts:

```json
{
      "method": {
        "id": "queryGroup",
        "searchBySummarization": "page",
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

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickstart_llm_1.png)

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

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickstart_instruct_10.png)

Now you've published your config to the endpoint `https://api.sensible.so/v0/extract/llm_basics` document type, you can get document data at scale using Sensible's APIs, SDKs, or bulk-upload UI. Put the extracted data to work in Excel files, databases, and other destinations. For more information, see [Integrating](doc:integrate).

## Test the prompt

Let's see if the config containing your prompt works with other bank statements. To test the prompt, take the following steps:

1. Navigate to [https://app.sensible.so/editor/?d=llm\_basics\&c=bank\_statement\&g=bank\_statement\&om=1](https://app.sensible.so/editor/?d=llm_basics\&c=bank_statement\&g=bank_statement\&om=1). Notice that the middle pane now displays a statement for a different customer.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickstart_ui_llm_2.png)

 Note that the extracted data in the right pane automatically updates to reflect the second example document.

## (Optional) Extract from your own documents

Sensible recommends grouping similar documents, for example, bank statements, into a *document type*. To extract data from your documents, first check if they're on Sensible's list of out-of-the-box [supported document types](doc:library-quickstart). If not, create document types and configure your custom extractions by taking the following steps:

1. To exit the SenseML editor, click **Sensible** in the upper left corner.
2. Click the **Document types** tab. Create a new document type using the dialog, then write prompts in the configuration editor to extract data using what you learned in previous steps.

## Row method example

The following example shows  extracting data from two consecutive tables using the Row method:

1. The first field has an anchor with two matches to avoid duplicate text in the second table. First the anchor matches the text `most popular on github`, then it anchors on the text  `first`  in a row. The method then extracts the top-ranked GitHub language name to the left of the anchor match. 
2. The second field also has an anchor with two matches. It anchors on the row containing `Python`, then extracts the second percentage in the row to the right of the anchor.

**Config**

```json
{
  "fields": [
    {
      "id": "number_1_language_on_github", /* user-friendly ID for extracted target data */
      "anchor": { /* an anchor is text that always occurs in the same position relative to your target data. */
        "match": [ /* array of Match objects. Sensible matches the last element
                      if each element matches a successive line in the document */
          {
            "text": "most popular on github", /* string to match */
            "type": "includes" /* match anywhere in line. */
          },
          {
            "text": "first", /* string to match */
            "type": "startsWith" /* line must start with the match */
          }
        ]
      },
      "method": {
        "id": "row", /* target data to extract is distributed on same horizontal line as anchor */
        "position": "left", /* target data is to left of anchor. */
      }
    },
    {
      "id": "python_change_in_TIBOE_rating", /* user-friendly ID for extracted target data */
      "type": "percentage", /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
      "anchor": { /* an anchor is text that always occurs in the same position relative  */
        "match": [ /* array of Match objects. Sensible matches the last element if each element matches a successive line in the document */
          {
            "text": "popular in search engines", /* string to match */
            "type": "includes" /* match anywhere in line. */
          },
          {
            "text": "Python", /* string to match */
            "type": "startsWith" /* line must start with the match */
          }
        ]
      },
      "method": {
        "id": "row", /* target data to extract is distributed on same horizontal line as anchor */
        "tiebreaker": 1 /* extract the line in the first non-empty cell to the right of the anchor. */
      }
    }
  ]
}
```

**Example document**

The following image shows the data extracted by this config for the following example document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/row.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/row_column.pdf) |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "number_1_language_on_github": {
    "value": "Javascript",
    "type": "string"
  },
  "python_change_in_TIBOE_rating": {
    "source": "2.75%",
    "value": 2.75,
    "type": "percentage"
  }
}
```

## Next

### Learn more about extraction

For advanced extraction strategies, see [Choosing an extraction approach](doc:author).

### Integrate

Get extracted document data out of Sensible and put it to work in Excel files, databases, and other destinations. See [Integrating](doc:integrate).