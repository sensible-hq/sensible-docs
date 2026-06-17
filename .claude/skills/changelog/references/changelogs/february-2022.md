---
title: February 2022
slug: february-2022
date: 2022-02-08
---

In the last month, Sensible launched a self-serve sign-up that includes a free-forever tier, no credit card required. We also introduced a new feature that lets you extract choices from a radio button group or other field group. We made several feature improvements, including a richer API response, and a customizable date type.

## Self-serve launch

Last month we launched a [self-serve sign-up](https://app.sensible.so/register/). With self-serve you can sign up, onboard a document, and publish an enterprise-grade API endpoint, all in an afternoon. Self-serve accounts start at a forever-free tier and don't require a credit card to create. 

To make onboarding for self-serve customers as easy (and even fun) as possible, we now preload all our accounts with in-app walkthroughs to teach SenseML:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_Feb2022_walkthroughs.png) 

## New feature:  Extract choices from radio buttons or other groups

With the [Pick values computed field](doc:pick-values) you can extract specified values from a group of fields. For example, extract the selected boxes from a checkbox group, or extract all "yes" answers from a group of fields with yes/no/maybe dropdowns:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_Feb2022_pick_values.png)  

## Improvement: API returns metadata about extraction selection

The extraction API now returns metadata about how Sensible automatically chooses the best-scoring configuration in a document type.\
It shows how Sensible scored the extraction for each configuration, for example:

```json
"classification_summary": [
    {
      "configuration": "anyco_rate_confirmation",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 3.5,
        "fields_present": 4,
        "penalities": 0.5
      }
    },
    {
      "configuration": "acme_co",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 0.5,
        "fields_present": 2,
        "penalities": 1.5
      }
    }
  ]
```

## Improvement: Text Table method can span pages

The [Text Table](doc:text-table) method can now recognize tables that span page breaks. Other table methods already include this feature. To enable this feature, be sure to specify a Stop parameter for the table.

## Improvement:  Configurable Date type

You can now configure your own date formats (for example, MM-YY) for Sensible to recognize as a [Date type](doc:types#date), in addition to or instead of the default date formats.

## Improvement: OCR preprocessor can match multiple pages

You can now specify to OCR all pages that match a line of text, rather than just the first-found page.

## Improvements: Web app UX

You can now view portfolios by clicking on them in the extractions section of the web app.

## Improvement: Consistent output for Address type

If an address in a source document is on one line, Sensible now formats the output by adding a newline between the street address and the city.
