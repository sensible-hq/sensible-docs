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

## Next steps

- [ ] Draft synonym list for all 20 pages; user reviews
- [ ] Decide which synonyms also go into excerpt/title/body (the part that affects Google/LLMs)
- [ ] Apply `metadata.keywords` to frontmatter
- [ ] Optional: before/after `mcp-search-eval` on a handful of pages
- [ ] PR referencing #722
