# Checklist — update-skill

Session name: update-skill  
Session ID: (run `claude` and check session list to get ID if resuming)

---

- [x] Make docs-from-PR skills more deterministic
  - [x] `update-docs-from-pr`: separate style guide loading into its own numbered gate step (Step 3); add `writing-rules.md`, `glossary.md`; renumber downstream steps
  - [x] `update-existing-doc`: add `writing-rules.md`, `glossary.md`; add missing vale check step (Step 5); add `mcp__vale__check_file` to allowed-tools
  - [x] `create-new-doc`: add `writing-rules.md`, `glossary.md`, `editorial-preferences.md`; add missing vale check step (Step 5); add `mcp__vale__check_file` to allowed-tools
  - [x] All three: add `Bash(git worktree:*)` to allowed-tools

- [ ] Break categorization logic out of the changelog skill into a standalone `categorize-pr` skill
  - Categorization rules live in `.claude/skills/changelog/references/categorization-rules.md`
  - Current usage is in `fetch-release-prs.md` Step 3 (annotation step)
  - New skill: takes a PR number + repo, returns `document / investigate / skip` with reason
  - Update `fetch-release-prs.md` to call the new skill instead of inlining the rules

- [ ] Build `scan-for-docs-needed` skill/automation
  - Trigger: scan `sensible-hq/sensible` for merged PRs that need docs
  - Signal 1: PR has `docs_needed` label
  - Signal 2: PR is categorized as `document` by the `categorize-pr` skill
  - Needs a cursor to track last-scanned PR so it doesn't reprocess
  - Output: list of PR numbers that need docs work

- [ ] Wire auto-scanner to docs drafting — **GH Actions based, not locally dependent**
  - Trigger options (both use GH Actions):
    - **Label trigger**: action fires when `docs_needed` label is applied to a PR in sensible-hq/sensible
    - **Scheduled scan**: cron action runs on a schedule, queries sensible-hq/sensible for recently merged PRs, runs categorization, drafts for any `document` results
  - **OPEN: How does Claude get invoked from the action?**
    - Claude API directly in the action (using Anthropic SDK) — possible but loses the full Claude Code skill environment (vale MCP, file access, etc.)
    - Claude Code CLI in the action — possible if runner has Claude Code installed and ANTHROPIC_API_KEY secret
    - Hybrid: action detects the PR and opens a GitHub issue in sensible-docs as a work queue; you (or another action) picks it up and runs the skill locally
  - **OPEN: How does the action open the docs PR?** It needs write access to sensible-hq/sensible-docs (separate repo — needs cross-repo token or a bot account)

- [ ] Add user brief as the first step in all docs-drafting skills
  - Brief is per-page, persists across releases — not per-PR
  - **OPEN: Where to store briefs?** Options:
    - `.claude/briefs/<page-slug>.md` (central, easy to grep)
    - `docs/.../briefs/<slug>.md` (co-located with the page)
  - **OPEN: Approval gate or in-PR?**
    - Gate: skill drafts brief → pauses for human approval → then drafts doc
    - In-PR: brief committed alongside the doc, reviewed in GitHub
  - **OPEN: What sources to pull from when drafting a brief?**
    - PR body/diff (always available)
    - GitHub issues in sensible-hq/sensible or sensible-hq/sensible-docs (search by feature name)
    - Existing page content (if updating)
    - Slack support channels / #questions?
  - Brief template to define (from the writer's description):
    - Page type (reference, guide, tutorial, concept)
    - Target reader: what do they know, how did they arrive, what vocabulary they use
    - What questions the reader is trying to answer
    - What information belongs on this page
    - What does NOT belong (belongs on a different page)
    - Sources consulted
  - Skills to update once design is settled:
    - `update-docs-from-pr`: Step 1 = find existing brief OR draft new one; subsequent steps reference it
    - `update-existing-doc`: Step 1 = read existing brief (or draft if missing); update brief if feature scope has changed
    - `create-new-doc`: Step 1 = draft brief for the new page
  - CLAUDE.md should reference the brief store location so agents always know to look there
