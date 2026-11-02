# docs_triage_ai criteria

Each line is one noul question Jev answers about a merged sensible-hq/sensible PR (title, description,
changed files, diff excerpt). T-* are triggers; X-* are exclusions.
A PR gets the docs_triage_ai label when any trigger is at or above the threshold and no exclusion is.

- [T-config] The PR adds, removes, or renames something a customer can write in a SenseML configuration, such as a method, a method parameter, a preprocessor, a postprocessor, a type or eduction, a JsonLogic operator, or a section or fingerprint option, or changes the values that such a setting accepts or its default.
- [T-behavior] The PR changes what an existing SenseML method, type, preprocessor, or computed field extracts or returns for the same document and configuration, in a way a customer would notice in their extraction output, and it is not just a fix that makes the feature behave as it was already supposed to.
- [T-api] The PR changes an endpoint in the public API list in the context (its path, request parameters, request or response or webhook body fields, status codes, error shapes, or limits), or adds an endpoint meant to be called from customers' own code. Changes to endpoints that only the Sensible web app uses, such as login, SSO, sign-up, account settings, billing, or usage reporting, don't count, and neither does moving or reimplementing an endpoint (for example on SST) when customers send and get back the same thing as before.
- [T-inputs] The PR changes which documents or inputs customers can send Sensible, such as adding support for a new file format or content type, or changes which OCR engine or document reader customers can choose.
- [T-models] The PR changes which LLM provider or model customers can select, or which model a customer-facing feature (such as queryGroup, list, nlpTable, classification, or confidence signals) uses by default.
- [T-output] The PR changes the shape of what customers get back from an extraction, such as fields in parsedDocument, extraction metadata, CSV or Excel output, or portfolio output.
- [X-internal] Every change in the PR is internal: a refactor, tests, dependency upgrades, build or CI, deployment or infrastructure, logging, monitoring, performance work with no change to results, internal accounting such as billing, HubSpot, Segment, Stripe, or usage tracking, or moving existing endpoints to new infrastructure (for example SST) or wiring up routes without changing what customers send or get back.
- [X-hidden] The PR describes the feature as experimental, internal-only, behind a flag, built for one specific customer, or not to be documented publicly yet.
