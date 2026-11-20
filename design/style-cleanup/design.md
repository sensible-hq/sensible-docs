# Style cleanup: design

Turns the findings in [style-system-map.md](../style-system-map.md) into a working system. Rules that a pattern can settle are enforced by Vale or a script while the agent writes. Rules that need reading become judgment specs for Jev. The guides keep the reasons and the examples. Every rule that exists in more than one of those places is tracked in one registry, so a guide and its check can't drift apart without a test failing.

Scope: `sensible-docs` only, on a branch. No change to `v0`. No content in `docs/` or `reference/` changes; violations already in the corpus are reported as a backlog, not fixed here.

## The problem this solves

1. The same rule lives in up to six places (guides, skills, templates, memory, Vale, friction logs), in different words, and they disagree (map §2).
2. Most rules have no check at all, so they hold only when the agent happens to read and apply them (map §7: 26 of 53 recorded corrections could be deterministic, 2 are enforced).
3. When a rule is duplicated between a probabilistic carrier (a guide or template the model reads) and a deterministic one (a Vale rule, a script, a Jev spec), nothing records that they're the same rule. Editing one leaves the other stale.

## Parts

### 1. The rule registry

`style-rules/registry.yaml` holds one entry per rule:

```yaml
- id: sensible-no-em-dash            # stable; also the Vale rule's base name where there is one
  map_id: D2                         # the ID in style-system-map.md, for traceability back to the analysis
  statement: Don't use em dashes. Split the sentence, or use a colon or parentheses.
  kind: deterministic                # deterministic | judgment | prose
  enforced_by:                       # the deterministic carriers
    vale: [Sensible.EmDash]
    script: []
    judgment: []                     # style-rules/judgment/<id>.yaml
  gate: block                        # block | warn | report: what the write-time hook does with a hit
  stated_in:                         # the probabilistic carriers: guides, templates, skills
    - file: .claude/style-guide/writing-rules.md
      quote: Do not use em dashes to join compound clauses.
  origin: [writing-rules.md, style-guide-overview.md]
  fixture: style-rules/tests/sensible-no-em-dash.md
```

A rule's **probabilistic carriers** are `stated_in`: text the model reads. Its **deterministic carriers** are `enforced_by`: a Vale rule, a script, or a Jev spec. The registry is the record of the relationship between them.

`scripts/style/check_registry.py` keeps the relationship honest. It fails when:

- a `stated_in.quote` no longer appears in its file (the guide changed; update the registry and decide whether the check still matches);
- a guide line carries a `<!-- rule: <id> -->` marker for an ID that isn't in the registry, or a `stated_in` entry has no marker in its file (the link has to be visible from both sides);
- a `Sensible.*` Vale rule has no registry entry, or an entry names a Vale rule, script, or judgment spec that doesn't exist;
- a deterministic rule has no fixture.

The marker is an HTML comment placed right after the rule's text in the guide. Readers and models see that the rule is enforced and by what; Markdown renders nothing.

### 2. Deterministic checks

- **Vale** (`.github/styles/Sensible/`): fixes to the four buggy or overlapping rules (map §4) and the new pattern rules from map §5 and §7 that test cleanly against the corpus.
- **Scripts** (`scripts/style/`): checks Vale can't express, such as code-fence rules and frontmatter comparisons.
- **Fixtures** (`style-rules/tests/<id>.md`): each deterministic rule's fail and pass lines, with the expected alert on each fail line. `scripts/style/test_rules.py` runs Vale on every fixture and asserts the exact result. This is eval layer 3 for deterministic rules.

Every new rule is measured on the full `docs/` + `reference/` corpus before it's kept. A rule whose hits are mostly false positives is narrowed or dropped, and the decision is logged.

### 3. Judgment specs

`style-rules/judgment/<id>.yaml`, in the format Frances drafted (id, source, applies, check with detector, precheck, question, criteria, examples). These are for Jev. Nothing in this PR calls Jev: wiring it in belongs with `sensible-docs-gen`, which owns the Jev integration and its calibration (L6).

### 4. Write-time enforcement

One hook script, `.claude/hooks/vale_gate.py`, replaces `vale-check.sh` and handles two events:

- **Before a write** (`PreToolUse` on Edit/Write): rebuild the file as it would be after the edit, run Vale on a copy at the same repo path, keep only alerts inside the new text, and deny the edit when an alert comes from a rule whose registry `gate` is `block`. The denial names the rule and its fix. A loop guard allows the edit after three denials on the same file.
- **After a write** (`PostToolUse`): report every warning or error on the **changed lines only**, as feedback.

Scope: `docs/**/*.md`. Generated `reference/**/*.md` is skipped (map C17).

The `vale-setup` memory records Vale as one `PostToolUse` hook plus CI. This keeps one hook script but adds a second event; see the decision log.

### 5. Guidance edits

The guides keep reasons, examples, and the rules no check can hold. The edits:

- resolve the contradictions in map §2, writing the decision into the guide rather than memory;
- remove examples that break the guides' own rules;
- replace the three calls to a Vale MCP tool that doesn't exist with the Vale CLI;
- align the doc skills' branch and commit steps;
- add a registry marker beside each rule that has a deterministic carrier.

## What this design leaves out

- Fixing the existing violations in `docs/`: a content change Frances should review page by page. The backlog is in the progress log.
- Converting the doc skills into subagents (map §8): the right direction, but it belongs in `sensible-docs-gen`, which already does it.
- Calling Jev: owned by `sensible-docs-gen`.
- Editing Claude memory: memory isn't in the repo, so a PR can't show it. Proposed memory edits are listed in the decision log.
- Shoalrun (`my-docs`): a separate repo.
