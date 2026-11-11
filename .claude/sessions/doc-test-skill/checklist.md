# Checklist: doc-test-skill

Claude Code session name: doc-detective
Claude Code session ID: 720fe7cf-48da-4332-8c4b-866ca3fa807d
Branch: doc-test-skill · started 2026-10-13 from /home/franc/GitHub/sensible-docs
Resume: `cd /home/franc/GitHub/sensible-docs && claude --resume 720fe7cf-48da-4332-8c4b-866ca3fa807d`

Also worked on by session `xlsb` (`1e71441a-3c84-48a0-baa5-c36aac379bbb`), 2026-11-10: wrote the skill's first version.
Handover: read `.claude/sessions/doc-test-skill/decisions.md` first (where things stand, progress log, decisions, open questions).

Goal: a skill that adds tests for new doc claims (with judgment), called by the doc-writing skills. Concept: `design/docs-test-skill/CONCEPT.md`.

Depends on: PR #737 (docs-test tooling, **merged**), PR #741 (classification markup, saved reports, fixture spreadsheets; **open**, merge first), PR #744 (API contract tests and design; **open**).

- [x] Research Doc Detective's best practices (docs + agent-tools) and fold into the concept
- [x] Draft the concept: triage rubric, per-surface tests (UI, code, SenseML reference incl. parameter tables, API), skill hooks
- [ ] User review of the concept and open questions
- [x] Parameter tables: decided no per-row markup and no spec files; schema checks need no markup, behavioral checks get one marker above the table (2026-10-14)
- [x] Prototype `scripts/param-tables/check_param_tables.py` + 18 offline tests; `row.md` passes; full run found 6 docs problems on 5 pages (signature, text-table, query-group, add-computed-fields, get-file-metadata), 17 gap warnings untriaged
- [ ] Design requirement (2026-10-14): every custom test format stays analogous to Doc Detective, so switching to Doc Detective later is easy, and each has a migration guide written as part of its design, not after
  - [ ] SenseML code tests (#737: `<!-- code test -->`, `<!-- example document|config|output -->`): match Doc Detective's inline shape (single-line `<!-- … {json} -->` statements, `testId`, `description`, `<!-- … end -->`), map each check to its nearest Doc Detective action (`httpRequest` with `response.body`/`required`, `runCode`), list what has no equivalent (the `...` comparison, LLM judge, envelopes) and how each would run via `runShell`
  - [ ] API contract tests (#744): same exercise against Doc Detective's `httpRequest` + `openApi` (#744 already has `design/doc-detective-contract-tests.md`; check it covers migration)
  - [ ] Parameter-table schema checks (#749: `scripts/param-tables/`): document how they'd run under Doc Detective (`runShell` per page or a custom markup pattern), and keep the planned `<!-- param tests {…} -->` marker in Doc Detective's statement shape
  - [ ] One migration guide per format, in `design/`, kept up to date when the format changes (the skill's "change a test format" step should require it)
- [ ] Licensing rule (2026-10-14, compliance): avoid AGPL. Doc Detective only as an unmodified, separately run CLI (never modify, vendor, redistribute or host; autoUpdate and telemetry off). No agent-tools or its hosted MCP. The skill must check the license of any tool it proposes. See CONCEPT.md "Licensing rule"
- [x] Write `.claude/skills/add-doc-tests/SKILL.md` (first version, 2026-11-10, from the xlsb session). Its classification markup and `DOC_TESTS_SAVE_REPORT` come from PR #741; merge #741 first
  - [ ] Frances reviews the skill (and the concept's open questions)
- [ ] Add the hook step to create-new-doc, update-existing-doc, update-docs-from-pr, create-concept-doc, create-docs-example, api-spec (optional: blog-how-to-parse-x)
- [ ] Check json5-commenter and revise-doc-style preserve test markup
- [ ] Re-implement (don't install: agent-tools is AGPL) a post-edit "tests may need updating" hook

## Next steps (2026-11-11)

- [ ] Frances: review the concept's open questions and the skill (decisions.md lists both)
- [ ] Merge #741 (the skill's classification markup and saved reports come from it)
- [ ] Merge `v0` into this branch (67 commits behind on 2026-11-11; keep this branch's session pointer files on conflict)
- [ ] Revise the skill from Frances's review
- [ ] Add the hook step to the doc-writing skills (item above)
- [ ] Skill: add a step to list new tested pages in `scripts/doc-detective/test-pages.json` with a priority (1 weekly, 2 monthly, 3 on demand; PR #803)
- [ ] Update the PR description and mark #749 ready
