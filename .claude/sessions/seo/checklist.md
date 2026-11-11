# SEO/GEO: search phrases in excerpts and first ~150 words

Claude Code session name: seo
Claude Code session ID: c14f96d2-faef-4dbe-8951-0d7f13df161c
Branch: seo-keywords (worktree: ~/GitHub/sensible-docs-seo-keywords)
Related issue: #722 (GEO/SEO for docs: options?)

## Research notes (2026-10-20)

- [x] Background research (other docs sites' search phrasing, a best-practice reference for page
      openings and llms.txt descriptions, and evidence on the keywords meta tag) was moved to a
      private Notion page and removed from this branch before merge.

## Goal

Get docs pages found by Google search (SEO) and cited by AI search and agents (GEO) by working the
search phrases people actually use into each important page's title, excerpt (source of truth for
`metadata.description`, the meta description, and the `llms.txt` description; see PR #702), and
first ~150 words. Draft per-page phrases: `keywords-draft.md`.

## Decision: not using `metadata.keywords` (2026-10-20)

ReadMe's frontmatter allows a `metadata.keywords` list. We're not filling it in. Why:

- **ReadMe strips it.** On a page with keywords set (`draft-jsonlogic`), the keywords appear only in
  ReadMe's embedded page JSON: no `<meta name="keywords">` in the HTML, and none in the page's `.md`
  or in `llms.txt`. (`metadata.description`, by contrast, renders as the meta description.) ReadMe's
  own docs: 0 of 150 pages render a keywords tag.
- **Search engines ignore the tag anyway.** Google: "not used by Google Search, and it has no effect on
  indexing and ranking at all" (current docs, updated 2025-12). Bing: at most a spam signal (2011),
  "dead in terms of SEO value" (2014).
- **AI crawlers and agents don't see it.** AI search features sit on search indexes; agent fetch tools
  convert page bodies to Markdown and drop `<head>`; crawler docs mention only robots.txt.
- **Comparable docs sites don't use it either.** (Sources are in the private research notes.)

## Terminology decision (2026-10-20)

