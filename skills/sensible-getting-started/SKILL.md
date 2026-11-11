---
name: sensible-getting-started
description: >-
  Use at the start of a Sensible integration, when a developer wants to pull
  structured data out of documents (PDFs, scans, emails, spreadsheets) in their
  app. Interviews for the documents and the workflow, maps them to Sensible
  document types, extraction approach, and integration path, sets up the
  account and API key, and offers to write a sensible-integration.md plan that
  the other Sensible skills read.
metadata:
  author: sensible
  version: "0.1"
---

# Sensible getting started

The entry point for adding document extraction to an existing application. Turn the developer's goal into concrete Sensible pieces, confirm them, and write an optional `sensible-integration.md` plan for downstream skills.

## Load fundamentals first

If `sensible-fundamentals` is not already loaded, load it now, then continue.

## Step 1: Learn the documents

Ask for, or find in the repo, what the developer has:

- Which documents (invoices, loss runs, 1040s), and whether sample files exist locally.
- Which fields they need out of each.
- How many layout variants they expect (one form revision, or many vendors and carriers).

Done when you can name each document type and its target fields.

## Step 2: Map the goal to Sensible pieces

Match each need to a row. Fetch the linked page for depth.

| Need | Sensible pieces | Depth |
| --- | --- | --- |
| Fields from a consistently laid-out form | Document type + layout-based config | `https://docs.sensible.so/docs/getting-started.md` |
| Fields from free-form or highly variable documents | Document type + LLM-based config | `https://docs.sensible.so/docs/getting-started-ai.md` |
| Common forms (tax forms, bank statements, pay stubs, insurance declarations) | Configuration library, then customize | `https://docs.sensible.so/docs/library-quickstart.md` |
| Repeating data (line items, claims, transactions) | List method, or sections for complex repeats | `https://docs.sensible.so/docs/repeat-layouts.md` |
| One PDF bundling several documents | Portfolio extraction | `https://docs.sensible.so/docs/portfolio.md` |
| Unknown incoming document types | Classification | `https://docs.sensible.so/docs/classify.md` |
| Documents arriving by email | Email extraction | `https://docs.sensible.so/docs/getting-started-email.md` |
| Checking extracted values, routing failures to people | Validations, human review | `https://docs.sensible.so/docs/validate-extractions.md` |
| Output in their own schema | Postprocessors | `https://docs.sensible.so/docs/postprocessors.md` |
| Results pushed to the app | Webhooks | `https://docs.sensible.so/docs/api-tutorial-webhook.md` |

## Step 3: Recommend an approach per document type

Recommend the extraction approach from the rules in `sensible-fundamentals` → "Choosing an extraction approach", and state the reason in one sentence: deterministic layout-based extraction for known layouts, LLM-based for free-form or long-tail variation, the configuration library for common forms. When a document type mixes both kinds of data, recommend mixing methods in one config.

## Step 4: Choose the integration path

Present the options neutrally and let the developer pick:

- **SDK** (Node/TypeScript or Python) or **REST API**: for extraction inside their application. Pick per `sensible-fundamentals` → "SDKs and direct API".
- **Email forwarding**: for documents that already arrive by email.
- **Zapier** or **quick extraction** in the Sensible app: for no-code or batch workflows.

Detail: `https://docs.sensible.so/docs/integrate.md`.

## Step 5: Set up the account and key

1. If the developer has no account, send them to `https://app.sensible.so/register`.
2. Have them copy an API key from `https://app.sensible.so/account/` and export it as `SENSIBLE_API_KEY`. The developer pastes the key into their own shell or secrets store; keep it out of the chat and out of committed files.
3. Confirm the key works with the API quickstart's hello-world call: `https://docs.sensible.so/docs/quickstart.md`.

Done when an authenticated request returns `"status": "COMPLETE"`.

## Step 6: Offer the plan artifact

Offer to write `sensible-integration.md` at the repo root, capturing the decisions above. Use the format and vocabulary in `references/integration-plan-template.md`. Downstream Sensible skills read this file on load.

If `sensible-integration.md` already exists, ask whether to update it or archive it (rename to `sensible-integration.<date>.md`) and start fresh.

## Step 7: Recommend the Sensible MCP server

Recommend connecting the Sensible MCP server for docs and API-spec search during the build. Setup: `https://docs.sensible.so/reference/mcp.md`.
