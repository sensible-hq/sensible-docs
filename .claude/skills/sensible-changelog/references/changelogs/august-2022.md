---
title: August 2022
slug: august-2022
date: 2022-08-03
---

In the last month, we released  powerful new web app UX improvements, as well as improved checkbox and date recognition and other improvements.

## Improvement: Web app UX

The web app is now more powerful than ever, with new features coming on the heels of [automatically detecting uploaded documents' types](https://docs.sensible.so/changelog/july-2022) and [deskewed views of documents](https://docs.sensible.so/changelog/june-2022). 

Improvements include:

* Zoom and pan on documents to view small text more easily: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_aug2022_zoom.png)

* Click the dot in the gutter next to extracted field IDs to jump to the source SenseML field and highlight the source lines in the PDF:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_aug2022_jump_extract_id.png)

* Add comments to your SenseML to help with configuration maintenance:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_aug2022_comments.png)

## Improvement: Checkbox recognition can bypass pixel rendering

To improve performance, Sensible now preferentially extracts checkbox selection status from PDF metadata, and falls back to pixel recognition of checkboxes only if the metadata is missing. 

## Improvement: Date types now support multiline recognition

Sensible can now recognize dates that span multiple lines. 

## Improvement: Indexed tiebreakers

For [tiebreakers](https://docs.sensible.so/docs/method), you can now use indices in addition to ordinal values to select an extraction target.

## Improvement: PDF metadata in extraction

You can now view metadata about the PDF in the extraction response's `file_metadata` parameter, for example creation date, author, and modified date. Sensible returns both raw metadata and normalized metadata.
