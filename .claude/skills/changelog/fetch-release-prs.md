# Subskill: Fetch Release PRs

Maintains a cursor, fetches new release notes from #engineering, annotates each PR with a disposition, and pushes the result to a hidden `prs-<month>-<year>` draft on readme.io.

**Cursor file:** `.claude/skills/changelog/release-notes-cursor.yaml` (in sensible-docs repo)
**Publish script:** `.claude/skills/changelog/scripts/publish_changelog.py`

---

## Step 1 — Read and show the cursor

Read `release-notes-cursor.yaml`. If the file is missing, stop and tell the user.

Print:
```
Cursor state:
  Last fetch:              <last_fetched>
  Last message:            <latest_message_date_cursor> (ts: <last_message_ts>)
  Last changelog through:  <last_changelog_through>
  History:                 <N> changelogs archived
```

Ask: "Does this look right, or do you want to adjust the start point before I fetch?"

---

## Step 2 — Fetch new release notes from #engineering

Call `mcp__claude_ai_Slack__slack_search_public_and_private` with:
- `query`: `release notes in:engineering after:<latest_message_date_cursor>`
- `sort`: `timestamp`
- `sort_dir`: `asc`
- `include_bots`: `true`
- `limit`: 20

If 0 results: tell the user nothing is new since `<latest_message_date_cursor>` and stop.

Print each result with its date and bullet items so the user can see what came in before annotating.

---

## Step 3 — Annotate each PR with a disposition

Read `references/categorization-rules.md` before annotating. Then for each bullet item, add an inline comment:

```
- <item text> (#NNNN) <!-- document / investigate / skip: <brief reason> -->
```

Do not reorder items or change any other formatting.

---

## Step 4 — Push to readme.io

Determine the title from the current month: `prs-<month>-<year>` (e.g., `prs-july-2026`).

Format the body with a dispositions summary at the top, followed by the annotated release notes:

```
## Disposition summary (fetched <YYYY-MM-DD>)

**document** (N): #XXXX (brief label), #XXXX (brief label)
**investigate** (N): #XXXX (brief label), #XXXX (brief label)
**skip** (N): #XXXX, #XXXX, ...

---

## Release notes fetched <YYYY-MM-DD> (cursor was <latest_message_date_cursor>)

### <date>
- item <!-- comment -->
...
```

Check whether the slug already exists by attempting to fetch it. If it exists, append (`--append`). If not, create it (no flag).

```bash
python /home/franc/GitHub/sensible-docs/.claude/skills/changelog/scripts/publish_changelog.py "prs-<month>-<year>" [--append] < /tmp/prs_body.txt
```

Print the hidden draft URL on success.

---

## Step 5 — Update the cursor

Update `release-notes-cursor.yaml`:
- `last_fetched`: today's date
- `last_message_ts`: `message_ts` of the most recent message fetched
- `latest_message_date_cursor`: human-readable date of that message

Do NOT touch `last_changelog_through` or `saved_for_later` — those are only updated during publishing (see `checklist.md`).

---

## Step 6 — Confirm

Print:
```
✓ Fetched <N> release note batch(es) (<date range>)
✓ Draft: https://docs.sensible.so/update/changelog/prs-<month>-<year>
✓ Cursor updated to <latest_message_date_cursor> (ts: <last_message_ts>)

Next fetch will start after: <latest_message_date_cursor>
```
