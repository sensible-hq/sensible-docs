---
title: October 2022
slug: october-2022
date: 2022-09-08
---

In the last month, we launched several significant UX improvements, including importing our open-source configuration library into the Sensible app and using the Sensible app instead of the Sensible API to run extractions.\
We also introduced advanced methods to improve the consistency and simplicity of sections' output.

## UX improvement: Extract in app

In addition to using the extraction API, you can now quickly extract by uploading a document to the [Sensible app](https://app.sensible.so/quick-extraction/) and selecting a document type. Sensible auto selects the best-fitting configuration unless you manually choose a configuration. Unlike extractions from reference documents, quick extractions you make in the Sensible app count against your monthly document billing quota, are visible in the recent extractions tab in the Sensible app, can be downloaded as Excel, and can be used in Zapier integrations.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_Oct2022_quick_extract.png)

## UX improvement: Import configurations library into the Sensible app

You can now import common document types and configurations into the [Sensible app](https://app.sensible.so/library) from the open-source [Sensible configuration library](https://github.com/sensible-hq/sensible-configuration-library), so you can get started with extracting from tax forms, insurance forms, and other common business forms in minutes.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_Sept2022_library.png)

## New feature: Add global information to sections with Copy to Section method

You can now add information to a section by copying from a field outside that section using the new [Copy to section](doc:copy-to-section) computed method. This is useful if you want to add globally applicable information to the sections, for example, adding a policy number to every claim section.

## New feature: Simplify section output with Copy from Sections method

Use the [Copy from Sections](doc:copy-from-sections) method to copy a field from a section group into a new field's array. For an example, see [Zip and flatten nested sections](https://docs.sensible.so/docs/sections-example-copy-from-sections).

## Improvement: More flexible Intersection method

Use the new Width and Height parameters on the [Intersection method](doc:intersection) to extract lines that intersect with a rectangular region instead of with a point. This gives you more flexibility to capture lines whose coordinates vary.

## Improvement: Split Text Table columns using identical coordinates

In the Text Table method, you can now split columns by defining identical coordinates for the column and specifying types.

For example, in the following image, you can split the first column into a column for the issuing bank and a column for the account number.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/text_table_overlap.png)

For more information, see [Text table](doc:text-table#example-2).
