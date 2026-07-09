---
name: changelog
description: Generates and publishes a monthly Sensible product changelog. Invoke whenever the user wants to write, draft, or publish a monthly changelog, or mentions writing up a release summary given a list of PRs. The user will provide PR numbers (from the frontend or backend GitHub repo, or both) and optionally a list of doc topic URLs. The skill structures the input, fetches PR context, drafts the changelog in Sensible's house style, gets user approval, then publishes as a hidden draft to readme.com.
---

# Sensible Changelog Skill

## Repos

- **Backend**: `sensible-hq/sensible`
- **Frontend**: `sensible-hq/sensible-app`
- **Docs**: `sensible-hq/sensible-docs`

---

## Subskill: Fetch new release PRs

Before drafting a changelog, run the fetch subskill to pull any new release notes from Slack, annotate them, and queue them in the readme.io draft. See **`fetch-release-prs.md`** for the full flow. This is also callable on its own whenever the user wants to sync the latest PRs without drafting a changelog.

---

## Step 1: Parse input, fetch PR titles, confirm with user

The user will paste an unstructured blob. It may contain any mix of:
- PR numbers from the backend or frontend repo (possibly labeled "frontend"/"backend")
- PR numbers from the docs repo (`sensible-docs`) — labeled "docs" or inferrable from context
- Doc topic URLs (`https://docs.sensible.so/...`)
- Pasted doc content (raw markdown or prose the user has copied directly)

**1a. Parse** out each of these. For PR numbers:
- If labeled by repo, use that. If unlabeled, try fetching from all three repos in parallel and use whichever returns a valid result. If still ambiguous, ask.

For pasted doc content: treat it as the user-facing description for the associated feature — note it in the summary as "pasted content" so the user can see it was captured.

**Similarity hints**: If the user says something like "this is similar to a past change" or "find the old wording for X", note which entries need a past-changelog search and carry that forward to Step 3b.

**1b. Fetch PR titles immediately** — run in parallel so the confirmation summary is useful:
```bash
gh pr view <number> --repo <org/repo> --json number,title,mergedAt
```

**1c. Present a structured summary** for the user to review before any further work:

```
## Input summary — please confirm before I continue

**PRs:**
- [#1234](https://github.com/sensible-hq/sensible/pull/1234) — backend — "Add Remove Lines preprocessor"
- [#567](https://github.com/sensible-hq/sensible-app/pull/567) — frontend — "Batch document upload UI"
- [#89](https://github.com/sensible-hq/sensible-docs/pull/89) — docs — "Add remove-lines reference page"

**Doc topics:**
- https://docs.sensible.so/docs/remove-lines
- Pasted content: "The Remove Lines preprocessor removes matched text from all pages…"

**Skipping (no user-facing changes):**
- [#890](https://github.com/sensible-hq/sensible/pull/890) — "Refactor auth middleware" — infra only

Proceed?
```

Wait for confirmation before continuing.

---

## Step 2: Fetch full PR context

Fetch all confirmed PR bodies in parallel — this is the only batched step:
```bash
gh pr view <number> --repo <org/repo> --json title,body,mergedAt,labels
```

From each body, extract:
- What changed (the "what")
- Why it matters or how users use it (the "so what")
- Any linked doc pages or feature names

Ignore boilerplate (checklists, "how to test", internal notes). Focus on user-facing description.

**Non-user-facing PRs**: If a PR is clearly infra-only, a refactor, a test change, or has no user-visible effect, skip it. Note it under "Skipping" in the Step 1 summary.

---

## Steps 3–4: Per-entry loop (do not batch)

**Complete all sub-steps for one PR before starting the next.** Batching these steps is the most common source of skipped research and missing doc links.

Read these three files once before starting the loop — they apply to every entry:
- `/home/franc/GitHub/sensible-docs/.claude/style-guide/changelog-style-guide.md`
- `/home/franc/GitHub/sensible-docs/.claude/style-guide/writing-rules.md`
- `/home/franc/GitHub/sensible-docs/.claude/preferences/editorial-preferences.md`

---

### 3a. Source the description

Use the best available source in priority order:

1. **Pasted doc content** — if the user pasted doc text directly, use it as-is.
2. **Docs PR** — fetch body and diff:
   ```bash
   gh pr view <number> --repo sensible-hq/sensible-docs --json title,body,files
   gh pr diff <number> --repo sensible-hq/sensible-docs
   ```
   Use added lines (`+`) as the primary source.
