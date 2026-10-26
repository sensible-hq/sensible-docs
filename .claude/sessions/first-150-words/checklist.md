# First 150 words

Claude Code session name: seo
Claude Code session ID: c14f96d2-faef-4dbe-8951-0d7f13df161c
Branch: first-150-words (worktree: ~/GitHub/sensible-docs-first-150-words), draft PR #763
Related: issue #722; follows PR #758 (seo-keywords: excerpts, phrase research) and PR #762 (merged)

## Goal

The first 150 words of each page's content explain exactly what the page covers, so human and agent
readers can tell whether the page is for them.

## Inputs

- `first-lines-draft.md`: per page, current excerpt, ui-docs short description (only #10
  Intersection), and the current first 150 words. Built by `build_first_lines.py` from `pages.json`
  (page list snapshot of PR #758's `keywords-draft.md`). Rerun the script to refresh.
- From PR #758 (`.claude/sessions/seo/` on branch seo-keywords; on v0 once merged): best phrases per page
  (`keywords-draft.md`) and terminology decisions (checklist). Background research (other docs
  sites, a best-practice reference for openings) is kept in a private Notion page, not in this repo.

## Order of operations

- [x] (2026-10-20: #758 merged as e305803; v0 merged in; draft rebuilt. First 150 words changed on
      #1, #3, #25, #27 only; those 4 re-graded.) Wait for PR #758 to merge, then merge `origin/v0` into this branch and rerun
      `build_first_lines.py` (until then the draft shows pre-#758 excerpts and openings; #758 edited the
      openings of overview, getting-started-email, getting-started, library-quickstart, author,
      choosing-an-endpoint, ocr-level, so rewriting before the merge would conflict)
- [x] Voice of the first body sentence: keep the house rule for now (decided 2026-10-20; may revisit).
      `revise-doc-style`: first sentence is third-person present ("Removes…", not "Use this to
      remove…"). Excerpts stay imperative; these are different fields.
- [x] Grade all 42 pages against the rubric (2026-10-20): `grades.md` (rendered by `render_grades.py`
      from `grades.json`; 5 grading subagents). Averages: A (explicit first paragraph) 1.0, B (plain
      title) 1.5, C (focus) 1.8, D (first 150 words) 1.4. Only #38 API quickstart scored 8/8; 37 of 42
      pages score 1 on A: openings say what the thing does, not what the page covers or what you'll be
      able to do. Lowest (4/8): #13 Query group, #17 Fingerprint, #31 SenseML reference intro,
      #32 Layout-based methods, #35 Types.
  - Fan-in notes: some suggested fixes conflict with decisions: #25 suggests a title with
    "templates" (config, not template); retitles (#17, #21, #25, #26, #27, #35) are out of scope for
    first-150-words unless the user wants them; #3 suggests splitting the tutorial (focus).
  - Body bugs found while grading (fix separately): #40 custom-computation.md has two `# Examples`
    H1s; #13 query-group.md has both `# Parameters` and `## Parameters`; #21 confidence.md says
    "Sensible support confidence signals" (should be "supports").
- [ ] Propose rewrites for all 42 openings (2026-10-26: user asked for proposals for every page;
      5 writer agents by topic batch, then an independent rubric grader; stored in `proposals.json`,
      rendered into `first-lines-draft.md` by `build_first_lines.py`)
- [ ] User review; apply

## Execution plan: per-page edits (agreed 2026-10-20)

Fan-out / fan-in with subagents, one topic group per agent (10 groups, 3–7 pages each).

- [ ] Shared inputs for every agent:
  - phrase-ownership map (which page owns which best phrase; non-owners don't use it)
  - opening pattern: sentence 1 defines the thing with search terms; sentence 2 says what
    problem it solves
  - terminology rules: "extract," not "parse"; "config," not "template" (defined aliases only where
    already added)
  - no self-naming filler; the page's opening should say what the reader gets and who it's for
  - first body sentence: third-person present per `revise-doc-style` ("Extracts…"), unlike excerpts
  - style rules: all `.claude/style-guide/` files, you-centric prose, `/* */` comments only in code,
    don't mention Label method, keep existing fence languages
  - exact scope of allowed edits (first ~150 words only); nothing else touched
- [ ] Fan-out: each agent edits only its own pages and writes a per-page change rationale; no
      agent edits shared files (checklist, draft)
- [ ] Fan-in (main session): check best-phrase collisions across pages; check new factual claims;
      check line endings and diff size (a one-sentence edit once converted a whole file's CRLF);
      run Vale; full style pass for one voice; present one consolidated summary
- [ ] Pilot one batch first; user reviews; tune the prompt; then run the remaining batches

## Carried over from PR #758 (2026-10-20)

- [ ] Evaluate the `ui-docs` branch (PR #660, worktree `~/GitHub/sensible-docs-ui-docs`, last
      commit 2026-08-12) for material to rework method docs, especially their first ~150 words.
      Contents: `assets/ai/mini-pages/box.md` and `intersection.md` (short-form method pages:
      plain-language description, annotated syntax example, link to full docs),
      `assets/ai/senseml-descriptions.json` (task-focused one-liners per method and per parameter
      for box, intersection, checkbox, nearestCheckbox), plus a session checklist and friction log
      under `.claude/sessions/2026-08-10-ui-hover-descriptions/`. Promising: the Intersection
      mini-page opens with "Finds and extracts the value at the point where a row and a column
      cross in a table, like looking up a cell in a spreadsheet... More reliable than the Row method
      when a table has unpredictably empty cells", which already hits #10's target phrases (table
      cell lookup, empty table cells) better than the live page's opening.
- [ ] Ask ReadMe support how to enable `agentSearch` / `projectSearch`
- [ ] #42 (spec-generated): find which OpenAPI field ReadMe uses for the meta description and
      llms.txt description (the page has no excerpt; `summary` is also the page title, so the start
      of `description` is likelier) before editing `reference/openapi_extraction.json`
- [ ] Excerpts that run ahead of their page body (update the first ~150 words to match when
      applying): #3 "template-based" (page never says "template"), #11 "variable positions",
      "keyword", "landmark", #19 "split" (page says "segment"), #28 scanned/handwritten framing
- [ ] Optional: before/after `mcp-search-eval` on a handful of pages

### Tooling that writes excerpts

- [ ] Update skills, templates, and scripts that write excerpts/descriptions so they follow the excerpt
      rules (no self-naming: never name the page's own method/object/preprocessor/setting; imperative
      mood; no "Learn how to" filler; <= 150 chars; "extract" not "parse"). Known places:
  - `scripts/descriptions/generate_excerpts.py` `PROMPT` (CI generates missing excerpts with Claude)
  - `.claude/skills/revise-doc-style/SKILL.md` "metadata.description" section (should say excerpt is
    the source of truth)
  - `.claude/style-guide/style-guide-overview.md` (still says `metadata.description` is a 4–7 word phrase)
  - `.claude/skills/api-spec/SKILL.md` (copies spec `description` into `excerpt`; spec descriptions can
    self-name)
  - `.claude/style-guide/*-template.md` (`excerpt: ''` placeholders; add a one-line rule comment?)
  - check `create-new-doc`, `create-concept-doc`, `update-docs-from-pr`, `update-existing-doc` for
    excerpt guidance
- (Decided above: first body sentences keep `revise-doc-style`'s third-person house rule.)
