---
title: November 2021
slug: november-2021
date: 2021-11-08
---

In the last month we’ve introduced the ability to associate reference documents to configurations, a new Nearest Checkbox method, and several improvements to existing features.

## Improvement: Associate a reference PDF with a config in the web app

You can now associate reference PDFs to a particular config, so that you don't have to pick the relevant PDF every time you open a config or vice versa. Associate the PDF and config by dragging and dropping, clicking the link icon on the reference doc, or by making a selection when you upload the PDF: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_Nov2021_ui.png)

Now, opening a PDF opens its config as well, and opening a config gives you the first associated PDF, as well as a group of other associated PDFs you can choose from the dropdown.

## New feature: Nearest Checkbox method

The new Nearest Checkbox method is an alternative to the Checkbox method.  Use the Nearest Checkbox method when the Checkbox method can't recognize an unusual checkbox format, or if the checkbox position varies on the page. The Nearest Checkbox method recognizes a wider range of checkbox formats and requires less configuration than the Checkbox method, but is slower. For more information, see [Nearest Checkbox](doc:nearest-checkbox).

## New feature: Search preceding lines for a match

When a difficult-to-match target line precedes an easy-to-match line, you can now use the Reverse parameter on a match in an array to search preceding lines.  For more information, see [Reverse match arrays](doc:match-arrays#reverse-match-arrays).

## Improvement: Correct for vertically misaligned text

Use the newly released Sort Lines parameter for misaligned text, for example handwritten text. This parameter corrects situations where slight jitter in the vertical positions of lines can otherwise cause Sensible to incorrectly sort lines that a human reader interprets as following left to right.  This new parameter **deprecates** the X Major Sort parameter because it handles a bigger range of misalignment cases, including misalignment in paragraphs.  For more information, see the `sortLines` example in [Method](doc:method#sort-lines-example).

## Improvement: Start table recognition on a row

The Starts On Row parameter is a new alternative method for excluding headings or rows. It allows you to start table recognition on the nth row of a table so you can filter out extraneous information. This option allows you to exclude headings in situations where there is no differentiating type that you can use to exclude headings (for example, all cells contain numbers, so you can't use the number type to exclude string-type column headings). For more information, see `startOnRow` in the docs for any of the table methods, for example [Table](doc:table).

## Improvement: Suppress extra output in computed fields

You can now specify fields to exclude from the extraction output using the Suppress Output computed field. For example, if you use the field ID  `_raw_data` as a source for a `nicely_formatted`  computed field, then specify the raw field's ID to show only the computed field in the output. For more information, see [Suppress output](doc:suppress-output).

## Improvements: Web app UX

We've improved error messages for extraction failures in both the SenseML editor and extraction history. We've also expanded our app's visual representation of the SenseML language: you can now view text that matches fingerprints as pink highlights.

## Improvement: Force ligature replacement

You can now specify to override Sensible's conservative approach to ligature replacement and use the Force Replace All parameter to replace all ligatures. For example, use this to replace ligatures in words not in an EN-US dictionary. For more information, see `forceReplaceAll` in [Ligature](doc:ligature).
