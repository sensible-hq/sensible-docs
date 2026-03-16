---
title: December 2022
slug: december-2022
date: 2022-12-12
---

In the last month, we released several feature improvements, including the ability to add instructions to the Summarizer method and the ability to extract from TIFF documents. We also added guided onboarding experiences to the Sensible app.

## New feature: Extract from TIFF documents

You can now use the Sensible API to OCR and extract data from TIFF images of documents. For TIFF documents, Sensible doesn't support:

* pixel-based methods, such as Box, Checkbox, Signature, and image coordinates found with the Document Range method
* Key/Value method
* OCR preprocessor
* Fixed Table and Table methods with the Stop parameter specified. Use the Text Table method as an alternative.

## Improvement: Simplified Summarizer method

You can now ask a free-text question using the Summarizer method's new Instructions parameter. This parameter makes it easier to configure this GPT3-powered method and improves the accuracy of results in combination with the Samples parameter. For example, for the following document, you can ask, 

`"list the rents, how often the rent must be paid, and when the rent is due"`: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/summarizer.png)

The Summarizer method returns the answer:

```
"rent_computed": [
    {
      "rent_in_dollars": "$895.00",
      "payment_time_period": "month",
      "payment_due": "on or before the 1st day of each month"
    }
  ]
```

The Summarizer method can also now return arrays if it finds multiple answers in the document. For example, if a lease listed several properties, it can return:

```
"rent_computed": [
    {
      "rent_in_dollars": "$895.00",
      "payment_time_period": "month",
      "payment_due": "on or before the 1st day of each month",
      "street_address": "1234 S Main street"
    },
    {
      "rent_in_dollars": "$1050.00",
      "payment_time_period": "month",
      "payment_due": "on or before the 1st day of each month",
      "street_address": "5432 N Central Ave"
    }
  ]
```

For examples, see [Summarizer](doc:summarizer#examples).

## UX improvement: Guided onboarding in the Sensible app

If you're a new user, you now get a guided experience when you first use the Sensible app. To revisit the tour, see our [walkthrough in the docs](doc:ui).

## Improvement: Custom type matches multiline regular expressions

With the Custom type's new MatchMultipleLines parameter, you can match regular expressions that span multiple lines. For more information, see the [Custom type](doc:types#custom).

## Improvement:  More accurate multi-line cell recognition for Text Table method

The Text Table now takes a line's membership in a column into account in order to more accurately recognize multi-line cells in tables.
