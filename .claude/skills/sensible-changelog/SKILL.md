---
name: sensible-changelog
description: Generates and publishes a monthly Sensible product changelog. Invoke whenever the user wants to write, draft, or publish a monthly changelog, or mentions writing up a release summary given a list of PRs. The user will provide PR numbers (from the frontend or backend GitHub repo, or both) and optionally a list of doc topic URLs. The skill structures the input, fetches PR context, drafts the changelog in Sensible's house style, gets user approval, then publishes as a hidden draft to readme.com.
---

# Sensible Changelog Skill

## Repos

- **Backend**: `sensible-hq/sensible`
- **Frontend**: `sensible-hq/sensible-app`
- **Docs**: `sensible-hq/sensible-docs`

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

For each confirmed PR, fetch the full body:
```bash
gh pr view <number> --repo <org/repo> --json title,body,mergedAt,labels
```

From the body, extract:
- What changed (the "what")
- Why it matters or how users use it (the "so what")
- Any linked doc pages or feature names

Ignore boilerplate (checklists, "how to test", internal notes). Focus on user-facing description.

**Non-user-facing PRs**: If a PR is clearly infra-only, a refactor, a test change, or has no user-visible effect, skip it from the changelog. Note it in the summary you showed in Step 1 (under "Skipping") so the user knows it was considered and excluded intentionally.

---

## Step 3: Source feature descriptions

For each changelog entry, use the best available source. Priority order:

1. **Pasted doc content** — if the user pasted doc text directly, use it as-is. It's already user-facing.
2. **Docs PR** — fetch the PR body and diff for the most accurate user-facing description:
   ```bash
   gh pr view <number> --repo sensible-hq/sensible-docs --json title,body,files
   gh pr diff <number> --repo sensible-hq/sensible-docs
   ```
   The diff shows exactly what was added to the docs — use the added lines (`+`) as the primary source.
3. **Doc URL → local file** — derive the path from the slug directly:
   ```
   https://docs.sensible.so/docs/remove-lines → slug = "remove-lines"
   Check: /home/franceselliott/GitHub/sensible-docs/docs/remove-lines.md
          /home/franceselliott/GitHub/sensible-docs/reference/remove-lines.md
   ```
4. **Code PR body** — use the user-facing description from the backend/frontend PR.
5. **MCP fallback** — `mcp__sensible-docs__search` with the feature name. Least reliable; use only if nothing else is available.

The goal is accurate, user-facing language — not copying the doc verbatim or paraphrasing internal PR descriptions.

---

## Step 3b: Search past changelogs for similar entries

Do this for any entry where:
- The user explicitly flagged it as similar to a past change, **or**
- The feature is clearly a repeat pattern (e.g., another LLM model version update, another JsonLogic operator, another preprocessor parameter)

Past changelogs are saved locally at:
```
references/changelogs/*.md
```

Search by grepping for relevant terms:
```bash
grep -ril "haiku\|model version\|llm model" \
  /home/franceselliott/GitHub/sensible-docs/.claude/skills/sensible-changelog/references/changelogs/
```

Then read the matching file(s) and find the specific section. Use that past entry's wording as a template — same sentence structure, same level of detail, same way of introducing the change. Update the specifics (version names, feature names, parameters) but preserve the established phrasing pattern.

When you do this, note it in the draft with a brief inline comment to yourself (which you'll remove before showing the user), e.g.: `<!-- modeled on january-2026: LLM model version updates -->`. This helps you stay consistent within a single draft when multiple entries draw on past wording.

If no good past match exists, draft from scratch using the style guides.

---

## Step 4: Draft the changelog

Read both style files before drafting:
- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/changelog-style-guide.md` — changelog structure, section types, doc link format, examples
- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/writing-rules.md` — cross-cutting prose rules (em dashes, passive voice, explicit subjects, terminology, gerunds)

Key reminders:
- Intro paragraph: third person ("Sensible released…"), no doc links
- Section headings: `## New feature:`, `## Improvement:`, `## UX improvement:`, `## UX improvements:`, `## Deprecation:` — use exactly these strings
- Section bodies: second person, 2–5 sentences, prose over bullets
- Doc links: `[text](doc:slug)` format
- Lead with the most significant features

---

## Step 5: Review with user

Print the full draft. Ask:
> "Does this look right? Any edits before I publish?"

Incorporate feedback. Do not publish until the user explicitly approves.

---

## Step 6: Publish as hidden draft

Once approved, write the body to a temp file and run `scripts/publish_changelog.py`:

```bash
cat > /tmp/changelog_body.txt << 'CHANGELOG_EOF'
<paste full body here>
CHANGELOG_EOF

python /home/franceselliott/.claude/skills/sensible-changelog/scripts/publish_changelog.py "March 2026" < /tmp/changelog_body.txt
```

The script handles auth, the POST request, and prints the draft URL on success or the full error on failure.
