---
title: November 2022
slug: november-2022
date: 2022-10-10
---

In the last month, we released several feature improvements, including the ability to visualize section boundaries in the app, a more powerful Currency type, and better handling of zipped arrays. 

## UX improvement: Visualize sections in app

You can now easily view the range for each [section](doc:sections) in a section group in the Sensible app. The app displays the start and end of each section's range using brackets: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/vertical_sections_col_sect_1.png)

You can turn the display on or off using the new `display` Boolean parameter in sections. Currently, sections specified in the Suppress Output  method never display their boundaries.

## Improvement: Match all with null

When zipping parallel arrays, you can encounter shortened zipped arrays if any of the source arrays omitted null values from the output.  With the new [`"match": "allWithNull"`](doc:field-query-object#parameters) option, you can preserve the maximum length of arrays. For an example, see [Zip](doc:zip#all-with-null-zip).  This option matches all anchors and returns extracted output, including null output, under a single key.

## Improvement: more flexible Currency type

For greater flexibility, we've deprecated the Accounting Currency type. You can now mimic the deprecated behavior by setting `"accountingNegative"`:`"default"` on the [Accounting type](doc:types#accounting). You also now have options to specify which accounting symbols to use for negative values.

You can also now configure the Accounting type to handle OCR errors with the new Remove Spaces parameter, which allows for better currency recognition by ignoring whitespaces between currency symbols and numbers.

You can now handle numbers that lack negative symbols, such as those in a debit accounting column, with the new Always Negative parameter.

## Improvement: Turn off default line merging

For advanced use cases, you can turn off the built-in line merging that occurs prior to the [Merge Lines preprocessor](doc:merge-lines) using the `prevent_default_merge_lines` parameter in the [Update Document Type](https://docs.sensible.so/reference/update-document-type) API endpoint.

## Improvement: Include anchor in Box output

The [Box](doc:box) method by default outputs all lines in a box, excluding the anchor line. You can now configure it to include the anchor line using the new Include Anchor parameter.
