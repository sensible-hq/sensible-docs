---
title: September 2025
slug: september-2025
date: 2025-09-02
---

In the last month, Sensible introduced a new visual editor that displays LLM-based extraction configurations as simple cards instead of as JSON code. A key usability feature is that new users can now modify the extraction configurations using plain English descriptions like `"update the field that extracts the customer's phone number to strip dashes and parentheses"` rather than writing JSON syntax.

## New feature: visual editor and quick edit for LLM-based document extraction

We're excited to announce a major step forward in making document extraction more accessible: visual cards for LLM-based methods. The Sensible app now displays your LLM prompts for document data extraction as cards in the left pane. Sensible supports visual cards for the Query Group and List methods. Click the **Visual editor** icon to view the cards.

<Image alt="click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2025_1.png" />

You can now quickly edit these cards by describing the changes you want to make, without any knowledge of SenseML or any need to write JSON. Click the **Quick Edit** button at the top of the left pane, and describe in natural language the data you want to extract, modify, or omit.

For example, you can write:

"Add a field to extract the customer's phone number"  
"Change the employee name field to also capture middle names"  
"Extract the due date from invoices"

The following screenshot shows what happens when you modify a payroll extraction with the following instructions: `extract net pay, and from the list of earnings, remove the rate property`.

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2025_2.png" />

Click the **Send** icon, and an LLM automatically updates your extraction configuration. You can then view a JSON diff and accept or reject the changes to the configuration:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2025_3.png" />

If you want to visually edit the cards without prompting an LLM for changes, click the **Edit** icon next to a field:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2025_4.png" />

You can remove or add fields and edit prompt text  in the visual cards:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2025_5.png" />

This visual interface bridges the gap between powerfully configurable document extraction and ease of use. As a new user, you can now:

* Upload a document and get auto-generated SenseML
* See visual cards representing their extraction logic
* Make changes in plain English without touching code
* Review and approve modifications to the extraction logic

At the same time, you still have access to the full power of Sensible's extraction capabilities simply by toggling to the JSON editor.

## Improvement: Auto-generate LLM-based document extraction available in-editor

The Sensible app has made [auto-generated](https://docs.sensible.so/changelog/july-2025) LLM-based extractions easier to access. You can now click the **Auto-generate fields** button in the SenseML editor for an existing document type to generate an extraction config and extract data:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2025_6.png" />

For example, the following configuration and extraction are auto-generated:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2025_7.png" />

Click the **Visual editor** icon at the top of the left pane to switch to a visual editor for this configuration.

## Regex for chaining LLM prompts and  fields

You can now select which prompts to chain using a regular expression.  For example, if you prompt an LLM to extract the fields `wages_tips` and `medicare_wages`  from a W-2 form, you can use the syntax `"source_ids": { "pattern": "._wage._" }` to run a subsequent LLM prompt on the output of all field IDs containing the string `"wages"`.

In addition to LLM methods, you can use a regular expression to specify source fields for Computed Field methods.  Sensible supports using a regular expression in the Source Ids parameter for the following methods:

* [List](doc:list)
* [Query Group](doc:query-group)
* [Concatenate](doc:concatenate)
* [Pick Values](doc:pick-values)
* [Suppress Output](doc:suppress-output)
* [Zip](doc:zip)

For an example, see [Chain prompts with regex](doc:query-group#example-chain-prompts-with-regex).
