# Docs triage criteria

Each line is one noul question Jev answers about a merged sensible-hq/sensible PR (title,
description, changed files, diff excerpt). T-* questions are triggers; X-* are exclusions.
`decide` in triage.py applies the rule:

- **docs_needed_ai:** T-config, T-inputs, or T-models scores 0.90 or higher, and every X-*
  question scores below 0.30.
- **docs_triage_ai:** otherwise, any trigger scores 0.70 or higher and X-internal doesn't. A
  high X-hidden, X-bugfix, X-in-progress, or X-customer score sends a PR here instead of to
  docs_needed_ai, but doesn't drop it: like the changelog skill's `investigate`, someone decides.
- **No label:** no trigger reaches 0.70, or X-internal does.

The exclusions follow `.claude/skills/changelog/references/categorization-rules.md`.

- [T-config] The PR adds, removes, or renames something a customer can write in a SenseML configuration, such as a method, a method parameter, a preprocessor, a postprocessor, a type or eduction, a JsonLogic operator, or a section or fingerprint option, or changes the values that such a setting accepts or its default.
- [T-behavior] The PR changes what an existing SenseML method, type, preprocessor, or computed field extracts or returns for the same document and configuration, in a way a customer would notice in their extraction output, and it is not just a fix that makes the feature behave as it was already supposed to.
- [T-api] The PR changes an endpoint in the public API list in the context (its path, request parameters, request or response or webhook body fields, status codes, error shapes, or limits), or adds an endpoint meant to be called from customers' own code. Changes to endpoints that only the Sensible web app uses, such as login, SSO, sign-up, account settings, billing, or usage reporting, don't count, and neither does moving or reimplementing an endpoint (for example on SST) when customers send and get back the same thing as before.
- [T-inputs] The PR changes which documents or inputs customers can send Sensible, such as adding support for a new file format or content type, or changes which OCR engine or document reader customers can choose.
- [T-models] The PR changes which LLM provider or model customers can select, or which model a customer-facing feature (such as queryGroup, list, nlpTable, classification, or confidence signals) uses by default.
- [T-output] The PR changes the shape of what customers get back from an extraction, such as fields in parsedDocument, extraction metadata, CSV or Excel output, or portfolio output.
- [X-internal] Every change in the PR is internal: a refactor, tests, dependency upgrades, build or CI, deployment or infrastructure, logging, monitoring, performance work with no change to results, internal accounting such as billing, HubSpot, Segment, Stripe, or usage tracking, or moving existing endpoints to new infrastructure (for example SST) or wiring up routes without changing what customers send or get back.
- [X-hidden] The PR describes the feature as experimental, internal-only, behind a flag, or not to be documented or announced publicly yet.
- [X-bugfix] The PR fixes a bug, an error, or a regression, and adds no new setting, option, or behavior that a customer would choose or rely on.
- [X-in-progress] The PR is one step of unfinished work that customers can't use yet, such as a WIP, a dummy or placeholder implementation, a first part of several, or groundwork for a later PR.
- [X-customer] The PR is built for one named customer or account, or turns a feature on or off per account through an internal tool or CLI, rather than for customers in general.
