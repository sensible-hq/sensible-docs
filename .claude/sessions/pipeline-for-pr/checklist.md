# Checklist: pipeline-for-pr

Claude Code session name: pipeline-for-pr
Claude Code session ID: 79f994ff-4a6d-4692-96c9-8f12f7e73745
Branch: pipeline-for-pr

- [x] Add `pipeline-for-pr`, which runs the docs skills in order for one engine PR
- [x] Remove the close-out step from `update-docs-from-pr`; reuse an existing worktree and docs PR
- [x] CLAUDE.md: split the Sensible API keys by purpose
- [ ] Run the pipeline on a real engine PR and fix the hand-offs it exposes
- [ ] Check which scripts that use `SENSIBLE_API_KEY` are formal tests and should use the test key
- [ ] Rename `update-docs-from-pr` to `draft-from-pr` once #832, #785, #784 and #712 merge or close
- [ ] Finish #749 (`add-doc-tests`) so step 7 can run
