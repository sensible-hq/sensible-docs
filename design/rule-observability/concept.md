# Rule observability: concept

Status: proposed, 2026-11-18. Implementation plan: [implementation.md](implementation.md). Decisions: `.claude/sessions/rule-observability/decisions.md`.

## The problem

House style is carried by three systems that grew separately:

- **Vale rules** (`.github/styles/`) match patterns.
- **Jev judgment specs** (`style-rules/judgment/`) ask a multiple-choice question about each candidate a detector finds, and labeled cases decide whether the answer can be trusted.
- **The registry** (`style-rules/registry.yaml`) links each rule to where it's stated in prose and what enforces it.

`check_registry.py` already catches one kind of drift: a guide reworded under a registered rule, a missing marker, a spec or Vale rule that disappeared. It can't catch four others:

1. **Rules nobody registered.** The style guides state many more rules than the registry's 42. An unregistered rule drifts with nothing watching.
2. **Rules that overlap or contradict.** Two specs can ask nearly the same question, two choices inside one spec can mean the same thing, and one rule's fix can break another rule. Nothing compares rules with each other.
3. **Labels that flatter the judge.** All 101 labels were written by Claude, several are copied word for word from the spec's own criteria, and samples of 4 to 9 cases can't separate a good rule from a lucky one.
4. **Rules that do nothing, or do harm.** No one knows which rules fire while an agent writes, which rewrites Frances keeps, and which she undoes.

## What we build

### 1. One map of every rule

Each registry entry gains a **scope**:

| scope | meaning | example |
| ----- | ------- | ------- |
| `general` | applies to every docs page | no em dashes |
| `page-type` | applies to one kind of page | changelog section headings |
| `construct` | applies to one element, term, or parameter | Start parameter values, "above" for position |

Enforcement (Vale, Jev, script, or prose only) is derived from `enforced_by`, so it can't disagree with it. A generated page, `style-rules/HIERARCHY.md`, groups every rule by scope and shows how each one is enforced, where it's stated, and, for judgment rules, its choices and calibration. The registry check fails when the page is stale.

The registry also gets a **coverage check**: imperative sentences in the style guides ("Do not…", "Use…", "Always…") with no rule marker are listed as candidates to register. The first pass registers the missing prose rules in the rule-dense guides.

### 2. Rules checked against each other

Three tests, each with a clear failure:

- **Choice hygiene (offline).** A catalog of every choice name across specs. Lint fails when one name has different criteria in two specs, or when a criterion quotes a labeled case word for word (the case then tests the wording it was copied from, not the rule).
- **Choice overlap (offline, from recordings).** For each spec, how often two choices split the probability on the same case. Two choices that both get 0.25 or more on a third of the cases are near-duplicates.
- **Rule relations (Jev).** For each pair of rules, Jev reads both statements and picks one of: `same-requirement`, `overlapping`, `conflicting`, `independent`. Code, not Jev, decides what a `conflicting` answer blocks.
- **Fixture cross-fire (Vale, offline).** Every Vale fixture's pass lines are linted with every gating Sensible rule. A pass line that another rule flags is a contradiction: following one rule breaks the other.

### 3. A gate for new rules

`scripts/style/new_rule_gate.py` compares the registry with the base branch. A new rule fails the gate unless it has:

- a registry entry with scope, statement, and every place it's stated, with markers;
- a fixture (Vale) or a label file (judgment) with at least 6 cases and 3 violations, none copied from the spec's criteria;
- a relation check against every existing rule, with no `same-requirement` or `conflicting` answer left unresolved (a resolved pair is recorded under the rule's `relations` field with a reason).

Jev's answers are recorded, so CI replays them without a key. A missing recording fails.

### 4. The judge gates on probability

The TypeSafe guidance is that confidence measures how concentrated an answer is, not whether it's right. The judge moves from "violation choice with confidence ≥ 0.70" to "the probabilities of the violation choices sum to ≥ 0.70". We also measure whether replacing the `other` option with a companion yes-or-no question ("Does any of these describe the marked text?") changes agreement on the labels, and adopt it only if it helps.

### 5. Weekly reports

| report | runs | reads | shows |
| ------ | ---- | ----- | ----- |
| Jev cleanup | GitHub workflow, Mondays | specs, labels, docs corpus, Jev | live calibration against the stored numbers, every judge verdict on `docs/`, hit rate per Vale-backed rule, rule relations, choice overlap, labels still marked `labeled_by: claude` |
| Rule usage | Frances's machine, weekly | Claude Code transcripts, git | firings per rule, what the agent did after each, and whether the text came back later |
| Rule hierarchy | every change to the registry | registry, specs | the map in section 1 |

Every report is a standalone HTML page in the house report style (`scripts/doc-detective/`), uploaded as a GitHub Actions artifact that opens in the browser and linked from the run summary. The weekly cleanup also opens or comments on one issue labeled `style-weekly`, with a link to the report.

### 6. Rule usage from agent transcripts

Claude Code keeps each session's transcript for 30 days. A weekly run reads the last week and keeps the derived scores in the repo (`style-rules/usage/<week>.json`), so history outlives the transcripts. A push of a new week's file triggers a workflow that renders the usage report.

For each firing of a rule (a write-time hook denial, a hook report after an edit, or a judge verdict) the run records:

- **acted**: the agent edited the file and the alert didn't come back in a later report in that session;
- **ignored**: the alert was still reported when the session's edits to that file ended;
- **reverted**: the alert was fixed in the session, but Vale flags the same rule on the same file on the default branch today;
- **pushback**: Frances's next message after the fix reads as a correction ("put it back", "don't change", "revert"), quoted in the report for her to judge.

Firings are deduplicated per session: the hook reports the same alert after every edit, and the transcript stores each hook output more than once.

It also counts how often each style guide was loaded. That's a weak signal (reading a guide loads every rule in it at once), so the report shows it per guide, not per rule.

## What this doesn't do

- It doesn't decide which rules to retire. The reports give the numbers; Frances decides.
- It doesn't relabel. Labels Frances changes become `labeled_by: frances`; the rest stay marked as unreviewed.
- It doesn't read transcripts in CI. They stay on Frances's machine; only the derived counts are committed.
