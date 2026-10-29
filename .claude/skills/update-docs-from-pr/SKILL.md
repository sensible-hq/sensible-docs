---
name: update-docs-from-pr
description: Given a sensible-hq/sensible PR number, analyze the engine/API changes and update the sensible-docs repo accordingly, then open a PR. Handles both updating existing pages and creating new pages. If you already know which type of change is needed, use update-existing-doc or create-new-doc directly for a more focused workflow.
argument-hint: <pr-number> [hints about affected doc areas or related PRs]
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(git checkout:*), Bash(git worktree:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read, Glob, Grep, Edit, Write, mcp__vale__check_file
---

# Update docs from an engine PR

This runs the docops workflow, which splits this skill's former steps into checked stages: find the affected pages, plan, draft code tests, write, verify, and open the PR.

1. Read `plugins/docops/skills/update-docs-from-pr-workflow/SKILL.md` in the private sensible-doc-ops checkout (default: `~/GitHub/sensible-docs-sandbox`).
2. Follow it, passing it these arguments: **$ARGUMENTS**

If that file isn't there, stop and say so. Don't fall back to an older version of these steps.

The previous step-by-step version of this skill is in git history; its steps 2 and 3 now live, word for word, in the workflow's `find-affected-docs` and `plan-docs-change` skills.
