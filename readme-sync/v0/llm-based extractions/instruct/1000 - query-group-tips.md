---
title: "Query group extraction tips"
hidden: true

---

This Sensible Instruct method extracts individual facts in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery.

Sensible recommends grouping queries together if they share [context](doc:query-group#notes).  Queries share context when data exists in the same location or region of a document.

For example, contact information can usually be found in the same location of a document:

```
New York City, NY
(123) 456-7890
jsmith@email.com 
```

Combining queries for the location, phone number, and email into the same group will help you maximize the accuracy and speed of your extractions. Frame each query, or prompt, in the group so that it has a single, short answer. 

### Prompt Tips

- Try framing each query, or prompt, so that it has a single, short answer such as:

  - "company address"
  - "name of recipient"
  - "document date"

- See the following resources for creating prompts:

  -  [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering)
  -  [Introduction to prompt engineering](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/prompt-engineering)
  -  [Short course: Building systems with the ChatGPT API](https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/) and [Short course: ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/). 

- Search for the most relevant context and disambiguate between multiple possible answers by adding location information to prompts:
  
	**Location relative to page number and position on page**

  - "address in the **top left of the first page** of the document"

  - "What is the medical paid value on the **last claim of the second page**?"

  - "consumer electronics device with highest sales mentioned **near end of document**"

    **Location relative to content in document**

  - "total amount **in the expense table**"

  - "phone number after **section 2**"

## Troubleshooting

- For information about troubleshooting error messages about prompts, see [Qualifying LLM accuracy](doc:confidence).

- You can view the source text for an LLM's answer highlighted in the document. In the Sensible Instruct editor, click the **Location** button in the output of a query field to view its source text in the document. For more information about how location highlighting works and its limitations, see [Location highlighting](doc:query#notes).

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/location.png)
  
  

Examples
===

Example 1
---

The following example shows using the Query method to extract agricultural data from a government report:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/query_group_instruct.png)

To try out this example in the Sensible app, take the following steps: 

1. Download the following example document:

   | Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer_crop.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then click the document type you created to edit it. In the document type's **Reference documents** tab, upload the example document you downloaded in a previous step.

3. Click the document type's **Configurations** tab, create a new test configuration, and click the configuration you created to edit it.

4. Click **Sensible Instruct** and create fields to extract data using the following table:

| Field name                     | Method | Prompt                                                       |
| ------------------------------ | ------ | ------------------------------------------------------------ |
| report_date                    | Query  | "for which month and year does this report describe wheat production. look in beginning of the document for the answer" |
| change_in_production           | Query  | "by what amount did US wheat production estimate change this month? if it didn't change, respond with 'no change'"" |
| seed_use                       | Query  | "what was US wheat seed use this year in the US in millions of bushels?" |
| seed_use_change                | Query  | "by what amount did US wheat seed use change this year, in million bushels? Use a negative sign for negative change and a positive sign for positive change" |
| global_wheat_production_change | Query  | by what amount did global wheat production change this year, measured in MMT? look near the end of the document for the answer" |

Notes
===

For the full reference for this method in SenseML, see [Query method](doc:query).