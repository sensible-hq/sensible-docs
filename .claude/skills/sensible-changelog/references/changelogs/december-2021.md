---
title: December 2021
slug: december-2021
date: 2021-12-02
---

In the last month we’ve made several minor feature and web app UX improvements while focusing on our upcoming launch of a self-serve signup flow (stay tuned). 

## Improvements: existing feature updates

* For the [Intersection](doc:intersection) method, you can now define a vertical anchor on any page, not just the same page as the main anchor.
* The [Portfolio](doc:portfolio) endpoints now have improved page range detection, including support for defining first and last page fingerprints on the same page. 
* API endpoints now support client-side validation of document type names, so if you enter a document type name incorrectly, you get an error message.

## Improvements: web app UX

* For better visual clarity, Sensible now represents filtered-out data with dotted lines:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_filtered_method.png)

```
{
  "fields": [
    {
      "id": "filtered_by_tiebreaker",
      "anchor": "Javascript",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "second"
      }
    }
  ]
}
```

You can now measure inch coordinates in the Sensible app, so you can more easily configure configure coordinate-based methods such as Region and Text Table.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/screenshots/changelog_dec2021_measure.gif)

## Improvements: documentation

We've added documentation for a couple of advanced free-text extraction methods:

* [TFIDF](doc:tfidf)
* [Summarizer](doc:summarizer)
