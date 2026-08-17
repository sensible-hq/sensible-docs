# MCP Search Eval — Questions

Testing the `mcp__sensible-docs` search tool's ability to find and surface relevant docs.

## Beginner questions

1. What file types can I upload?
2. Do I need to write code to use this?
3. How do I pull out a specific field from a PDF?
4. What's the difference between the LLM and layout-based approaches, and when should I use each?
5. Can Sensible handle scanned documents or photos of documents?
6. What does the output actually look like?
7. How do I handle documents from the same category that look slightly different from each other?
8. Can it extract tables?
9. Can it detect whether a checkbox is checked?
10. What happens if a field isn't present in a document?
11. How do I get extracted data into Excel or a database?
12. Is there a way to try it without setting up API calls?
13. Are there prebuilt extractors I can use off the shelf?
14. How do I handle a single PDF that contains multiple different documents?
15. How do I know if my extraction is accurate?

## Expert / niche / corner case questions

### To score (ground truth set)

1. How does Sensible OCR behave on a mixed PDF where some pages are digitally generated and others are scanned — do preprocessors apply uniformly?
2. What happens when a section's anchor match text appears multiple times *within* a single section — does `requireStop` fully resolve this, or are there edge cases?
6. Can computed fields reference other computed fields, and if so, is there a declared evaluation order or does it depend on array position?

### To score later

3. Can you mix fingerprint-based and LLM-based segmentation within a single portfolio extraction, or is it one mode for the whole request?
4. How does the `tiebreaker` comparison operator (`>`, `<`) interact with a `currency` type field — does it compare numeric values or raw source strings?
5. When a JsonLogic postprocessor transforms the output schema, do validations run on the pre- or post-transform `parsed_document`?
7. How does `xRangeFilter` interact with multi-column layouts processed by the `multicolumn` preprocessor — do the x-coordinates refer to pre- or post-reflow positions?
8. What's the behavioral difference between `lineFilters` on a vertical section range vs `wordFilters` on the method object — is there a case where one works and the other fails?
9. How does `angleFilter` in `removeLines` interact with different OCR engines (e.g., Google vs default) — is angle metadata available for all engines?
10. When two configs in the same document type have overlapping fingerprints and produce the same score, what's the tiebreaker?
11. Can dynamic external ranges in sections search *backwards* (preceding each section start) and if so, how does `reverse: true` on the anchor interact with `anchorIsAbsolute`?
12. Does `requiredFields` on sections interact with extraction coverage scoring — i.e., do omitted sections count as missing fields?
13. Can preprocessors be conditionally applied based on document content, or do they always run unconditionally?
14. What are the performance/cost tradeoffs between `searchBySummarization: "page"` vs other summarization strategies in `queryGroup`?
15. When a portfolio uses LLM segmentation and a document spans pages that start mid-page, how does Sensible fail — silent drop, error, or partial extraction?
