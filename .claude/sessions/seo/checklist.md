# SEO/GEO: search phrases in excerpts and first ~150 words

Claude Code session name: seo
Claude Code session ID: c14f96d2-faef-4dbe-8951-0d7f13df161c
Branch: seo-keywords (worktree: ~/GitHub/sensible-docs-seo-keywords)
Related issue: #722 (GEO/SEO for docs: options?)

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
- **Competitors don't use it.** None of Parseur, Docparser, Nanonets, Docsumo, Ocrolus curate keywords
  (Parseur's API docs have tool-generated ones plus one hand-set value).
- Evidence and sources: `research-keywords-evidence.md`, `competitors/`.

## Terminology decision (2026-10-20)

- "Extract," not "parse," throughout the docs, for terminology rigor. Parse-words appear in body text
  only as defined aliases, once each: Overview ("Sensible extracts structured data from documents
  (also called document parsing)") and the email extraction page ("also called email parsing").
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
- [x] Aliases added 2026-10-20: `docs/welcome/overview.md` ("...structured data from documents (also
      called document parsing)"; also replaced an unrelated "parse extracted data types" with "filter and
      format" and cut "Welcome!") and `docs/integrations/getting-started-email.md` ("This is also called
      email parsing."). Note: the Vale config already has "parse" on its Avoid list.

## Research

- [x] Competitor scan (2026-10-01): every sitemap page of Parseur, Docparser, Nanonets, Docsumo,
      Ocrolus (~1,400 pages). Terms competitors put in titles/headings that Sensible docs barely use:
      parse / parser / parsing, data extraction / extract data, bank statement, purchase order, bill
      of lading, receipt, table extraction, line items, export, FAQ, rate limits, SSO, user
      management, billing, post-processing. Doc-type pages: Ocrolus ~540, Docsumo ~40; Sensible
      covers doc types on the marketing site (8 /extract/* pages + ~20 how-to blog posts), out of
      scope for docs. Competitors document AI coding tools around their MCP servers.
- [x] Competitor top-20 analysis, one file per competitor plus `competitors/summary.md`: title, meta
      description, target phrases, closest Sensible page, borrowable phrases
- [x] Evidence on search engines and AI agents vs. the keywords tag (`research-keywords-evidence.md`)
- [x] Best-practice reference (not a competitor): Payabli top 10 pages, llms.txt descriptions, first
      150 words (`best-practice/payabli.md`). Pattern: sentence 1 defines the thing with search terms;
      sentence 2 says what problem it solves. llms.txt: one-paragraph product summary, audience-grouped
      "Choose your path" with short task-focused link descriptions; top-level "Cookbooks" section
      (relevant to the 'cookbook' idea for the config library page).
- [x] Password-protected PDFs: not supported per user (2026-10-19); phrase dropped
- [ ] Evaluate the `ui-docs` branch (PR #660, worktree `~/GitHub/sensible-docs-ui-docs`, last
      commit 2026-08-12) for material to rework method docs, especially their first ~150 words.
      Contents: `assets/ai/mini-pages/box.md` and `intersection.md` (short-form method pages:
      plain-language description, annotated syntax example, link to full docs),
      `assets/ai/senseml-descriptions.json` (task-focused one-liners per method and per parameter
      for box, intersection, checkbox, nearestCheckbox), plus a session checklist and friction log
      under `.claude/sessions/2026-08-10-ui-hover-descriptions/`. Promising: the Intersection
      mini-page opens with "Finds and extracts the value at the point where a row and a column
      cross in a table, like looking up a cell in a spreadsheet... More reliable than the Row method
      when a table has unpredictably empty cells", which already hits #10's target phrases (table
      cell lookup, empty table cells) better than the live page's opening.

## ReadMe findings

- `agentSearch` (ReadMe's agent search endpoint, e.g.
  `https://docs.readme.com/main/agentSearch?query=term1%20term2`) is not enabled for us:
  `docs.sensible.so/agentSearch`, `/docs/agentSearch`, `/main/agentSearch` all 404. Our `.md` pages
  expose only `agentTools.projectIndex`, no `projectSearch`.
- [ ] Ask ReadMe support how to enable `agentSearch` / `projectSearch`
- Stale reference descriptions: all 14 reference/ `.md` pages have description != excerpt, but when
  description is empty ReadMe falls back to the excerpt (verified live on /reference/mcp). Only
  non-empty stale descriptions hurt: `choosing-an-endpoint.md` and `authentication.md`. FIXED
  2026-10-19 (manual sync to excerpt; reference/ frontmatter is mostly OpenAPI-generated, so no
  script change). (`senseml-reference-link.md` has 'null'; check.)

## Pages

Grouping and per-page phrases: `keywords-draft.md`. Numbers are stable IDs.

Original list (approved 2026-10-19)
- [ ] 1. Overview — `docs/welcome/overview.md`
- [ ] 2. Getting started — `docs/welcome/getting-started-ai.md`
- [ ] 3. Getting started with layout-based extractions — `docs/document extraction/getting-started.md`
- [ ] 4. Intelligent document processing — `docs/Senseml reference/concepts/idp.md` (116 words; thin)
- [ ] 5. Supported file types — `docs/Senseml reference/concepts/file-types.md`
- [ ] 6. OCR — `docs/Senseml reference/concepts/ocr.md`
- [ ] 7. Row — `docs/Senseml reference/layout-based-methods/row.md`
- [ ] 8. Region — `docs/Senseml reference/layout-based-methods/region.md`
- [ ] 9. Passthrough — `docs/Senseml reference/layout-based-methods/passthrough.md`
- [ ] 10. Intersection — `docs/Senseml reference/layout-based-methods/intersection.md`
- [ ] 11. Anchor object — `docs/Senseml reference/field-query-object/anchor.md`
- [ ] 12. Table methods — `docs/Senseml reference/concepts/table-methods.md`
- [ ] 13. Query group — `docs/Senseml reference/llm-based-methods/query-group.md`
- [ ] 14. List — `docs/Senseml reference/llm-based-methods/list.md`
- [ ] 15. NLP table — `docs/Senseml reference/llm-based-methods/nlp-table.md`
- [ ] 16. Sections — `docs/Senseml reference/sections/index.md`
- [ ] 17. Fingerprint — `docs/Senseml reference/config-settings/fingerprint.md`
- [ ] 18. Classifying documents by type — `docs/document type classification/classify.md`
- [ ] 19. Multi-document extractions — `docs/document extraction/portfolio.md`
- [ ] 20. Validating extractions — `docs/monitor and qa/validate-extractions.md`

Added from competitor analysis and review (2026-10-19)
- [ ] 21. Qualifying LLM accuracy — `docs/document extraction/best-practices/confidence.md`
- [ ] 22. Human review — `docs/monitor and qa/human-review.md`
- [ ] 23. Preprocessors — `docs/Senseml reference/preprocessors/index.md`
- [ ] 24. Try a webhook — `docs/api/api-tutorial/api-tutorial-webhook.md`
- [ ] 25. Out-of-the-box extractions — `docs/document extraction/library-quickstart.md`
- [ ] 26. Integrating — `docs/welcome/integrate.md`
- [ ] 27. API Introduction — `reference/Introduction/choosing-an-endpoint.md`
      (live: https://docs.sensible.so/reference/choosing-an-endpoint). Stale description fixed and
      "Welcome to Sensible!" opening cut 2026-10-19; first ~150 words still need a rewrite.
- [ ] 28. OCR preprocessor — `docs/Senseml reference/preprocessors/ocr-preprocessor.md` (target: force OCR)

High-traffic pages (ReadMe dashboard, past year; added 2026-10-20). Views in parentheses.
- [ ] 29. Merge lines — `docs/Senseml reference/preprocessors/merge-lines.md` (888)
- [ ] 30. JsonLogic extensions — `docs/Senseml reference/concepts/jsonlogic.md` (792)
- [ ] 31. SenseML reference introduction — `docs/Senseml reference/senseml-reference-introduction.md` (701)
- [ ] 32. Layout-based methods — `docs/Senseml reference/layout-based-methods/index.md` (535)
- [ ] 33. Field query object — `docs/Senseml reference/field-query-object/index.md` (450)
- [ ] 34. LLM-based methods — `docs/Senseml reference/llm-based-methods/index.md` (397)
- [ ] 35. Types — `docs/Senseml reference/field-query-object/types.md` (349)
- [ ] 36. API tutorial — `docs/api/api-tutorial/index.md` (290)
- [ ] 37. Match object — `docs/Senseml reference/field-query-object/match.md` (288)
- [ ] 38. API quickstart — `docs/integrations/quickstart.md` (271)
- [ ] 39. Getting started with email extraction — `docs/integrations/getting-started-email.md`
- [ ] 40. Custom computation — `docs/Senseml reference/advanced-computed-field-methods/custom-computation.md`
- [ ] 41. Custom computation group — `docs/Senseml reference/advanced-computed-field-methods/custom-computation-group.md`
- [ ] 42. Extract data from a document (sync) — `reference/Extraction/document-1/extract-data-from-a-document.md`
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
- [x] Apply Best-phrase +/- changes from competitor research and review (14 pages; marked
      "Applied 2026-10-20" in the draft)
- [x] Propose a new excerpt per page (fan-out by topic group, fan-in merge into draft). Done
      2026-10-20: 5 subagents; fan-in checked lengths (all <= 150), parse-words, phrase collisions,
      and edited 12 for length/wording.
      Limit: target <= 150 chars, hard cap 160 (`MAX_LENGTH` in `scripts/descriptions/frontmatter.py`;
      prompt in `generate_excerpts.py`). Note: #27's current excerpt is 185 chars (over the cap).
      Note: `.claude/style-guide/style-guide-overview.md` still says `metadata.description` is a 4–7
      word phrase; that predates PR #702 (excerpt = source of truth) and should be updated.
- [ ] User reviews draft
- [ ] #42 (spec-generated): find which OpenAPI field ReadMe uses for the meta description and
      llms.txt description (the page has no excerpt) (`summary` is also the page title; `description` start is likelier) before
      editing `reference/openapi_extraction.json`
- [ ] Excerpts that run ahead of their page body (update the first ~150 words to match when
      applying): #3 "template-based" (page never says "template"), #11 "variable positions",
      "keyword", "landmark", #19 "split" (page says "segment"), #28 scanned/handwritten framing
- [ ] Apply approved excerpts. Excerpt is the source of truth: edit `excerpt` and also run
      `scripts/descriptions/sync_description.py` locally (or set `metadata.description` to match) so the
      `generate-descriptions` workflow doesn't open a follow-up sync PR. `sync_description.py` covers
      docs/ only: for reference/ #27 set both fields by hand; #42 lives in the OpenAPI spec.
      `llms.txt` regenerates from `metadata.description` (`sync-llmstxt` workflow).
- [ ] Optional: before/after `mcp-search-eval` on a handful of pages
- [ ] Execute per-page edits (plan below)

## Execution plan: per-page edits (agreed 2026-10-20)

Fan-out / fan-in with subagents, ~5 pages each.

- [ ] Decide scope: excerpt + first ~150 words, or excerpt only (the first-150-words rewrites are where
      the SEO/GEO value is, but cost more review time per page)
- [ ] Batch pages by topic, using the draft's topic groups (10 groups, 3–7 pages each), so each agent
      sees related pages and keeps phrasing consistent
- [ ] Shared inputs for every agent:
  - phrase-ownership map (which page owns which best phrase; non-owners don't use it)
  - Payabli opening pattern: sentence 1 defines the thing with search terms; sentence 2 says what
    problem it solves (`best-practice/payabli.md`)
  - terminology rule: "extract," not "parse" (see Terminology decision)
  - style rules: all `.claude/style-guide/` files, you-centric prose, `/* */` comments only in code,
    don't mention Label method, keep existing fence languages
  - exact scope of allowed edits; nothing else touched
- [ ] Fan-out: each agent edits only its own pages and writes a per-page change rationale; no
      agent edits shared files (checklist, draft)
- [ ] Fan-in (main session): check best-phrase collisions across pages; check any new factual
      claims; run Vale; full style pass across all edits for one voice; present one consolidated
      summary or draft PR
- [ ] Pilot one batch of ~5 pages first; user reviews; tune the prompt; then run the remaining batches
