---
title: "Getting started with AI-powered extractions"
hidden: false
---

In this tutorial, you'll learn to extract data from a set of similar documents using an AI-powered visual authoring tool, Sensible Instruct. You'll use natural language to instruct Sensible about which data to extract from an example document. Sensible uses large-language models (LLMs) such as GPT-4 to extract your target information.

You can then save your descriptions as an extraction configuration, or "config." Publish your config to automate extracting from similar documents.  

Use this tutorial if you want a guided tour of configuring AI-powered document extractions in the Sensible app. Or see the following links:

- You can mix and match Sensible Instruct methods with SenseML methods for advanced config authoring. SenseML is a superset of Sensible Instruct. For more information about SenseML versus Sensible Instruct, see [Choosing extraction approach](doc:author). For authoring in SenseML, see [Getting started with SenseML](doc:getting-started).
- If you want to explore without much explanation, [sign up](https://app.sensible.so/register) for an account and check out our interactive in-app example extractions. For links to the examples, see [AI-powered resources](doc:no-code).

Get structured data from a bank statement
===

Let's get started with Sensible Instruct! Sensible Instruct makes it easy to specify the data you want to extract from documents.

 In this tutorial, you'll:

- Edit a collection of descriptions ("a config") about the data you want to extract from an example PDF
- Test the config against a second, similar PDF
- Download extracted document data as an Excel sheet. 

Get an account
====

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

Configure the extraction
====

1. To view an example bank statement PDF extraction, navigate to [https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement). 

   You'll see a "config", or list of instructions for extracting from the example document (in the left pane), and extracted data in the right pane.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_1.png)

   

2. Take the following steps to edit the config to extract more data from the document.
   
Extract a query
-----

3. To extract a single data point from the document, click **Query**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_2.png)

  - Edit the query as shown in the following screenshot by entering `checking account number (not savings)` in the query field. Give the query an ID, `account_num_checking` then click the **Send** icon:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_3.png)

- You should see the extracted account number, `8347-3248`, populate in the **Extracted data** section.
- Click **Back to fields**.

Extract a table
-----

To extract a table, take the following steps:

1. Click  **Table**.

2. Configure the table extraction using the following screenshot and instructions:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_4.png)

| Field name                  | Method | Overall table description     | Column IDs and descriptions                                  |
| --------------------------- | ------ | ----------------------------- | ------------------------------------------------------------ |
| savings_transaction_history | Table  | "savings transaction history" | **date** - "date"<br/><br/>**description** - "description without totals"<br/><br/>**amount** - "amount" |

Click the **Send** icon for each column.

3.  To verify the extracted data, scroll down in the right pane and compare the **Extracted data** section to the document in the left pane:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_5.png)

4. (**Optional**) To standardize the representation of the extracted dates and dollar amounts, configure `date` and `currency` types as shown in the following screenshots:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_6.png)

   You should see that the formatting of the extracted data changes according to the types you specified. For example, Sensible reformats the date `04/11/23` to a standardized output format, `2023-04-11`:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_7.png)

Test the config against another document
===

To test the config against a second example document, take the following steps:

1. Download the following document:


| Example PDF | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/bank_2.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Navigate to the **Reference documents** tab of the `sensible_instruct_basics` document type at [https://app.sensible.so/document-types/detail/?d=sensible_instruct_basics&t=reference_documents](https://app.sensible.so/document-types/detail/?d=sensible_instruct_basics&t=reference_documents). 
3. Click **Upload document** and select the document you just downloaded.

1. To test the uploaded document, *bank_2.pdf*, navigate to [https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_2](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_2):

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_8.png)

2. In the right pane, scroll down to the fields you authored in previous steps. Verify that the extracted information automatically updated to reflect the second example document. For example, the account number updated from `8347-3248` to `987612345`: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_9.png)

(Optional) Extract more data
===

Try out extracting other pieces of information using what you learned in previous steps, such as:

- The bank address or customer address
- The time period for each account. **Hint:** To extract repeating data that isn't in table format, use the [List method](doc:list). For example, in this config, the `accounts_list` uses the List method.
- The Spanish-speaking customer service phone number.


Publish the config
===

To publish your config, click **Publish**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

(Optional) Export extracted data as spreadsheets
===

Now you've tested and published your config, you can upload new bank statements, automatically extract from them using the config, and download the extracted data as Excel.

Take the following steps:

1. Download the following PDF document:

| Example PDF | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/bank_3.pdf) |
| ----------- | ------------------------------------------------------------ |



1. Navigate to the [Quick Extraction](https://app.sensible.so/quick-extraction/) tab.
   1. In the dropdown in the right pane, select `sensible_instruct_basics / Auto select` . The document type, `sensible_instruct_basics`, contains configs for bank statements and other document types such as resumes and contracts.  When you specify `Auto select`,  Sensible automatically chooses the bank config when you upload a bank statement.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_11.png)



2. Click **Upload document** and select the document you just downloaded.
2. Click **Run Extraction**.

4. Sensible displays the extracted data as JSON in the right pane. Click the **Download excel** to convert the extracted document data to Excel:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_12.png)



  The following spreadsheet shows the example output. The first tab contains fields with single values, for example the start date field, and succeeding tabs contain fields with table output, for example, the account list table. 

[block:html]
{
  "html": "<div><iframe class=\"spreadsheet\" src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vTwZYVB1DHgb-RrlCzqAMvnE0yUausiTp4CtEVIVeVVoTLyi8rFBmSyzfiznfPrbmbFnnifXAWZZPx6/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n<style>.spreadsheet{width:100%;height:200px}</style>"
}
[/block]

**Note** Each downloaded Excel file contains the data from one document. To combine extracted documents into one Excel file, use the [Sensible API](https://docs.sensible.so/reference/get-excel-extraction).

Next
---

Congratulations! You edited your first config and extracted your first document data. 

- If you want to process bank statements generated by a different company, you can [import](https://app.sensible.so/library/) our [pre-authored configs](https://github.com/sensible-hq/sensible-configuration-library/tree/main/bank_statements) for several major banks and get started with out-of-the-box extractions. 
- Or, create a new config for your custom documents:
  - In the [**Document Types**](https://app.sensible.so/document-types/) tab, Click **New document type**  to create a new document type and name  it. Leave the defaults and click **Create**.
  - In the document type's **Reference documents** tab, upload an example of the type of PDF document you want to extract from.
  - In the document type's **Configurations** tab, create a new test configuration, and click the configuration you just created to edit it.
  
  - Click **Sensible Instruct** and create fields to extract data using what you've learned in this guide.

