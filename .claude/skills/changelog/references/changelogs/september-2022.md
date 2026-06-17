---
title: September 2022
slug: september-2022
date: 2022-08-10
---

In the last month, we launched several exciting new features, including the ability to convert document extractions to Excel spreadsheets and a beta Zapier integration.

## New feature: Extract document data to spreadsheets

You can now download any document extraction as an Excel spreadsheet.  This feature lets you easily convert tables, rows, labels, checkboxes, and other document primitives into well structured spreadsheets, unlike many tools that map PDF formatting onto a spreadsheet with no meaningful relationship to the underlying cells.

For example, the [document](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/auto_insurance_anyco.pdf) in the [Getting started guide](doc:getting-started) converts to the following spreadsheet:

<HTMLBlock>{`
<div><iframe class="spreadsheet" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vRJO_nwPRVe84ZdAi-gc6mny0zhRO9iz4nclfEKSBFQWHotARcgUkwfcinpGJTzPM4GIoIvf6PcN7zv/pubhtml?widget=true&amp;headers=false"></iframe></div>

<style>.spreadsheet{width:100%;}</style>
`}</HTMLBlock>

You can download spreadsheets either through the [Sensible app](https://app.sensible.so/extractions/) or the [Sensible API](https://docs.sensible.so/reference/get-excel-extraction).

For more information, see [Quickstart PDF to Excel](doc:excel-quickstart) and [SenseML to spreadsheet reference](doc:excel-reference).

## Beta feature: Zapier integration

Connect Sensible with your favorite tools -- Google Drive, Dropbox, and more -- through our new [Zapier integration](doc:zapier).

## UX improvement: Autocomplete SenseML in Sensible app

You can now author SenseML faster in the Sensible app by using autocomplete suggestions.

For example, if you type `field`:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_Sept2022_autocomplete.png" />

Sensible autocompletes `field` as:

```json
{
      "id": "",
      "anchor":,
      "type":,
      "match":,
      "method": {
        "id":
      }
    }
```

## Improvement: Faster checkbox recognition

Sensible can now use embedded PDF metadata to extract a checkbox's selection status. If the PDF lacks metadata, Sensible falls back to the slower, existing method of pixel recognition. For more information, see [Checkbox](doc:checkbox).

## Improvement: Address type in paragraphs

Sensible now recognizes addresses in paragraphs in addition to addresses in block format. Use `"block_format":"false"` to recognize addresses such as the following example:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/type_address_paragraph.png" />

For more information, see the [Address type](doc:types#address).

## Improvement: Accounting Currency type recognizes trailing negative signs

Sensible now recognizes [accounting currencies](doc:types#accounting-currency) when formatted with a trailing negative sign, for example,  `$527.01-`.

## Improvement: Zip sections

You can now combine all the fields in multiple section groups into a new section group using the [Zip](doc:zip) computed field method. For an example, see [Advanced: Zip sections](doc:sections-example-zip).

## Improvement: Configure SenseML execution order

For advanced use cases, for example to suppress source section groups so you can have clean output for a zipped section group, you can now configure the order in which Sensible executes fields, computed fields, and sections.

For more information, see [Field extraction order](doc:field-order).

## Improvement: Configure the Remove Header and Remove Footer preprocessors with text matches

To recognize footer or header text that varies slightly or isn't present on all pages, you can now bypass automatic header or footer recognition by configuring a text match. Sensible removes all text below the bottom or top boundary of the matched text. For more information, see the [Remove header](doc:remove-header) and [Remove footer](doc:remove-footer) preprocessors.

## Improvement: Sections verbosity

When you configure a higher [verbosity](doc:verbosity), Sensible now returns metadata for sections.
