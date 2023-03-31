---
title: "Table extraction tips"
hidden: false
---



Extracts TBD TODO test 

For more information about how to write instructions (or "prompts") for the Table method's Description parameters, see [Best practices for prompt engineering with OpenAI](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api).

**Tips**

Partially extracted tables may not be accurately captured. Try extracting all columns to get the best results.

Try framing each description as the exact title and column headers in the table.

You can improve results by being more specific:

- Budget column in the expense table
- Transaction amount column in the last column of the summary table
- Vehicle make (not model)

Examples
===

Example 1
----

The following example shows using the Table method to extract data from an auto insurance policy declaration:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/table_instruct.png)

To try out this example in the Sensible app, take the following steps: 

1. Download the following example PDF:

   | Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/nlp_table.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then click the document type you just created to edit it. In the document type's **Reference documents** tab, upload the example PDF you just downloaded.

3. Click the document type's **Configurations** tab, create a new test configuration, and click the configuration you just created to edit it.

4. Click **Sensible Instruct** and create fields to extract data using the following table:

| Field name | Method | Overall list description | Property ids and descriptions |
| ---------- | ------ | ------------------------ | ----------------------------- |

|      |      |
| ---- | ---- |

Notes
===
For the full reference for this method in SenseML, see [NLP Table](doc:NLP Table).
