---
title: "Getting started"
hidden: true
---

## Overview

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Sensible is highly configurable. You can get simple data about text and images in documents in minutes by leveraging GPT-4 and other large language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful layout-based document primitives.



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform_senseml.png)

See the following list for an overview of going live with Sensible:

- **Learn** to extract data, or use out-of-the-box supported document types
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Quality control**](doc:validate-extractions) extracted data
-  [**Monitor**](doc:metrics) extracted data in production 

This guide gets you started with the first step, extracting data.

## Learn to extract data

Let's get started with extracting document data from an example bank statement. We'll author a prompt for a large language model (LLM) to extract document information in minutes. 

 In this guide, you'll:

- View example document extractions.
- Test the example extraction configuration against similar documents to ensure it extracts the same target data, for example, a checking account number.
- Extract data from an example document using natural-language prompts describing your target data.
- Publish your prompts as part of a "config" so you can extract from documents in bulk.

**Note:** In addition to LLM-based extractions, Sensible offers [layout-based](doc:getting-started) extraction methods for advanced use cases.

## Get an account

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

## View an example

When you register for a new account, you can upload a custom document to auto-extract data from it, or you can view Sensible's collection of examples. Take the following steps to view an example extraction:

1. Log into the [Sensible app](https://app.sensible.so/signin/) as a new user. Sensible displays the following onboarding dialog. In the dialog, select the following options:

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

- Click the second example document in the left pane. Verify that the extracted fields updated with new data. For example, verify that the `beginning_balance_all_accounts` field updated from `$61715.98` to `$181527.75` :

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_8.png)

For supported fields, you can click the location icon to view the source location in the document for the extraction data:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_9.png)

### Upload your own example

To test one of your own documents, take the following steps:

- In the left pane, click **Add file**.
- Select a new example bank statement to upload from your local file system:
  - If you use one of your own bank statement, ensure it combines multiple accounts. Note that extracting data from single-account bank statements using our out-of-the-box [support](doc:library-quickstart) is outside the scope of this tutorial. 
  - If you don't have a statement on hand, you can download the following example, then upload it to the Sensible app:


| Example document | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/bank_statements/bank_of_america/boa_sample.pdf) |
| ---------------- | ------------------------------------------------------------ |

- Click your uploaded document in the left pane and verify that the extracted data updated for the new file. For example:


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_13.png)


## Edit extraction configuration

Behind the scenes, an *extraction configuration* extracts data from each document using queries, or *fields*. The fields can be based on prompts for LLM, or on layout-based extraction rules written in JSON. Let's take a look at LLM-based prompts.

### View the prompts

To edit a prompt, click a field to display the LLM prompts that extract the data. For example, in the `Alley` bank statement example,  click the `ending_balance_all_accounts` field to view its prompts:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_3.png)

The left pane shows two prompts that are grouped together (a "query group") because they target information that's clustered together in a one- to two-page range in the document. Note that the information in the group must be co-located, but it doesn't need to be conceptually related. For an example, see the following image: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_4.png) 

Click a prompt to edit it. Or see the following steps to author more prompts.

### Extract more data

To manually author an extraction prompt, click **Create new query**, author your prompt, and click **Extract**. Sensible displays the extracted data below the prompt. For example, for the `Alley` bank statement:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_5.png) 

### Auto-extract  data

To extract document data by automatically authoring prompts, take the following steps:

1. Click **Suggest queries**. Sensible suggests relevant facts to extract.
2. Select the facts that you want to extract from the document, then click **Add selected**:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_6.png) 

Sensible displays the auto-generated prompts and extracted data:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_llm_7.png) 



## Publish the prompts and integrate

To extract data from bank statements in bulk in production,  publish the "config" containing your prompt.

 Click **Publish configuration**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

Now you've published your config, you can get document data at scale using Sensible's APIs, SDKs, or bulk-upload UI. Put the extracted data to work in Excel files, databases, and other destinations. For more inforamtion, see [Integrating](doc:integrate).

## Next: Learn more about extraction

- See [prompt authoring tips](doc:instruct)
- For advanced extraction strategies, see [Choosing an extraction approach](doc:author)





