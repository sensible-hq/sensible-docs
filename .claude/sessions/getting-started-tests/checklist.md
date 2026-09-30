# Checklist: getting-started-tests

Claude Code session name: getting-started-tests
Claude Code session ID: 720fe7cf-48da-4332-8c4b-866ca3fa807d
Branch: getting-started-tests · started 2026-09-30 from /home/franc/GitHub/sensible-docs
Resume: `cd /home/franc/GitHub/sensible-docs && claude --resume 720fe7cf-48da-4332-8c4b-866ca3fa807d`

Goal: add real Doc Detective tests to `docs/document extraction/getting-started.md`, a mix of UI tests (Sensible app steps) and code tests (code samples).

Prior art: `doc-detective-poc` branch (PR #725), `sessions/docs-as-tests/CONCEPT.md`. Key findings to carry over:
- Inline statements: `<!-- test {...} -->` … `<!-- test end -->`, `<!-- step {...} -->`. ReadMe preserves HTML comments (D1).
- `detectSteps` is on by default, so every link gets a `checkLink` unless disabled.
- CLI exits 0 on failure unless `--exit-on-fail`.
- Don't use `httpRequest` response assertions to compare Sensible output (null crash, order-insensitive arrays).
- Doc Detective 4.38.1 installed globally (`doc-detective`).

- [x] Create worktree and draft PR
- [ ] Decide UI test auth approach (test account + credentials in env vars)
- [ ] Dry run Doc Detective against getting-started.md; see what `detectSteps` picks up
- [ ] UI tests: account/sign-in links, Document Types flow
- [ ] Code tests: config samples (extract + compare output)
- [ ] Code tests: API/integration samples
- [ ] Local green run
- [ ] CI wiring (secrets, workflow)
