# Jev style judge progress

Newest first.

## 2026-11-17: J1–J7 done

- `scripts/style/jev.py`: client with record and replay.
- `scripts/style/judge.py`: 10 detector kinds, one Jev `choice` question per candidate, verdicts from the spec.
- `scripts/style/calibrate.py`: precision, recall, and agreement per rule from labeled cases; `--write` stores them in the spec.
- Every judgment spec has `check.find` and `check.verdicts`; `check_registry.py` validates them and the labels.
- 20 tests, all offline (61 recorded calibration responses, 8 recorded page responses).
- Doc skills run the judge before committing; `style-rules/README.md` documents it.

### Calibration (jev-1.14.0, 61 Claude-labeled cases, $0.001)

| rule | cases (violations) | precision | recall | status |
| ---- | -----------------: | --------: | -----: | ------ |
| sensible-context-terms | 9 (5) | 0.00 | 0.00 | advisory |
| sensible-copy-sibling-wording | n/a | n/a | n/a | manual: Jev can't see the engine source |
| sensible-example-per-scenario | 4 (2) | 1.00 | 0.50 | advisory |
| sensible-example-var | 4 (2) | 0.00 | 0.00 | advisory |
| sensible-explicit-actor | 8 (5) | 1.00 | 0.60 | trusted |
| sensible-gerunds | 7 (4) | 1.00 | 0.25 | advisory |
| sensible-integrate-before-heading | 3 (2) | 0.00 | 0.00 | advisory |
| sensible-label-method | 4 (2) | 1.00 | 0.50 | advisory |
| sensible-no-table-for-unconfigurable | 4 (2) | 1.00 | 1.00 | advisory |
| sensible-opening-sentence | 8 (3) | 1.00 | 1.00 | trusted |
| sensible-parent-link | 4 (2) | 0.00 | 0.00 | advisory |
| sensible-scenario-first | 6 (3) | 1.00 | 1.00 | trusted |

Weak rules, and why:

- `sensible-context-terms`: Jev calls the avoided senses legitimate ("each key in the output", "the field is empty"). One question covers six terms; splitting it per term is the next thing to try.
- `sensible-integrate-before-heading`: Jev sees the new section but not the page's existing sections, so it can't tell whether one already covers the topic.
- `sensible-parent-link`, `sensible-example-var`: low-confidence answers near 0.5; the questions need sharper criteria.
- `sensible-gerunds`: right choices at low confidence (0.58–0.66), so recall is 0.25.

### First live run on 4 pages (8 calls, $0.0002)

- `extra-data.md` opening "Use this method to…": `review` (right: Extra Data is the documented exception).
- `copy-to-section.md:28` "are listed once in the document": `unsure` explicit actor.
- No trusted violations after fixing a detector false positive (JD-005).

## 2026-11-17: start

- Probed Jev's choice question format; wrote the design.
