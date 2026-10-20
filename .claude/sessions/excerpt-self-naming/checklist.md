# Excerpt self-naming cleanup

Claude Code session name: seo
Claude Code session ID: c14f96d2-faef-4dbe-8951-0d7f13df161c
Branch: excerpt-self-naming (worktree: ~/GitHub/sensible-docs-excerpt-self-naming)
Related: PR #758 (seo-keywords), issue #722

Rule (from PR #758 review): an excerpt never names its own method, object, preprocessor, or setting;
the slug already does. Cut the superfluous wording only ("Learn how to use the Regex method to",
"Linearize preprocessor breaks" -> "Breaks"); fix only capitalization and basic grammar.

- [x] Scope: SenseML element pages under `docs/Senseml reference/` (methods, computed field methods,
      preprocessors, Cell Rows field type, config and document type settings, Method object) NOT
      covered by PR #758's 42 pages. Skipped: hidden pages, concept pages (topic wording, not
      self-naming), category index pages, Label (near-deprecated; doesn't self-name).
- [x] Edit 39 excerpts, plus matching `metadata.description` (text-level edit; no other frontmatter
      keys changed; verified with YAML round-trip and `sync_description.py --dry-run`)
- [ ] Open PR
- [ ] User review
