# MCP Search Eval — Checklist

**Session:** mcp-search-eval  
**Session ID:** fd57d974-a931-40a3-a3c6-74d13cf283af  
**Worktree:** `~/GitHub/sensible-docs-mcp-search-eval` (branch `mcp-search-eval`)  
**PR:** https://github.com/sensible-hq/sensible-docs/pull/680

Goal: evaluate the `mcp__sensible-docs` search tool's ability to surface relevant docs for a range of questions, and turn this into a formal, recurring eval.

## Phase 1 — Manual baseline run

- [x] Confirm MCP tools are accessible in subagent context (run 1 test agent)
- [x] Set up results directory structure (`results/raw/`, `results/answers/`)
- [ ] Spawn 30 parallel subagents (1 per question) to search + fetch + save artifacts
- [ ] Review raw outputs and answer quality

## Phase 2 — Formalize as evals

- [ ] Define a scoring rubric for search quality (e.g., did the right doc appear in results? was the answer complete? did it hallucinate anything not in the fetched docs?)
- [ ] Write an evaluator agent/script that takes each `results/answers/q{N}.md` and scores it against the rubric
- [ ] Decide on eval format: JSONL (standard LLM eval format) with `{question, expected_topics, search_results, answer, scores}`
- [ ] Write expected answers / ground truth for each question (or at minimum, expected doc IDs that should appear in results)
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
