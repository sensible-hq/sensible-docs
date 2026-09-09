# Page Briefs

One brief per doc page. Briefs are **persistent** — they span releases and accumulate context over time. A brief is never thrown away when a page is updated; it's revised.

**Naming:** `<page-slug>.md` where slug = the doc filename without extension (e.g., `region.md` for `docs/Senseml reference/layout-based-methods/region.md`). Slugs are unique across the docs tree.

Briefs are about the **reader**, not the feature. They capture who lands on a page, how, what vocabulary they bring, and what questions they expect answered. Feature details belong in the doc itself; reader context belongs in the brief.

**When Claude uses a brief:**
- **Updating an existing page:** read the brief before writing anything. It shapes phrasing, depth, and what to include or skip. If the PR scope changes who reads the page or why, update the brief too.
- **Creating a new page:** draft the brief first. The brief determines structure, depth, and what to include or exclude before a word of the page is written.

**Claude should say in transcripts and PR comments** when the brief shaped a decision — e.g., "per the brief, readers arrive from the admin console and already have an account set up, so I skipped the onboarding preamble" or "brief says this belongs on X page, not here."

## How briefs get created

Claude drafts them. You review and edit. The brief is committed alongside (or before) the doc change in the PR — it's a first-class artifact, not a scratch file.

## Sources Claude draws on when drafting a brief

- The engine PR body and diff
- GitHub issues in sensible-hq/sensible and sensible-hq/sensible-docs (searched by feature name)
- Existing page content (what's already there implies what the page is for)
- Adjacent pages in the same category (what the page is *not* for)
