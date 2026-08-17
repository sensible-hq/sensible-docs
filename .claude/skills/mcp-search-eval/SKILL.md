---
name: mcp-search-eval
description: Evaluates the mcp__sensible-docs search tool's ability to surface relevant docs for a set of questions. Runs subagents (one per question) to search, fetch, and synthesize answers, then compiles a scored results table. Invoke whenever the user wants to run or re-run the MCP search eval, test doc coverage, or check whether the search tool surfaces the right pages for a question set.
---

# MCP Search Eval

Runs the Sensible docs MCP search evaluation: one subagent per question searches the docs MCP, fetches results, synthesizes an answer, and saves artifacts. Results are compiled into a scored table.

## What this actually is

This is a **structured retrieval audit with LLM-as-judge scoring** — not a true eval in the ML sense yet.

What makes it eval-like:
- Fixed question bank (30 questions, stable across runs)
- Numeric scoring rubric (1–5)
- Baseline results to compare against
- Measures a specific system behavior: retrieval quality of the MCP search tool

What makes it not a real eval:
- **Claude is the judge.** Scores are assigned by the same model doing the synthesis — no ground truth, no human labels, no expected answer set. Score drift between runs is invisible.
- **No assertions.** There's no automated pass/fail — Phase 4 golden fixtures don't exist yet.
- **Retrieval and synthesis are conflated.** A score of 2 means "right docs, wrong answer" but that assessment still relies on Claude's interpretation of whether the docs answered the question.

### Path to a real eval

**Full fix (15-question human baseline):** User reads the 15 expert answer files (`e01`–`e15`) and assigns their own 1–5 scores. Those become ground truth. Future runs compare against human labels, not Claude's self-assessment. The delta between user scores and Claude's 2026-08-14 scores shows how well-calibrated the LLM-as-judge is — important to know before trusting it to score reruns automatically. Beginner questions (b01–b15) can stay LLM-scored since they all hit 4–5 and the signal is in the expert set.

**Lighter fix (Phase 4):** Designate 4–5 questions with known-good expected doc IDs and assert those IDs appear in results. Enough to catch retrieval regressions without scoring 15 questions. Until this exists, reruns compare vibes, not metrics.

The baseline scores in this skill and in `results-table.md` are **Claude-assigned**, not human-labeled.

## Context

- **Question bank:** `sessions/mcp-search-eval/questions.md` (15 beginner + 15 expert)
- **Results dir:** `sessions/mcp-search-eval/results/` (in the `mcp-search-eval` worktree at `~/GitHub/sensible-docs-mcp-search-eval/`)
- **Results table:** `sessions/mcp-search-eval/results/results-table.md`
- **PR:** https://github.com/sensible-hq/sensible-docs/pull/680
- **Worktree branch:** `mcp-search-eval`

## Pipeline (how results are produced)

1. Agent calls `mcp__sensible-docs__search` with 1–2 query variants → MCP returns `{id, title, url}` list
2. Agent calls `mcp__sensible-docs__fetch` on each result ID → MCP returns raw doc text
3. Agent (Claude) reads the fetched text and synthesizes an answer — **no prior knowledge used**

"Docs returned" in the results table = verbatim from MCP fetch calls. "Answer" = LLM interpretation of fetched content only.

## Concurrency limit

**Max 5 agents in parallel.** Running more simultaneously causes `ConnectionRefused` errors on WSL2 (network bridge saturation). Batch questions into groups of 5 and wait for each batch to complete before spawning the next.

## Step 1: Check what's already done

```bash
ls sessions/mcp-search-eval/results/raw/
ls sessions/mcp-search-eval/results/answers/
```

Skip any question whose raw JSON and answer `.md` already exist. Only run missing ones.

## Step 2: Run agents (batches of 5)

Spawn one agent per question. Each agent must:

1. Call `mcp__sensible-docs__search` with 1–2 relevant queries
2. Call `mcp__sensible-docs__fetch` on each result ID
3. Save raw output to `results/raw/{id}.json`:
   ```json
   {
     "question": "...",
     "search_queries": ["...", "..."],
     "search_results": [{ "query": "...", "results": [{...}] }],
     "fetched_pages": [{ "id": "...", "title": "...", "url": "...", "content": "..." }]
   }
   ```
4. Save answer to `results/answers/{id}.md`:
   - The question
   - Answer based only on fetched content (no prior knowledge)
   - Quality verdict: score 1–5 with reasoning; note if question is unanswerable from docs

