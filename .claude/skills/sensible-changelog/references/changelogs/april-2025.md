---
title: April 2025
slug: april-2025
date: 2025-04-02
---

In the last month, we released UX improvements for the Sensible app and advanced output schema manipulation features.

## UX improvements: Download JSON and batch extraction history

In the **Extraction history** tab, you can now download an extraction as a JSON file in addition to downloading it as an Excel file:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_april2025_json.png)

In the **Extraction history** tab on the **Batch extractions** tab, you can now view the description and ID for each batch and copy the ID:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_april2025_batch.png)

## New feature: Advanced JsonLogic operations

In addition to the existing [JsonLogic](doc:jsonlogic)  operators, Sensible released new extended JsonLogic operations for transforming the output schema:

* The Merge Objects operator takes an array of objects and returns a single object containing all the fields from each object. 
* Use the Stateful Map operation to perform a mapping operation on an array while keeping track of a state variable from previous iterations in the loop.

For more information, see [Merge Objects](doc:jsonlogic#merge-objects) and [Stateful Map](doc:jsonlogic#stateful-map).
