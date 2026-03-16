---
title: March 2023
slug: march-2023
date: 2023-03-02
---

In the last month, Sensible released GPT-3-powered natural-language methods to capture tables and get answers from documents. We also completely overhauled our web app's design for better navigation, improved several existing features, and added advanced configurability for text tables and types.

## New feature: NLP Table method

With the [NLP Table](doc:nlp-table) method, you can use low-code, natural-language descriptions to extract table data from a document. This new table method is powered by GPT-3 and OpenAPI's Embeddings API and is a powerful alternative to Sensible's layout-based table methods.  There's no need to anchor on text nearby the table; just provide an overall description of the table, such as `"covered vehicle information"`. Then provide descriptions about the columns you want to extract, as well as instructions about filtering or formatting the data, for example `"vehicle make, not model"` or `"transaction amount, as an absolute value"`.  For more information, see [NLP Table method](doc:nlp-table).

## Improvement: Question method

Our Question method now uses GPT-3 and OpenAPI's Embeddings API for improved accuracy and improved ability to phrase complex questions.  You can now ask a question like `"when is the rent due? don't include details about grace periods"` and get back an answer. This method lets you quickly get started with less structured or unstructured documents, for example legal or research documents, since you don't need to know about the document's layout. Or use it as a low-code alternative to layout-based SenseML methods in semi-structured documents, such as business forms. For more information, see [Query method](doc:query).

## UX improvement: Improved app navigation

We've reorganized and polished the global navigation for the Sensible app. See the following walkthrough for an overview of the redesign:

<HTMLBlock>{`
<div style="position: relative; padding-bottom: calc(87.19723183391004% + 41px); height: 0;"><iframe src="https://demo.arcade.software/676OJnQQRimXqJSncpnU?embed" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>
`}</HTMLBlock>

## Improvement: Faster performance for Nearest Checkbox method

The Nearest Checkbox method can now use embedded PDF metadata to extract a checkbox's selection status. If the PDF lacks metadata, Sensible falls back to the slower, existing method of pixel recognition. For more information, see [Nearest Checkbox](doc:nearest-checkbox).

## Improvement: Advanced configuration for Text Table method

In advanced use cases, you can use the syntax `"stop": {"type": "last"}` to recognize [text tables](doc:text-table) that span pages, but that lack text you can use match on with the Stop parameter. This type of stop specifies to end the table at the end of the document or section. For example, use this type of stop to recognize tables in sections, where each table extends to the end of each section.

## New feature: Advanced configuration for type transformation

For advanced use cases, you can now transform types into custom types with the new [Compose](doc:types#compose) type.\
For example, in the following table, if you wanted to transform the dates in the first column into a custom YYYY-MM format, you can define a Compose type that transforms the date type's standard output into a custom type.\
![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/compose_type.png)
