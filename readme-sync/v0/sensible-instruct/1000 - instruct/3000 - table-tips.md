---
title: "Table extraction tips"
hidden: false
---

This Sensible Instruct method extracts a table in a document based on your description of the table title and each of its column headers.

**Tips**

- Try extracting all columns to get the best results. If you describe only a few of the columns, your results may be less accurate.

- Try using the table titles or table column headers in the document as descriptions.

- For more information about how to write descriptions, or "prompts", see [Query extraction tips](doc:query-tips).


Examples
===

Example 1
----

The following example shows using the Table method to extract data from an auto insurance document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/nlp_table_instruct.png)



To try out this example in the Sensible app, take the following steps: 

1. Download the following example PDF:

   | Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/nlp_table.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then click the document type you created to edit it. In the document type's **Reference documents** tab, upload the example PDF you downloaded in a previous step.

3. Click the document type's **Configurations** tab, create a new test configuration, and click the configuration you created to edit it.

4. Click **Sensible Instruct** and create fields to extract data using the following table:

| Field name             | Method | Overall table description            | Column IDs and descriptions                                  |
| ---------------------- | ------ | ------------------------------------ | ------------------------------------------------------------ |
| insured_vehicles_table | Table  | "insured vehicles"                   | **manufacturer** - "vehicle make (not model)"<br/><br/>**year** - "year of manufacture" |
| transactions_table     | Table  | "transactions for insurance account" | **transaction_date** - "transaction date."<br/><br/>**transaction_description** - "transaction description" |

For example, use the following screenshot as a guide for configuring the `insured_vehicles_table` field:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/nlp_table_instruct_2.png)




Notes
===
For the full reference for this method in SenseML, see [NLP Table](doc:nlp-table).
