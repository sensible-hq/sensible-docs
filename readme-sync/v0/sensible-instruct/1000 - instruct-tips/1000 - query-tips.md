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

Download the following example document and upload it to Sensible (link)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_crop.pdf) |
| ----------- | ------------------------------------------------------------ |



Try creating a new configuration and asking the following questions about the example document in Sensible Instruct (link):

- for which month and year does this snippet describe wheat production
- by what amount did US wheat production estimate change this month? if it didn't change, respond with 'no change'
- what was US wheat seed use this year in the US in millions of bushels?
- by what amount did US wheat seed use change this year, in million bushels? Use a negative sign for negative change and a positive sign for positive change

You should see output like the following:

![image-20230323100044464](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230323100044464.png)



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question_instruct.png)

**Learn more**

For more details about how this method works see [Question method](doc:question).