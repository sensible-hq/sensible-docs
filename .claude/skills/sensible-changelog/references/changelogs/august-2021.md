---
title: August 2021
slug: august-2021
date: 2021-08-09
---

This month we're introducing a development environment for Sensible, along with several other enhancements.

## New feature: Development environment

You can now publish your configs to a development environment instead of straight to production. Configurations in the development environment have no impact on your production API calls. You can run a development query by adding ?environment=development to your queries. Development queries prefer the development version of configurations and fall back to the production version if no development version is present.

![click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_August2021_drafts_env.png)

## New feature: Drafts and versions

Previously, Sensible stored your draft configurations in your browser's local storage. We now store drafts server-side, and also retain a history of all your published versions. You can click the "Version history" dropdown to see all your past versions and copy and paste them to restore them to the editor. You can also see which versions are currently in the production and development environments from this dropdown.

![click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_August2021_version_history.png)

## Improvement: Visually debug SenseML queries

Depending on your query parameters, Sensible finds data in your document, and then filters out some of that data before it returns parsed document output. The Sensible app now represents this filtered-out data using pale colored boxes. This makes it easier to debug whether a query is returning null due to missing an anchor, missing target lines, or some other issue. For more information, see the [UI guide](doc:color).

## Improvement: Webhooks

Our webhook request bodies now exactly mimic the response you receive from the GET /documents/:id endpoint. The webhook now includes additional metadata such as the status of the extraction and its error state if relevant. The one distinction between the two bodies is that the webhook request body includes the webhook payload at the top level.

## Improvement: Download PDF button for extractions

You can now click on any extraction in the Sensible app and download the associated PDF. We also now capture PDF documents for future download even if an error occurs when Sensible processes the PDF.

## New feature: Engine support for custom validations

We’ve added a new validations array in your API responses so that you can write custom validations for your SenseML. Look for UI support for this feature soon!

## Improvement: Web app UX

The Sensible app’s new design uses a sidebar that contains document types, recent extractions, and the sign out link. Look for more changes to the app in the coming weeks.

## Improvement: Better OCR fallback

We now detect more cases where it's appropriate to fall back to OCR-based text extraction.
