---
title: "List tips"
hidden: false
---
This LLM-based method extracts repeating data in a document based on your description of the list’s overall contents and each individual item. Data such as the work history or skills on a resume, the vehicles on an auto insurance policy, or the line items on an invoice are best suited for this method. 

This method is an alternative to the [NLP Table](doc:table-tips) method, when the data you want can appear either as a table or as another layout. The List method can find data in paragraphs of free text or in more structured layouts, such as key/value pairs or tables.  

### Prompt tips

- The list description describes the overall contents for the list, while each property is a single description of an item that repeats in the list.
- You can use location hints to describe the target list's position in the document. For examples of location hints, see [Query Group](doc:query-group-tips) extraction tips.
- For more information about how to write descriptions, or "prompts", see [Query Group](doc:query-group-tips) extraction tips.
- For advanced options, see [Advanced prompt configuration](doc:prompt).

### Troubleshooting

- If Sensible partially extracts a multi-page list, for example skipping pages in the list, use a different LLM engine. For more information, see the [LLM Engine parameter](doc:list#parameters). 

Examples
===

Example 1
----

The following example shows using the List method to extract data from a restaurant menu:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/list_instruct.png)

To try out this example in the Sensible app, take the following steps: 

1. Download the following example document:

   | Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/list.pdf) |
   | ----------- | ------------------------------------------------------------ |

2. Create a test document type in the Sensible app, then follow the prompts in the dialog to upload the example document and create the type.

4. Create fields to extract data using the following table:

| Field name | Method | Overall list description                                     | Property descriptions                                        |
| ---------- | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| dinners    | List   | "dinner special menu items"                                  | "entree description"<br/><br/> "dinner price"                |
| desserts   | List   | "dessert special menu items"                                 | "dessert description"<br/><br/> "dessert price"              |
| wines      | List   | "red wines and white wines (not other drinks such as beers or liquors)" | "wine brand name"<br/><br/>"wine varietal name (not brand), for example, return 'Red:cabernet savignon' or 'white:varietal not found'"<br/><br/> "wine description"<br/><br/> "smallest wine serving size and its dollar price, formatted like '6 oz: $11'"<br/><br/> "second-smallest wine serving size and its dollar price, formatted like '6 oz: $11'"<br/><br/> "price per bottle, in dollars" |

For example, use the following screenshot as a guide for configuring the `dinners` field:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/list_instruct_2.png)

Notes
===

For the full reference for this method, see [List method](doc:list).
