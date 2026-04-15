# Testing Plan: sensible-quickbooks skill

## Context

The `sensible-quickbooks` skill guides a developer (using an AI coding assistant) through the Sensible + QuickBooks Online integration tutorial. The skill collapses a multi-step human+agent workflow into four phases, two of which require browser action and two of which are fully automated.

The first eval run was blocked because subagents lacked Bash and Read tool permissions in the sandboxed environment. This plan captures what to test and how to run it properly.

---

## What to test

The three eval cases cover the three realistic starting points a developer might be in when they invoke the skill:

| Eval | Starting point | Key behaviors under test |
|------|---------------|--------------------------|
| 1 — from scratch | Has credentials, nothing installed | Collects credentials upfront, clones repo, installs deps, writes `.env`, runs setup script, surfaces OAuth URL as browser step |
| 2 — has credentials | Credentials ready, repo already cloned | Skips clone + pip install, writes `.env`, runs setup script, surfaces OAuth URL |
| 3 — all done | OAuth complete, tokens saved | Skips all setup phases, runs `invoice_to_quickbooks.py`, parses and reports output |

The scripts will fail at the API level in all three cases (fake credentials). That's expected — the assertions are about procedural behavior, not API success.

---

## Assertions per eval

### Eval 1 (from scratch)
1. Agent writes a `.env` file containing `SENSIBLE_API_KEY`, `QBO_CLIENT_ID`, and `QBO_CLIENT_SECRET` before running any scripts
2. Agent clones `sensible-quickbooks-py` repo
3. Agent installs Python dependencies (`sensible-sdk`, `python-quickbooks`, `intuit-oauth`)
4. Agent runs `quickbooks-setup.py`
5. Agent surfaces the OAuth URL as a browser step and stops — does not attempt to automate it

### Eval 2 (has credentials, repo cloned)
1. Agent does NOT re-clone the repo or re-run pip install
2. Agent writes or verifies a `.env` file with the provided credentials
3. Agent runs `quickbooks-setup.py`
4. Agent asks user to open the OAuth URL in a browser

### Eval 3 (all done, just run)
1. Agent skips clone, pip install, and OAuth phases
2. Agent runs `invoice_to_quickbooks.py`
3. Agent parses and reports the script output (success or specific error)
4. Agent does not prompt the user to complete any browser steps

---

## How to run

### Requirements
- Subagents must have **Bash** and **Read** tool permissions. Run in an environment where these are available (not the default sandboxed subagent mode).
- No real credentials needed — fake values are sufficient for testing procedural behavior.

### Steps
1. Spawn with-skill and without-skill subagents in parallel for each eval (6 total)
2. Point with-skill agents at `skills/sensible-quickbooks/SKILL.md`
3. Have each agent save a `summary.md` to the workspace outputs directory
4. Grade against the assertions above
5. Run `aggregate_benchmark.py` and launch the eval viewer

### Workspace location
Results go in `~/.claude/skills/sensible-quickbooks-workspace/iteration-1/` (already created).

---

## Known gaps to address in the next iteration

1. **Token file detection**: The skill says to check for "any `.json` file that looks like a token store." This is vague — the actual filename used by the `python-quickbooks` library should be confirmed and hardcoded.

2. **`.env` file path**: The skill says to write `.env` to "the repo directory" but doesn't specify an absolute path. Agents have written it to the wrong location in informal testing.

3. **Error message specificity**: The error triage at the end of Phase 4 is generic. Once we've run the scripts with fake credentials, we'll know the actual error shapes and can make the guidance more precise.

4. **Partial completion ambiguity**: If the user says "I already cloned the repo," the skill doesn't tell the agent how to verify that's actually true before skipping the clone step.
