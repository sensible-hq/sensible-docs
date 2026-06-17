---
title: August 2023
slug: august-2023
date: 2023-08-01
---

In the last month, we introduced new traceability for the LLM-powered Query method by highlighting the source text for the LLM's answer in the document, made advanced LLM prompt configuration options available in the Sensible Instruct editor for the Query method, made filtering past extractions available in the app and API, and released a new preprocessor for handling page-rotation edge cases.

## New feature: Highlight source text location for LLM's response in document

For the Query method, you can now view the source text for an LLM's answer highlighted in the document you're extracting data from. In the Sensible Instruct editor,  click the **Location** button in the output of a query field to view its source line or lines in the document.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_August2023_location.png)

Since an LLM's answer can vary from the original text in the document, Sensible uses fuzzy matching to highlight the source text. For more information about how location highlighting works and its limitations, see the [Query](doc:query#notes) method.

## New feature: Highlight source document chunks for LLM's response

As  an alternative to highlighting the source text location for an LLM response in the Sensible Instruct editor, you can also view the top-scoring [chunks](doc:prompt) for the Instruct methods in the SenseML editor. This alternative is more robust than the newly released location highlighting feature, since it doesn't rely on fuzzy matching, but less precise. Sensible outlines the chunks with green rectangles. Note that for the Query and List methods, Sensible merges highlighting for contiguous chunks into one highlighted rectangle. Sensible doesn't highlight chunks for any fields listed in the Suppress Output method.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_August2023_chunk_query.png) 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_August2023_chunk_nlp_table.png) 

## New feature: Filter past extractions

In the **Extractions** tab, you can now filter and view up to 1,000 past extractions, instead of being limited to the 50 most recent extractions. Filter by time range, document types, configurations, environments, and statuses. You can get the same summarized list of past extractions using the new [List extractions](ref:list-extractions) endpoint. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_August2023_filter.png) 

## New feature: Rotate Page preprocessor

In most cases, Sensible corrects page rotation automatically. For edge cases, we've introduced the Rotate Page preprocessor. For example, if a scanned document contains vertically oriented text, and the scanner adds automatically generated horizontal text, you can use this preprocessor to correct the mix of text orientations. Configure the preprocessor to match the text that you want to see horizontally aligned. 

For example, match text in an ID card to ensure it's horizontal, while ignoring the automatically generated vertical text near the card:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/rotate_page_2.png)

For more information, see the [Rotate Page](doc:rotate-page) preprocessor.

## UX improvement: Advanced Query method options in Sensible Instruct

Several of the advanced prompt configuration we released [last month](changelog:july-2023) are now available in the Sensible Instruct editor in addition to the SenseML editor:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_August2023_instruct.png)

You can configure the following parameters in Sensible Instruct for the Query method in individual fields:

* Page Hinting
* Prompt Introduction
* Context Description
* Chunk Scoring Text
* Chunk Size
* Chunk Overlap Percentage
* Chunk Count

For more information, see [Advanced prompt configuration](doc:prompt).
