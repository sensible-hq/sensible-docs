# Style rules

## Summary

These checks keep you from adding a style rule that repeats or conflicts with one you already have. They run in three places:

- **While you edit:** when you edit a file that holds a rule, a hook checks the rules you touched and reports drift or a clashing pair. It never blocks the edit.
- **On each PR:** CI confirms that the registry still matches the guides.
- **Every Monday:** a workflow checks every pair of rules, including with Jev, and posts a report.

When a pair is flagged, settle it once: merge the two rules, mark one as overriding the other, or record the pair as fine in `overlaps.yaml`. The pair stays quiet until someone rewords one of the rules.

Two rules are compared only if they check the same kind of text, such as prose, headings, tables, or code. Each rule's `applies` list in the registry names its kinds. Of the 861 possible pairs among 42 rules, 403 share a kind. The weekly run compares those by wording and asks Jev about each one twice, once in each order. Jev's answers are cached, so after the first run Jev is only asked about pairs where a rule was added or reworded. The Vale fixture layer runs each of the 19 fixtures once against all rules. The hook compares only the rules an edit touched.

What the checks cost at 42 rules:

| Run | Time | Jev calls | Cost |
| --- | --- | --- | --- |
| Hook, after an edit to a rule file | under 1.5 s | 0 | $0 |
| Weekly, without Jev | 3 s | 0 | $0 |
| Weekly, with Jev, first run | 21 s | 806 (403 pairs, asked in both orders) | $0.02 |
| Weekly, with Jev, nothing changed | under 1 s | 0 | $0 |
| Weekly, with Jev, one rule added | a few seconds | 2 per rule it shares a kind with | under $0.01 |

No step calls Claude or any other LLM besides Jev.

## How rules are carried

House style rules are carried in two ways:

- **In prose**, in guides, templates, and skills that the model reads (`.claude/style-guide/`, `.claude/preferences/`, `.claude/skills/`). This is probabilistic: the model may or may not apply what it reads.
- **As checks**: Vale rules (`.github/styles/Sensible/`), scripts (`scripts/style/`), and judgment specs for Jev (`style-rules/judgment/`).

Many rules are carried both ways. [`registry.yaml`](registry.yaml) records, for each rule, every place it's stated and everything that enforces it, so the two can't drift apart silently.

## Files

| path | what it is |
| ---- | ---------- |
| `registry.yaml` | One entry per rule: `stated_in` (prose carriers), `enforced_by` (Vale, script, judgment), `kind`, `gate`, `fixture` |
| `judgment/<id>.yaml` | What Jev needs to judge a rule: source, scope, detector, precheck, question with criteria, examples |
| `tests/<id>.md` | Test examples for a Vale rule: sentences it must catch, marked `<!-- fail -->`, and correct sentences it must leave alone, marked `<!-- pass -->` |
| `corpus-before.tsv`, `corpus-after.tsv` | Vale alert counts per rule on `docs/` and `reference/`, before and after the 2026-11 cleanup |

## Checks

```bash
python3 scripts/style/check_registry.py          # registry agrees with guides, Vale rules, scripts, specs
python3 scripts/style/test_rules.py              # every Vale rule passes its fixture
python3 -m pytest -q scripts/style/test          # script and hook tests, including the registry check
python3 scripts/style/check_code_blocks.py       # json fences and /* */ comments in docs/
python3 scripts/style/check_excerpts.py          # excerpt length, sync, and self-naming in docs/
python3 scripts/style/check_order.py             # every docs page is in its _order.yaml
python3 scripts/style/compare_param_descriptions.py   # parameters worded differently across pages
python3 scripts/style/check_overlap.py [--jev]   # rules that duplicate, overlap, or contradict each other
bash scripts/vale-doctor.sh                      # the write-time hook works the way Claude Code runs it
```

The pytest suite runs in CI (`test-scripts.yml`) whenever a guide, skill, Vale style, or this directory changes.

## How a rule is enforced while the agent writes

`.claude/hooks/vale_gate.py` runs on every Edit or Write to `docs/**/*.md`:

- **Before the edit**, it lints the page as it would be after the edit. If a changed line breaks a rule whose `gate` is `block`, the edit is denied with the rule and its fix, and the agent rewrites. After 3 denials on one file, the edit goes through with the alerts as context, so a false positive can't stall the work.
- **After the edit**, it reports warnings and errors on lines changed since the last commit.

`gate` is set per rule in the registry. Reserve `block` for rules that are almost never wrong: a false positive that blocks a write costs a round trip, while one in feedback costs a line of reading.

Some patterns also match correct text: "against" in "validate against your rules", "above" for position on the page, "template" as a defined alias. Those rules are `kind: judgment` with `gate: judge`. Vale finds the candidates, the after-write report lists them apart as possibly fine, and the Jev judge decides before commit. Today that's `AgainstPhrasing`, `Terminology`, `InternalTerms`, `Filler`, the word lists, and `Google.Passive` (for the explicit-actor rule).

## The link between a guide and its check

When a guide states a rule that has a check, put a marker right after the rule's text:

```markdown
Do not use em dashes to join compound clauses. Split into two sentences instead. <!-- rule: sensible-em-dash -->
```

and list the file and a quote in the rule's `stated_in`. `check_registry.py` fails if:

