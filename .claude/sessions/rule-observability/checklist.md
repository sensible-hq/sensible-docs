# Rule observability checklist

Worktree: `~/GitHub/sensible-docs-rule-observability`, branch `rule-observability`
Design: `design/rule-observability/concept.md`, `implementation.md`

- [x] R0 Concept and implementation docs
- [x] R1 Registry: scope on every entry, missing prose rules registered with markers, coverage list
- [x] R2 Hierarchy page (Markdown in repo, HTML report), stale-page check
- [x] R3 Jev hygiene: catalog lint, choice overlap, rule relations, fixture cross-fire
- [x] R4 Judge gates on probability; recalibrated; companion-question probe
- [x] R5 New-rule gate, in pytest/CI
- [x] R6 Weekly cleanup workflow: HTML artifact, run summary, issue linking the report
- [x] R7 Usage from transcripts: collect, weekly JSON, HTML report, skill, render workflow on push
- [x] R8 vale_gate reports only new alerts; Google.WordListCase stops flagging "Email"
- [x] R9 All checks pass; PR open
- [x] R10 Skills restating or contradicting rules: scan, pointers and markers, exceptions, gate
- [x] R11 Skill routing: request set, overlap check, description edits, CI job
- [x] R12 Usage: corrections attributed to instructions outside the repo
- [x] R13 Skill checks in the weekly report and as a CI HTML artifact; PR updated

Every report is a standalone HTML artifact linked from its run summary (RO-003): hierarchy (`rule_map.py --html`), new-rule gate (test-scripts.yml), weekly cleanup (style-weekly.yml, also linked from the issue), usage (style-usage-report.yml).

Open for Frances:
- [ ] Review the 4 rule pairs Jev called conflicting and the resolutions recorded under `relations` in the registry
- [ ] Review the 22 registered prose rules (scopes and statements)
- [ ] Review labels: 99 still `labeled_by: claude`; 12 are copied from their spec (the catalog lists them)
- [ ] Decide the "Review:" exceptions in `style-rules/skill-exceptions.yaml` (blog scope of code-fences and filler, blog boilerplate, the integration guide's "Congratulations!")
- [ ] Check the skill description edits (RO-026)
- [ ] Run the weekly workflow once by hand after merge (Actions > Weekly style rule cleanup > Run workflow)
