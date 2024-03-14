---
title: "Getting started"
hidden: false
---

## Overview

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. It's highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large-language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful layout-based document primitives.



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform.png)

See the following list for an overview of going live with Sensible:

- **Learn** to extract data, or use out-of-the-box supported document types
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Quality control**](doc:validate-extractions) extracted data
-  [**Monitor**](doc:metrics) extracted data in production 

This guide gets you started with the first step, extracting data.

## Learn to extract data

Let's get started with extracting document data from an example bank statement. We'll use a large-language model (LLM) prompt to extract a checking account number in minutes.

 In this guide, you'll:

- Extract data from an example document using a natural-language description of your target data 
- Publish your prompt as part of a "config."
- Test your config against a second, similar document to ensure it extracts the same target data.

## Get an account

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

## View an example

1. To view an example bank statement extraction, navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement>. 

   Sensible displays an example document in the left pane, and fields of extracted data in the right pane. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_1.png)

Take the following steps to create a prompt to extract more data from the document.

## Extract an account number from a bank statement

1. To extract data points from the document, click **Query group**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_2.png)

2. Edit the query group as shown in the following screenshot by entering `checking account number (not savings)` in the query field.  Click **Create new query** and enter  .  Click **Extract**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_3.png)

- Sensible displays the extracted account number, `8347-32348`, in the **Extracted data** section.
- Click **Back to fields**.

Congratulations! You extracted the checking account number from the bank statement.

## Publish the prompt

To extract checking account numbers from other bank statements, you'll need to publish the "config" containing your prompt.

 Click **Publish configuration**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

## Test the prompt

Let's see if the config containing your prompt works with other bank statements. To test the prompt, take the following steps:

1. Navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement_2>. Notice that the left pane now displays a statement for a different customer.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_8.png)

2. In the right pane, scroll down to the `account_num_checking` field you authored in previous steps. Verify that the extracted information automatically updated to reflect the second example document. For example, the account number updated from `8347-32348` to `9876-12345`: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_9.png)

It looks like your prompt was successful at extracting the checking account number from another document. Great! 

## (Optional) Extract more data

Try extracting other pieces of information using what you learned in previous steps, such as:

- The customer's address
- The Spanish-speaking customer service phone number
- The time period for each account. **Hint:** Use the [List method](doc:list). For example, in this config, the `accounts_list` uses the List method.

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



