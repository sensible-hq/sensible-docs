---
title: "Query extraction tips"
hidden: false

---

This method extracts an individual fact in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery.

**Tips**

- Try framing each query so that it has a single, short answer such as:

  - "company address"
  - "name of recipient"
  - "document date"

- You can narrow down your search and improve accuracy by being more specific:

  - "address in the top left of the document"
  - "total amount in the expense table"
  - "phone number in section 2"

- For more information about how to write instructions (or "prompts") for the Question method's Question parameter, see [Best practices for prompt engineering with OpenAI](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api).

Examples
===

Example 1
---

The following example shows using the Query method to extract agricultural data from a government report:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/query_instruct.png)

To try out this example in the Sensible app, take the following steps: 

1. Download the following example PDF:

   | Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_crop.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then click the document type you just created to edit it. In the document type's **Reference documents** tab, upload the example PDF you just downloaded.

3. Click the document type's **Configurations** tab, create a new test configuration, and click the configuration you just created to edit it.

4. Click **Sensible Instruct** and create fields  extract data using the following table:

| Field name           | Method | Describe what you want to extract                            |
| -------------------- | ------ | ------------------------------------------------------------ |
| report_date          | Query  | "for which month and year does this snippet describe wheat production" |
| change_in_production | Query  | "by what amount did US wheat production estimate change this month? if it didn't change, respond with 'no change'"" |
| seed_use             | Query  | "what was US wheat seed use this year in the US in millions of bushels?" |
| seed_use_change      | Query  | "by what amount did US wheat seed use change this year, in million bushels? Use a negative sign for negative change and a positive sign for positive change" |

Notes
===

For the full reference for this method in SenseML, see [Question method](doc:question).