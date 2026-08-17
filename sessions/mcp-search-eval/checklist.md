# MCP Search Eval — Checklist

**Session:** mcp-search-eval  
**Session ID:** fd57d974-a931-40a3-a3c6-74d13cf283af  
**Worktree:** `~/GitHub/sensible-docs-mcp-search-eval` (branch `mcp-search-eval`)  
**PR:** https://github.com/sensible-hq/sensible-docs/pull/680

Goal: evaluate the `mcp__sensible-docs` search tool's ability to surface relevant docs for a range of questions, and turn this into a formal, recurring eval.

## Phase 1 — Manual baseline run

- [x] Confirm MCP tools are accessible in subagent context (run 1 test agent)
- [x] Set up results directory structure (`results/raw/`, `results/answers/`)
- [x] Spawn subagents (1 per question) to search + fetch + save artifacts — all 30 questions complete
- [x] Compile results into `results/results-table.md` with scores and comments
- [x] Fix doc links for entries where agents saved fetched pages under non-standard JSON keys (e05–e08, e11)
- [ ] Review raw outputs and answer quality (human scoring — see below)

## Phase 2 — Eval framing and ground truth

- [x] Define scoring rubric (1–5 scale, in results table and SKILL.md)
- [x] Rewrite SKILL.md to accurately describe what this is: a retrieval audit with LLM-as-judge scoring, not a true eval
- [x] Designate ground truth question set: e01, e02, e06 (in `questions.md`); remaining expert questions deferred to "score later"
- [x] Add `Human score` and `Human notes` columns to results table
- [ ] User scores e01, e02, e06 answer files and fills in Human score/notes columns
- [ ] Decide on eval format: JSONL with `{question, expected_topics, search_results, answer, scores}`
- [ ] Store ground truth in `sessions/mcp-search-eval/ground-truth.json`

## Phase 3 — Recurring runs + reporting

- [ ] Write a script (`scripts/run-mcp-eval.sh` or similar) that runs the full eval pipeline end to end
- [ ] Set up a cron job or scheduled trigger to run it periodically (weekly? on doc deploys?)
- [ ] Set up result delivery — options:
  - Slack: post summary + score delta to a channel via webhook
  - Email: send a report to frances@sensible.so
  - Both
- [ ] Decide what to alert on: score regression below threshold, new questions that get zero results, etc.
- [ ] Store run history so scores can be trended over time

## Phase 4 — Eval framework validation

- [ ] Designate a small set of "golden" questions (e.g., b01, plus 2-3 expert ones) with known-good expected doc IDs and expected answer content — these serve as fixtures for the eval pipeline itself
- [ ] Write a smoke test: given a golden question, assert that (a) the expected doc ID appears in search results and (b) the fetched content contains expected key strings
- [ ] Add a meta-eval step to the run script: before scoring all 30 questions, run the golden fixtures and fail fast if any fixture breaks — this catches regressions in the MCP tool, the agent prompt, or the file-writing logic before wasting 30 agent runs
- [ ] Version the question list and ground truth separately from the run artifacts so changes to questions/rubric are auditable (i.e., a score drop could be from a worse MCP or from a harder question set)
- [ ] Document the intended change process: if you update the eval (new questions, new rubric, new scoring), re-run the golden fixtures first to confirm the framework is still valid before comparing scores across runs
