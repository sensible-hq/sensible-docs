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

##  Test more documents

### View a second example

Let's test that the fields in the right pane can accurately extract data from a second document. To test a second bank statement:

- Click the second example document in the left pane. Verify that the extracted fields updated:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_8.png)

For supported fields, you can click the location icon to view the source of the extraction data:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_9.png)

### Upload your own example

To test one of your own documents, take the following steps:

- In the left pane, click **Add file**.
- Select your own bank statement, preferably one that combines multiple accounts.

- Click your uploaded document in the left pane and verify that the extracted data updated for the new file.

## Edit extraction configuration

If you uploaded your own bank statement in the previous statement and observed any inaccurately extracted data, then you can edit the extraction configuration for each field.  

### View the prompts

To edit, click a field to display the LLM prompts that extracts the data. These prompts are how you configure extractions. For example, in the `Alley` bank statement example,  click the `ending_balance_all_accounts` field to view its prompts:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_3.png)

The left pane shows two prompts that are grouped together (a "query group") because they target information that's clustered together in a one- to two-page range in the document: 

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_4.png) 

Click a prompt to edit it. Or see the following steps to author more prompts.

## Extract more data

To manually author an extraction prompt, click **Create new query**, author your prompt, and click **Extract**. Sensible displays the extracted data below the prompt. For example, for the `Alley` bank statement:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_5.png) 

## Auto-extract more data

To extract document data by automatically authoring prompts, take the following steps:

1. Click **Suggest queries**.
2. Select the data points that you want to extract from the document, then click **Add selected**:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_6.png) 

Sensible displays the auto-generated prompts and extracted data:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_7.png) 

## Extract a table

So far, you've extracted short, simple facts. Now let's extract more complex data, such as tables and lists. To extract a table, take the following steps:

- Click **Back to fields**.

- Click **Table**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_10.png)

- To extract the account activity for the savings account, configure the table as shown in the following image. Configure a query for each column in the table, for example, `credits`, `debits`, and `balance`.

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_11.png)

- Scroll down the right pane and click **Extract**. Sensible displays the extracted data:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_12.png)

   It looks like your prompt was successful at extracting the account activity. Great! 



## Publish the prompt and integrate

To extract data from bank statements at scale in production,  publish the "config" containing your prompt.

 Click **Publish configuration**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

### 

Now it's published you can get document data using Sensible's APIs, SDKs, or bulk-upload UI. Put the extracted data to work in Excel files, databases, and other destinations. See [Integrating](doc:integrate).



## Next: Learn more about extraction



- See [prompt authoring tips](doc:instruct)
- Explore extracting lists, tables, and single data points with other interactive examples: 
  - [Resume](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=resume&g=resume&v=)
  - [Purchase contract](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=contract&g=contract&v=)

- For advanced extraction strategies, see [Choosing an extraction approach](doc:author)





