# Checklist: doc-test-skill

Claude Code session name: doc-detective
Claude Code session ID: 720fe7cf-48da-4332-8c4b-866ca3fa807d
Branch: doc-test-skill · started 2026-10-13 from /home/franc/GitHub/sensible-docs
Resume: `cd /home/franc/GitHub/sensible-docs && claude --resume 720fe7cf-48da-4332-8c4b-866ca3fa807d`

Goal: a skill that adds tests for new doc claims (with judgment), called by the doc-writing skills. Concept: `design/docs-test-skill/CONCEPT.md`.

Depends on: PR #737 (docs-test tooling), PR #744 (API contract tests and design).

- [x] Research Doc Detective's best practices (docs + agent-tools) and fold into the concept
- [x] Draft the concept: triage rubric, per-surface tests (UI, code, SenseML reference incl. parameter tables, API), skill hooks
- [ ] User review of the concept and open questions
- [x] Parameter tables: decided no per-row markup and no spec files; schema checks need no markup, behavioral checks get one marker above the table (2026-10-14)
- [x] Prototype `scripts/param-tables/check_param_tables.py` + 18 offline tests; `row.md` passes; full run found 6 docs problems on 5 pages (signature, text-table, query-group, add-computed-fields, get-file-metadata), 17 gap warnings untriaged
- [ ] Write `.claude/skills/add-doc-tests/SKILL.md`
- [ ] Add the hook step to create-new-doc, update-existing-doc, update-docs-from-pr, create-concept-doc, create-docs-example, api-spec (optional: blog-how-to-parse-x)
- [ ] Check json5-commenter and revise-doc-style preserve test markup
- [ ] Try agent-tools' LSP server; copy its post-edit "tests may need updating" hook
