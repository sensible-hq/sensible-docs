# Style cleanup progress

Newest first.

## 2026-11-16: M0–M9 done, PR opened

### What exists now

| piece | where | check |
| ----- | ----- | ----- |
| Rule registry: 40 rules (23 deterministic, 12 judgment, 5 prose) | `style-rules/registry.yaml` | `check_registry.py`: 0 problems |
| 20 Sensible Vale rules (3 fixed, 15 new, 2 unchanged) | `.github/styles/Sensible/` | `test_rules.py`: 19 fixtures, 0 problems |
| 4 scripts | `scripts/style/` | 12 pytest tests pass |
| 12 judgment specs | `style-rules/judgment/` | validated by `check_registry.py`, including their source quotes |
| Write-time hook, before and after each edit | `.claude/hooks/vale_gate.py` | 6 hook tests; `vale-doctor.sh` all checks pass, including a pre-write denial |
| Guide and skill edits | `.claude/` | 31 markers link guide text to the registry |

### Corpus before and after (Vale, `docs/` + `reference/`, all levels)

Total: 1,651 → 1,653 alerts. 55 duplicate word-list alerts are gone; 63 new alerts are real problems the old rules couldn't see.

| check | before | after | note |
| ----- | -----: | ----: | ---- |
| Sensible.WordList | 60 | 5 | duplicates of Google.WordListCase removed |
| Sensible.ExcerptFiller | 0 | 23 | "Learn how to…" excerpts |
| Sensible.NoJSXImage | 0 | 13 | JSX images in docs pages |
| Sensible.ModelNames | 0 | 7 | all in `draft-llm-models.md` |
| Sensible.AgainstPhrasing | 5 | 4 | now limited to 6 words between verb and "against"; catches adjacent text |
| Sensible.Numbers | 0 | 4 | "90 percent" |
| Sensible.Terminology | 0 | 4 | "extraction templates", "prompt context" |
| Sensible.ParamNameCode | 0 | 2 | |
| Sensible.Filler | 0 | 2 | "In this guide" |
| Sensible.ImageURL | 0 | 2 | alt text other than "Click to enlarge" |
| Sensible.EmDash / Google.EmDash | 1 | 1 | rule swapped |
| Sensible.LinkArticle | 0 | 1 | |

### Backlog: existing violations in `docs/` (not fixed here; see D-004)

| check | hits | where |
| ----- | ---: | ----- |
| `//` comments in json fences | 56 | 19 files; most in `senseml-reference-introduction.md` (11), `jsonlogic.md` (12), `coverage.md` (5), `query-group.md` (5) |
| Excerpt over 150 characters (cap 160) | 27 | warnings only; none over the cap |
| `metadata.description` differs from `excerpt` | 1 | `docs/welcome/overview.md` |
| Excerpt names its own feature | 1 | `document-type-settings/ocr-engine.md` |
| `_order.yaml` drift | 4 | `docs/_order.yaml` lists `Email extraction`, which no longer exists; `integrations/_order.yaml` lacks `getting-started-email` and `quickbooks` (both visible); `field-query-object/_order.yaml` lists `draft-named-anchor`, which doesn't exist |
| Parameters worded differently across pages | 49 keys | detector output for the judgment rule; most differences are legitimate |
| Vale hits from the new rules | 63 | table above |

### Not done

- Fixing the backlog: content changes, page by page (D-004).
- Calling Jev on the judgment specs: belongs in `sensible-docs-gen`.
- Converting the doc skills to subagents: belongs in `sensible-docs-gen`.
- The 5 harness spikes from the map (skill-frontmatter hooks, `` !`command` ``, `updatedInput`, a blocking `Stop` hook, `PreToolUse` on `Skill`). The hook here uses only `PreToolUse` deny, `PostToolUse` exit 2, and `additionalContext`, which are already in use in this repo or in `sensible-docs-gen`.
- Memory edits: proposed in `decisions.md` (D-005).

## 2026-11-16: start

- Wrote the design and implementation plan. Started the session files.
