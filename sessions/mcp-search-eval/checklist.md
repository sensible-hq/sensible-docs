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

- [x] Write eval runner script (`run_eval.py`) — runs 18 questions via `claude -p`, compares against ground-truth.json, writes report
- [x] Add `--send-email` flag to `run_eval.py` (smtplib, env var config)
- [x] Write `run_eval.sh` wrapper — first-Tuesday-of-month guard + calls `run_eval.py --send-email`
- [ ] **Activate cron job on WSL2:**
  - Add `EVAL_SMTP_*` env vars to `~/.profile`
  - Add crontab entry: `TZ=America/Denver` + `15 12 * * 2 /home/franc/GitHub/sensible-docs/.claude/skills/mcp-search-eval/scripts/run_eval.sh >> /tmp/mcp-eval.log 2>&1`
  - Ensure cron daemon starts on boot (WSL2 doesn't auto-start cron)
- [ ] Store run history so scores can be trended over time

## Phase 3.5 — LLM contamination

The LLM pass/fail verdict emitted by eval agents is contaminated by training knowledge (Claude has been trained on Sensible's public docs) and repo context (CLAUDE.md loads because agents run from the repo root). A different account or empty dir doesn't fix training contamination.

- [ ] **Treat `missing_anchors` as the primary regression signal**, not LLM pass/fail — `missing_anchors` is a mechanical check on returned doc IDs, contamination-proof
- [ ] Change `cwd` in `run_eval.py` from `REPO_ROOT` to a temp dir, and pass MCP settings explicitly — eliminates repo context (CLAUDE.md) contamination
- [ ] Update SKILL.md to document this limitation and the `missing_anchors`-first interpretation

## Phase 4 — Eval framework validation

- [ ] Designate a small set of "golden" questions (e.g., b01, plus 2-3 expert ones) with known-good expected doc IDs and expected answer content — these serve as fixtures for the eval pipeline itself
- [ ] Write a smoke test: given a golden question, assert that (a) the expected doc ID appears in search results and (b) the fetched content contains expected key strings
- [ ] Add a meta-eval step to the run script: before scoring all 30 questions, run the golden fixtures and fail fast if any fixture breaks — this catches regressions in the MCP tool, the agent prompt, or the file-writing logic before wasting 30 agent runs
- [ ] Version the question list and ground truth separately from the run artifacts so changes to questions/rubric are auditable (i.e., a score drop could be from a worse MCP or from a harder question set)
- [ ] Document the intended change process: if you update the eval (new questions, new rubric, new scoring), re-run the golden fixtures first to confirm the framework is still valid before comparing scores across runs
