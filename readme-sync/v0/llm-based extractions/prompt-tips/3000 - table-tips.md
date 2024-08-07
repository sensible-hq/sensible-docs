---
title: "NLP table extraction tips"
hidden: false
---

This LLM-based method extracts a table in a document based on your description of the table title and each of its column headers.

**Prompt Tips**

- Extract all columns to get the best results. If you describe only a few of the columns, your results may be less accurate.

- Use the table titles or table column headers in the document as descriptions.

- For more information about how to write descriptions, or "prompts", see [Query Group](doc:query-group-tips).

- For advanced options, see [Advanced prompt configuration](doc:prompt).


Examples
===

Example 1
---



The following example shows using the NLP Table method to extract data from a bank statement:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_4.png)

To try out this example in the Sensible app, take the following steps: 

1. Navigate to the following example document:

   | Example document | [https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement) |
   | ----------- | ------------------------------------------------------------ |

2. Create fields to extract data using the following table:


| Field name                  | Method | Overall table description     | Column IDs and descriptions                                  |
| --------------------------- | ------ | ----------------------------- | ------------------------------------------------------------ |
| savings_transaction_history | NLP Table  | "savings transaction history" | **date** - "date"<br/><br/>**description** - "description without totals"<br/><br/>**amount** - "amount" |

Click the **Send** icon for each column.

3. To verify the extracted data, scroll down in the right pane and compare the **Extracted data** section to the document in the left pane:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_5.png)

4. (**Optional**) To standardize the representation of the extracted dates and dollar amounts, configure `date` and `currency` types as shown in the following screenshots:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_6.png)

   You should see that the formatting of the extracted data changes according to the types you specified. For example, Sensible reformats the date `04/11/23` to a standardized output format, `2023-04-11`:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_7.png)



Example 2
----

The following example shows using the NLP Table method to extract data from an auto insurance document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/nlp_table_instruct.png)



To try out this example in the Sensible app, take the following steps: 

1. Download the following example document:

   | Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/nlp_table.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then follow the prompts in the dialog to upload the example document and create the type.

4. Create prompts to extract data using the following table:

| Field name             | Method | Overall table description            | Column IDs and descriptions                                  |
| ---------------------- | ------ | ------------------------------------ | ------------------------------------------------------------ |
| insured_vehicles_table | NLP Table  | "insured vehicles"                   | **manufacturer** - "vehicle make (not model)"<br/><br/>**year** - "year of manufacture" |
| transactions_table     | NLP Table  | "transactions for insurance account" | **transaction_date** - "transaction date."<br/><br/>**transaction_description** - "transaction description" |

For example, use the following screenshot as a guide for configuring the `insured_vehicles_table` field:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/nlp_table_instruct_2.png)




Notes
===
For the full reference for this method, see [NLP Table](doc:nlp-table).
