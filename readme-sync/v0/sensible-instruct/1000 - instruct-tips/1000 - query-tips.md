---
title: "Query extraction tips"
hidden: false

---



**Best practices/tips**

- For more information about how to write instructions (or "prompts") for the Question method's Question parameter, see [Best practices for prompt engineering with OpenAI](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api).
- Suited to labeled data. For example, `"Policy end date: Sept 23, 2023"`  or `"Date of birth: 2000"`. When extracting non-labeled data, using "positional" or layout-based natural language language helps (for example, `what is the company name in the top left of the document`).
- Being as specific as possible will give the best results (including location, section of the document, type of data, rough location in the document such as 'near the beginning' or 'near the end').
- Capable of manipulating output in the question. For example, asking a question and following that with “where unchecked boxes mean no” will output no for unchecked boxes

Try framing each query so that it has a single, short answer such as:

- Address
- Name of recipient
- Date

You can narrow down your search and improve accuracy by being more specific:

- Address in the top left of the document
- Total amount in the expense table
- Phone number in section 2

**How to extract a query**

See TBD TODO LINK TO (video, getting started, etc)

Examples
===

Example 1
---

The following example shows using the Query method to extract agricultural data from a government report:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/query.png)

To try out this example in the Sensible app, take the following steps: 

1. Download the following example PDF:

   | Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_crop.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then click the document type you just created to edit it. In the document type's **Reference documents** tab, upload the example PDF you just downloaded.

3. Click the document type's **Configurations** tab, create a new test configuration, and click the configuration you just created to edit it.

4. Click **Sensible Instruct** and create fields using the following table:

| Field name           | Method | Describe what you want to extract                            |
| -------------------- | ------ | ------------------------------------------------------------ |
| report_date          | Query  | "for which month and year does this snippet describe wheat production" |
| change_in_production | Query  | "by what amount did US wheat production estimate change this month? if it didn't change, respond with 'no change'"" |
| seed_use             | Query  | "what was US wheat seed use this year in the US in millions of bushels?" |
| seed_use_change      | Query  | "by what amount did US wheat seed use change this year, in million bushels? Use a negative sign for negative change and a positive sign for positive change" |

Notes
===

For the full reference for this method in SenseML, see [Question method](doc:question).