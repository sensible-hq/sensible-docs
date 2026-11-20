# Checklist: doc-detective-ci-fix

Claude Code session name: doc-detective
Claude Code session ID: 720fe7cf-48da-4332-8c4b-866ca3fa807d
Branch: doc-detective-ci-fix · started 2026-10-15 from /home/franc/GitHub/sensible-docs
Resume: `cd /home/franc/GitHub/sensible-docs && claude --resume 720fe7cf-48da-4332-8c4b-866ca3fa807d`

Goal: fix the first CI run's failure after #737 merged (issue #751): code tests crashed because the SENSIBLE_TEST_API_KEY secret has stray whitespace, and the crash left no record.

- [x] Trim key values (settings.key) and run.sh's scrub values
- [x] Record unexpected errors as RUNNER_ERROR with keys redacted; redacted traceback to the log
- [x] Cleanup (doc type delete) failures never hide a test's result
- [x] Tests: 3 new offline tests (73 total pass); live run with newline-suffixed keys and no .env passes
- [ ] User: re-save the SENSIBLE_TEST_API_KEY secret without the trailing newline (optional after this fix, but tidy)
- [ ] After merge: run the workflow manually (workflow_dispatch), confirm green, close #751
