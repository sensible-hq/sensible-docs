---
title: April 2024
slug: april-2024
date: 2024-03-11
---

In the last month we released support for GPT-4 Vision, so you can extract information from non-text images in documents. We also released a new **recommend query groups** feature, so you can upload and extract data from a document with a few button clicks instead of having to author your own LLM prompts. We added a new filterable extraction status, deprecated several methods, and made several improvements to advanced configurability. 

## New feature: GPT-4 Vision support for extracting data from non-text images

With the [Query Group](doc:query-group#parameters) method's new Multimodal Engine parameter, you can ask questions about non-text images embedded in documents. For example, for a real estate offering memorandum document containing a photo of a property, you can ask questions like `does the house pictured have trees on the property?`.  You can also use the Multimodal Engine to extract from complex text layouts, for example, handwriting. For examples, see the [Query Group](doc:query-group#examples) method.

## New feature: Automatic extraction with recommended query groups

You can now automatically extract data from a document without configuring queries manually. Sensible generates LLM-based queries based on the current page you're viewing. For example, if you're looking at a lease page summarizing the rents, clicking **auto-generate** can automatically target relevant data, create prompts, and extract structured data like `monthly_rent` or `late_fee`. Reuse your automatically generated prompts to extract from similar documents.

For more information, see the release announcement [post](https://www.sensible.so/blog/recommended-query-groups) and see the following walkthrough:

<Embed url="https://www.youtube.com/watch?v=TNdYnH4QQiw" title="Introducing Sensible's recommended query groups" favicon="https://www.google.com/favicon.ico" image="https://i.ytimg.com/vi/TNdYnH4QQiw/hqdefault.jpg" provider="youtube.com" href="https://www.youtube.com/watch?v=TNdYnH4QQiw" typeOfEmbed="youtube" html="%3Ciframe%20class%3D%22embedly-embed%22%20src%3D%22%2F%2Fcdn.embedly.com%2Fwidgets%2Fmedia.html%3Fsrc%3Dhttps%253A%252F%252Fwww.youtube.com%252Fembed%252FTNdYnH4QQiw%253Ffeature%253Doembed%26display_name%3DYouTube%26url%3Dhttps%253A%252F%252Fwww.youtube.com%252Fwatch%253Fv%253DTNdYnH4QQiw%26image%3Dhttps%253A%252F%252Fi.ytimg.com%252Fvi%252FTNdYnH4QQiw%252Fhqdefault.jpg%26key%3D7788cb384c9f4d5dbbdbeffd9fe4b92f%26type%3Dtext%252Fhtml%26schema%3Dyoutube%22%20width%3D%22854%22%20height%3D%22480%22%20scrolling%3D%22no%22%20title%3D%22YouTube%20embed%22%20frameborder%3D%220%22%20allow%3D%22autoplay%3B%20fullscreen%3B%20encrypted-media%3B%20picture-in-picture%3B%22%20allowfullscreen%3D%22true%22%3E%3C%2Fiframe%3E" />

<br />

## Deprecation: LLM-based methods replace Invoice, Key-Value, and TFIDF methods

The [Invoice](doc:deprecated-invoice), [Key-Value](doc:deprecated-key-value), and [TFIDF](doc:deprecated-tfidf)   methods are now deprecated. To duplicate these methods' functions, use [LLM-based methods](doc:llm-based-methods).

## Improvement: Keyset pagination for List Extractions API endpoint

You can now navigate paginated results from the [List Extractions](ref:list-extractions) endpoint using keyset navigation instead of date navigation.  Get the next page of results using the `continuation_token` query parameter, and configure page size with the new `limit` parameter.  The date range parameters are now optional. The `cutoff_date` parameter is now deprecated.

## Improvement: New PROCESSING status for extractions

In addition to filtering extractions by the WAITING, FAILED, and COMPLETED statuses,  you can filter by the new PROCESSING status in the Sensible app or with the List Extractions endpoint. The status indicates that Sensible received the document and is working on the extraction.

## Improvement: Round Currency and Number types

You can round extracted [Currency](doc:types#currency)- and [Number](doc:types#number)-typed values to a specified decimal point using these types' new Round To parameter. For example, configuring `"roundTo":2` rounds the number  `5.919` to `5.92`.

## Improvement: Advanced Document Range configuration

The new Stop Offset Y parameter adds advanced configurability to the [Document Range](doc:document-range) method. Use the parameter to offset the end of the range up or down the page from the range's Stop line. 

## UX improvement: Advanced config-level options in Sensible Instruct

The LLM Engine parameter we [released](https://docs.sensible.so/changelog/dec-2023#improvement-choose-your-llm-model-for-the-list-method)  for the [List](doc:list)  method is now available in the Sensible Instruct editor in addition to the SenseML editor. 

The Page Span Threshold parameter we [released](https://docs.sensible.so/changelog/dec-2023#improvement-advanced-configuration-for-multi-page-llm-based-tables)  for the [NLP Table](doc:nlp-table)  method is now available in the Sensible Instruct editor in addition to the SenseML editor.
