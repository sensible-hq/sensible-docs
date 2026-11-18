# Style system map

This file maps every place this repo stores writing guidance: skills, templates, exemplars, style guides, editorial preferences, memory, and Vale rules. It lists where they contradict or repeat each other, and proposes which rules to turn into deterministic Vale checks or scripts. Those checks let an agent correct itself while it writes. A final section maps skill content onto the deterministic features of the Shoalrun port in `my-docs`.

Surveyed 2026-11-11 on `v0` at `39ff57219`, and on `my-docs` at `d4b2dd8` with Shoalrun CLI 1.2.0 and Vale 3.25.1.

## Summary

1. **The most frequent decision has five answers.** The first sentence of a page has five conflicting rules across five files (see [C1](#c1-opening-sentence-voice-five-sources-four-answers)). The corpus settles it: 50 of 75 SenseML pages open with a third-person verb ("Extracts…"). Until one rule wins, no detector or judge can enforce it.
2. **Three skills call a Vale tool that doesn't exist.** `blog-short`, `blog-how-to-parse-x`, and `update-docs-from-pr` call `mcp__vale__check_file`. No Vale MCP server is configured. The Vale hook covers only `docs/` and `reference/`, so blog drafts in `drafts/` get no Vale check at all.
3. **The glossary isn't enforced.** The glossary lists 23 terms to avoid. Vale checks 3 of them: "the UI", "dashboard", and "parse". The `docs-checker` skill does this work in an LLM pass instead. It's a lookup table, so Vale should do it.
4. **Four Vale rules have bugs or overlap.** `AgainstPhrasing` misses adjacent text like "classification against". `Sensible.WordList` repeats `Google.WordListCase`, so "disabled" gets flagged twice. One `WordList` swap can never fire because the vocabulary accepts the word. `Google.EmDash` "fixes" an em dash in a way that still breaks the house rule.
5. **The guides teach the errors they forbid.** The changelog guide's own examples use "against", "we", and an em dash. The blog template uses "template" and "let's". The glossary and `revise-doc-style` use "e.g.", which `Google.Latin` flags as an error.
6. **Shoalrun already has a slot for most of this.** In Shoalrun, guides map to `authoring.guideFiles`, sibling-page picks to `authoring.exemplarFiles`, templates to `scaffold`, frontmatter rules to `frontmatter.schema`/`enforced`, page shape to DocShape Tengo scripts, and the eval skill to `audit.evals`. Prose judgment is the only part with no deterministic home.
7. **The guides are frozen in March, and the corrections live in memory.** The core guides were written from 2026-03-10 to 03-16 and never majorly revised. From September on, every style correction went into memory or the friction log instead (see [Timeline](#timeline-when-each-piece-was-written)).
8. **53 recorded corrections, and half could be deterministic.** They come from memory, five friction logs, and your recorded edits. 26 could be deterministic, and only 2 are fully enforced. [Section 7](#7-correction-inventory) triages each one and adds 13 new rules.
9. **Skills can't enforce their own steps; the layer around them can.** A skill is instructions. Subagent `skills:`, `tools:`, and frontmatter hooks are deterministic, and verified in `sensible-docs-gen`. Vale can run before each write, not only after. [Section 8](#8-enforcement-what-can-make-an-agent-follow-the-rules) records what is verified and lists 5 spikes.

## 1. Inventory

### Guidance files

| file | kind | scope | rules (approx.) | enforced by |
| ---- | ---- | ----- | --------------- | ----------- |
| `.claude/style-guide/writing-rules.md` | style guide | all content | 6 | partly Vale (`AgainstPhrasing`, `Google.Passive`) |
| `.claude/style-guide/sentence-word-guidance.md` | style guide | SenseML reference | ~25 | nothing |
| `.claude/style-guide/style-guide-overview.md` | style guide | SenseML reference | ~30 | `DocLinks` only |
| `.claude/style-guide/glossary.md` | term list | all, plus SenseML | 23 avoid-terms | 3 in Vale; `docs-checker` (LLM) |
| `.claude/style-guide/changelog-style-guide.md` | style guide | changelog | ~15 | `changelog/structural-check.md` (LLM) |
| `.claude/style-guide/friction-log.md` | correction log | reference | 1 | nothing |
| `.claude/style-guide/json5-comments-reference.md` | canonical comments | code blocks | ~60 comments | `json5-commenter` (LLM doing a lookup) |
| `.claude/style-guide/reference-topic-template.md` | template | reference page | structure | nothing |
| `.claude/style-guide/concept-topic-template.md` | template | concept page | structure | nothing |
| `.claude/style-guide/integration-guide-template.md` | template | integration guide | structure | nothing |
| `.claude/style-guide/blog-post-template.md` | template | how-to blog | structure + style notes | nothing |
| `.claude/skills/blog-short/blog-short-template.md` | template | short blog | structure + length | nothing |
| `.claude/skills/changelog/structural-check.md` | template + checks | changelog | 3 checks | LLM |
| `.claude/style-guide/config-library-supported-document-types.md` | reference data | blog/integration | none | n/a |
| `.claude/preferences/editorial-preferences.md` | correction log | reference, changelog | ~10 | nothing |
| `.claude/knowledge/fingerprints.md` | verified facts | fingerprints | facts, not style | doc tests |
| `internal-doc-guidelines.md` | human notes | links, images | 3 | `DocLinks` |
| auto-memory (`~/.claude/projects/.../memory/`) | feedback | all | 10 style-relevant | nothing; loads only for Claude, only in this project |

### Exemplars

No file is labelled as an exemplar. Exemplars are hard-coded inside skills instead:

| skill | exemplars it names |
| ----- | ------------------ |
| `create-concept-doc` | `coverage.md`, `ocr.md`, `fallbacks.md`, `field-order.md`, `lines.md`, `anchor-nuances.md`, `llm-features.md`, `prompt.md` |
| `create-new-doc` | "1–2 nearby pages in the same category" (not named) |
| feedback memory `full-style-pass` | "the closest sibling", copied word for word |
| `blog-post-template.md` | derived from 5 posts (listed in the `blog_post_template` memory) |
| `changelog-style-guide.md` | quoted 2024–2026 changelogs |

### Skills and what they read

`●` = the skill reads the file. `V` = the skill runs Vale (or tries to).

| skill | writing-rules | sentence-word | overview | glossary | templates | editorial-prefs | other | V |
| ----- | :-: | :-: | :-: | :-: | :-: | :-: | ----- | :-: |
| `update-docs-from-pr` | | ● | ● | ● | reference | ● (updates only) | | `mcp__vale__check_file` (missing) |
| `update-existing-doc` | | ● | ● | | | ● | | |
| `create-new-doc` | | ● | ● | | reference, integration | | | |
| `create-concept-doc` | ● | | ● | | concept | | exemplar list | |
| `revise-doc-style` | ● | | | | | | its own ~20 rules | |
| `docs-checker` | | | | ● | | | | |
| `json5-commenter` | | | | | | | json5-comments-reference | |
| `changelog` | ● | | | via docs-checker | entry template | ● | changelog guide, structural-check | |
| `blog-how-to-parse-x` | ● | ● | ● | ● | blog-post | | json5-comments-reference | `mcp__vale__check_file` (missing) |
| `blog-short` | ● | | | ● | blog-short | | | `mcp__vale__check_file` (missing) |
| `api-spec` | ● | ● | | ● | openapi template | | source-of-truth files | |
| `style-guide-generator-senseml` | writes | writes | writes | | writes reference | | | |
| `integration-guide-generator` | | | | | writes integration | | doc-types list | |
| `create-docs-example` | | | | | | | inline rules (comments, truncation) | |

What the matrix shows:

- **No skill reads all the guides.** The `full-style-pass` memory compensates by telling Claude to read every file before a PR. That memory doesn't exist for other agents or for a fresh clone.
- **`update-existing-doc` and `create-new-doc` skip `writing-rules.md`**, the file that says it "takes precedence". Only `revise-doc-style` and the blog/concept skills load it.
- **`friction-log.md` and `json5-comments-reference.md` are read only through memory** (`full-style-pass`) or by `json5-commenter`.

### Vale today

| style | rules | notes |
| ----- | ----- | ----- |
| `Google` (vendored) | 35 | `Google.WordList` and `Google.Colons` off |
| `Sensible` | 5 | `AgainstPhrasing`, `DocLinks`, `NoDraftLinks`, `Terminology` (1 swap), `WordList` (a copy of Google's list) |
| `Vale` vocab `Sensible` | accept 70+, reject 6 | reject: JSON editor, dashboard, parse, native text, sub-document, subdocument |

Where Vale runs: the CI job `lint_style.yml`, plus the `PostToolUse` hook `.claude/hooks/vale-check.sh`, which covers `docs/` and `reference/` at warning level and above. `.claude/**` has no styles, so guides aren't linted.

Alert counts on `docs/` and `reference/` today, top 10 out of about 1,500:

| check | count | | check | count |
| ----- | ----: | - | ----- | ----: |
| Google.Parens | 572 | | Google.Headings | 74 |
| Google.Acronyms | 182 | | Sensible.WordList | 60 |
| Vale.Spelling | 155 | | Google.Quotes | 53 |
| Google.WordListCase | 117 | | Google.Jargon | 33 |
| Google.Spacing | 100 | | Google.OxfordComma | 27 |
| Google.Passive | 76 | | | |

### Timeline: when each piece was written

The dates come from `git log --follow` on `v0`.

- **started**: the first commit.
- **major revisions done**: the last commit whose added plus deleted lines reach 20% of the file's current length.
- **last touched**: the latest commit of any size.

Commit dates can trail the writing. Skills marked † were moved into the repo from `~/.claude/skills/` on 2026-06-17 (`b025f15ce`), so their real start is earlier and git can't see it. Skills marked ‡ came over in the same commit after a rename, and `--follow` traces their history from before the move.

| file | started | major revisions done | last touched | commits (major) |
| ---- | ------- | -------------------- | ------------ | --------------: |
| **Skills** | | | | |
| `update-docs-from-pr` | 2026-02-18 | 2026-02-19 | 2026-09-30 | 6 (2) |
| `revise-doc-style` | 2026-02-18 | 2026-02-18 | 2026-03-16 | 3 (1) |
| `create-docs-example` | 2026-02-18 | 2026-02-18 | 2026-05-11 | 2 (1) |
| `upload-pr-extractor` | 2026-02-18 | 2026-02-18 | 2026-02-18 | 1 (1) |
| `create-new-doc` | 2026-03-10 | 2026-03-10 | 2026-03-10 | 1 (1) |
| `update-existing-doc` | 2026-03-10 | 2026-03-10 | 2026-03-10 | 1 (1) |
| `style-guide-generator-senseml` ‡ | 2026-03-10 | 2026-03-10 | 2026-06-17 | 3 (1) |
| `integration-guide-generator` ‡ | 2026-03-10 | 2026-03-11 | 2026-06-17 | 3 (2) |
| `create-concept-doc` | 2026-03-13 | 2026-03-13 | 2026-03-16 | 2 (1) |
| `changelog` ‡ | 2026-03-16 | 2026-07-09 | 2026-07-09 | 8 (2) |
| `api-spec` ‡ | 2026-05-04 | 2026-06-17 | 2026-07-07 | 11 (2) |
| `docs-checker` † | before 2026-06-17 | 2026-06-17 | 2026-06-17 | 1 (1) |
| `quickbooks` † | before 2026-06-17 | 2026-06-17 | 2026-06-17 | 1 (1) |
| `json5-commenter` | 2026-06-17 | 2026-06-17 | 2026-10-28 | 2 (1) |
| `blog-how-to-parse-x` | 2026-06-17 | 2026-06-25 | 2026-06-30 | 15 (3) |
| `blog-short` (+ template) | 2026-07-14 | 2026-07-14 | 2026-07-14 | 2 (1) |
| `mcp-search-eval` | 2026-08-17 | 2026-08-17 | 2026-08-18 | 4 (2) |
| `close-docs-pr` | 2026-09-30 | 2026-09-30 | 2026-09-30 | 1 (1) |
| `categorize-pr` | uncommitted | | | 0 |
| **Style guides and templates** | | | | |
| `reference-topic-template` | 2026-03-10 | 2026-03-10 | 2026-03-10 | 1 (1) |
| `style-guide-overview` | 2026-03-10 | 2026-03-10 | 2026-10-16 | 4 (1) |
| `sentence-word-guidance` | 2026-03-10 | 2026-03-10 | 2026-10-16 | 4 (1) |
| `integration-guide-template` | 2026-03-10 | 2026-03-10 | 2026-03-11 | 2 (1) |
| `editorial-preferences` | 2026-03-10 | 2026-03-10 | 2026-07-02 | 4 (1) |
| `config-library-supported-document-types` | 2026-03-11 | 2026-03-11 | 2026-03-11 | 1 (1) |
| `concept-topic-template` | 2026-03-13 | 2026-03-13 | 2026-10-16 | 2 (1) |
| `writing-rules` | 2026-03-16 | 2026-03-16 | 2026-05-07 | 3 (1) |
| `changelog-style-guide` | 2026-03-16 | 2026-03-16 | 2026-06-25 | 2 (1) |
| `glossary` | 2026-03-19 | 2026-03-19 | 2026-09-15 | 2 (1) |
| `blog-post-template` | 2026-05-15 | 2026-06-22 | 2026-06-25 | 8 (3) |
| `json5-comments-reference` | 2026-06-17 | 2026-06-17 | 2026-10-28 | 7 (1) |
| `changelog/structural-check` | 2026-07-09 | 2026-07-09 | 2026-07-09 | 1 (1) |
| `friction-log` | 2026-09-08 | 2026-09-08 | 2026-09-08 | 1 (1) |
| `knowledge/fingerprints` | 2026-10-16 | 2026-10-16 | 2026-10-16 | 1 (1) |
| **Vale** | | | | |
| `.vale.ini` | 2026-03-24 | 2026-05-07 | 2026-05-08 | 4 (3) |
| `Sensible/WordList` | 2026-05-05 | 2026-05-05 | 2026-05-05 | 1 (1) |
| vocab `accept.txt` | 2026-05-05 | 2026-05-05 | 2026-10-20 | 8 (1) |
| `Sensible/AgainstPhrasing` | 2026-05-08 | 2026-05-08 | 2026-05-08 | 1 (1) |
| `Sensible/Terminology` | 2026-05-08 | 2026-05-08 | 2026-09-15 | 2 (1) |
| `Sensible/DocLinks`, `NoDraftLinks` | 2026-09-14 | 2026-09-14 | 2026-09-14 | 1–2 (1) |
| `.claude/hooks/vale-check.sh` | 2026-05-05 | 2026-10-13 | 2026-10-13 | 3 (2) |
| **Style memories** (file date) | | | | |
| `you-centric-style` | 2026-09-09 | | | |
| `block-comments-only`, `keep-code-fence-language` | 2026-09-28 | | | |
| `full-style-pass`, `label-method-near-deprecated` | 2026-09-30 | | | |
| `excerpt-rules`, `seo-terminology` | 2026-10-20 | | | |
| `anthropic-model-naming` | 2026-11-10 | | | |

What the timeline shows:

- **You wrote the core guidance in one week and never substantially revised it.** The reference template, overview, sentence-word guidance, writing rules, and editorial preferences all date from 2026-03-10 to 03-16. Each has had exactly one major commit: the first one. Later commits are small patches.
- **From September on, corrections went somewhere else.** From 2026-09-08 to 11-10, your style corrections landed in `friction-log.md` and 8 memory files, not in the guides. That's why the guides contradict the memories (C1, C2, C4, C14). The guides still describe March, and the memories describe September through November.
- **The skills that write most of your doc PRs were written once, in February and March.** `create-new-doc`, `update-existing-doc`, and `create-concept-doc` have 1–2 commits each. Their worktree flow (C12) and hard-coded `Sonnet 4.6` (C13) date from then. Only `update-docs-from-pr` got the September fixes.
- **The skills you kept iterating are the blog and changelog skills.** `blog-how-to-parse-x` has 15 commits, `blog-post-template` 8, `changelog` 8. Those are the ones with a human gate and a friction log.
- **Vale rules were written from May to September and haven't kept up.** No Vale rule exists for anything decided after 2026-09-15: excerpts, SEO terms, model naming, the Label method, `json5` fences.

To rerun: `python3 scripts/style_baseline/guidance_timeline.py` from the repo root.

## 2. Contradictions

Ranked by how often an agent hits them. Each has a proposed resolution. Where the corpus can settle a question, I counted.

### C1. Opening sentence voice (five sources, four answers)

| source | says |
| ------ | ---- |
| `revise-doc-style/SKILL.md:22` | third person: "Removes…", **not** "Use this to remove…" |
| `style-guide-overview.md:64` | "imperative present tense. Start with a verb", but every example is third person ("Extracts…") |
| `friction-log.md:13` | lead with "Use this method to…", not "Returns a…" |
| `concept-topic-template.md:36` | "imperative or declarative"; its examples mix both |
| memory `you-centric-style` | "With a postprocessor, you transform…"; says `revise-doc-style` is "wrong for this project" |
| memory `excerpt-rules` | excerpt imperative; first body sentence third person ("decided 2026-10-20; user may revisit") |

Corpus (first body sentence, 75 SenseML pages): 50 third-person verb, 5 "Use this/the…", 5 "You…", 1 "With…, you…", the rest notes and examples.

**Resolve:** keep third person for reference pages. It matches the corpus and the excerpt decision. Rewrite the friction-log entry as an exception ("not 'Returns a…' when the user supplies the input"), or delete it. Fix the word "imperative" in `style-guide-overview.md:64`. Limit the you-centric memory to concept and how-to pages, or retire it. Then the rule becomes a judgment check (J1 below).

### C2. Actor: "Sensible" or "you"

`writing-rules.md:20` and `sentence-word-guidance.md:77` make "Sensible" the subject for platform behavior. The you-centric memory says prefer "you" wherever the user chooses. These don't conflict if you write the boundary down: the user makes the choices, and Sensible performs the behavior. Add that sentence to `writing-rules.md` and drop the memory's claim that the rule is wrong.

### C3. Imperative in steps

`sentence-word-guidance.md:77` says "Don't use imperative … in numbered-step lists. Use 'You upload…'". `integration-guide-template.md` and the corpus's integration guides use imperative steps ("Click **Create**"), and so does the excerpt rule. **Resolve:** limit the "no imperative" rule to the "how Sensible works" overview lists it came from, and allow imperative in procedures.

### C4. `metadata.description` and `excerpt`

| source | says |
| ------ | ---- |
| `style-guide-overview.md:46`, `reference-topic-template.md:14` | `excerpt: ''`; only `title` and `metadata.description` vary |
| `style-guide-overview.md:58`, 3 templates | description 4–7 words, lowercase. The examples are capitalized ("Extract labeled values") |
| `revise-doc-style/SKILL.md:25` | include the key behavior detail; example is 10 words |
| memory `excerpt-rules` | `excerpt` is the source of truth, ≤150 chars (hard cap 160), imperative, synced into `metadata.description` |

The templates are stale. The 2026-10 excerpt work replaced them, and `scripts/descriptions/` enforces it. **Resolve:** update the templates to the excerpt rules and delete "4–7 words, lowercase".

### C5. Examples: separate or merged

`revise-doc-style/SKILL.md:33` says to give each distinct use case its own `##` and never merge. `create-new-doc/SKILL.md:62` and `editorial-preferences.md` (cell-rows log) prefer one well-chosen example over a basic/advanced pair. They're compatible if you state the axis: one example per **scenario**, never one per **difficulty level**. Write that in one place.

### C6. Examples heading level and form

`style-guide-overview.md` says "Use `## Examples`". `reference-topic-template.md:85` uses `# Examples`. The corpus has 53 pages with H1 and 7 with H2. For example subheadings, the overview says `## Example: Descriptive name` (15 in the corpus), and `revise-doc-style` says plain verb phrases. The `full-style-pass` memory already notes this conflict and says to follow siblings. **Resolve:** H1 `# Examples`, and plain verb-phrase H2s for new pages. Then enforce it with a structure script (D14).

### C7. Image syntax

The SenseML guides say markdown `![Click to enlarge](…)` (280 uses in `docs/`). The changelog guide says JSX `<Image>` (13 uses in `docs/`). This isn't a real conflict, because the two apply to different scopes, but nothing states the scope split. **Resolve:** state it, then enforce by glob (D9).

### C8. Changelog guide against its own rules

- `changelog-style-guide.md:29,31`: the intro examples say "We also added" and "We introduced", against the guide's own "Not 'we released'" and `Google.We`.
- `changelog-style-guide.md:80`: "classification **against** specified document types" breaks `writing-rules.md` and is meant to be caught by `AgainstPhrasing`, but isn't (V1).
- `changelog/structural-check.md:17`: the entry template has "You can now … **—** for example". That breaks the em dash rule, and every entry drafted from the template inherits it.
- `changelog/SKILL.md:169`: "Fix all errors and warnings [docs-checker] returns". `docs-checker` only reports terminology, with no levels. This sentence dates from when the step ran Vale.

### C9. Blog template against the glossary and Vale

- `blog-post-template.md:216`: the heading "Test the extraction **template**…" breaks "config, not template".
- `blog-post-template.md:86,134,321`: "What **we'll** cover" and "**let's**" are in the template and the tone note. `Google.We` and `Google.FirstPerson` flag both in `docs/`. Blogs aren't linted, so either allow "we" in blogs in writing, or remove it.
- The blog template's "SenseML is JSON5" is fine for blogs (Webflow/Notion). Note that the `no-json5-fences` memory covers only sensible-docs.

### Smaller conflicts and drift

| # | issue | where |
| - | ----- | ----- |
| C10 | Latin "e.g." used in guidance that agents copy | `glossary.md` (SenseML table), `revise-doc-style:27,37,53,78`, `integration-guide-template.md:57`, memory files. `Google.Latin` is level `error` in docs. |
| C11 | `revise-doc-style:53` good-comment example contains "e.g.," inside a `/* */` comment | code isn't linted, so this teaches a form the prose rules forbid |
| C12 | Branch flow: three skills use `git checkout -b`; global CLAUDE.md and `update-docs-from-pr` use worktrees | `create-new-doc:71`, `update-existing-doc:68`, `create-concept-doc:59` |
| C13 | Hard-coded `Co-Authored-By: Claude Sonnet 4.6` | `create-new-doc:73`, `update-existing-doc:70`, `create-concept-doc:63`, `create-docs-example:161` |
| C14 | Memory `block-comments-only` says `sentence-word-guidance.md` prescribes `//` | stale: the guide now says `/* */` everywhere. Update the memory. |
| C15 | Em dash rule (house) against `Google.EmDash` (Google) | see V3 |
| C16 | Notes: `**Note:**`, never `>` | 10 blockquotes remain in `docs/` |

## 3. Overlaps

| rule | stated in | keep it in |
| ---- | --------- | ---------- |
| Em dashes | `writing-rules`, `style-guide-overview`, `blog-short` step 5b, `blog-how-to-parse-x` 6.7b | Vale rule D2; delete the prose copies, keep one line in `writing-rules` |
| Passive voice / explicit subject | `writing-rules`, `sentence-word-guidance`, both blog skills | judgment rule J2 |
| "against" → "using" | `writing-rules`, Vale `AgainstPhrasing`, both blog skills | Vale only |
| Gerunds over nominalizations | `writing-rules`, `sentence-word-guidance` (verbatim copy) | judgment rule J3 |
| Filler phrases | `writing-rules`, `style-guide-overview`, `changelog-style-guide`, `blog-short-template` | Vale D4 (SPCA `Filler` covers part of it) |
| Glossary terms | `glossary`, `docs-checker`, `blog-short` 5c (partial copy), Vale `Terminology` (1 term), vocab reject (3) | Vale D1; `docs-checker` becomes a Vale wrapper or is deleted |
| `/* */` comments, `json` fences | `sentence-word-guidance`, `style-guide-overview`, `create-docs-example`, `blog-post-template`, 2 memories | script D11 |
| Scenario-first framing | `editorial-preferences`, `revise-doc-style` (copied) | judgment rule J4 |
| Doc link format | `style-guide-overview`, `changelog-style-guide`, `internal-doc-guidelines`, Vale `DocLinks` | Vale only |
| Image URL in `final/` | `style-guide-overview`, `concept-topic-template`, `integration-guide-template`, `changelog/structural-check`, memory | Vale D10 |
| Copy sibling parameter wording | `editorial-preferences`, memory `full-style-pass` | script D16 (detector), then judgment |
| Branch, commit, PR boilerplate | 5 skills, each different (C12, C13) | the `pr` skill, plus one shared snippet |
| `Sensible.WordList` and `Google.WordListCase` | both active | see V2 |

## 4. Vale rule audit

Verified by running Vale 3.25.1 on a probe file in `docs/`.

| # | finding | evidence | fix |
| - | ------- | -------- | --- |
| V1 | `AgainstPhrasing` needs at least one word between the verb and "against", so "classification against" passes | probe: `extracts data against` flagged; `classification against` not | `(?:\s+\S+)+` → `(?:\s+\S+)*` |
| V2 | `Sensible.WordList` is Google's list with `Google.WordList = NO`. "disabled" is flagged twice (with `Google.WordListCase`). It's full of Google-product swaps (Container Engine, Google I/O, omnibox), and `disabled → turn off` is wrong for parameter docs | probe: both rules fire on "is disabled by default" | prune to swaps that apply to Sensible; turn off `Google.WordListCase` or drop the duplicated keys |
| V3 | `Google.EmDash` says "Don't put a space before or after a dash". Its fix produces `processor—Sensible`, which still breaks the house rule. An unspaced em dash isn't flagged at all | probe | turn off `Google.EmDash`; add D2 |
| V4 | `WordList` swap `application: app` can never fire, because `accept.txt` has `[Aa]pplication` | probe: no alert | decide which wins and delete the other |
| V5 | `Sensible.Terminology` has 1 swap, and the glossary has 23 avoid-terms | | D1 |
| V6 | `Google.Parens` is 572 of about 1,500 alerts (suggestion level) | full run | the hook already filters it out (warning and above). Turn it off in CI too, or it buries the real alerts. |

## 5. What to make deterministic

The format follows your two examples. Deterministic rules settle with a pattern. Judgment rules use a pattern to find candidates and a question to decide them. I didn't include source quotes for judgment rules that resolve contradictions above, because the source has to be fixed first.

The **Where** column says which tool fits. Vale works for anything inside one sentence or line. A Tengo script under Vale (`extends: script`, as Shoalrun's DocShape uses) works for page shape. A Python script in `scripts/` works for cross-file checks.

### Deterministic: Vale

```yaml
id: sensible-glossary-terms                                   # D1
source:
  file: .claude/style-guide/glossary.md
  quote: When writing or reviewing any doc … use these terms consistently.
applies: prose sentences
check:
  kind: deterministic
  extends: substitution
  swap:
    '\bthe UI\b': the Sensible app
    '\bthe dashboard\b': the Sensible app
    '\b(?:extraction )?templates?\b': config|configuration        # allowlist the 2 alias pages via file-scoped .vale.ini sections
    'result objects?': output
    'repeating groups?': sections
    'free form (?=documents?|contracts?|forms?)': free-form
    'entirely free-form': entirely free form
    '(?:prompt context)': context
    '(?:data|field) types?': type
    '(?:object|key) path': dot notation
examples:
  fail: Open the dashboard and edit the extraction template.
  pass: Open the Sensible app and edit the config.
fix: apply the swap; docs-checker is then redundant
note: '"response", "segment", "section", "key", "empty" stay judgment (J5); each has a legitimate meaning'
```

```yaml
id: sensible-no-em-dash                                       # D2
source:
  file: .claude/style-guide/writing-rules.md
  heading: Em dashes
  quote: Do not use em dashes to join compound clauses. Split into two sentences instead.
applies: prose sentences
check:
  kind: deterministic
  extends: existence
  nonword: true
  tokens: ['—', '\s--\s']
examples:
  fail: Configure portfolio mode — Sensible can segment the file.
  pass: Configure portfolio mode. Sensible can segment the file.
fix: split into two sentences, or use a colon or parentheses for an aside. Replaces Google.EmDash.
```

```yaml
id: sensible-against-phrasing                                 # D3, a V1 fix of the existing rule
check:
  kind: deterministic
  tokens: ['(?:extract(?:s|ed|ing|ion)?|classif(?:ies|y|ied|ication))(?:\s+\S+){0,6}\s+against']
examples:
  fail: LLM-based attachment classification against specified document types
  pass: LLM-based attachment classification using specified document types
```

```yaml
id: sensible-filler                                           # D4
source:
  file: .claude/style-guide/writing-rules.md
  heading: Tone
  quote: 'Avoid: "please note that", "it''s important to remember", "it is worth mentioning"'
check:
  kind: deterministic
  extends: existence
  ignorecase: true
  tokens:
    - please note(?: that)?
    - it'?s important to (?:remember|note)
    - it is worth (?:mentioning|noting)
    - excited to announce
    - powerful new
    - seamless(?:ly)?
    - in this guide
    - this guide (?:will )?show(?:s)? you
examples:
  fail: Please note that the Stop parameter is optional.
  pass: The Stop parameter is optional.
fix: delete the phrase. Overlaps SPCA Filler and Voices; vendor those instead if they cover it.
```

```yaml
id: sensible-param-names-not-code                             # D5
source:
  file: .claude/style-guide/style-guide-overview.md
  heading: Method and feature names in prose
  quote: Never use camelCase with backticks for method or preprocessor names in running prose.
applies: prose sentences (raw scope, outside fences and tables)
check:
  kind: deterministic
  extends: existence
  scope: raw
  tokens: ['the `[a-z]+(?:[A-Z][a-z0-9]*)*` (?:method|preprocessor|parameter|object)']
examples:
  fail: the `customCompute` method
  pass: the Custom Compute method
fix: convert camelCase to spaced Title Case and drop the backticks
```

```yaml
id: sensible-param-cell-opener                                # D6
source:
  file: .claude/style-guide/sentence-word-guidance.md
  heading: description column
  quote: Don't start with "This parameter..." or "Use this to...".
applies: table.cell
check:
  kind: deterministic
  extends: existence
  scope: table.cell
  tokens: ['^(?:This parameter|Use this to)\b', '^Specifies the method type']
examples:
  fail: This parameter specifies the direction of the target data.
  pass: Specifies the direction of the target data relative to the anchor point.
```

```yaml
id: sensible-model-names                                      # D7
source:
  memory: feedback_anthropic_model_naming
  quote: Name Claude models the way Anthropic does … Never "Claude 5.5 Sonnet".
check:
  kind: deterministic
  extends: substitution
  swap:
    'Claude (\d(?:\.\d)?) (Opus|Sonnet|Haiku|Fable)': Claude $2 $1      # capture groups verified in Vale 3.25.1
examples:
  fail: Claude 4.5 Haiku
  pass: Claude Haiku 4.5
```

```yaml
id: sensible-product-ui-names                                 # D8
source:
  file: .claude/preferences/editorial-preferences.md
  quote: The tab that lists past extractions is called **Extraction history**
check:
  kind: deterministic
  extends: substitution
  swap:
    'Extractions history|Extractions tab': Extraction history
```

```yaml
id: sensible-image-syntax                                     # D9 (two rules, scoped by glob)
source:
  files: [style-guide-overview.md "Image format", changelog-style-guide.md "Images"]
check:
  kind: deterministic
  scope: raw
  docs: { token: '<Image\b', message: 'Use ![Click to enlarge](…) in docs pages.' }
  changelog: { token: '!\[[^\]]*\]\(', message: 'Use <Image alt="Click to enlarge" border={false} src="…" /> in changelogs.' }
```

```yaml
id: sensible-image-url                                        # D10
source:
  file: style-guide-overview.md
  quote: Images live in `assets/images/final/`. Use the GitHub raw URL on the `v0` branch.
check:
  kind: deterministic
  scope: raw
  tokens:
    - 'assets/images/screenshots/'                                     # memory: never point at screenshots/
    - '!\[(?!Click to enlarge\])[^\]]*\]\(https://raw'                 # alt text
    - 'raw\.githubusercontent\.com/(?!sensible-hq/sensible-docs/v0/)'  # wrong repo/branch
```

Also deterministic in Vale, one line each:

| id | rule | pattern |
| -- | ---- | ------- |
| D12 | `**Note:**`, not blockquote | raw `^> ` (prose files only) |
| D13 | Numbers: "90%", not "90 percent"; decimals, not fractions | `\b\d+ percent\b`, `\b(?:two|one)-(?:thirds?|tenths?|halves)\b` |
| D15 | Changelog heading types | raw `^## (?!(?:New feature|Improvement|UX improvements?|Deprecation): )`, plus a ban on `^## Update:` |
| D17 | No draft slugs, wrapped doc links | already done (`NoDraftLinks`, `DocLinks`) |
| D18 | Latin abbreviations | already done (`Google.Latin`). Also lint `.claude/style-guide/**` with this one rule, so the guides stop teaching it (C10). |
| D19 | Excerpt filler openers | `scope: frontmatter.excerpt` (works in Vale 3.25, as Shoalrun's `SummaryLength` does), tokens `^(?:Learn how to|How .+ works)` |

### Deterministic: scripts (page shape and cross-file checks)

| id | rule | source | how |
| -- | ---- | ------ | --- |
| D11 | No ` ```json5 ` fences in `docs/`. No `//` comments inside `json` fences. The JSON5 header comment appears once per page, on the first commented block | 2 memories, `json5-comments-reference` | Tengo (fence-tracking, as `ShoalrunTypeBoundary.tengo` does) or Python |
| D14 | Reference page shape: frontmatter → opening paragraph → `# Parameters` → `# Examples` → optional `# Notes`. Jump links only to sections that exist, with `\` line breaks. Table header `\| key \| value \| description \|` | `style-guide-overview`, `reference-topic-template` | Tengo, like DocShape `Structure` |
| D16 | Parameter description drift: the same `key` on two pages with different descriptions | `editorial-preferences` ("copy existing wording precisely") | Python: index every parameter table, report pairs under a similarity threshold. Its output becomes the candidate list for a judgment check ("same implementation?"), because only the engine knows. |
| D20 | Excerpt length ≤160 and `excerpt == metadata.description` | memory `excerpt-rules` | already done: `scripts/descriptions/` plus `generate-descriptions.yml`. List it in the guides so agents run it. |
| D21 | Excerpt doesn't name its own page | memory `excerpt-rules` | Python: lowercased `title` tokens in `excerpt`. Deterministic, because it needs only the title, not judgment. |
| D22 | New page registered in `_order.yaml` and its category `index.md` | `create-new-doc`, `create-concept-doc` | Python: every `.md` under `docs/` appears in its `_order.yaml` |
| D23 | Canonical JSON5 comments | `json5-comments-reference`, `json5-commenter` | The skill says "verbatim only, don't invent": a key lookup. Make the reference a JSON map and the skill a script, leaving the LLM only "notably different behavior?" (J7). |
| D24 | Changelog: each `##` section has a `doc:`/`reference:` link; intro starts "In the last month, Sensible"; intro has no links | `structural-check.md` steps 1–3, changelog guide | Tengo or Python; steps 1–3 of `structural-check` are already pattern checks run by an LLM |
| D25 | Blog length 400–600 words | `blog-short-template` | `wc`; Vale `occurrence` with `scope: text` |

### Judgment: detector plus question

These stay for the judge. Vale finds candidates; the judge decides.

```yaml
id: sensible-opening-sentence                                 # J1, after C1 is resolved
applies: first body paragraph of docs/Senseml reference/**
check:
  kind: judgment
  detector: first sentence after frontmatter (Tengo) not matching '^[A-Z][a-z]+s\b'
  precheck: skip index.md and pages whose first block is a **Note:** callout
  question:
    type: choice
    ask: Does the first sentence state what the feature does, in third-person present?
    criteria:
      third-person: '"Extracts lines near the anchor."'
      use-this: '"Use this method to…": allowed only when the user supplies the input (extra-data)'
      mechanism: '"Returns a value from…": rewrite'
examples:
  fail: Returns a value from an extra_data object you supply.
  pass: Extracts a value you supply at request time, so you can validate and transform output.
```

```yaml
id: sensible-explicit-actor                                   # J2, your active-voice rule plus the C2 boundary
check:
  kind: judgment
  detector: '\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b'
  precheck: skip table cells in the value column and "is enabled/disabled by default"
  question:
    type: choice
    ask: Who performs the action, and is it named?
    criteria:
      user-hidden: the user acts but isn't named ("when Anthropic is configured") → "you"
      sensible-hidden: the platform acts but isn't named ("documents are classified") → "Sensible"
      adjective: the participle describes a state
```

| id | rule | detector | question |
| -- | ---- | -------- | -------- |
| J3 | Gerunds over nominalizations | `\bthe \w+(?:tion|ment|ance)s? of\b` | Is this a nominalized verb the sentence could use as a gerund? |
| J4 | Scenario-first framing | first sentence of a new section contains `spec\|config\|parameter\|matcher\|selector` | Does it lead with configuration before the reader's situation? |
| J5 | Glossary terms that need context | `\b(?:response\|segment\|key\|empty\|section)s?\b` | API envelope or SenseML term (OK), or a synonym for output/chunk/field/null? |
| J6 | Table for non-configurable values | table in a new diff whose header lacks `key` | Can the user set these values through the API or the app? |
| J7 | Re-comment a parameter | D23 finds a parameter already commented earlier on the page | Does this block show different behavior? |
| J8 | Label method in lists | `\bLabel\b` in a series with other method names | New text listing sibling methods? Then drop Label. |
| J9 | Free-form hyphenation | `free[- ]form` | Attributive or predicative? |
| J10 | Integrate rather than create a heading | a new `###` in a diff with fewer than 3 paragraphs under it | Does this extend an existing section? |

### What stays prose

Some rules carry an editorial reason, and no detector exists for them: compare features only when the reader has a choice; use realistic example data; focus on new capability, not removed friction; lead a changelog entry with the UI. Keep these in `editorial-preferences.md` as directives with their "why". That file already has the format Shoalrun recommends: rule, reason, example.

## 6. Shoalrun mapping (`my-docs`)

What the port has today: `.vale.ini` with Voices, Direct, DocShape, and SPCA, scoped to `content/**`. The `vale-changed` audit test lints only new or edited pages. `frontmatter.taxonomy` comes from a generated map, plus `search.synonyms`. `docs.config.yaml` has **no `authoring` block yet**. That block is the biggest unused feature.

| content now in sensible-docs | Shoalrun feature | deterministic? | notes |
| ---------------------------- | ---------------- | -------------- | ----- |
| `writing-rules`, `sentence-word-guidance`, `style-guide-overview` | `authoring.guideFiles` | no: guidance an agent reads | `docs project --section guidance` returns them with digests, so an agent can't use a stale copy. That replaces the "read these files" step in five skills. |
| `editorial-preferences`, `friction-log`, style memories | `authoring.directives` | no | Short rules with reasons go in `directives`. Memory is Claude-only and per machine; directives travel with the repo. |
| Exemplar lists hard-coded in `create-concept-doc`, "closest sibling" | `authoring.exemplarFiles` | no | One list, per page type. Shoalrun's guide warns against cross-type exemplars ("an API reference is a poor model for an explanation"), which is the same reason `create-concept-doc` picks by topic shape. |
| `reference-topic-template`, `concept-topic-template`, `integration-guide-template` | `templates` + `shoalrun scaffold <template>` | **yes** | Templates become scaffolds with required fields and `[[TODO]]` placeholders. **The compiler fails a public page with an unresolved `[[TODO]]`**, so `revise-doc-style`'s "leave TODOs, report them" rule is enforced for free. |
| Page section order, heading levels, jump links (D14) | DocShape `Structure` (Tengo) + `TypeBoundary` | **yes** | Copy `ShoalrunStructure.tengo` as the base for a `reference` structure script. `TypeBoundary` already flags reference pages containing steps, which is the concept/reference split that `create-concept-doc` routes on. |
| Table introduced by a sentence | DocShape `TableIntroduction` | **yes** | Already measured: 8 findings on 4 pages. The standard "**Note:** For additional parameters…" sentence satisfies it. |
| Frontmatter template (`deprecated`, `hidden`, `robots`, `next`) | `frontmatter.defaults` / `frontmatter.enforced` + `frontmatter.schema.json` | **yes** | Constant fields move to defaults, so agents stop writing them. Enforced values override pages. |
| Excerpt ≤160, no filler opener (D19, D20) | DocShape `SummaryLength` (`scope: frontmatter.summary`, max 160) | **yes** | The import already makes `description` equal `summary` (D19 in `plans/decisions.md`). Add D19's tokens on the same scope. |
| Excerpt names its own page (D21) | Vale script on `frontmatter` | **yes** | Tengo can read `title` and `summary` from the same raw header, as `TypeBoundary` reads `type`. |
| SEO aliases ("parse" only as a defined alias on 2 pages) | `search.synonyms` | **yes** | Synonyms in search, rather than in prose. Then Vale can ban "parse" and "template" everywhere with no per-page exceptions. |
| `doc:` link format, draft slugs (`DocLinks`, `NoDraftLinks`) | page `id` links + `audit.links: true` | **yes** | The compiler resolves links by stable ID; broken or draft targets fail the audit. Both Sensible rules become unnecessary there. |
| `_order.yaml` / `index.md` registration (D22) | `navigation` config + `docs validate` | **yes** | The nav comes from config. Validation reports a page left out of navigation. |
| `docs-checker`, glossary (D1) | `audit.tests` → Vale | **yes** | Same Vale rule, run by `vale-changed`. |
| Doc Detective code tests, fingerprint/portfolio doc tests | `audit.tests` | **yes** | Already planned (D17, D22 in `plans/decisions.md`); the markers stay in sensible-docs. |
| `mcp-search-eval` | `audit.evals` (`eval prepare` / `eval check`) | partly | Shoalrun checks the task file and the reviewed results against the build; you run the agent. It replaces the skill's own scoring scaffolding. |
| `update`-date rule | Shoalrun author skill ("set `updated` to the edit date") + DocShape `Structure` | **yes** | 103 pages lack `updated:`; the plan derives it from git. |
| Changelog (D15, D24) | changelog identifier (`date` / `releaseVersion`) + a custom template | partly | Out of the port's scope today (SenseML reference only). |
| Edit-time Vale (hook) | none in Shoalrun | n/a | Vale's Claude Code plugin in my-docs, `.claude/hooks/vale-check.sh` here. Same idea. |
| Prose judgment (J1–J10) | none | no | Shoalrun "doesn't load these files into a model or run the instructions". Jev stays the judge; Shoalrun supplies the inputs (guides, exemplars, `docs validate` report). |

## 7. Correction inventory

Every place a correction you made has been written down, with each entry triaged to the place it should live. This is the intake list for new rules. Draft deterministic rules from here, not from the style guides: the guides describe March, and these entries describe what actually went wrong after that (see [Timeline](#timeline-when-each-piece-was-written)).

**Destinations:**

- **Vale**: a rule in `.github/styles/Sensible/`.
- **script**: a check in `scripts/`, run by the hook or CI.
- **judgment**: a J-rule for Jev.
- **guide**: a sentence in a style guide or template.
- **skill**: a step or gate in a skill.
- **process**: how you or Claude work, with no doc output to check.
- **drop**: duplicate, or done.

**Status:**

- **encoded**: a check enforces it.
- **prose**: written in a repo guide or skill, but not checked.
- **memory**: lives only in Claude's memory.
- **log**: lives only in a friction log or session file.

### Sources

| source | entries | where |
| ------ | ------: | ----- |
| Claude memory, sensible-docs project | 20 | `~/.claude/projects/-home-franc-GitHub-sensible-docs/memory/` (not in the repo) |
| Style friction log | 1 | `.claude/style-guide/friction-log.md` |
| Changelog friction log | 8 | `.claude/skills/changelog/friction-log.md` |
| Blog friction log + intro feedback | 10 | `.claude/skills/blog-how-to-parse-x/friction-log.md`, `intro-rewrite-feedback.md` |
| Session friction logs | 12 | `.claude/sessions/xml-postprocessor-docs/`, `2026-07-02-region-asImage/` |
| Your recorded edits | 3 sessions | `.claude/sessions/*/frances-edits.md` (region-asImage, actor, changelog-july) |
| Unfinished rule plan | 1 | `.claude/sessions/vale-method-names/plan.md` |
| Revision commits (unlabeled) | 257 | `design/style-baseline/revisions.csv` |
| Editorial preferences log | 6 | `.claude/preferences/editorial-preferences.md` (rules already in §2–§5) |

### Claude memory

| memory | destination | rule | status | note |
| ------ | ----------- | ---- | ------ | ---- |
| `you-centric-style` | guide + judgment | C1, C2 → J1, J2 | memory | Contradicts `revise-doc-style`; the same correction also appears in the xml-postprocessor session log (#5). Resolve in `writing-rules.md`. |
| `excerpt-rules` | Vale + script + guide | D19, D20, D21; C4 | partly encoded | Length is checked (`scripts/descriptions/`); mood, self-naming, and filler aren't. Templates still say `excerpt: ''`. |
| `seo-terminology` | Vale + Shoalrun | D1, `search.synonyms` | partly encoded | "parse" is in `reject.txt`; "template" isn't. |
| `block-comments-only` | script | D11 | prose | Guides were updated in the fingerprint session; nothing checks code blocks. The memory's claim that `sentence-word-guidance` says `//` is stale (C14). |
| `keep-code-fence-language` | script + guide | D11 | memory | **No repo guide says it.** Worse, `json5-comments-reference.md` itself uses ` ```json5 ` fences (lines 19–79), so the file `json5-commenter` reads models the banned fence. |
| `anthropic-model-naming` | Vale | D7 | memory | |
| `label-method-near-deprecated` | judgment | J8 | memory | |
| `image-processing` (point at `final/`, copy into it) | Vale + script | D10; new D30 | prose | D10 checks the path. D30 checks that each referenced image exists in `screenshots/` or `final/`. |
| `full-style-pass` | process → drop | | memory | Exists because nothing ran the checks. Drop it once the hook and CI run the D and J rules. |
| `brief-naming` | script | new D31 | memory | `.claude/briefs/` files match `brief-*.md`. Trivial. |
| `blog_post_template` | drop | | memory | Duplicates `.claude/style-guide/blog-post-template.md`; two copies will drift. |
| `worktree-flow`, `worktree-session-link`, `checklists-to-file`, `session-checklist-id` | skill | C12 | memory | Belong in the shared PR/branch snippet the doc skills call. |
| `no-api-reference-markdown` | script + hook | new C17 | memory | **The Vale hook lints `reference/**/*.md`, which is generated**, so it asks the agent to fix files it must not edit. Lint the JSON spec descriptions instead (D29). |
| `jq-for-json-schema-extraction` | skill | | memory | `api-spec` tooling. |
| `test-api-key` | process | | memory | Not style. |
| `no-agpl` | process | | memory | Not style; a license check could be a script later. |
| `vale-setup` | constraint | | memory | "No new Vale integrations": applies to §8 step 3. Add rules to the existing CI job and hook, not new runners. |

### Friction logs

| entry | destination | rule | status | note |
| ----- | ----------- | ---- | ------ | ---- |
| style #1: open with what the user does, not "Returns a…" | judgment | C1 → J1 | log | |
| changelog #1: doc links missing | script | D24 | prose (LLM `structural-check`) | |
| changelog #2: image format | Vale | D9 | prose (LLM `structural-check`) | |
| changelog #3: categorization was session-only | skill | | encoded as `references/categorization-rules.md` | |
| changelog #4: template is post-draft | skill / Shoalrun | `scaffold` | log | The fix the log proposes (entry templates up front) is exactly what Shoalrun `scaffold` does. |
| changelog #5: "docs PR exists" isn't `document` | script | new D32 | log | `gh` query: open docs PR, not merged → `investigate`. |
| changelog #6: touched feature has no public page | script → judgment | new D33 | log | Detector: grep `docs/` for the method or parameter the PR touches; no hit → `investigate`. |
| changelog #7: "interim / hack / not ready" signals | script | new D34 | log | Pure keyword detector on the PR body: `interim\|hack\|workaround\|not ready\|step 1 of`. |
| changelog #8: mixed PRs need split dispositions | judgment | | log | |
| blog: invented output blocks | script | new D27 | log (skill step) | Every output block must equal the saved extraction for its config. Also checks the `{"type", "value"}` shape. |
| blog: sections flattened in the field summary | skill | | log | |
| blog: config files lost inline comments | script | | encoded (`extract_config_from_draft.py`) | |
| blog: golden re-upload is fatal | script | | log | A bug in `upload_pr_extractor.py`. |
| blog: wrong app URL / URL not shown | skill | | log | A blocking checkpoint in the skill. |
| blog: Notion drops content after `<!-- -->` | script | | log | Strip HTML comments before the Notion call. |
| blog: Notion doesn't highlight long blocks | drop | | log | Notion limit. |
| blog: "two objects per array" impossible | guide | | log | Soften in `blog-post-template.md`. |
| blog intro: 3-paragraph structure | guide + script | new D35 | log | P2 must contain the "hybrid deterministic and LLM-based" boilerplate: a fixed string. |
| xml #1–2: misread PR comment target | skill | | log | Read the comment's `line` field. |
| xml #3–4: `open()` newline, `sed` with backticks | process | | log | Tooling habits. |
| xml #5: style pass flipped "you" to "Sensible" | judgment | C1, C2 | log | Same as `you-centric-style`. |
| xml #6: link to the parent index page | judgment | new J11 | log | Detector: a link changed to a child page of a renamed section. |
| xml #7: article doesn't match link noun | Vale | new D36 | log | `\ba \[[^\]]*s\]\(doc:` (article "a" before a plural link text). |
| xml #8: `attrs` example hardcodes a constant | judgment | new J12 | log | Detector: `"attrs"` with a literal value in a code block. |
| region #1: paraphrased sibling wording | script → judgment | D16 | log + `editorial-preferences` | |
| region #2: consolidate edits by file | process | | log | |
| region #3: Vale failed (Google style not synced) | script | | encoded (`scripts/vale-doctor.sh`) | |
| region #4: session artifacts belong in the repo, not memory | process | | log | **Contradicts current practice**: the 20 memories above are that. |

### Your recorded edits (`frances-edits.md`)

| edit | destination | rule | note |
| ---- | ----------- | ---- | ---- |
| "Cognito users", "reprocessing", "auth tokens" → user-facing names | Vale | new D26 | A ban list of internal implementation terms: `Cognito`, `reprocessing`, `Lambda`, `S3 bucket`, `worker`, `auth token`. Grow it from engine PR vocabulary. |
| `this is <value>` → `the value is "<value>"` in schema descriptions | script | new D29 | Lint `reference/*.json` description strings (extract, then run Vale). Today nothing lints the source of the API reference. |
| `asImage`: mechanism-first → scenario-first | judgment | J4 | |
| "end-user to review" → "human to interpret" | judgment | | Too specific for a rule; keep as an exemplar pair. |
| query-group table column widths normalized | script | new D28 | A Markdown table formatter in the hook. Formatting is never worth a review comment. |
| "SenseML config editor" → "SenseML editor"; "Template library" tab | Vale | D1, D8 | Add to the glossary and UI-names swaps. |
| changelog: lead with the UI, then the API | judgment | | Already in `editorial-preferences`. |

### Unfinished rule plan

`vale-method-names/plan.md` stalled on "Vale cannot distinguish inline code in a paragraph from inline code in a table cell". D5 sidesteps that: it matches the prose phrase ``the `x` method/parameter``, which never occurs in a table's key column. So the plan's four options aren't needed. Fold the plan into D5 and close the session.

### New rules this inventory adds

| id | rule | where |
| -- | ---- | ----- |
| D26 | Internal implementation terms | Vale `existence` |
| D27 | Output blocks equal the saved extraction | script (blog drafts; docs already have Doc Detective) |
| D28 | Markdown table formatting | formatter in the hook |
| D29 | Lint OpenAPI description strings | script → Vale |
| D30 | Referenced images exist | script |
| D31 | Brief file naming | script |
| D32–D34 | Changelog categorization signals | script in `categorize-pr` |
| D35 | Blog intro boilerplate present | script |
| D36 | Article agrees with plural link text | Vale |
| C17 | The hook lints generated `reference/**/*.md` | hook fix: lint `docs/` and the JSON specs |
| J11 | Link to the durable parent page | judgment |
| J12 | Examples pull values with `var` | judgment |

### Tally

53 entries in the tables above. Not counted: the unlabeled revisions, and the editorial-preferences rules, which are already in §2–§5. Each entry is counted once, under its main destination:

| destination | entries | enforced today |
| ----------- | ------: | -------------: |
| Vale or script (deterministic) | 26 | 2 fully, 2 partly |
| judgment | 10 | 0 |
| guide or template edit | 1 | 0 |
| skill step | 7 | 1 |
| process or drop | 9 | n/a |

So half of the corrections you've recorded could be deterministic, and only 2 of those 26 are fully enforced. The labeled `revisions.csv` adds the corrections nobody wrote down.

### Keeping it current

Until the cleanup is done, a new correction goes into this table, not into memory or a new friction log. Each entry gets its destination, rule ID, and status at the time you write it down. A memory can stay as a one-line pointer to its rule. The share of entries with status `encoded` is a guidance-health metric for the evals (`style-baseline/README.md`, layer 4).

## 8. Enforcement: what can make an agent follow the rules

A rule is only as strong as what enforces it. This section records which Claude Code mechanisms are deterministic, which are only instructions, and what has been verified on this machine. **Verified** means a spike or working config in `sensible-docs-gen` or this repo shows it. **Unverified** means documented or believed, but not yet tested here. Spike it before relying on it.

### Skills are text

Invoking a skill is one tool call (`Skill`). Everything inside `SKILL.md` is instructions the model reads and chooses to follow. A skill can't make a tool call happen: "Read `glossary.md`" or "run `scripts/x.py`" in a skill can be skipped, and the `full-style-pass` memory exists because they were. Steps that must happen have to move into the layer around the skill.

| mechanism | what it does | deterministic? | status |
| --------- | ------------ | -------------- | ------ |
| Agent frontmatter `skills:` | Loads the skill's content into a subagent at start. The agent doesn't choose to read it. | yes | verified: `sensible-docs-gen/.claude/agents/doc-writer.md` (`skills: [sensible-docs-style]`) |
| Agent frontmatter `hooks:` | Hooks scoped to one subagent | yes | verified: `doc-planner.md`, `doc-writer.md` (`PreToolUse` on `SubagentHandback`) |
| Agent frontmatter `tools:` | Refuses tools not on the list | yes | verified: M1 spike H5 |
| Skill frontmatter `allowed-tools` | Limits and pre-approves tools while the skill runs. Restricts calls; can't require one. | yes, for restriction | in use (`update-docs-from-pr` and others) |
| Skill frontmatter `hooks:` | Hooks active only while the skill runs | yes | **unverified**; no skill here uses it |
| `` !`command` `` in a skill | Runs a shell command when the skill loads and inlines its output, so "run the script" has already happened | yes | **unverified**; no skill here uses it |
| Hook `additionalContext` | A hook adds text to the agent's context | yes | verified: `sensible-docs-gen/report/budget_hook.py` |
| Hook `updatedInput` (`PreToolUse`) | Rewrites a tool call's input before it runs, such as an automatic Vale fix | yes | **unverified** |

**Consequence:** the doc-writing workflows (`update-docs-from-pr`, `create-new-doc`, `update-existing-doc`, `create-concept-doc`) are stronger as subagents with `skills:` for guidance, `tools:` for limits, and a handback gate for checks. `sensible-docs-gen` already made this move. Leave only judgment in the prose.

### Hooks see tool calls, not intent

Hooks receive the tool call (`tool_input`), the agent (`agent_id`, `agent_type`; verified in M1 H3), and `transcript_path`. So a hook can enforce any step that leaves a tool call behind, and nothing else.

| want | how | note |
| ---- | --- | ---- |
| "Read every style guide" | A `PreToolUse` gate on `git commit` / `gh pr create` parses the transcript for a full Read of each required file since the `Skill` call, and denies with a reason if one is missing | A Read with `limit` is still a Read; require the whole file, as `sensible-docs-gen` check I3 does. **Reading doesn't prove applying**: the xml-postprocessor PR ran the full style pass and applied the wrong rule. |
| "Check the output passes" | The same gate runs the D-rules and Jev on the J-rules, and denies until they pass | **Prefer this.** It enforces the result reading was meant to produce, and works even while guides contradict each other. |
| Keep a subagent working until it passes | `PreToolUse` on `SubagentHandback` in the agent's frontmatter | verified (M1 H1b). A `Stop` hook doesn't hold a subagent: it fires after the handback (M1 H1, failed). |
| Keep the main session working until it passes | Blocking `Stop` hook | **unverified** here |
| Measure compliance after a run | Parse the run log (`sensible-docs-gen` I3, I4) | an eval metric, not a gate |

Use read gates only where the output can't show the step happened, such as "read the sibling page before writing a shared parameter". Even that becomes an output check once D16 exists.

### Vale while the agent writes

The earliest a hook can see text is the tool call that writes it. Prose drafted in chat and pasted in later is invisible until the write.

| stage | hook | enforces | status |
| ----- | ---- | -------- | ------ |
| before each write | `PreToolUse` on Edit/Write: rebuild the file with the edit applied, run Vale on a copy at the same repo path, keep alerts inside `new_string`, **deny** on error-level alerts with the fix | high-precision D-rules only, each with fixture tests (eval layer 3). A false positive here stalls the agent. | proposed |
| after each write | `PostToolUse`: feedback on **changed lines only** | warnings and broader D-rules | exists (`.claude/hooks/vale-check.sh`) but lints the whole file; port the changed-lines filter from `sensible-docs-gen/validators/__init__.py:243` |
| at commit or handback | gate | all D-rules, plus Jev on the J-rules | proposed |

Design notes for the pre-write hook:

- **Loop guard.** After 3 denials on the same file, allow the edit and report it for the end gate.
- **Automatic fixes.** If `updatedInput` works, unambiguous one-to-one swaps (D7, Latin abbreviations) can be applied silently and logged. Everything else is denied with a reason.
- **One integration.** The `vale-setup` memory records Vale as deliberately one `PostToolUse` hook plus CI. Either fold the pre-write check into that one hook script, or record the change of decision.
- **Scope.** Lint `docs/` and the JSON spec descriptions (D29), not the generated `reference/**/*.md` (C17). Deciding on `drafts/` (blogs) is part of the same `vale-setup` decision.
- **Subagents.** Settings hooks fire on subagent writes (M1 H3), so one hook covers both.

### Spikes needed

Each is small and modelled on M1: a fixture repo and `claude -p`, asserting harness behavior only.

1. A `hooks:` block in skill frontmatter fires while the skill runs, and not after.
2. `` !`command` `` output is inlined when a skill loads.
3. `PreToolUse` `updatedInput` rewrites an Edit's `new_string`.
4. A blocking `Stop` hook keeps the main session working.
5. `PreToolUse` fires on the `Skill` tool, so a hook can inject guide sections as `additionalContext` when a doc skill starts.

## 9. Order of work

1. **Resolve C1–C6 in the guide files** (1–2 hours). The detectors are useless while the rules disagree. Commit the resolution in the guides themselves, not in memory.
2. **Fix V1–V4 and add D1–D4** in `.github/styles/Sensible/`. Run the full corpus before and after, and paste the counts into the PR.
3. **Remove the three `mcp__vale__check_file` steps.** Replace them with `vale <file>` in Bash. Widening the hook to `drafts/` is the other option. It changes the one existing integration, so check it against the `vale-setup` memory first.
4. **Fix C17.** Stop the hook from linting generated `reference/**/*.md`, and add D29 to lint the JSON specs instead.
5. **Delete `docs-checker`**, or make it a thin `vale --filter` wrapper. Point `changelog` step 5 at Vale.
6. **Scripts D11, D14, D21, D22, D26–D30** in `scripts/style/`, run by the hook and CI.
7. **In `my-docs`:** add the `authoring` block (`directives`, `guideFiles`, `exemplarFiles`), a `reference` scaffold, and the Sensible Vale style next to DocShape.
8. **Hooks** (section 8): port the changed-lines filter into `vale-check.sh` first (about an hour). Then run spikes 1–5. Then add the pre-write gate for D1–D4 once their fixtures exist, and the commit/handback gate.
9. **Judgment rules** last, as YAML specs in `.github/styles/Sensible/judgment/`, for Jev to read.

Measure the effect with [style-baseline/README.md](style-baseline/README.md): the baseline is recorded there, and the evals rerun after each step.
