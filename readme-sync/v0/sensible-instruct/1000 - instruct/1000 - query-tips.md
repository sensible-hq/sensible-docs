---
title: "Query extraction tips"
hidden: false

---

This Sensible Instruct method extracts an individual fact in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery.

**Tips**

- Try framing each query so that it has a single, short answer such as:

  - "company address"
  - "name of recipient"
  - "document date"

- You can narrow down your search and improve accuracy by adding location information:

    ​       **Location relative to page number and position on page**

  - "address in the top left of the first page of the document"

  - "What is the medical paid value on the last claim of the second page?"

  - "consumer electronics device with highest sales mentioned near end of document"

    **Location relative to content in document**

  - "total amount in the expense table"

  - "phone number after section 2"

    

- For more information about how to write instructions (or "prompts") for the Question method's Question parameter, see [Best practices for prompt engineering with OpenAI](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api).

Examples
===

Example 1
---

The following example shows using the Query method to extract agricultural data from a government report:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question_instruct.png)

To try out this example in the Sensible app, take the following steps: 

1. Download the following example PDF:

   | Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_crop.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then click the document type you just created to edit it. In the document type's **Reference documents** tab, upload the example PDF you just downloaded.

3. Click the document type's **Configurations** tab, create a new test configuration, and click the configuration you just created to edit it.

4. Click **Sensible Instruct** and create fields to extract data using the following table:

| Field name                     | Method | Describe what you want to extract                            |
| ------------------------------ | ------ | ------------------------------------------------------------ |
| report_date                    | Query  | "for which month and year does this report describe wheat production. look in beginning of the document for the answer" |
| change_in_production           | Query  | "by what amount did US wheat production estimate change this month? if it didn't change, respond with 'no change'"" |
| seed_use                       | Query  | "what was US wheat seed use this year in the US in millions of bushels?" |
| seed_use_change                | Query  | "by what amount did US wheat seed use change this year, in million bushels? Use a negative sign for negative change and a positive sign for positive change" |
| global_wheat_production_change | Query  | by what amount did global wheat production change this year, measured in MMT? look near the end of the document for the answer |

Notes
===

For the full reference for this method in SenseML, see [Question method](doc:question).