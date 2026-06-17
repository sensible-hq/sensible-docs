---
title: August 2025
slug: august-2025
date: 2025-08-05
---

In the last month, Sensible significantly improved LLM accuracy for long documents with a new document-outlining feature and added several advanced configuration options for layout-based methods. 

## Improvement: Enhanced LLM accuracy with document outlining

For LLM-based methods, Sensible improved its ability to accurately locate target data to extract, especially in long or repetitive documents. When you set the new `"searchBySummarization": "outline"`  option, Sensible generates a content-based outline of the document behind the scenes, summarizes each segment of the outline, and locates the answers to your LLM prompts based on the summaries. Outline-based summaries can be more accurate but slower than Sensible's existing page-based summaries. The [Query Group](doc:query-group#parameters)  and [List](doc:list#parameters)  methods support the new outline option.

 For more information, see [Advanced LLM prompt configuration](doc:prompt).

## Improvement: Advanced syntax for concise Match arrays

When you want to match the nth occurrence of a string or regular expression, the new Repeat match object is a more concise alternative to a [match array](doc:match-arrays). For example, to find the fifth occurrence of the string "customer account", you can specify:

```json
"match": [
          {
            /* match the 5th line that starts with "customer account" */
            "type": "repeat",
            "times": 5,
            "match": { "type": "startsWith", "text": "customer account" }
          }
        ]
```

For more information, see [Repeat match](doc:match#repeat-match). 

## New feature: Advanced JsonLogic rounding operation

In addition to the existing JsonLogic operators for transforming extracted data, Sensible released the new Round operator. This allows you to round a number to the specified decimal place. For more information, see [Round](doc:jsonlogic#round). 

## Improvement: Advanced Text Table configuration

You can now troubleshoot newline detection in multiline cells for the Text Table method. When varying font sizes cause row recognition issues, use the new Max Gap parameter to configure the expected vertical gaps in cells.

For example, in the following image, you can configure the Max Gap parameter to correct the Text Table method's default interpretation of the small-font lines as a row. 

<br />

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_aug2025_maxgap.png)

<br />

## Improvement: Multipage Deskew preprocessor

The Deskew preprocessor corrects the alignment of text in documents that are skewed, for example, ID cards or receipts  photographed at an angle instead of straight on. With the new Match All parameter, you can now deskew multiple pages in a document based on matching text. For more information, see the [Deskew](doc:deskew#parameters) preprocessor.
