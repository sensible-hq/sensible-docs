# Style cleanup: implementation plan

Design: [design.md](design.md). Working files: `.claude/sessions/style-cleanup/` (`checklist.md`, `progress.md`, `decisions.md`).

Each milestone ends with a commit and its checks passing. Corpus counts are taken with Vale 3.25.1 on `docs/` + `reference/` at warning level and above.

| # | milestone | done when |
| - | --------- | --------- |
| M0 | Baseline | Per-rule alert counts on the corpus before any change are saved in `style-rules/corpus-before.tsv` |
| M1 | Test harness | `scripts/style/test_rules.py` runs Vale on `style-rules/tests/*.md` and asserts the expected alerts; it passes on an empty fixture set |
| M2 | Vale fixes | `AgainstPhrasing` catches adjacent text; `Sensible.WordList` loses the entries that duplicate `Google.WordListCase` or can't fire; `Google.EmDash` is replaced by `Sensible.EmDash`. Each has a fixture. |
| M3 | New Vale rules | Each rule from map §5 and §7 is either added (fixture passes, corpus hits reviewed) or recorded as rejected with its reason |
| M4 | Registry | `style-rules/registry.yaml` covers every rule from M2–M3 and the scripts, plus the judgment rules and the main prose rules; `check_registry.py` passes |
| M5 | Guide and skill edits | Contradictions C1–C13 resolved in the guides; registry markers in place; `check_registry.py` still passes |
| M6 | Scripts | Code-fence and comment check, excerpt self-naming check, `_order.yaml` registration check. Each with tests and corpus numbers. |
| M7 | Hook | `vale_gate.py` with unit tests that feed it hook JSON: a block-rule hit denies, a warn-rule hit allows with feedback, unchanged lines are ignored, `reference/` is skipped, the loop guard releases. `vale-doctor.sh` updated. |
| M8 | Judgment specs | J-rules as YAML specs, each validated by `check_registry.py` for required fields |
| M9 | Wrap-up | Corpus counts after (`corpus-after.tsv`); progress log has the before and after table and the backlog; PR opened against `style-map` |

Order matters in three places:

- M0 before M2, or the before-and-after comparison is lost.
- M4 before M5, so every guide edit that touches a rule updates the registry in the same commit.
- M2–M3 before M7, because the gate reads `gate:` from the registry.
