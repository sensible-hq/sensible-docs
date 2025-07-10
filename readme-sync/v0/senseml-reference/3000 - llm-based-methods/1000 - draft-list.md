---
title: "List"
hidden: true
---

This LLM-based method extracts repeating data in a document based on your description of the list’s overall contents and items. This method is suited to extracting data such as the work history on a resume, the vehicles on an auto insurance policy, or the line items on an invoice.

Use this method when your target data can appear either as a table or as another layout.

For advanced options, see [Advanced LLM prompt configuration](doc:prompt).

This method is an alternative to the [NLP Table](doc:nlp-table) method. 

#### Limitations

- Sensible can output lists of different maximum lengths depending on how you configure the LLM Engine and Single LLM Completion [parameters](doc:list#parameters). If the extracted list exceeds the limit, Sensible truncates the list.
- For highly complex repeating layouts, such as insurance loss run documents, use the [Sections](doc:sections) method.

#### Prompt tips

- The list description describes the overall contents for the list, while each property is a single description of an item that repeats in the list.
- For more information about how to write descriptions, or "prompts", see [Query Group](doc:query-group) extraction tips.

For information about how this method works, see [Notes](doc:list#notes).

[**Parameters**](doc:list#parameters)
[**Examples**](doc:list#examples)
[**Notes**](doc:list#notes)

Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method. 

**Note** You can configure some of the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrides the NLP preprocessor's parameter.




| key                   | **value**                                                    | description                                                  | interactions                                                 |
| :-------------------- | ------------------------------------------------------------ | :----------------------------------------------------------- | ------------------------------------------------------------ |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              | ***FIND CONTEXT***                                           |                                                              |
| searchBySummarization | boolean,<br/>or<br>`outline`, or <br/>`page` (equivalent to `true`)<br/> default: `false`<br/> | (Recommended) Configure this to search for [context](doc:prompt) using document summarization.<br/>If you set `page`, an LLM summarizes each page of the document to find context. <br/>If you set `outline`, an LLM summarizes each chunk of the document's content outline to find context. For more information, see [Advanced LLM prompt configuration](doc:prompt#recommended-locate-context-by-summarizing-document).<br/>This parameter is compatible with documents up to 1,280 pages long.<br/> | If you configure this parameter for a document 5 pages or under in length, Sensible submits the entire document as context, bypassing summarization.<br/> If you configure this parameter for a document over 5 pages long, then Sensible sets the Chunk Count parameter to 5 and ignores any configured value.<br/>Note that the LLM Engine parameter doesn't configure the LLMs Sensible uses for locating context with this parameter. |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |
|                       |                                                              |                                                              |                                                              |





Notes
===

For an overview of this method's default approach to locating context, see the following steps. 

For alternate approaches, see [Advanced LLM prompt configuration](doc:prompt#full-prompt).

### How it works by default


1. Sensible finds the chunks of the document that most likely contain your target data: 
     - Sensible splits the document into equal-sized chunks. 
     - Sensible scores each chunk by its similarity to the concatenated Description parameters.
     - Sensible selects a number of the top-scoring chunks:
       - If you specify Thorough or Long for the Mode parameter in the LLM Engine parameter, the Chunk Count parameter determines the number of top-scoring chunks Sensible selects to submit to the LLM.
       - If you specify Fast for the Mode parameter,  1. Sensible selects a number of top-scoring chunks as determined by the Chunk Count parameter. 2. To improve performance, Sensible removes chunks that are significantly less relevant from the list of top-scoring chunks. The number of chunks Sensible submits to the LLM can therefore be smaller than the number specified by the Chunk Count parameter.

2. Sensible batches the selected chunks into groups. The chunks in each page group can come from non-consecutive pages in the document.
     - If you set the Single LLM Completion parameter to True, then Sensible creates a single group that contains all the top-scoring chunks and sets a larger maximum token input limit for the single group (about 120k tokens) than it does for batched groups.

3. For each chunk group, Sensible submits a full prompt to an LLM. The full prompt includes the chunks as context, page-hinting data, and your prompts. The full prompt instructs the LLM to create a list formatted as a table, based on the context.
     - You can configure the LLM engine using the LLM Engine parameter. 

4. Sensible concatenates the results from the LLM for each page group and returns a list, formatted as a table.



