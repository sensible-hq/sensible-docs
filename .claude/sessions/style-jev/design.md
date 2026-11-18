# Jev style judge: design

Runs the judgment rules in `style-rules/judgment/` against docs pages, using TypeSafe's Jev (`POST https://api.typesafe.ai/v1/systemone`). Lives in this repo, next to the rules it judges, rather than in `sensible-docs-gen`.

## How a rule is judged

1. **Find candidates (code).** Each spec's `check.find` names a detector the judge runs: a regex over prose sentences, a Vale check, the page's first sentence, added lines or tables or headings in a diff, JSON code blocks, or the Examples section. Code decides where to look; Jev never scans a whole page.
2. **Ask Jev (model).** Each candidate becomes one Jev call: the candidate text plus its paragraph and the page title as `state`, and the spec's question as a `choice` question with the spec's criteria. Jev answers with a choice, a confidence, and probabilities per option.
3. **Decide (code).** The spec's `check.verdicts.violation` lists the choices that break the rule. A violation with confidence at or above the threshold (0.70, as in `sensible-docs-gen`) is reported with the spec's `fix`. Below the threshold the candidate is reported as unsure, never as a pass.

Jev returns no reasons, so the choice names and their criteria are the explanation.

## Calibration

`style-rules/judgment/labels/<id>.yaml` holds labeled cases: a text and the choice a reviewer expects. `calibrate.py` asks Jev each case and reports agreement per rule. A rule whose agreement is below 90% isn't trusted to fail anything: its `gate` stays `report`. Labels written by Claude are marked `labeled_by: claude` for Frances to review.

## Record and replay

Every call can be recorded (`JEV_RECORD=<dir>`) and replayed (`JEV_REPLAY=<dir>`), keyed by a hash of the request, so tests and calibration reruns are offline and free. A missing replay fails; it never passes.

## Where it runs

- On demand: `python3 scripts/style/judge.py <file> [--base <ref>]`.
- In the doc skills, as the last style step before committing.
- Not in the write-time hook: a network call per edit is too slow, and judgment needs a whole change, not one edit.

## What is sent to Jev

Only prose from `docs/` and `drafts/`: the candidate, its paragraph, and the page title. Code blocks are sent only for the code rule (`sensible-example-var`). The docs repo is public; drafts can describe unreleased features, which TypeSafe already sees through `sensible-docs-gen`.
