# Sensible product skills: decisions

Decisions behind the published agent skills in `skills/`. Each entry states the decision, why, and its status. **Decided** entries have your sign-off. **Proposed** entries are drafts waiting for your comments.

## 1. Skills live in `sensible-docs`, under `skills/`

**Status:** decided

The skills live in this repo on the `product-skills` branch, one `skills/<name>/SKILL.md` per skill, with an optional `references/` folder loaded on demand. The layout matches `payabli/integration-skills`, so a later move to a dedicated repo would be a plain copy.

## 2. First slice is fundamentals plus getting started

**Status:** decided

`sensible-fundamentals` and `sensible-getting-started` ship first. The deterministic-extraction skill, the SenseML primer, and the CLI tool come later.

## 3. The skills follow the writing-for-agents reference

**Status:** proposed

Drafts follow Matt Pocock's `writing-for-agents` skill:

- Cut any sentence that doesn't change agent behavior.
- State the behavior you want rather than prohibitions.
- End every step on a checkable done-condition.
- Push anything only some branches need behind a pointer.

## 4. All skills are model-invoked

**Status:** proposed

Each skill keeps a trigger-bearing `description`, so a developer's agent reaches it without the developer knowing the skill's name. Published skills serve people who don't know they exist, so user-invoked skills would never fire.

## 5. Fundamentals is the shared reference; other skills load it first

**Status:** proposed

Auth, the document type / config / field model, the extraction-approach rules, environments, sync vs. async, and the response shape live only in `sensible-fundamentals`. Other skills point to its sections rather than restating them, so each fact has one place to edit.

## 6. Exact facts come from the live docs, not the skill

**Status:** proposed

The skills carry procedure. They send the agent to `https://docs.sensible.so/llms.txt`, to `.md` page URLs, and to the Sensible MCP server for endpoint paths, parameters, and SenseML syntax. A skill that restates those facts goes stale on the next docs release.

## 7. Recommend layout-based extraction where both approaches work

**Status:** proposed

Getting started recommends deterministic layout-based extraction for known layouts, LLM-based extraction for free-form or long-tail documents, and the configuration library for common forms. This follows the existing docs page `Choosing an extraction approach`. The integration path (SDK, API, email, Zapier, quick extraction) is presented neutrally, because the right one depends on the developer's app.

## 8. Getting started writes a `sensible-integration.md` plan

**Status:** proposed

The plan records each document type with its approach, target fields, and sample location, plus the integration path, SDK, environment, and async delivery. Values come from a fixed vocabulary so downstream skills read them reliably. The per-document-type section exists because the extraction skill needs exactly that input.

## 9. The API key stays out of the chat

**Status:** proposed

Getting started has the developer export `SENSIBLE_API_KEY` in their own shell or secrets store. The agent never asks for the key itself. A key pasted into an agent chat lands in transcripts and logs.

## 10. No hand-off to the extraction skill until it exists

**Status:** proposed

Getting started's capability table links to docs pages only. When the extraction skill lands, its row gets a skill hand-off. A published skill pointing at a missing skill sends agents nowhere.

## 11. The extraction skill can't depend on `sensible-llm-toolkit` while it's internal

**Status:** open

The internal `sensible` skill gets its extract, probe, and config-push CLI from `sensible-hq/sensible-llm-toolkit`. That repo is internal, so a published skill can't link to it. Either the toolkit goes public, or the extraction skill ships its own CLI.
