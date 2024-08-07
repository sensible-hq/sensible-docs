---
title: "Query group extraction tips"
hidden: false

---

This LLM-based method extracts individual facts in a document, such as the date of an invoice, the liability limit of an insurance policy, or the destination address of a shipping container delivery. When you configure the Multimodal Engine parameter, this method can extra data from non-text images, such as photographs, charts, or illustrations. For an example, see [Example: Extract from images](doc:query-group#example-extract-from-images)

Sensible recommends grouping queries together if they share [context](doc:query-group#notes).  Queries share context when data exists in the same location or region of a document, for example, on the same page. You can configure context using [Advanced prompt configuration](doc:prompt). 

For example, contact information can usually be found in the same location of a document:

```
New York City, NY
(123) 456-7890
jsmith@email.com 
```

Combining queries for the location, phone number, and email into the same group will help you maximize the accuracy and speed of your extractions. Frame each query, or prompt, in the group so that it has a single, short answer. Sensible recommends a maximum group size of 10 queries.

### Prompt Tips

- Try framing each query, or prompt, so that it has a single, short answer such as:

  - "company address"
  - "name of recipient"
  - "document date"
- See the following resources for creating prompts:

  -  [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering)
  -  [Introduction to prompt engineering](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/prompt-engineering)
  -  [Short course: Building systems with the ChatGPT API](https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/) and [Short course: ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/). 

Examples
===

Example 1
---

The following example shows using the Query Group method to extract agricultural data from a government report:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/query_group_instruct.png)

To try out this example in the Sensible app, take the following steps: 

1. Download the following example document:

   | Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/summarizer.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then follow the prompts in the dialog to upload the example document and create the type.

4. Click **Query group** create the following queries to extract data using the following table:

| Prompt                                                       | (Optional) Type |
| ------------------------------------------------------------ | --------------- |
| tenancy terms start date                                     | Date            |
| tenancy terms end date                                       | Date            |
| number of days notice for tenant must give to terminate lease | String          |
| monthly rents in dollars                                     | Currency        |
| when is the rent due in the month                            | String          |
| grace period for the rent due                                | String          |
| late fee amount                                              | String          |
| fee in dollars for returned checks or rejected payments      | Currency        |

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/query_group_instruct_1.png)

Notes
===

For the full reference for this method, see [Query group method](doc:query-group).