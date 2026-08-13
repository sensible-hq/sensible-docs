# PR 3412 — Verbosity levels 2 and 4 (per-field LLM duration)

**Branch:** `doc/pr-3412-verbosity-duration`  
**Worktree:** `~/GitHub/sensible-docs-llm-time`  
**Claude Code session ID:** 5dfab085-ad0c-41b5-8369-bf0d22a37505  
**Source PR:** [sensible-hq/sensible#3412](https://github.com/sensible-hq/sensible/pull/3412)

---

## Docs changes

- [x] Update `docs/Senseml reference/config-settings/verbosity.md`
  - [x] Fix property name `duration` → `durationMs` in levels 2 and 4 descriptions
  - [x] Remove TODO comment
  - [x] Add `## Verbosity level 1` heading to existing example
  - [x] Add `## Verbosity level 2` example (query-group + list, showing `durationMs` placement)
  - [x] Fix pre-existing vale errors (quotes, unit spacing)

---

## Testing

- [ ] Add test script to `scripts/test/` for verbosity 2 and 4
  - Create verbose configs: upload a SenseML config with `"verbosity": 2` and one with `"verbosity": 4` for an existing doc type (e.g., a query-group + list invoice config)
  - The upload step uses the [Create configuration](https://docs.sensible.so/reference/create-configuration) endpoint or the Sensible app
  - Verify `durationMs` appears in the extraction output for LLM-extracted fields
  - Verify it does NOT appear on layout-based fields
  - Verify query-group fields in the same batch share the same `durationMs` value
  - Verify list fields show `durationMs` at the top level of the list object (alongside `columns`)
  - Verify verbosity 4 shows both `durationMs` AND the full level 3 metadata (points, regions, OCR confidence)
