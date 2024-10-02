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
- For advanced options, see [Advanced LLM prompt configuration](doc:prompt).

### Troubleshooting

- If Sensible partially extracts a multi-page list, for example skipping pages in the list, use a different LLM engine. For more information, see the [LLM Engine parameter](doc:list#parameters). 

### Notes

For the full reference for this method, see [List method](doc:list).
