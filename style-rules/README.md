# Style rules

House style rules are carried in two ways:

- **In prose**, in guides, templates, and skills that the model reads (`.claude/style-guide/`, `.claude/preferences/`, `.claude/skills/`). This is probabilistic: the model may or may not apply what it reads.
- **As checks**: Vale rules (`.github/styles/Sensible/`), scripts (`scripts/style/`), and judgment specs for Jev (`style-rules/judgment/`).

Many rules are carried both ways. [`registry.yaml`](registry.yaml) records, for each rule, every place it's stated and everything that enforces it, so the two can't drift apart silently.

## Files

| path | what it is |
| ---- | ---------- |
| `registry.yaml` | One entry per rule: `stated_in` (prose carriers), `enforced_by` (Vale, script, judgment), `kind`, `gate`, `fixture` |
| `judgment/<id>.yaml` | What Jev needs to judge a rule: source, scope, detector, precheck, question with criteria, examples |
| `tests/<id>.md` | Fixtures: lines each Vale rule must flag (`<!-- fail -->`) and must not flag (`<!-- pass -->`) |
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
