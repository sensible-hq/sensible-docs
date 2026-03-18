---
title: Intelligent document processing
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Intelligent document processing with Sensible'
  robots: index
next:
  description: ''
---
Intelligent document processing (IDP) automates extracting structured data from documents so that business systems can consume and act on it. The core challenge of IDP is document variability, which requires a mix of extraction techniques to handle the full range of documents that real organizations deal with.

## The document variability problem

Document content varies along two axes: **structure** (how consistently the layout is arranged) and **variability** (how many format revisions or issuer variations exist).

At one extreme, a standard W-2 form has a predictable, fixed layout. The same fields appear in the same positions across issuers and years. At the other extreme, a legal contract from a new counterparty may be entirely free form, with no fixed layout and no guaranteed field positions. Most business documents fall somewhere in between:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/document_landscape.png)

File format adds a second dimension. PDFs, emails, spreadsheets, and images each require different handling. Image-based document require OCR, PDFs with embedded fonts need direct text extraction, and  spreadsheets and email attachments need format normalization. For details, see [Supported file types](doc:file-types) and [OCR](doc:ocr).

## Approaches to IDP

Today's IDP has a history that began with OCR and rules-based document extraction. In traditional document automation, you targeted data by its fixed position in a document. It was fast and deterministic, but brittle. It broke when layouts changed slightly or varied across issuers, and often required human review loops to catch errors. Fast forward to today, and LLMs handles document layout variation automatically, but are indeterminate.

Neither deterministic nor indeterminate approaches covers the full document landscape. Sensible's answer is a hybrid: use layout-based methods, boosted with machine learning (ML), for structured, consistently formatted documents. The combination of ML and layout-based rules results in robust deterministic output. Then, use LLM-based methods for free-form or highly variable documents where flexibility matters. At Sensible, both are part of the same query language, [SenseML](doc:senseml-reference-introduction), so you can mix them in a single config or chain them as fallbacks. For guidance on choosing between approaches, see [Choosing an extraction approach](doc:author).

## The IDP lifecycle

A complete IDP system does more than extract data. Sensible covers the full lifecycle, and you can choose and configure each step:

- **Ingest** — Accept documents in any supported format, normalize them into a standardized text representation, and apply OCR where needed.
- **Classify** — Route each document to the right extraction config automatically, handling both document type (e.g., `bank_statements`) and subtype (e.g., `chase_statements`).
- **Extract** — Run SenseML queries and return structured JSON. Pre-built configs for common business forms are available in Sensible's open-source [configuration library](doc:library-quickstart).
- **Validate and monitor** — Catch errors with both deterministic and LLM-based validation rules, track extraction coverage and accuracy in production, and route low-confidence extractions to human review. Patterns that surface through review — recurring nulls, systematic misreads — indicate where configs need tuning, closing the feedback loop between production accuracy and config development.

For a detailed breakdown of each stage, see [Devops platform](doc:devops-platform).

## Developer-first design

Sensible is built for developers integrating document automation into applications. Its JSON-based extraction configs are version-controlled, testable, and deployable through Sensible's platform. You interact with Sensible through a [REST API](doc:quickstart) or [Node/Python SDKs](doc:sdk-guides), and configs live alongside your application code.

This makes it practical to treat document extraction as a first-class software engineering problem: write configs, test against sample documents, review diffs in pull requests, and deploy to production with confidence.
