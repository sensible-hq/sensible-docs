# Config library link audit

**Goal:** Update all links to the Sensible configuration library across docs, blog posts, SDK repos, API reference, and the ReadMe changelog.

**Branch:** `config-lib`  
**Worktree:** `~/GitHub/sensible-docs-config-lib`

---

## !! Do first

- [ ] **Verify with Horacio: will the old GitHub repo links (`github.com/sensible-hq/sensible-configuration-library`) change?** Nothing else in this checklist can be completed without this answer.
- [ ] **Follow up with Matt on how to handle Webflow assets** — see [Slack thread](https://sensiblehq.slack.com/archives/C03EQ0AHHP0/p1784062509706119)

---

## Link treatment taxonomy

Before editing any link, classify it into one of three treatments:

| Treatment | When to apply | New destination |
|-----------|--------------|-----------------|
| **A — App flow** | Tutorials and prerequisites where the user is actively cloning a doc type into their account | `app.sensible.so` links (mostly as-is) |
| **B — Asset internalization** | Raw GitHub file links (`raw.githubusercontent.com`) that users download — PDFs, etc. | Copy asset to `sensible-docs/assets/pdfs/`, update link to new GitHub raw URL |
| **C — Discovery page** | "Learn more about the config library" context — general references not tied to an in-app action | `https://www.sensible.so/configuration-library` |

Note: `www.sensible.so/configuration-library` lets users browse and interact with supported doc types in a SenseML sandbox, but does **not** clone the doc type to their account. Use treatment A (not C) anywhere the user needs to actually add a doc type.

---

## Open questions before starting

- [ ] Does the `app.sensible.so/library` in-app URL change?
- [ ] Do `doc:library-quickstart` internal cross-reference slugs change (i.e., is the ReadMe page moving)?
- [ ] Are old historical changelog entries (e.g., October 2022) in scope, or only current/future content?

---

## Surface 1: `/docs` (this repo) — 25 matches across 10 published files

Search: `sensible-configuration-library` (exact string, from your 602-file scan).

### GitHub repo root links → Treatment C

| File | Link |
|------|------|
| `docs/document extraction/library-quickstart.md` | `https://github.com/sensible-hq/sensible-configuration-library` |
| `docs/integrations/quickbooks.md` | `https://github.com/sensible-hq/sensible-configuration-library` |
| `docs/welcome/author.md` | `https://github.com/sensible-hq/sensible-configuration-library/` |

- [ ] `docs/document extraction/library-quickstart.md`
- [ ] `docs/integrations/quickbooks.md`
- [ ] `docs/welcome/author.md`

### Deep links into specific GitHub template folders → Treatment A, B, or C depending on context

Review each link in context to assign treatment before editing.

| File | Link target |
|------|-------------|
| `docs/document type classification/classify.md` | `.../Financial%20Services/Bank%20Statements` |
| `docs/document type classification/classify.md` | `.../Tax%20Forms/1040s` |
| `docs/integrations/draft-make-integration.md` | `.../Tax%20Forms/1040s/refdocs` |
| `docs/integrations/zapier/zapier-getting-started.md` | `.../Tax%20Forms/1040s/refdocs` |
| `docs/integrations/zapier/zapier-tutorial-2.md` | `.../Tax%20Forms/1040s/refdocs` |

- [ ] `docs/document type classification/classify.md`
- [ ] `docs/integrations/draft-make-integration.md`
- [ ] `docs/integrations/zapier/zapier-getting-started.md`
- [ ] `docs/integrations/zapier/zapier-tutorial-2.md`

### Raw PDF links (`raw.githubusercontent.com/.../1040_2021_sample.pdf`)

Used as sample document download links in API tutorials. Each requires a human judgment call before updating the link:

1. **Evaluate the download flow** — decide whether keeping a direct `raw.githubusercontent.com` download link still makes sense, or whether users should be directed to a page on the Sensible website instead.
2. **Internalize if needed** — if the file should no longer live in the GitHub repo, move it to `sensible-docs/assets/pdfs/` so it becomes an internal dependency with a stable URL.

- [ ] `docs/api/api-tutorial/api-tutorial-async-1.md`
- [ ] `docs/api/api-tutorial/api-tutorial-async-2.md`
- [ ] `docs/api/api-tutorial/api-tutorial-sync.md`
- [ ] `docs/api/api-tutorial/api-tutorial-webhook.md`
- [ ] `docs/integrations/draft-make-integration.md`
- [ ] `docs/integrations/zapier/zapier-getting-started.md` (2 occurrences)
- [ ] `docs/integrations/zapier/zapier-tutorial-2.md`

### Also: `app.sensible.so/library` and `doc:library-quickstart` (separate search needed)

These patterns weren't in the `sensible-configuration-library` search. Audit separately:

- [ ] Run search for `app.sensible.so/librar` in `/docs`
- [ ] Run search for `doc:library-quickstart` in `/docs` — affects ~18 files; only change if the page slug moves

---

## Surface 2: `.claude/` internal files (this repo)

These files are internal skill prompts, not published docs. They fetch from the config library at runtime, so their URLs matter.

### Skills that fetch from the config library

| File | What it uses |
|------|-------------|
| `.claude/skills/blog-how-to-parse-x/SKILL.md` | `raw.../README.md`, `.../templates/[Category]/[Doc Type]/configurations`, raw config JSON |
| `.claude/skills/blog-short/SKILL.md` | `raw.../README.md` |
| `.claude/skills/integration-guide-generator/SKILL.md` | `.../templates/[Category]/[Doc Type]/configurations`, raw config JSON |

- [ ] `.claude/skills/blog-how-to-parse-x/SKILL.md`
- [ ] `.claude/skills/blog-short/SKILL.md`
- [ ] `.claude/skills/integration-guide-generator/SKILL.md`

### Style guide reference

| File | What it uses |
|------|-------------|
| `.claude/style-guide/config-library-supported-document-types.md` | Repo root + branch `v0` |

- [ ] `.claude/style-guide/config-library-supported-document-types.md`

---

## Surface 3: ReadMe changelog (via API)

Live changelog pages are in ReadMe; local copies in `.claude/skills/changelog/references/changelogs/` are a cache that may be stale.

Steps:
- [ ] Run `.claude/skills/changelog/scripts/download_changelogs.py` to refresh the local cache
- [ ] Grep the refreshed cache for `sensible-configuration-library`: `grep -rl "sensible-configuration-library" .claude/skills/changelog/references/changelogs/`
- [ ] Review each hit — note whether it's a hyperlink or prose-only mention, and whether it's in a historical entry
- [ ] Decide whether historical entries need updating (current known hit: `october-2022.md` line 18, hyperlink to GitHub repo + `app.sensible.so/library`)
- [ ] Update live pages via `mcp__readme__update-docs` where applicable
- [ ] Re-run the download script after edits to sync the local cache

---

## Surface 4: SDK repos (external)

SDK docs live in external GitHub repos — nothing from them is in `sensible-docs`.

- [ ] Fetch and search `https://github.com/sensible-hq/sensible-api-js` README for `sensible-configuration-library`
- [ ] Fetch and search `https://github.com/sensible-hq/sensible-api-py` README for `sensible-configuration-library`
- [ ] Note each hit (file, line, link type) and add to this checklist
- [ ] Open PRs in each SDK repo to update the links

---

## Surface 5: Webflow blog posts (external)

Blog posts are in Webflow CMS — not in this repo.

- [ ] Use the Webflow MCP to search blog post content for `sensible-configuration-library`
- [ ] Note each hit (post title/slug, field, link text) and add to this checklist
- [ ] Update affected posts via the Webflow MCP
