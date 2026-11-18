# claim-kinds session: decisions

| Date | Decision | Why | Who |
| --- | --- | --- | --- |
| 2026-11-11 | Stack on #760, not directly on #803 | #760 rewrites the same runner and report code; stacking on it keeps this PR from conflicting with it | Claude (Frances: "go ahead with the refactor in a stacked PR") |
| 2026-11-11 | One module per kind, as plain modules with a documented set of names, not classes | Matches the codebase's module-and-function style; `tests/test_kinds.py` checks every kind defines the names | Claude |
| 2026-11-11 | "output" is a kind too, though it has no expect marker | Every test then has exactly one kind, so nothing branches on "no kind" | Claude |
| 2026-11-11 | Records get a top-level `"kind"`, and keep their existing section keys (`segments`, `fingerprint`, `classification`), instead of the review's `claim: {kind, ...}` nesting | Same benefit (a record says its kind) without changing every report's reads or the saved evidence's meaning; nesting can come with O2 | Claude |
| 2026-11-11 | Each kind's record section schema in `schemas/kinds/<kind>.schema.json`, assembled by `record.schema()` | Otherwise a new kind still needs edits to the shared schema; only record.py reads the schema | Claude |
| 2026-11-11 | Error messages unchanged | Unit tests and the add-doc-tests skill quote them | Claude |
| 2026-11-11 | O2 and the rest of O3 left for later | O2 is a design change across runners; O3's remainder changes how output tests use the test account. Neither is a refactor | Claude |
