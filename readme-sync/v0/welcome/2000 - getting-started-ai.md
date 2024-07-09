---
title: "Getting started"
hidden: false
---

## Introduction

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Sensible is highly configurable. You can get simple data about text and images in documents in minutes by leveraging GPT-4 and other large language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful layout-based document primitives.

See the following list for an overview of going live with Sensible:

- **Learn** to extract data, or use out-of-the-box supported document types
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

2. Log into the [Sensible app](https://app.sensible.so/signin/). As a new user, you complete a guided walkthrough of the steps for extracting data from documents.

## View an example

1. After you complete Sensible's guided tour as a new user, navigate to a prebuilt example bank extraction at <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement>. 

   Sensible displays an example document in the left pane, and fields of extracted data in the right pane. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_1.png)

Take the following steps to create a prompt to extract more data from the document.

## Auto-extract data

To extract document data automatically, take the following steps:

1. Click **Query group**:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_2.png)

2. Click **Auto generate**, then click **Generate**:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_auto.png)

3. Sensible automatically generates queries and extracts their answers from the document:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_auto_2.png)

4. (Optional) Add more queries by clicking **Suggest queries**, selecting the field IDs that interest you, and clicking **Add selected queries**:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_auto_3.png)

To test the automatically generated extraction configuration with another document,  see [Test the prompt](doc:getting-started-ai#test-the-prompt). To author your own extraction configurations, see the following steps.

## Manually configure extraction

### Extract a table

So far, you've extracted short, simple facts. Now let's extract more complex data, such as tables and lists. To extract a table, take the following steps:

- Click **Back to fields**.

- Click **Table**

- The example already extracts the transaction history for the checking account. To extract the transaction history for the savings account, configure the table as shown in the following image. Configure a query for each column in the table, for example, `date`, `description`, and `amount`.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_11.png)

- Scroll down the right pane and click **Extract**. Sensible displays the extracted data. 

## Publish the prompt

To extract similar data from other bank statements in production,  publish the "config" containing your prompt.

 Click **Publish configuration**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

Now you've published your config, you can get document data at scale using Sensible's APIs, SDKs, or bulk-upload UI. Put the extracted data to work in Excel files, databases, and other destinations. For more information, see [Integrating](doc:integrate).

## Test the prompt

Let's see if the config containing your prompt works with other bank statements. To test the prompt, take the following steps:

1. Navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement_2>. Notice that the left pane now displays a statement for a different customer.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_8.png)

2. In the right pane, scroll down to view the fields you authored in previous steps. Verify that the extracted data automatically updated to reflect the second example document.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_9.png)

## (Optional) Extract more data

Try extracting more complex pieces of information. For example, try extracting the time period for each account using the [List method](doc:list-tips). See the  `accounts_list` field in this config for an example of using the List method.

Publish the config to save your changes.

## (Optional) Extract from your own documents

Sensible recommends grouping similar documents, for example, bank statments, into a *document type*. To extract data from your documents, first check if they're on Sensible's list of out-of-the-box [supported document types](doc:library-quickstart). If not, create document types and configure your custom extractions by using the interactive [tutorial](https://app.sensible.so/tutorial/) or taking the following steps:

1. To exit the Sensible Instruct editor, click **Sensible** in the upper left corner.
2. Click the **Document types** tab. Create a new document type by following the prompts, then write prompts in the configuration editor to extract data using what you learned in previous steps.

## Next

### Learn more about extraction

- See [prompt authoring tips](doc:instruct)
- Explore extracting lists, tables, and single data points with other interactive examples: 
  - [Resume](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=resume&g=resume&v=)
  - [Purchase contract](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=contract&g=contract&v=)

- For advanced extraction strategies, see [Choosing an extraction approach](doc:author)

### Integrate

Get extracted document data out of Sensible and put it to work in Excel files, databases, and other destinations. See [Integrating](doc:integrate).