- the quoted text changes (someone reworded the guide; decide whether the check still matches);
- a marker is missing, or names a rule the registry doesn't have;
- a Vale rule exists without a registry entry, or an entry names a rule, script, fixture, or spec that doesn't exist.

So changing a rule means changing the guide, the check, and the registry in the same commit.

## Adding a rule

1. Decide the kind. A pattern settles it: deterministic. A pattern finds candidates but reading decides: judgment. Neither: prose.
2. Deterministic: write the Vale rule (or script) and a fixture with fail and pass lines. Run `test_rules.py`.
3. Run Vale on the whole corpus and read every hit. Narrow the rule until the hits are real, or drop it and record why.
4. Judgment: write `judgment/<id>.yaml` in the same shape as the others.
5. Add the registry entry, with `stated_in` for every guide, template, or skill that states the rule, and add the markers.
6. Run `check_registry.py`.

## Vale behaviors that catch rule authors

- An `existence` rule wraps each token in word boundaries. A token that starts or ends with a symbol (`![`, `<Image`, `^## `, a trailing `/`) never matches unless the rule sets `nonword: true`.
- `scope: raw` sees the Markdown source, including image and link syntax.
- A word in the accepted vocabulary (`.github/styles/config/vocabularies/Sensible/accept.txt`) suppresses any match that contains it. "config" is accepted, so a rule about "SenseML config editor" needs `vocab: false`.
- When two `.vale.ini` sections match a file, the later section wins. Changelog drafts (`drafts/*changelog*.md`) and blog drafts (`drafts/blog-*.md`) have their own sections after `[*.md]`.
- Quote YAML tokens that contain `: `, or the rule fails to load. `test_rules.py` reports Vale load errors instead of missing alerts.
- Vale exits 1 when it finds an error-level alert, so don't chain other commands after it with `&&`.

## Judging the judgment rules with Jev

`scripts/style/judge.py` runs the judgment rules on docs pages with TypeSafe's Jev:

```bash
python3 scripts/style/judge.py <file> [...] [--base origin/v0] [--rules id,...] [--dry-run]
```

1. **Code finds candidates.** Each spec's `check.find` names a detector: a regex over prose sentences, a Vale check, the page's first sentence, the first sentence under each heading, JSON code blocks, the Examples section, or, with `--base`, added tables, added headings, and changed links.
2. **Jev answers the spec's multiple-choice question** about each candidate. The state is the candidate, its paragraph, and the page title. Jev returns a choice, a confidence, and probabilities, but no reasons; the choice names are the explanation.
3. **Code decides.** A choice in `check.verdicts.violation` with confidence of at least 0.70 is a `violation`, and below that it's `unsure`. A choice in `verdicts.review` is `review`.

A rule fails a run (exit 1) only when its calibration earned trust: on its labeled cases (`judgment/labels/<id>.yaml`), at least 90% of what it flagged was a real violation (precision), it found at least half of the labeled violations (recall), and there were at least 6 cases with 3 violations. Other rules print `(advisory)`. `scripts/style/calibrate.py --write` reruns calibration and stores the result in each spec. Precision comes first: a judge that flags good text teaches writers to ignore it.

Jev isn't deterministic: the same request can come back with a different confidence. Tests replay recorded responses (`JEV_REPLAY`), so they're stable; record new ones with `JEV_RECORD`. A missing recording fails; it never passes. A live run needs `TYPESAFE_API_KEY` and costs $0.042 per million input tokens (about $0.0002 for four pages).

The judge doesn't run in the write-time hook: a network call per edit is too slow, and judgment needs the whole change. The doc skills run it before committing.

## Duplicate and conflicting rules

`scripts/style/check_overlap.py` compares rules in pairs, in three layers:

- **Fixtures:** every Vale fixture runs against every registered rule. A line marked `pass` for one rule that another rule flags is a contradiction: the example of correct text breaks a house rule. When the other rule is a judgment rule, its pattern only finds candidates, so the finding is marked as a detector finding.
Only rules that share a kind of text in their `applies` lists are paired for the next two layers.

- **Wording:** pairs whose statements and quotes share most of their content words, which catches a rule restated in a second file.
- **Jev** (`--jev`): two yes-or-no questions per pair (same requirement, can conflict), asked in both orders. Jev leans toward whichever rule comes first, so the two answers are averaged, and a pair whose orders disagree is reported as unstable. Answers are cached in `.cache/rule-overlap.json` by the exact request, so a pair is asked again only when a rule's wording changes.

A pair you've ruled on goes in [`overlaps.yaml`](overlaps.yaml) with the hash the script prints; rewording either rule reopens it. A deliberate conflict goes in the registry as `overrides: [loser]` on the winning rule.

The checks run in three places:

- After every edit to a rule carrier (`CLAUDE.md`, `AGENTS.md`, `.claude/style-guide/`, `.claude/preferences/`, `.claude/skills/`, `style-rules/`, `.github/styles/`), the `.claude/hooks/rule_gate.py` hook runs the registry check and the deterministic layers for the rules the edit touched. It reports and never blocks, because changing a rule takes edits to several files.
- On every PR that touches a carrier, CI runs the registry check.
- Every Monday, `rule_overlap.yml` runs all three layers and posts the report as the job summary.