3. **Doc URL → local file** — derive the path from the slug:
   ```
   https://docs.sensible.so/docs/remove-lines → slug = "remove-lines"
   Check: /home/franc/GitHub/sensible-docs/docs/remove-lines.md
          /home/franc/GitHub/sensible-docs/reference/remove-lines.md
   ```
4. **Code PR body** — use the user-facing description from the backend/frontend PR.
5. **MCP fallback** — `mcp__sensible-docs__search` with the feature name. Least reliable.

---

### 3b. Search past changelogs for similar entries

Do this if:
- The user flagged it as similar to a past change, **or**
- The feature is a repeat pattern (another LLM model update, another JsonLogic operator, another preprocessor parameter, another method configurability improvement)

```bash
grep -ril "<relevant terms>" \
  /home/franc/GitHub/sensible-docs/.claude/skills/changelog/references/changelogs/
```

Read the matching section. Model the new entry on the same sentence structure, level of detail, and phrasing — update only the specifics. Record the source for the review step (`https://docs.sensible.so/changelog/<slug>`).

If no past match exists, draft from scratch.

---

### 3c. Draft the entry

Use the **entry template** in `.claude/skills/changelog/structural-check.md`. Draft directly into the template so the doc link slot and heading format are present from the start.

Key reminders:
- Heading: `## New feature:`, `## Improvement:`, `## UX improvement:`, `## UX improvements:`, `## Deprecation:`
- Body: second person, 2–5 sentences, prose over bullets
- Doc link: `[text](doc:slug)` — every entry needs one; use `<!-- DOC LINK NEEDED -->` if no public page exists
- Parameter names: Title Case in prose — "the Ignore Form Data parameter", not `` `ignoreFormData` ``

---

### 3d. Per-entry checklist (fill out before moving to the next PR)

```
PR #NNNN — [title]
  [ ] Source: [which source was used and why]
  [ ] Past changelog: [searched / not applicable — if applicable: modeled on <month-year>]
  [ ] Entry drafted using template
  [ ] Heading type confirmed: [New feature / Improvement / UX improvement / Deprecation]
  [ ] Doc link: [slug used / DOC LINK NEEDED comment added]
```

Do not move to the next PR until all five boxes are filled.

---

### After the loop: assemble and order

Once all entries are drafted, assemble them in order: New features first, then Improvements, then UX improvements, then Deprecations. Within each group, lead with the most significant. Write the intro paragraph last (third person, no doc links).

---

## Step 5: Style check, then review with user

Run the **`docs-checker`** skill (`.claude/skills/docs-checker/SKILL.md`) on the full draft. Fix all errors and warnings it returns. Use judgment on suggestions — Google style rules often don't apply to changelogs.

Then run the **`structural-check`** subskill (`.claude/skills/changelog/structural-check.md`) to verify doc links and image format.

After fixing, print the full draft. If any entries were modeled on past changelog entries, print a reference list:

```
**Based on:**
- "Filter past extractions" (August 2023): https://docs.sensible.so/changelog/august-2023
```

Then ask:
> "Does this look right? Any edits before I publish?"

Incorporate feedback. Do not publish until the user explicitly approves.

---

## Step 6: Publish as hidden draft

Once approved, write the body to a temp file and run `scripts/publish_changelog.py`:

```bash
cat > /tmp/changelog_body.txt << 'CHANGELOG_EOF'
<paste full body here>
CHANGELOG_EOF

python /home/franc/GitHub/sensible-docs/.claude/skills/changelog/scripts/publish_changelog.py "March 2026" < /tmp/changelog_body.txt
```

Flags:
- (no flag) — create new draft (auto-avoids slug conflicts)
- `--update` — replace the entire body of an existing draft
- `--append` — append content to an existing draft

The script handles auth, the POST/PUT request, and prints the draft URL on success or the full error on failure.

### Updating a single section without touching the rest

Use `scripts/update_section.py` when Frances has already edited the draft and you need to rewrite one section only:

```bash
cat << 'EOF' | python /home/franc/GitHub/sensible-docs/.claude/skills/changelog/scripts/update_section.py july-2026 "## Improvement: Advanced configurability"
## Improvement: Advanced configurability for the Region method

For the [Region](doc:region) method, you can now relax the criteria ...
EOF
```

The script matches the first heading that starts with the given prefix, replaces from that heading to the next `##` heading, and PUTs the full body back. All other sections are left exactly as they are.
