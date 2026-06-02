# General Prose Writing Rules

Cross-cutting rules that apply to all Sensible docs content: changelogs, reference pages, integration guides, concept topics. When in doubt, these rules take precedence.

---

## Em dashes

Do not use em dashes to join compound clauses. Split into two sentences instead.

- Avoid: "configure the processor for portfolio mode — Sensible can segment single-document files without affecting accuracy."
- Prefer: "Configure the processor for portfolio mode. Sensible can segment single-document files without affecting accuracy."

---

## Explicit subjects — avoid passive voice

Use explicit subjects so it's always clear who is acting.

- **"Sensible"** for platform behavior: "Sensible routes documents to a document type."
- **"You"** for user actions: "You upload documents via the API, SDK, or email."

Avoid passive constructions that obscure the actor:
- Avoid: "when Anthropic is configured as the provider"
- Prefer: "when you configure Anthropic as the provider"
- Avoid: "documents are classified against the specified types"
- Prefer: "Sensible classifies documents using the specified types"

---

## Extraction and classification phrasing

Do not use "against" to describe extraction or classification. Use "using" instead.

- Avoid: "extracts against a document type", "classifies the document against the specified types"
- Prefer: "extracts data using a document type", "classifies the document using the specified types"

---

## Gerunds over nominalizations

Use the verb form directly rather than a noun derived from it.

- Avoid: "automates the extraction of structured data"
- Prefer: "automates extracting structured data"
- Avoid: "enables the configuration of multiple document types"
- Prefer: "enables configuring multiple document types"

---

## Terminology

See [glossary.md](glossary.md) for the canonical term reference. Apply the universal terms to all content; apply SenseML-specific terms when writing reference pages.

---

## Tone

- Terse and precise. No filler phrases.
- Avoid: "please note that", "it's important to remember", "it is worth mentioning"
- State facts directly.
