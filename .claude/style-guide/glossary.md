# Sensible Docs Terminology Glossary

Canonical term reference for all Sensible documentation. When writing or reviewing any doc — reference pages, changelogs, integration guides, concept topics — use these terms consistently.

Organized in two sections:
- **Universal terms** — apply to all Sensible content
- **SenseML-specific terms** — apply when writing or updating SenseML reference pages

---

## Universal terms

| Concept | Use | Avoid | Notes |
| ------- | --- | ----- | ----- |
| The JSON extraction configuration | "config" or "configuration" | "template", "schema" | "schema" has a specific meaning in the product |
| The Sensible web interface | "the Sensible app" | "the UI", "the editor", "the dashboard" | |
| The Sensible product | "Sensible" (always capitalized) | "sensible", "the tool", "the engine" | |
| The result Sensible returns | "output", "extracted field", "field" | "result object", "response" | "response" refers to the API response envelope |
| Repeated document structures | "sections" | "repeating groups", "loops" | |
| An extraction that returned nothing | "null" | "empty", "undefined", "no value" | |

---

## SenseML-specific terms

These apply when writing SenseML reference pages (methods, preprocessors, computed field methods, the anchor and match objects).

| Concept | Use | Avoid | Notes |
| ------- | --- | ----- | ----- |
| The text Sensible matches to find a location | "anchor", "anchor line", "anchor point" | "reference text", "marker" | |
| The document text sent to an LLM | "context" | "prompt context", "input" | |
| A scored portion of the document for LLM use | "chunk" | "segment", "section" | "section" has a specific SenseML meaning |
| The SenseML data output type | "type" (e.g., "currency type", "date type") | "data type", "field type" | |
| A defined extraction unit | "field" | "extraction", "key" | |
| JSON path into extracted output | "dot notation" (e.g., `claims.columns.3.values`) | "object path", "key path" | |
| Unstructured/variable documents — adjective before noun | "free-form documents", "a free-form contract" | "free form documents" | hyphenate when preceding a noun |
| Unstructured/variable documents — predicate adjective | "the document is free form", "entirely free form" | "entirely free-form" | no hyphen in predicate position |
