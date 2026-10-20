# SEO/GEO synonym keywords

Claude Code session name: seo
Claude Code session ID: c14f96d2-faef-4dbe-8951-0d7f13df161c
Branch: seo-keywords (worktree: ~/GitHub/sensible-docs-seo-keywords)
Related issue: #722 (GEO/SEO for docs: options?)

## Goal

Build a synonym list per page for `metadata.keywords` (ReadMe frontmatter), aimed at
internal search, Google SEO, and GEO (LLM citation).

Caveat to keep in mind: Google ignores `<meta name="keywords">` (since 2009), and LLM
crawlers read page text. Synonyms only move external traffic when they also land in
titles, excerpts (source of truth for SEO description, see PR #702), or body text.
`metadata.keywords` alone mostly serves ReadMe internal search (unverified).

Format (see `docs/Senseml reference/concepts/draft-jsonlogic.md`):

```yaml
metadata:
  title: ''
  description: ...
  keywords:
    - custom computation
  robots: index
```

## Competitor research (2026-10-01)

Scanned every sitemap page of Parseur, Docparser, Nanonets, Docsumo, Ocrolus (~1,400 pages).

- None use curated meta keywords. Only developer.parseur.com (Apidog) emits them, auto-generated:
  page title + fixed boilerplate. Docparser: 20/181 Zendesk articles have internal labels, no
  label used more than twice.
- Terms competitors put in titles/headings that Sensible docs barely use:
  parse / parser / parsing (6 body mentions, 0 titles), data extraction / extract data (0 titles),
  bank statement, purchase order, bill of lading, receipt, table extraction, line items,
  export, FAQ, rate limits, SSO, user management, billing, post-processing.
- Doc-type pages: Ocrolus ~540, Docsumo ~40. Sensible covers doc types on the marketing site
  (8 /extract/* pages + ~20 how-to blog posts) — out of scope for docs.
- Competitors document AI coding tools (Docsumo: Claude Code, Cursor, Windsurf, Gemini CLI,
  VS Code Copilot, ChatGPT) around their MCP server.

## Pages (approved 2026-10-19)

Entry points / concepts
- [ ] 1. Overview — `docs/welcome/overview.md`
- [ ] 2. Getting started — `docs/welcome/getting-started-ai.md`
- [ ] 3. Getting started with layout-based extractions — `docs/document extraction/getting-started.md`
- [ ] 4. Intelligent document processing — `docs/Senseml reference/concepts/idp.md` (116 words; thin)
- [ ] 5. Supported file types — `docs/Senseml reference/concepts/file-types.md`
- [ ] 6. OCR — `docs/Senseml reference/concepts/ocr.md`

Layout-based methods
- [ ] 7. Row — `docs/Senseml reference/layout-based-methods/row.md`
- [ ] 8. Region — `docs/Senseml reference/layout-based-methods/region.md`
- [ ] 9. Passthrough — `docs/Senseml reference/layout-based-methods/passthrough.md`
- [ ] 10. Intersection — `docs/Senseml reference/layout-based-methods/intersection.md`
- [ ] 11. Anchor object — `docs/Senseml reference/field-query-object/anchor.md`
- [ ] 12. Table methods — `docs/Senseml reference/concepts/table-methods.md`

LLM-based methods
- [ ] 13. Query group — `docs/Senseml reference/llm-based-methods/query-group.md`
- [ ] 14. List — `docs/Senseml reference/llm-based-methods/list.md`
- [ ] 15. NLP table — `docs/Senseml reference/llm-based-methods/nlp-table.md`

Structure / classification / QA
- [ ] 16. Sections — `docs/Senseml reference/sections/index.md`
- [ ] 17. Fingerprint — `docs/Senseml reference/config-settings/fingerprint.md`
- [ ] 18. Classifying documents by type — `docs/document type classification/classify.md`
- [ ] 19. Multi-document extractions — `docs/document extraction/portfolio.md`
- [ ] 20. Validating extractions — `docs/monitor and qa/validate-extractions.md`

Added 2026-10-19 from competitor analysis
- [ ] 21. Qualifying LLM accuracy — `docs/document extraction/best-practices/confidence.md`
- [ ] 22. Human review — `docs/monitor and qa/human-review.md`
- [ ] 23. Preprocessors — `docs/Senseml reference/preprocessors/index.md`
- [ ] 24. Try a webhook — `docs/api/api-tutorial/api-tutorial-webhook.md`
- [ ] 25. Out-of-the-box extractions — `docs/document extraction/library-quickstart.md`
- [ ] 26. Integrating — `docs/welcome/integrate.md`
- [ ] 27. API Introduction — `reference/Introduction/choosing-an-endpoint.md`
      (live: https://docs.sensible.so/reference/choosing-an-endpoint). Found 2026-10-19:
      `metadata.description` is stale ("API introduction and endpoint overview") and does NOT match
      the excerpt; that stale string is the live `<meta name="description">`. The excerpt→description
      sync (PR #702) doesn't fix reference/ files. Also the first sentence is "Welcome to Sensible! If
      you have any questions..." (weak first-150-words opening). Check other reference/ pages for
      the same drift. Checked: all 14 reference/ .md pages have description != excerpt, but when
      description is empty ReadMe falls back to the excerpt (verified live on /reference/mcp). Only
      non-empty stale descriptions hurt: `choosing-an-endpoint.md` ("API introduction and endpoint
      overview") and `authentication.md` ("API authentication methods"), both live as-is. FIXED 2026-10-19 (manual sync to excerpt; reference/
      frontmatter is mostly OpenAPI-generated, so no script change). (`senseml-reference-link.md` has 'null'; check.)
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
      (pointer to `openapi_extraction.json`; keywords need a hand-added `metadata` block)
- [x] Truncated dashboard slugs resolved by user (2026-10-20): added getting-started-email,
      custom-computation, custom-computation-group, reference/extract-data-from-a-document.
- [x] Keyword rows drafted for 29–42
- Already in list and high-traffic: overview (1.3K), choosing-an-endpoint (997), sections (421),
  query-group (409), anchor (279), portfolio (278), library-quickstart (259), preprocessors (244).
- Not in the top ~30 by views: Row, Region, Passthrough, Intersection (most-used methods by
  customers, but not most-viewed pages).

## ReadMe findings (2026-10-19)

- `metadata.keywords` is stored, not rendered: hidden page `draft-jsonlogic` carries
  `"keywords":"custom computation"` (comma-joined string, so phrases survive as entries) in ReadMe's
  embedded page JSON, but the HTML has no `<meta name="keywords">`. `metadata.description` IS rendered
  as `<meta name="description">` (checked on live Sections page). Caveat: that page is hidden/noindex;
  confirm on a public page.
- ReadMe's own docs: 0 of 150 pages render a keywords meta tag.
- `agentSearch` (ReadMe's agent search endpoint, e.g.
  `https://docs.readme.com/main/agentSearch?query=term1%20term2`) is not enabled for us:
  `docs.sensible.so/agentSearch`, `/docs/agentSearch`, `/main/agentSearch` all 404. Our `.md` pages
  expose only `agentTools.projectIndex`, no `projectSearch`.

## Next steps

- [x] Draft synonym list for all 20 pages (`keywords-draft.md`)
- [x] Add "best 2–3 phrases per page" column to draft (keywords column kept)
- [ ] User reviews draft
- [x] (see `research-keywords-evidence.md`) Give user evidence and reasoning for the claim "Google has ignored the keywords meta tag for
      ranking since 2009, and Bing gives it little or no weight": primary sources (Google Search
      Central 2009 post / Matt Cutts video, Google's current meta-tags documentation, Bing statements
      by Duane Forrester ~2014 re: keywords as spam signal, Bing Webmaster Guidelines), dates, and
      what's still uncertain (e.g., current Bing behavior, LLM crawlers)
- [x] (see `research-keywords-evidence.md`) Investigate whether AI agents/crawlers (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot,
      Claude-User, PerplexityBot, Google-Extended / AI Overviews, Bing/Copilot) and agent fetch tools
      use `<meta name="keywords">` or ReadMe's `metadata.keywords`, with evidence and reasoning
- [x] (see `competitors/`, incl. `summary.md`) Competitor top-20 analysis, one file per competitor in `competitors/` (Parseur, Docparser,
      Nanonets, Docsumo, Ocrolus): title, meta description, meta keywords, target phrases,
      closest Sensible page, borrowable phrases
- [ ] Decide whether to add confidence, human review, preprocessors, webhook tutorial, library
      quickstart to the 20 pages (competitors target these topics)
- [x] Password-protected PDFs: not supported per user (2026-10-19); phrase dropped
- [ ] Evaluate rewriting our most relevant topics for SEO/GEO in the first ~150 words and in
      descriptions (excerpts, which feed `metadata.description` and `llms.txt`). Model to study
      (NOT a competitor): https://docs.payabli.com/llms.txt. User's view: Payabli shows strong
      discipline around (1) highly relevant first ~150 words on each page and (2) good per-page
      descriptions in llms.txt. Observed 2026-10-19: llms.txt opens with a one-paragraph product
      summary, a "Documentation sections" list, and a "Choose your path" section grouped by
      audience, with short task-focused link descriptions (e.g. "Developer quickstart — Make your
      first API call"); ~260 links. They also have a top-level "Cookbooks" section ("Short, focused
      API recipes for common tasks"), which is relevant to the 'cookbook' keyword idea for the
      config library page.
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
- [ ] Ask ReadMe support: (a) does site search / agentSearch / docs MCP index `metadata.keywords`?
      (b) how do we enable `agentSearch` / `projectSearch`?
- [ ] Keyword vs. keyphrase test on live docs (needs merge to v0 to publish):
  - Pick 2 public pages. Page A gets a unique single-token keyword (e.g. `zqxsynonymtest`);
    page B gets a unique two-word keyword phrase made of individually-unique tokens
    (e.g. `zqxalpha zqxbeta`).
  - Control: add a unique token to the *body* text of a third page (or page A) so you can tell
    "keywords aren't indexed" apart from "index hasn't refreshed yet."
  - Check: (1) does a `<meta name="keywords">` tag render on a public page? (2) ReadMe site search
    box and `GET https://api.readme.com/v2/search` for each token, and for `zqxalpha zqxbeta`
    vs. `zqxbeta zqxalpha` vs. `zqxalpha` alone (phrase vs. token matching), (3) docs MCP search
    and `agentSearch` if enabled.
  - If testing via MCP/agent search, wait for the index to update: re-query the body-text control
    token until it's found before trusting a negative result for the keyword tokens. Record how
    long the refresh took.
  - Remove all test tokens afterward.
- [ ] Decide which synonyms also go into excerpt/title/body (the part that affects Google/LLMs)
- [ ] Apply `metadata.keywords` to frontmatter
- [ ] Optional: before/after `mcp-search-eval` on a handful of pages
- [ ] PR referencing #722