**File ID format:** `b01`–`b15` for beginner, `e01`–`e15` for expert.

**Write to the worktree**, not the main repo: `/home/franc/GitHub/sensible-docs-mcp-search-eval/sessions/mcp-search-eval/results/`

## Step 3: Handle partial failures

If an agent returns `ConnectionRefused` / `FailedToOpenSocket`, the batch was too large or the API was temporarily down. Retry the failed questions individually (single agent) to confirm connectivity, then resume in batches of 5.

If an agent saved the raw JSON but not the answer file (partial completion), spawn a synthesis-only agent:
- Read the existing raw JSON
- Write the answer `.md` only
- Do not call any MCP tools

**Note on raw JSON schema variance:** Some prior agents saved fetched pages under non-standard keys (`fetched_docs`, `fetched_content`, `fetched`) instead of `fetched_pages`. When building the results table, check all of these keys and fall back to the answer `.md` file for page URLs if metadata is missing.

## Step 4: Update the results table

After all agents complete, update `results/results-table.md` with one row per question using this format:

| # | Question | Search queries sent to MCP | Docs returned by MCP | LLM-synthesized answer (from fetched content) | Score | Comments |
|---|---|---|---|---|---|---|

- **Search queries:** verbatim from `search_queries` in raw JSON
- **Docs returned:** linked titles + URLs verbatim from `fetched_pages` in raw JSON (or equivalent key). Never infer or construct URLs — only use what the MCP returned.
- **Answer:** synthesized from fetched content; 1–2 sentences max
- **Score:** 1–5 (5 = right docs + complete answer; 1 = wrong/no docs, unanswerable)
- **Comments:** why it passed or failed; note if failure is a docs gap vs. retrieval failure

Include averages by category (beginner / expert) and a summary of failing questions at the bottom.

## Step 5: Commit and push

```bash
git -C ~/GitHub/sensible-docs-mcp-search-eval add sessions/mcp-search-eval/results/
git -C ~/GitHub/sensible-docs-mcp-search-eval commit -m "sessions: add eval results run YYYY-MM-DD"
git -C ~/GitHub/sensible-docs-mcp-search-eval push
```

## Scoring rubric

| Score | Meaning |
|---|---|
| 5 | Right doc(s) on first query, answer fully supported by fetched content, no gaps |
| 4 | Right docs found but required multiple query variants, or answer requires inference across pages |
| 3 | Partially answered — core question addressed but documented edge cases missing |
| 2 | Docs retrieved but answer is not in them — docs gap, not retrieval failure |
| 1 | Wrong docs returned, or no results, or answer hallucinated beyond fetched content |

**These scores are LLM-assigned.** Treat them as directional, not authoritative. Human review of the expert answer files is required to make them ground truth.

## Baseline results (run 2026-08-14, LLM-as-judge scores)

| Category | Avg | Pass (≥4) |
|---|---|---|
| Beginner (b01–b15) | 4.7 / 5 | 15/15 |
| Expert (e01–e15) | 3.3 / 5 | 7/15 |
| Overall | 4.0 / 5 | 22/30 |

**Known docs gaps** (score ≤ 2, retrieval worked but answer not in docs):
- e05 — validation order relative to JsonLogic postprocessor
- e07 — `xRangeFilter` coordinate frame when used with `multicolumn`
- e09 — `angleFilter` availability across OCR engines
- e10 — fingerprint score tiebreaker for equal scores
- e12 — `requiredFields` interaction with coverage scoring
- e15 — portfolio mid-page failure mode at runtime

## Phase 4: Eval framework validation

Before re-running, the minimum viable hardening step is golden fixtures:

1. Designate 4–5 questions (e.g., b01 + 2–3 expert) with **known-good expected doc IDs** — docs you've verified should appear in results
2. Write a smoke test: assert the expected doc ID appears in search results and the fetched content contains expected key strings
3. Add a meta-eval step to the run script: run golden fixtures first, fail fast if any break — catches regressions in the MCP tool, agent prompt, or file-writing logic before wasting 30 agent runs
4. Version the question list and ground truth separately from run artifacts so changes to questions/rubric are auditable

**Longer term:** User scores the 15 expert answer files (`e01`–`e15`) as domain expert → those become human-labeled ground truth → future runs can be compared meaningfully. Gap between those scores and Claude's 2026-08-14 scores shows how well-calibrated the LLM-as-judge is.
