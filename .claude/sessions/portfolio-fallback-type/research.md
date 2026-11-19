# Research: portfolio `fallback_type`

Source PR: [sensible-hq/sensible#3523](https://github.com/sensible-hq/sensible/pull/3523), "Extract unmatched portfolio pages with a fallback doc type", merged and listed in the Nov 17, 2026 release notes.

Customer names are internal. This page calls the customer "Customer A".

## Customer need

Customer A sends every extraction as a portfolio. Their `bank_statements` document type has 9 configs: 8 layout configs with fingerprints, and 1 LLM config without a fingerprint, meant as the catch-all for banks they have no layout for. In a portfolio segmented with fingerprints, pages that no fingerprint matched were dropped instead of going to the LLM config. A single doc type extraction of the same file fell back to the LLM config as expected.

Customer A's contact asked for exactly that fallback: any bank statement that doesn't match a fingerprint should go to the LLM config. Nicolas proposed the fallback setting on Nov 3. On Nov 4, the contact also asked to route documents from other doc types to the catch-all, which a fallback doc type covers. On Nov 18, Nicolas announced the feature to Customer A, created `general_bank_statements` in their account as the fallback type, and sent them a short guide to adding it to their extraction requests.

Sources:

- [Notion: Portfolio + Fingerprint mode: Fallback to LLM config](https://app.notion.com/p/409c7dd497888050a022d8c14c5cf836) (Product feedback, status "Review pending")
- [Slack: Nov 3 proposal](https://sensiblehq.slack.com/archives/C08TC7N67GD/p1793721233116939?thread_ts=1787132716.062909&cid=C08TC7N67GD)
- [Slack: Nov 4 request for other doc types](https://sensiblehq.slack.com/archives/C08TC7N67GD/p1793780123730269?thread_ts=1787132716.062909&cid=C08TC7N67GD)

## Real-world use case

A file holds bank statements from many banks. Statements from known layouts match their configs' fingerprints. Statements from any other bank go to a general LLM config instead of disappearing from the output.

The same pattern applies to any portfolio with a long tail of document types: fingerprint the documents you know, and send everything else to a catch-all document type, for example one that classifies the document and pulls a few general fields.

## Problem it solves

Before this option, a portfolio extraction silently left out pages that no doc type recognized, with no error. A user who had built a catch-all config got nothing for exactly the documents it was built for. Because the same file worked as a single doc type extraction, the failure was hard to diagnose.

## What it does

`fallback_type` is a new portfolio extraction option that names one of the portfolio's `types`. Pages that no other doc type claims are extracted with that doc type instead of being dropped. With fingerprint segmentation, each run of consecutive unmatched pages becomes one document, runs of blank pages are skipped, and a file where nothing matches becomes one document. With LLM segmentation, segments the LLM classifies as unknown become fallback documents.

Details for the docs:

- A `fallback_type` that isn't in `types` gets a 400: `Fallback type "<name>" must be one of the portfolio document types`. Verified on dev.
- The fallback doc type runs the configs a single doc type extraction would pick: the configs without fingerprints, or all of them when every config has fingerprints, or none with `fingerprint_mode: strict`.
- Supported in the extraction request, `multi.json`, batches, and golden editor extractions. Email processor portfolio specs don't support it yet.
- If the fallback doc type's configs are gone when the extraction runs, for example unpublished, the extraction fails with "Fallback type X has no configuration to run in this portfolio".

## Related PRs

| PR | State | Relation |
| --- | --- | --- |
| [sensible#3521](https://github.com/sensible-hq/sensible/pull/3521) | merged | Prerequisite: #3523 is stacked on it. Lets portfolio batches set `ocr_engine` and `ocr_every_page`, and rejects portfolio options on single doc type batches. Not related to the fallback need. |
| [sensible#3520](https://github.com/sensible-hq/sensible/pull/3520) | merged | Defines portfolio options once, in `src/engine/portfolio-options.ts`, where `fallback_type` was added. |
| [sensible#3524](https://github.com/sensible-hq/sensible/pull/3524) | merged | Sibling fix for the same problem: reports doc types and configs without fingerprints in the portfolio's `errors`, fails a fingerprint portfolio with no fingerprints at all with a 400, and returns `errors` in the GET extraction response. |
| [sensible-app#1907](https://github.com/sensible-hq/sensible-app/pull/1907) | open | UI for #3524: lists portfolio errors without a page range in a "Portfolio errors (n)" popover. |
| [sensible-app#1894](https://github.com/sensible-hq/sensible-app/pull/1894) | open, WIP | Fingerprint validator flags pages a portfolio fingerprint leaves out. Same problem, caught while building configs. |

## UI changes

None shipped and none planned. The app has no code for `fallback_type`, and no app PR, app issue, Notion page, or Slack thread proposes a UI for it. The feature is API-only, so the docs have no app screenshots to show. Quick Extract's Portfolio + Fingerprint mode, where the problem was reproduced, would be the natural place for a fallback picker.

## Example

The PR's own example, `extractors/11multidoc/multi_fallback`, can't be published: its golden contains a real person's life insurance statements and real certificates of insurance.

The docs example on this branch, `docs/document extraction/draft-portfolio-fallback-example.md`, uses public docs assets instead. It extends the Fingerprint example in Multi-document extractions with an invoice, a lease, and a bank statement, and adds an `other_documents` doc type with an LLM config and no fingerprint. Run on the personal dev account on Nov 18, 2026:

| Page | With `fallback_type` | Without `fallback_type` |
| --- | --- | --- |
| 1, invoice | `other_documents` / `catch_all` | dropped |
| 2, car insurance quote | `auto_insurance_quotes` / `anyco` | same |
| 3, lease | `other_documents` / `catch_all` | dropped |
| 4, car insurance quote | `auto_insurance_quotes` / `anyco` | same |
| 5, loss run | `loss_run_reports` / `acme` | same |
| 6, bank statement | `other_documents` / `catch_all` | dropped |

Without `fallback_type`, the response's `errors` reports that `other_documents` has no fingerprints, so it can't match any page.

## Gaps

- The Notion page "Detect fingerprint-less configs in portfolio extractions" is probably the spec for #3524, but its body is an embedded object that couldn't be read.
- GitHub issues in `sensible` and `sensible-app` had nothing beyond the PRs above.
