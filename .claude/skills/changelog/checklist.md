# Changelog Workflow Checklist

---

## Recurring: fetch new release notes → prs

This flow runs whenever Frances wants to pull the latest release notes and queue them for review. It maintains a cursor so nothing slips through the cracks.

### Step 1 — Read the cursor

Read `.claude/skills/changelog/release-notes-cursor.yaml`. If it doesn't exist, create it with defaults (see schema below).

Print to the user:
```
Last fetch:              <last_fetched>
Last message:            <last_message_date> (ts: <last_message_ts>)
Last changelog through:  <last_changelog_through>
History:                 <N> changelogs archived
```

Ask: "Does this look right, or do you want to adjust the start point?"

---

### Step 2 — Fetch new release notes from #engineering

Search Slack for release notes posted after the cursor:

```
query: "release notes in:engineering"
after: <last_message_ts converted to YYYY-MM-DD>
sort: timestamp asc
include_bots: true
```

If 0 results: tell the user and stop.

If results: print each one with date and bullet items so the user can see what came in.

---

### Step 3 — Append raw notes to prs on readme.io

Determine the entry title from the current month: `prs-<month>-<year>` (e.g., `prs-july-2026`).

Format the content to append:

```
## Release notes fetched <YYYY-MM-DD> (cursor was <prior cursor date>)

### <date of each release note batch>
- item
- item
...
```

Check if the prs entry already exists:
```bash
python /home/franc/GitHub/sensible-docs/.claude/skills/changelog/scripts/publish_changelog.py "prs-<month>-<year>" --append < /tmp/prs_body.txt
```

If it doesn't exist yet, create it (omit `--append`). The script auto-avoids slug conflicts.

Print the hidden draft URL so Frances can review it in the readme.io dash.

---

### Step 4 — Update the cursor

Update `.claude/skills/changelog/release-notes-cursor.yaml` with:
- `last_fetched`: today's date
- `last_message_ts`: the `message_ts` of the most recent release notes message fetched
- `last_message_date`: human-readable date of that message (for sanity checking)

Do NOT update `last_changelog_through` — that's only updated when a changelog is actually published (see Publishing flow below).

---

### Step 5 — Confirm to user

Print:
```
✓ Fetched <N> release note batches (<date range>)
✓ Appended to prs: https://docs.sensible.so/update/changelog/prs-<month>-<year>
✓ Cursor updated to <last_message_date> (ts: <last_message_ts>)

Next time, fetch will start after: <last_message_date>
```

---

## Cursor file schema

Location: `.claude/skills/changelog/release-notes-cursor.yaml`

```yaml
# Tracks state for the release notes → changelog workflow.
# last_message_ts: Slack message_ts of the most recent #engineering
#   release notes post fetched. Next fetch starts after this.
# last_changelog_through: date through which items have been PUBLISHED
#   in a changelog. May lag behind last_fetched if items are pending review.
# changelog_history: append-only archive — one entry per published changelog,
#   recording which release note date range it covered.

last_fetched: "2026-07-08"
last_message_ts: "1782909583.512839"
last_message_date: "2026-07-01"
last_changelog_through: "2026-06-11"

changelog_history:
  - changelog: "june-2026"
    release_notes_from: "2026-05-11"
    release_notes_through: "2026-06-09"
    published: "2026-06-11"
    url: "https://docs.sensible.so/changelog/june-2026"
```

---

## Publishing flow (when drafting the monthly changelog)

1. Read the cursor — note `last_changelog_through` and `saved_for_later`
2. Pull any `saved_for_later` items into the draft as candidates
3. Pull the prs entry from readme.io for the current month as additional raw material
4. Follow the main changelog skill steps (SKILL.md) to draft and publish
5. After Frances approves and publishes, update the cursor:
   - Set `last_changelog_through` to today
   - Append a new entry to `changelog_history` with the range of release notes covered, the publish date, and the live URL
