# testable-claims session: decisions and progress

Claude Code session name: ocrIfMissing
Claude Code session ID: 0ded2aae-03f7-4ca1-bf75-b37050ab318e
Resume: `cd /home/franc/GitHub/sensible-docs-private && claude --resume 0ded2aae-03f7-4ca1-bf75-b37050ab318e`
Checklist: `.claude/sessions/testable-claims/checklist.md` · Design: `design.md` · Evidence: `evidence/README.md`
This PR: sensible-hq/sensible-docs#834 (branch `testable-claims-skill`, worktree `~/GitHub/sensible-docs-testable-claims`)
Related: sensible-hq/sensible-docs#825 (the OCR page whose claims were tested), sensible-hq/sensible#3519 and #3533 (engine)

## Decisions

| decision | why | who |
| --- | --- | --- |
| A skill, `extract-testable-claims`, lists the claims worth testing after a docs draft, with evidence and a proposed test each; it doesn't run tests unless asked | Frances wants to test defaults, types, compatibility, and null/empty behavior before a change ships | Frances |
| The criteria for "worth testing" are written down (`criteria.md`), and Jev judges each claim's probability of meeting them | Frances: specify the criteria so Jev can judge them | Frances |
| Jev answers a **noul** (one yes/no probability), not a choice label | Frances asked for a noul answer | Frances |
| Threshold 0.70 (test) / 0.30 (skip), unsure between | Frances set 0.7 for nouls on 2026-11-18 | Frances |
| Output-block claims skip Jev and are always `test` | Jev scored the same output claim 0.31 and 0.63 | Claude |
| Only docs text goes to Jev; engine code stays with Claude | Jev is approved for docs, not the engine codebase (Frances, Slack, 2026-11-10) | Frances |
| A proposed test must give a different result if the claim is false, with a control run | A test that passes either way proves nothing; the first test-1 attempt was invalid for this reason | Claude |
| Record-only priority below 3, one pointer comment per page, details in the traceability matrix | Avoid bloating page HTML with markup | Frances |
| `extract-testable-claims` gets a review step: Frances approves what goes in the matrix and the page | Frances | Frances |
| Handoff lives on this PR, and #825 gets its own checklist of tested claims with proof links | Frances, at session end | Frances |

## Progress log

### 2026-11-19
- Built `extract-testable-claims` (`SKILL.md`, `criteria.md`, `score_claims.py`, `cases.yaml`). Calibration: 14 cases, precision and recall 1.00 on the last run; the advice case "Choose OCR If Missing text…" swings between 0.33 and 0.52 across runs.
- Dry run on #825: 13 claims, 8 test, 4 unsure, 1 skip (`evidence/claims/`).
- Ran two of the proposed tests on production, with controls (`evidence/README.md`):
  - "checks the document's embedded text": contradicted. Frances reworded the row on #825.
  - "OCRs every page": likely engine bug with Page Range. Draft for eng in `eng-page-range-bug.md`, not sent.
- Earlier, a match-array test confirmed `ocrIfMissing` accepts a Match array and evaluates it as a sequence.
- Frances asked how QA handles durable proof; Claude found the repo's own framework already covers it except for record-only claims. Proposal in `design.md`.