- "Extract," not "parse," throughout the docs, for terminology rigor. Parse-words appear in body text
  only once: the defined alias on the Overview ("Sensible extracts structured data from documents
  (also called document parsing)"). An email-page alias ("This is also called email parsing.") was
  added, then removed per review (2026-10-20) as awkward.
- Reasoning: Google and LLM-based tools match synonyms semantically, so pages that say "extract" can
  still rank or be retrieved for "parse" queries; literal keyword search (possibly ReadMe site search
  / docs MCP search; unverified) may not, which the defined aliases partly cover.
- "Config," not "template." "Template" appears only as a defined alias, on two pages (added
  2026-10-20): `docs/document extraction/getting-started.md` (#3: 'save your descriptions as a "config"
  (also called a template)') and `docs/document extraction/library-quickstart.md` (#25: 'prebuilt
  configs (also called templates)', where the app's **Template library** tab appears). Low-traffic
  pages that already equate them: `config-settings/index.md`, `document-type-settings/index.md`.
- "Probabilistic" as a descriptor (not an alias) for LLM-based methods, paired with "deterministic"
  for layout-based. Added 2026-10-20 on `docs/welcome/author.md` only (Choosing an extraction
  approach): intro sentence and the comparison table's Deterministic row ("No. LLM output is
  probabilistic."). Not added to #34 LLM-based methods (messaging caution: can read as "unreliable").
- [x] Alias added 2026-10-20: `docs/welcome/overview.md` ("...structured data from documents (also
      called document parsing)"; also replaced an unrelated "parse extracted data types" with "filter and
      format" and cut "Welcome!"). Note: the Vale config already has "parse" on its Avoid list.

## Research

- [x] Research (kept privately; see Research notes above): how comparable docs sites target search
      phrases, a best-practice reference for page openings, and keywords-tag evidence. Takeaways used
      here: openings should define the topic with search terms in sentence 1 and say what problem it
      solves in sentence 2; descriptions should be task-focused; document-type pages are covered on
      the marketing site (8 /extract/* pages + ~20 how-to blog posts), out of scope for docs.
- [x] Password-protected PDFs: not supported per user (2026-10-19); phrase dropped

## ReadMe findings

- `agentSearch` (ReadMe's agent search endpoint, e.g.
  `https://docs.readme.com/main/agentSearch?query=term1%20term2`) is not enabled for us:
  `docs.sensible.so/agentSearch`, `/docs/agentSearch`, `/main/agentSearch` all 404. Our `.md` pages
  expose only `agentTools.projectIndex`, no `projectSearch`.
- Stale reference descriptions: all 14 reference/ `.md` pages have description != excerpt, but when
  description is empty ReadMe falls back to the excerpt (verified live on /reference/mcp). Only
  non-empty stale descriptions hurt: `choosing-an-endpoint.md` and `authentication.md`. FIXED
  2026-10-19 (manual sync to excerpt; reference/ frontmatter is mostly OpenAPI-generated, so no
  script change). (`senseml-reference-link.md` has 'null'; check.)

## Pages

Excerpts applied for #1–41 (2026-10-20, `apply_excerpts.py`). Open items moved to PR #763's checklist.

Grouping and per-page phrases: `keywords-draft.md`. Numbers are stable IDs.

Original list (approved 2026-10-19)
- [x] 1. Overview — `docs/welcome/overview.md`
- [x] 2. Getting started — `docs/welcome/getting-started-ai.md`
- [x] 3. Getting started with layout-based extractions — `docs/document extraction/getting-started.md`
- [x] 4. Intelligent document processing — `docs/Senseml reference/concepts/idp.md` (116 words; thin)
- [x] 5. Supported file types — `docs/Senseml reference/concepts/file-types.md`
- [x] 6. OCR — `docs/Senseml reference/concepts/ocr.md`
- [x] 7. Row — `docs/Senseml reference/layout-based-methods/row.md`
- [x] 8. Region — `docs/Senseml reference/layout-based-methods/region.md`
- [x] 9. Passthrough — `docs/Senseml reference/layout-based-methods/passthrough.md`
- [x] 10. Intersection — `docs/Senseml reference/layout-based-methods/intersection.md`
- [x] 11. Anchor object — `docs/Senseml reference/field-query-object/anchor.md`
- [x] 12. Table methods — `docs/Senseml reference/concepts/table-methods.md`
- [x] 13. Query group — `docs/Senseml reference/llm-based-methods/query-group.md`
- [x] 14. List — `docs/Senseml reference/llm-based-methods/list.md`
- [x] 15. NLP table — `docs/Senseml reference/llm-based-methods/nlp-table.md`
- [x] 16. Sections — `docs/Senseml reference/sections/index.md`
- [x] 17. Fingerprint — `docs/Senseml reference/config-settings/fingerprint.md`
- [x] 18. Classifying documents by type — `docs/document type classification/classify.md`
- [x] 19. Multi-document extractions — `docs/document extraction/portfolio.md`
- [x] 20. Validating extractions — `docs/monitor and qa/validate-extractions.md`

Added from research and review (2026-10-19)
- [x] 21. Qualifying LLM accuracy — `docs/document extraction/best-practices/confidence.md`
- [x] 22. Human review — `docs/monitor and qa/human-review.md`
- [x] 23. Preprocessors — `docs/Senseml reference/preprocessors/index.md`
- [x] 24. Try a webhook — `docs/api/api-tutorial/api-tutorial-webhook.md`
- [x] 25. Out-of-the-box extractions — `docs/document extraction/library-quickstart.md`
- [x] 26. Integrating — `docs/welcome/integrate.md`
- [x] 27. API Introduction — `reference/Introduction/choosing-an-endpoint.md`
      (live: https://docs.sensible.so/reference/choosing-an-endpoint). Stale description fixed and
      "Welcome to Sensible!" opening cut 2026-10-19; first ~150 words still need a rewrite.
- [x] 28. OCR preprocessor — `docs/Senseml reference/preprocessors/ocr-preprocessor.md` (target: force OCR)

High-traffic pages (ReadMe dashboard, past year; added 2026-10-20). Views in parentheses.
- [x] 29. Merge lines — `docs/Senseml reference/preprocessors/merge-lines.md` (888)
- [x] 30. JsonLogic extensions — `docs/Senseml reference/concepts/jsonlogic.md` (792)
- [x] 31. SenseML reference introduction — `docs/Senseml reference/senseml-reference-introduction.md` (701)
- [x] 32. Layout-based methods — `docs/Senseml reference/layout-based-methods/index.md` (535)
- [x] 33. Field query object — `docs/Senseml reference/field-query-object/index.md` (450)
- [x] 34. LLM-based methods — `docs/Senseml reference/llm-based-methods/index.md` (397)
- [x] 35. Types — `docs/Senseml reference/field-query-object/types.md` (349)
- [x] 36. API tutorial — `docs/api/api-tutorial/index.md` (290)
- [x] 37. Match object — `docs/Senseml reference/field-query-object/match.md` (288)
- [x] 38. API quickstart — `docs/integrations/quickstart.md` (271)
- [x] 39. Getting started with email extraction — `docs/integrations/getting-started-email.md`
- [x] 40. Custom computation — `docs/Senseml reference/advanced-computed-field-methods/custom-computation.md`
- [x] 41. Custom computation group — `docs/Senseml reference/advanced-computed-field-methods/custom-computation-group.md`
- [ ] 42. Extract data from a document (sync) — `reference/Extraction/document-1/extract-data-from-a-document.md` (excerpt pending: spec-generated; tracked in PR #763)
      (pointer to `openapi_extraction.json`; description and body text live in the spec)
- Already in list and high-traffic: overview (1.3K), choosing-an-endpoint (997), sections (421),
  query-group (409), anchor (279), portfolio (278), library-quickstart (259), preprocessors (244).
- Not in the top ~30 by views: Row, Region, Passthrough, Intersection (most-used methods by
  customers, but not most-viewed pages).

## Next steps

- [x] Draft per-page phrases for all 42 pages (`keywords-draft.md`), grouped by topic
- [x] Apply first round of PR review comments (2026-10-20)
- [x] Add current excerpt (extracted deterministically from frontmatter; OpenAPI summary for
      spec-generated #42) to each page in the draft, with character counts (2026-10-20)
- [x] Apply Best-phrase +/- changes from research and review (14 pages; marked
      "Applied 2026-10-20" in the draft)
- [x] Propose a new excerpt per page (fan-out by topic group, fan-in merge into draft). Done
      2026-10-20: 5 subagents; fan-in checked lengths (all <= 150), parse-words, phrase collisions,
      and edited 12 for length/wording.
      Limit: target <= 150 chars, hard cap 160 (`MAX_LENGTH` in `scripts/descriptions/frontmatter.py`;
      prompt in `generate_excerpts.py`). Note: #27's current excerpt is 185 chars (over the cap).
      Note: `.claude/style-guide/style-guide-overview.md` still says `metadata.description` is a 4–7
      word phrase; that predates PR #702 (excerpt = source of truth) and should be updated.
- [x] User reviews draft (four review rounds, 2026-10-20)
- [x] Apply approved excerpts (2026-10-20): `.claude/sessions/seo/apply_excerpts.py --write` set `excerpt`
      and `metadata.description` on 41 pages from the draft's Proposed excerpts (text-level edit, other
      keys untouched; `sync_description.py --dry-run` and `check_excerpt.py` clean; rerun is a no-op).
      #42 skipped: spec-generated, no excerpt (see the #42 item).
- [x] Per-page body edits: moved to PR #763 (`first-150-words`)

## Moved: first 150 words and per-page edit plan

Moved 2026-10-20 to branch `first-150-words` (`.claude/sessions/first-150-words/`): the first-lines draft,
its build script, and the per-page edit execution plan.

## Moved to PR #763 (2026-10-20)

Not merge blockers for this PR; carried over to `.claude/sessions/first-150-words/checklist.md` on branch `first-150-words`: ui-docs evaluation, ReadMe support question (agentSearch), #42 spec field, excerpts that run ahead of their page body, optional mcp-search-eval, and tooling that writes excerpts.
