---
title: September 2021
slug: september-2021
date: 2021-09-15
---

This month we're introducing custom extraction validations and a new look for the Sensible app, along with several other enhancements.

## New feature: Custom validations

You can now quality control data extractions using custom JsonLogic validations in your extraction flows. Configure validations in a document type to test extracted fields using a wide range of logical statements, including numeric and string comparisons, existence checks, and regex patterns. The Sensible app then displays validation errors and warnings in the extractions tab, and you'll also receive a validations array in your API responses with any errors, warnings, or skipped validations.

For more information about validations, see the [docs](doc:validate-extractions).

![click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_Sept2021_validations.png)

## Improvement: Web app UX

We've completely overhauled the Sensible app to show key information about your configurations, reference documents, and extractions at a glance. On one page, you can see:

* whether configurations are deployed to your dev or prod environments
* first-page previews of reference documents
* information about recent extractions (how many fields are present in each extraction, validation errors and warnings, and extraction status).

![click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2021_dashboard.png)

## New feature: Intersection method

This method lets you easily pull data from loosely tabular layouts without pulling the whole table. You specify a horizontal and vertical anchor and Sensible returns the line at their intersection. For more information, see the [docs](doc:intersection).

## New feature: Topic method

This experimental method supports a broader range of free text extractions. It  finds the section of a document that overlaps the most with a bag of words. This is useful for extracting a section from a doc, for example, payment terms from a long contract document. For more information, see the [docs](doc:topic).

## Improvement: Better handling for rotated pages

We've made several changes to better handle rotated pages both in the core engine as well as in the Sensible app. If you're seeing an extraction issue that may be a result of document rotation, please let us know at [support@sensible.so](mailto:support@sensible.so)!
