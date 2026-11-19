# Rule observability progress

Newest first.

## 2026-11-19: skills (R10 to R13)

- Skill scan: 393 sections of 41 skill, template, and preference files against 64 rules. First pass: 93 restatements without a marker and 29 strong contradictions. After: 3 checklists became pointers, 60 sections carry markers, 3 contradictions fixed, 23 cleared with reasons; 0 problems.
- Routing: 41 requests, 19 skills. Expected skill won every time; 10 close collisions before the description edits, 0 after.
- Usage: corrections attributed to repo rules, repo skills, or outside instructions. None in the backfilled weeks.
- Coverage now includes skills: 63 rule-like sentences with no registry entry.
- Jev: about $0.58 for the extension, about $0.62 in total.

## 2026-11-18: R1 to R8 done

- Registry: 64 rules (was 42), every one scoped: 11 general, 7 page-type, 46 construct. 22 prose rules registered from the two reference guides. `HIERARCHY.md` generated; `check_registry.py` fails when it's stale.
- Hygiene: the choice catalog found 2 collisions (renamed, RO-018); overlap found no near-duplicate choices once opposite-side splits counted as Jev being unsure; relations found 4 conflicting pairs (RO-019); cross-fire found no fixture whose correct text breaks another gating rule.
- Judge gates on probability (RO-016). Companion question probe: no difference (RO-017).
- New-rule gate in CI, with its own job and HTML report. The 22 new prose rules pass it.
- Weekly cleanup workflow. A 12-page live run: 16 rules calibrated, 9 trusted, 2 violations and 1 unsure on the pages. About $0.002.
- Usage: W42 to W46 backfilled. 70 firings, all in October: 40 from after-edit hook reports (the older `vale-check.sh`), 30 from the deleted PR-wide hook (RO-011); none in W44 to W46. The vale_gate hook has barely fired since it merged, so the acceptance numbers need a few weeks of writing to mean anything.
- Hook reports each alert once per session (RO-014). WordListCase stops flagging "Email" (RO-015).
- Live Jev spend tonight: about $0.04.
- Pre-existing failures on v0, unrelated and untouched: `check_code_blocks.py` (quickbooks.md uses `//`), `check_excerpts.py` (quality-control.md is 154 characters), `check_order.py` (quickbooks missing from `_order.yaml`).

## 2026-11-18: start

- Baseline on v0 (`7d52f49a9`): `check_registry.py` clean (42 rules), fixtures clean, pytest 23 passed and 1 failed. The failure: Frances changed one `sensible-internal-terms` label and removed another in #830, so the stored calibration no longer matches the recordings. Recalibrated in R1, with her changed case marked `labeled_by: frances`.
- Corpus dry run: 385 judge candidates over 170 docs pages, 2.5 minutes, mostly Vale.
- Transcripts: the vale_gate hook has fired only 8 PostToolUse reports so far (from the older `vale-check.sh`); no PreToolUse denials yet. The usage parser is built against those formats plus synthetic cases.
