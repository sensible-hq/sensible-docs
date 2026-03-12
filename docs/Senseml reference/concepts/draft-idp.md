---
title: Intelligent document processing
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: 'Intelligent document processing with Sensible'
  robots: index
next:
  description: ''
---
Intelligent document processing (IDP) automates the extraction of structured data from documents — PDFs, emails, spreadsheets, images, and more — so that downstream systems can consume and act on it. The core challenge of IDP is document variability: real-world documents range from rigidly templated tax forms to free-form legal contracts, and no single extraction technique handles both ends of that spectrum well.

Sensible addresses this by combining two complementary extraction strategies in a single query language, [SenseML](doc:senseml-reference-introduction).

## The document landscape

Documents vary along two axes: **structure** (how consistently the layout is arranged) and **variability** (how many format revisions or issuer variations exist).

At one extreme, a standard W-2 form has a predictable, fixed layout — the same fields appear in the same positions across issuers and years. At the other extreme, a legal contract from a new counterparty may be entirely free-form, with no fixed layout and no guaranteed field positions.

Most business documents fall somewhere in between:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/document_landscape.png)

## Sensible's hybrid extraction approach

Because no single technique covers the full document landscape, Sensible supports two extraction strategies that you can mix within the same config:

| strategy | best suited for | characteristics |
| -------- | --------------- | --------------- |
| [LLM-based methods](doc:llm-based-methods) | Free-form, variable documents — legal contracts, clinical notes, open-ended forms | Describe what to extract in natural language. Handles layout variation automatically. Non-deterministic; suited to workflows with [human review](doc:human-review) or fault tolerance. |
| [Layout-based methods](doc:layout-based-methods) | Structured, consistently formatted documents — tax forms, insurance declarations, bank statements | Target data by its position relative to anchor text and document layout. Deterministic and fast; suited to automated pipelines requiring predictable output. |

When either approach works, Sensible recommends layout-based methods for their speed and deterministic output. When a document type spans both structured and unstructured variants, you can [mix strategies in the same config](doc:author) or use [fallback fields](doc:fallbacks) to chain them.

## The IDP pipeline

Sensible's platform covers the full IDP lifecycle, not just extraction. For a detailed breakdown of each stage, see [Devops platform](doc:devops-platform). At a high level:

1. **Ingest** — Upload documents via API, SDK, bulk UI, or email. Sensible normalizes inputs into a standardized text representation and applies [OCR](doc:ocr) where needed.
2. **Classify** — Documents are routed to a *document type* (a category like `bank_statements`) and automatically classified into a matching *config* (a subtype like `chase_statements`). Sensible uses [fingerprints](doc:fingerprint) and LLM-based classification to select the best config.
3. **Extract** — SenseML queries run against the document and return structured JSON. Sensible includes an open-source [configuration library](doc:library-quickstart) with out-of-the-box support for common business forms.
4. **Validate and monitor** — Write [validation rules](doc:validate-extractions) to catch extraction errors, track [extraction coverage](doc:coverage) and [accuracy](doc:accuracy-measures) in production, and route low-confidence extractions to [human review](doc:human-review).

## Developer-first design

Sensible is built for developers integrating document automation into applications. Extraction configs are JSON — version-controlled, testable, and deployable through Sensible's [CI/CD platform](doc:devops-platform). You interact with Sensible through a [REST API](doc:quickstart) or [Node/Python SDKs](doc:sdk-guides), and configs live alongside your application code.

This design makes it practical to treat document extraction as a first-class software engineering problem: write configs, test against sample documents, review diffs in pull requests, and deploy to production with confidence.
