---
page: jsonlogic
doc-path: docs/Senseml reference/concepts/jsonlogic.md
page-type: reference
last-updated: 2026-09-09
---

# User brief: JsonLogic extensions

## Who is reading this page

- **Role:** A developer or technical config author building a Sensible extraction config
- **How they arrive:** From the Custom Computation method page, the Postprocessor page, or via search for "JsonLogic" when they need to transform extracted values
- **Subscription / setup context:** Has an active Sensible account; is writing or debugging a config; already extracts fields and wants to transform or validate them
- **Vocabulary they use:** "JsonLogic", "rule", "operator", "transform", "computed field", "postprocessor", "var", "validation"
- **What they already know:** Basic JsonLogic syntax (the `{ "operator": [args] }` form); has already read the JsonLogic.com docs; knows what `var`, `if`, `==`, `cat` do
- **What they don't know yet:** Which operators Sensible adds beyond the base JsonLogic spec; null-handling behavior of Sensible's custom operators; edge cases like non-string inputs

## What they're trying to do

Accomplish a specific data transformation inside a JsonLogic rule — normalizing string case, rounding a number, shifting a date, filtering an array — without leaving the config. They arrive knowing what they want to do and need to find the right operator and understand its behavior.

## Questions they expect this page to answer

- What extra operators does Sensible support beyond the base JsonLogic spec?
- How do I do case-insensitive string comparisons?
- What does this operator return if the field is null?
- What happens if I pass the wrong type?
- Where can I use this operator — validations, custom computation, postprocessor?

## What belongs on this page

- A quick-reference table of all Sensible-specific operators with compatibility indicators (validations / custom computation / postprocessor)
- Per-operator sections with: what it does, null/error behavior, syntax, one realistic example
- Syntax tips that aren't obvious from the JsonLogic docs (dot notation, escape behavior, traversal notation)
- Links to the base JsonLogic docs and the Sensible-specific tutorial blog post

## What does NOT belong here

- Full tutorials for custom computation or postprocessor — those live on their own pages and are linked from here
- Explanation of how fields, anchors, or methods work — that's the SenseML reference, not this page
- Operator behavior that is identical to the base JsonLogic Engine spec — just link to it

## Sources

- PR context: sensible-hq/sensible#3457 (toLower, toUpper operators)
- PR body: "Config authors had no way to normalize string case inside JsonLogic, so case-insensitive comparisons and lookups had to be worked around with regex replaces or pushed out of the config entirely."
- Existing page content and adjacent pages (custom-computation.md, postprocessor.md, validate-extractions.md)
