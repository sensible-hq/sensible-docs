---
title: "Getting started with AI-powered extractions"
hidden: false
---

In this tutorial, you'll learn to extract data out of a collection of similar documents using an AI-powered visual authoring tool, Sensible Instruct. You'll use natural language to instruct Sensible about which data to extract from an example document, as if you were chatting with an AI bot. Sensible uses large-language models (LLMs) such as GPT-4 to extract your target information.

You can then save your descriptions as an extraction configuration, or "config." Publish your config to automate extracting from similar documents.  

Use this tutorial if you want a guided tour of configuring AI-powered document extractions in the Sensible app. Or see the following links:

- You can mix and match Sensible Instruct methods with SenseML methods for advanced config authoring.  For more information about SenseML versus Sensible Instruct, see [Choosing extraction strategy](doc:author). For authoring in SenseML, see [Get started extracting with SenseML](doc:getting-started).
- If you instead want to explore without much explanation, then [sign up](https://app.sensible.so/register) for an account and check out our interactive in-app example extractions. For links to the examples, see [AI-powered resources](doc:no-code).

Get structured data from a bank statement
===

Let's get started with Sensible Instruct! Sensible Instruct makes it easy to specify in the data you want to extract from documents. If you can chat with an AI bot, then you can configure document extractions. 

 In this tutorial, you'll:

- Edit a collection of descriptions ("a config") about the data you want to extract from an example PDF
- Test the config against a second, similar PDF
- Download the extracted document data as an Excel sheet. 

Get an account
====

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

Configure the extraction
====

1. To view an example bank statement PDF extraction, navigate to [https://app.sensible.so/editor/instruct?d=sensible_instruct_basics&c=bank&g=bank](https://app.sensible.so/editor/instruct?d=sensible_instruct_basics&c=bank&g=bank). 

   You'll see a 'config', or list of instructions for extracting from the example menu document (in the left pane), and extracted data in the right pane.

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_1.png)
   
   
   
2. Take the following steps to edit the config to extract more data from the document.
   
Extract a query
-----

3. To extract a single data point from the document, click **Query**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_2.png)

  - Edit the query as shown in the following screenshot by entering `checking account number (not savings)` in the query field, then click the **Send** icon:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_3.png)

- You should see the extracted account number, `8347-3248`, populate in the **Extracted data** section.
- Click **Back to fields**.

Extract a table
-----

To extract a table, take the following steps:

1. Click  **Table**.

2. Configure the table extraction using the following screenshot and instructions:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_4.png)

| Field name                  | Method | Overall table description     | Column IDs and descriptions                                  |
| --------------------------- | ------ | ----------------------------- | ------------------------------------------------------------ |
| savings_transaction_history | Table  | "savings transaction history" | **date** - "date"<br/><br/>**description** - "description without totals"<br/><br/>**amount** - "amount" |

Click the **Send** icon for each column description.

3.  To verify the extracted data, scroll down in the right pane and compare the **Extracted data** section to the document in the left pane:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_5.png)

4. (**Optional**) To standardize the representation of the extracted dates and dollar amounts, configure types as shown in the following screenshots:

5. ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_6.png)

   You should see that the formatting of the extracted data changes according to the types you specified. For example, Sensible reformats the date`04/11/23` to a standardized output format, `2023-04-11`:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_7.png)

TODO talk about LIST
Test the config against another document
===

To test the config against a second example document, take the following steps:

1. To select a second example document, *bank_2.pdf*, navigate to [https://app.sensible.so/editor/instruct?d=sensible_instruct_basics&c=bank&g=bank_2](https://app.sensible.so/editor/instruct?d=sensible_instruct_basics&c=bank&g=bank_2). Or, select the document by clicking the dropdown in the left pane and selecting  **bank_2**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_8.png)

2. In the right pane, scroll down to the fields you authored in previous steps. Verify that the extracted information automatically updated to reflect the second example document: 

(Optional) Extract more data
===

Try out extracting other pieces of information, such as:

- The bank address or customer address
- The time period for each account. **Hint** To extract repeating data that isn't in table format, use the [List method](doc:list). For example, in this config, the `accounts_lis`t uses the list method.
- The Spanish-speaking customer service phone number.


Publish the config
===

To publish your config, click **Publish**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

(Optional) Export extracted data as spreadsheets
===

Now you've tested and published your config, you can upload new bank statements, automatically extract from them using the config, and download the extracted data as Excel.

Take the following steps:

1. Download the following PDF document:

| Example PDF | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/bank_3.pdf) |
| ----------- | ------------------------------------------------------------ |



1. Navigate to the [Quick Extraction](https://app.sensible.so/quick-extraction/) tab.
   1. In the dropdown in the right pane, select `sensible_instruct_basics / Auto select` . The document type, `sensible_instruct_basics`, contains configs for bank statements and other document types such as resumes and contracts.  When you specify `Auto select`,  Sensible automatically chooses the bank config when you upload a bank statement.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_11.png)



2. Click **Upload document** and select the document you just downloaded.
2. Click **Run Extraction**.

4. Sensible displays the extracted data as JSON in the right pane. Click the **Download excel** to convert the extracted document data to Excel:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/instruct/readme-sync/assets/v0/images/final/quickstart_instruct_12.png)



  The following spreadsheet shows the example output:

[block:html]
{
  "html": "<div><iframe class=\"spreadsheet\" src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vTwZYVB1DHgb-RrlCzqAMvnE0yUausiTp4CtEVIVeVVoTLyi8rFBmSyzfiznfPrbmbFnnifXAWZZPx6/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n<style>.spreadsheet{width:100%;height:200px}</style>"
}
[/block]

**Note** Each downloaded Excel file contains the data from one document. To combine extracted documents into one Excel file, use the [Sensible API](https://docs.sensible.so/reference/get-excel-extraction).



 