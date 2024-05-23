---
title: "Getting started"
hidden: false
---

## Overview

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Sensible is highly configurable. You can get simple data about text and images in documents in minutes by leveraging GPT-4 and other large language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful layout-based document primitives.



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform.png)

See the following list for an overview of going live with Sensible:

- **Learn** to extract data, or use out-of-the-box supported document types
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Quality control**](doc:validate-extractions) extracted data
-  [**Monitor**](doc:metrics) extracted data in production 

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

## View an example

When you register for a new account, you can upload a document to auto-extract data from it, or you can view Sensible's example document extractions. Take the following steps to view Sensible's example bank statements extractions:

1. When you sign in as a new user, Sensible displays the following dialog. In the dialog, select the following options:

   - Click **Start with a sample document**
   - Click **Finance**
   - Click **Bank statement**
   - Click **Get started**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_1.png) 

Sensible displays an example document in the middle pane, and fields of extracted data in the right pane. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_2.png)

Click a field to display the LLM prompts that extracts the data. For example, click the `ending_balance_all_accounts` field to view its prompts:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_3.png)

The left pane shows two queries that are grouped together (a "query group") because they target information that's clustered together within the same page or few pages in the document: 

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_4.png) 

To add your own prompt to the group, click **Create new query**, author your prompt, and click **Extract**. For example:









Let's see if the config containing your prompt works with other bank statements. To test the prompt, take the following steps:

1. Navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement_2>. Notice that the left pane now displays a statement for a different customer.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_8.png)





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

1. To author your own LLM prompts to extract data points from the document, click **Query group**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_2.png)

2. Edit the query group as shown in the following screenshot by entering `checking account number (not savings)` in the query field.  Click **Extract**. 
2. Sensible displays the extracted account number, `8347-32348`, in the **Extracted data** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_3.png)

4. Click **Back to fields**.

Congratulations! You extracted the checking account number from the bank statement.

## Publish the prompt

To extract checking account numbers from other bank statements in production,  publish the "config" containing your prompt.

 Click **Publish configuration**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

## Test the prompt

Let's see if the config containing your prompt works with other bank statements. To test the prompt, take the following steps:

1. Navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement_2>. Notice that the left pane now displays a statement for a different customer.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_8.png)

2. In the right pane, scroll down to the checking account number field you authored in previous steps. Verify that the extracted information automatically updated to reflect the second example document. For example, the account number updated from `8347-32348` to `9876-12345`: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_9.png)

It looks like your prompt was successful at extracting the checking account number from another document. Great! 

## (Optional) Extract more data

Try extracting more complex pieces of information. For example, try extracting the time period for each account using the [List method](doc:list-tips). See the  `accounts_list` field in this config for an example of using the List method.

Publish the config to save your changes.

## (Optional) Extract from your own documents

To extract data from your documents, first check if they're on Sensible's list of out-of-the-box [supported document types](doc:library-quickstart). If not, configure your custom extractions by using the interactive [tutorial](https://app.sensible.so/tutorial/) or taking the following steps:

1. To exit the Sensible Instruct editor, click **Sensible** in the upper left corner.
2. Click the **Document types** tab. Create a new document type, then click the type you created to edit it.
3. In the document type's **Reference documents** tab, upload your own example document.
4. In the document type's **Configurations** tab, create a new test configuration, and click the configuration you created to edit it.
5.  Write prompts in the configuration editor to extract data using what you learned in previous steps.

## Next

### Learn more about extraction

- See [prompt authoring tips](doc:instruct)
- Explore extracting lists, tables, and single data points with other interactive examples: 
  - [Resume](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=resume&g=resume&v=)
  - [Purchase contract](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=contract&g=contract&v=)

- For advanced extraction strategies, see [Choosing an extraction approach](doc:author)

### Integrate

Get extracted document data out of Sensible and put it to work in Excel files, databases, and other destinations. See [Integrating](doc:integrate).



