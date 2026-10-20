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
  (`keywords-draft.md`), competitor research (`competitors/`), Payabli best-practice reference
  (`best-practice/payabli.md`), terminology decisions (checklist).

## Order of operations

- [ ] Wait for PR #758 to merge, then merge `origin/v0` into this branch and rerun
      `build_first_lines.py` (until then the draft shows pre-#758 excerpts and openings; #758 edited the
      openings of overview, getting-started-email, getting-started, library-quickstart, author,
      choosing-an-endpoint, ocr-level, so rewriting before the merge would conflict)
- [x] Voice of the first body sentence: keep the house rule for now (decided 2026-10-20; may revisit).
      `revise-doc-style`: first sentence is third-person present ("Removes…", not "Use this to
      remove…"). Excerpts stay imperative; these are different fields.
- [ ] Propose rewrites (fan-out by topic group; pilot one group first; plan below)
- [ ] User review; apply

## Execution plan: per-page edits (agreed 2026-10-20)

Fan-out / fan-in with subagents, one topic group per agent (10 groups, 3–7 pages each).

- [ ] Shared inputs for every agent:
  - phrase-ownership map (which page owns which best phrase; non-owners don't use it)
  - Payabli opening pattern: sentence 1 defines the thing with search terms; sentence 2 says what
    problem it solves (`best-practice/payabli.md`)
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
