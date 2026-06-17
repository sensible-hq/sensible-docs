---
title: April 2023
slug: april-2023
date: 2023-04-07
---

In the last month, we released a powerful new extraction tool powered by large-language models (LLMs), including GPT-4. We also released a new natural-language method, List, and several improvements to existing features.

## Visual authoring with GPT-4: Sensible Instruct

Sensible Instruct is a visual authoring tool that lets you simply describe the document data you want to extract and retrieve the results.  With Sensible Instruct, anyone from developers to business operations managers can transform documents into structured data.

Sensible Instruct methods are a natural-language subset of SenseML methods, and you can switch over from a visual view in Sensible Instruct to a JSON view in SenseML. Sensible Instruct offers the following methods:

* [Query](doc:query-tips)
* [List](doc:list-tips)
* [Table](doc:table-tips)

Check out our in-app interactive tutorial, or see the following slides for an overview.

<HTMLBlock>{`
<div style="position: relative; padding-bottom: calc(87.19723183391004% + 41px); height: 0;"><iframe src="https://demo.arcade.software/vEkxP2R6WLI0MuFt4aNu?embed" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>
`}</HTMLBlock>

## New feature: List method

With the newly released List method, you can extract repeating data in a document based on your description of the list’s overall contents and each individual item. Data such as the work history or skills on a resume, the vehicles on an auto insurance policy, or the line items on an invoice are best suited for this method. See the [Sensible Instruct tips](doc:list-tips) or the full [SenseML reference](doc:list) for more information.

This method is an alternative to the Table method, when the data you want can appear either as a table or as another layout. The List method can find data in paragraphs of free text or in more structured layouts, such as key/value pairs or tables. It's also a simpler alternative to [layout-based Sections](doc:sections) for less complex or less structured document layouts.

## Improvement: Header and footer preprocessors

The [Remove Header](doc:remove-header) and [Remove Footer](doc:remove-footer) preprocessors now let you define the header or area footer area to remove in inches. Use the new Offset Y parameter to define the area relative to the start or end of the page, or to a text anchor.

## Improvement: Updated to GPT-4 for NLP Table method

The NLP table method now uses GPT-4 instead of GPT-3 to return extracted tables. For more information about this method, see [Sensible Instruct tips](doc:table-tips) or the [full SenseML reference](doc:nlp-table). This method can now extract tables that span pages.

## Boolean logic for text matching

We've added All and Not to our Boolean match types. Along with Any, use these match types to write Boolean logic about the text you want to match in a document. For example, use the Any match to match on an array of synonymous terms if a document contains small wording variations across revisions. Or combine All and Not to write a condition like:  "match a line that meets ALL of the conditions: it includes "Email" but NOT "customer". For more information, see [Boolean matches](doc:match#boolean-matches).
