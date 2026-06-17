---
title: August 2024
slug: august-2024
date: 2024-08-02
---

In the last month, we released a new feature for visualizing extracted data in the JSON editor and advanced configuration for several layout-based methods.

## UX improvement: Visualize extracted data in JSON editor

For easier config editing, you can now click the **UI Output** icon in the JSON editor's right pane to view a compact visual representation of the extracted JSON:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_aug2024_ui_output.png)

## Update: Filter extraction history by environment in the dashboard

With the new Environment drop-down, you can filter extraction metrics in the [dashboard](doc:metrics) by environment. If you don't specify an environment, Sensible displays extractions for both development and production. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_august2024_metrics_environment.png)

You can also filter metrics returned by the [/statistics](https://docs.sensible.so/reference/statistics)  API endpoint using the new `environment` query parameter.

## New feature: Replace type

Use the new [Replace](doc:types#replace)  type to replace all instances of a regular-expression pattern match in source lines and return the transformed source lines. For example, strip out whitespaces from the source text `$ 5 00 0` and return the string `$5000` with this type.

## Update: Validate fields in sections

With the new Scope parameter, you can validate each instance of a field that occurs in sections. Specify the parent sections' IDs as the scope for the validation when you create it. For an example, see [Validating extractions](doc:validate-extractions#validation-6). 

## Update: Match columns above an anchor

In addition to the default behavior of capturing a column below an anchor, you can now extract a column above an anchor using the new [Position](doc:column#position)  parameter.

## Update: API extraction responses include Charged parameter

API extraction responses now include a Charged parameter that indicates the number of documents charged to your account for this extraction ID. For example, if a portfolio extraction segments 3 documents from a file, this parameter returns 3.
