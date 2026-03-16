---
title: April 2022
slug: april-2022
date: 2022-04-06
---

In the last month, we released several new features, including the ability to correct scanned documents' scale, fuzzy matching, and programmatic control over your extraction configuration.  We also made improvements to box recognition and added support for viewing the web app on mobile devices.

## Documentation: Extraction configuration API reference

Now you don't need to go to the Sensible app to configure your extractions. You can programmatically control document types, configurations, and reference documents with our newly published [Configuration API documentation](https://docs.sensible.so/reference/list-document-types).

## New feature: Scale preprocess for correcting unpredictably sized text

The new [Scale preprocessor](doc:scale) corrects the size of text in PDF documents whose size varies, for example as a result of being scanned or photographed at different scales. This preprocessor enables coordinates-based methods, such as the Region or Text Table methods, to work with such unpredictably scaled documents.

Note that the existing [Deskew](doc:deskew) method fixes scaling problems in skewed documents, while the Scale preprocessor is an easier-to-configure and more robust choice for unskewed or only slightly skewed documents. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_april2022_scale.png) 

## New feature: Filter out types

You can use the [Types Filter](https://docs.sensible.so/docs/method#type-filters-example) parameter on the Method object to extract anything that *isn't* one of the listed types. For example, for a target box containing a delivery date, a street address, and delivery notes, you can filter out the lines containing Date and Address types in order to extract the delivery notes.

## New feature: Fuzzy matching

Blurry, poorly scanned documents often result in "typos" in the OCR output, for example, `chi` instead of `city`. You can fuzzy match to such "typos" using the new [Edit Distance](https://docs.sensible.so/docs/match#:~:text=EDIT%20DISTANCE%20EXAMPLE) parameter.

## Improvement: Box recognition

We greatly improved the [Box method's](doc:box) ability to recognize:

* box backgrounds that aren't pure white and box borders that aren't pure black, a common situation for scanned or photographed documents. 
* box borders that are discontinuous, or in other words, have small gaps in their outlines. 

## Improvement: Configurable OCR for pages with low line counts

Pages with a low line count (i.e., not much embedded text) are more likely to contain text images that require OCR. You can now run the OCR preprocessor on all pages with a configurable low line count using the new [Page Lines Limit parameter](doc:ocr).

## Improvement: Web app UX

You can now view and interact with most features in the Sensible web app on mobile devices' web browsers, excluding editing SenseML.

You can also now view your API usage on your account page, including the number of calls you've made compared to your plan's monthly API call limit.
