---
name: sensible-fundamentals
description: >-
  Foundation reference for any Sensible document-extraction work. Use for API
  authentication, the document type / config / field model, choosing LLM-based
  or layout-based extraction, development vs. production environments, sync vs.
  async extraction, and reading the extraction response. Other Sensible skills
  load it first. Reads sensible-integration.md on load if present.
metadata:
  author: sensible
  version: "0.1"
---

# Sensible fundamentals

Cross-cutting knowledge every Sensible integration needs. Other Sensible skills load this skill first.

## On load

If `sensible-integration.md` exists at the repo root, read it now and apply its decisions (document types, extraction approach, SDK, environment). When the repo's code contradicts the plan, follow the code and tell the developer about the mismatch.

## Look up exact facts in the docs

This skill carries procedure. Take exact endpoint paths, parameters, SenseML syntax, and response fields from the live docs:

- Index of every page: `https://docs.sensible.so/llms.txt`. Take page URLs from it rather than composing them.
- Any page as markdown: append `.md` to its URL, for example `https://docs.sensible.so/docs/author.md`.
- Docs and API-spec search: the Sensible MCP server at `https://docs.sensible.so/mcp` (setup: `https://docs.sensible.so/reference/mcp.md`).

## Authentication

Sensible authenticates with an API key sent as a bearer token: `Authorization: Bearer <key>`. The developer creates the key on their account page, `https://app.sensible.so/account/`. Read it from the `SENSIBLE_API_KEY` environment variable or a secrets store, and keep it in server-side code. Detail: `https://docs.sensible.so/reference/authentication.md`.

The API base URL is `https://api.sensible.so/v0`.

## Object model

- **Document type**: a category of similar documents, such as `auto_insurance_quotes`. Every extraction request names one.
- **Config**: a SenseML extraction template inside a document type, usually one per layout variant (one per carrier, form revision, or vendor). When a request names only the document type, Sensible runs every config in it and returns the best-scoring result. Naming a config in the path (`/extract/{document_type}/{config_name}`) skips that selection.
- **Field**: the unit of a config. Each field has an `id` and a method, and returns one key in the response's `parsed_document`.

Field IDs become the developer's data contract. Keep a field's `id` identical across every config in a document type, so downstream code reads one schema.

## Choosing an extraction approach

SenseML mixes two method families in one config:

- **Layout-based** methods are **deterministic**: they find data by anchor text and position, return the same output for the same document, and run fast. Use them for structured documents with a known, finite set of layouts.
- **LLM-based** methods (Query Group, List, NLP Table) take a natural-language description. Use them for free-form or highly variable documents, and in workflows that tolerate probabilistic output or include human review.

Where both work, prefer layout-based for determinism and speed. Common forms (tax forms, bank statements, insurance declarations) often have a ready-made config in Sensible's open-source configuration library; start from it. Detail: `https://docs.sensible.so/docs/author.md`.

## Environments

Configs are published to `development` or `production`. Extraction requests take an `environment` query parameter that defaults to `production`. Test config changes with `environment=development`, then publish to production. When several configs in a document type change, publish them to production together, so config selection behaves the same as it did in testing. Detail: `https://docs.sensible.so/docs/environments.md`.

## Sync vs. async extraction

- **Sync** (`POST /extract/{document_type}`): returns the result in the response. Use it for testing.
- **Async** (`/generate_upload_url/...` or `/extract_from_url/...`): returns an extraction ID. Use it in production, and get the result by polling `GET /documents/{id}` until `status` is `COMPLETE` or `FAILED`, or by setting a webhook.

Multi-document PDFs ("portfolios") use the portfolio variants of the async endpoints. Endpoint guide: `https://docs.sensible.so/reference/choosing-an-endpoint.md`.

## Reading the response

- `parsed_document`: one key per field ID. Any field's value can be `null` when Sensible found nothing, so code handles `null` for every field.
- `status`: `WAITING`, `PROCESSING`, `FAILED`, or `COMPLETE`.
- `errors` and `validations`: extraction errors, and the results of validation rules written in the config.
- `coverage`: the fraction of fields that returned a value. Use it as a completeness signal.

## SDKs and direct API

Sensible has official SDKs for Node/TypeScript (`npm install sensible-api`) and Python (`pip install sensibleapi`). They wrap upload, polling, and auth. Detect the project's language from its manifest (`package.json`, `pyproject.toml`, `requirements.txt`). For a Node or Python project, offer the matching SDK. For any other language, call the REST API directly. Record the choice in `sensible-integration.md` under `## SDK`. Detail: `https://docs.sensible.so/docs/sdk-guides.md`.

## Supported files

PDF, Word (DOC, DOCX), spreadsheets (XLSX, XLS, XLSM, CSV), JPEG, PNG, and TIFF. Some methods work only on some file types. Check `https://docs.sensible.so/docs/file-types.md` before choosing a method for a non-PDF file.
