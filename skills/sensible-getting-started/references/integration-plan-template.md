# sensible-integration.md template

Write this file to the repo root as plain markdown with no frontmatter. Its reader is an agent that loads the whole file, so section headers are a legibility convention, not a parsing contract. Keep the first line exactly as shown; it is the schema version.

## Template

```markdown
<!-- sensible-integration-plan: schema-v1 -->
# Sensible integration plan

## What we're extracting
<one or two sentences on the goal, in the developer's words>

## App shape
<framework, language, and where documents enter the app>

## Document types
- auto_insurance_quotes: layout-based
  fields: policy_number, premium, effective_date
  samples: samples/quotes/
- loss_runs: llm-based
  fields: claims (repeating)
  samples: none yet

## Integration path
sdk

## SDK
node-sdk

## Environment
development

## Async delivery
polling
```

## Controlled vocabulary

Use these exact values so downstream skills read them reliably. Prose may follow a value on later lines.

| Section | Allowed values |
| --- | --- |
| `## Document types`, per type | `layout-based`, `llm-based`, `mixed`, `library` |
| `## Integration path` | `sdk`, `api`, `email`, `zapier`, `quick-extraction` |
| `## SDK` | `node-sdk`, `python-sdk`, `raw-http`, `none` |
| `## Environment` | `development`, `production` |
| `## Async delivery` | `polling`, `webhook`, `sync-only` |

Document type names follow Sensible's naming: lowercase with underscores.

## Guardrail

The plan records declared intent. When the repo's code contradicts it, follow the code and note the mismatch.
