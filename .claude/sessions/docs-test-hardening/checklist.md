# docs-test-hardening

Session: fingerprint-match-array-comments (Claude Code session abbb26a9-022f-426d-b62a-97bc541c74e3). Worktree: /home/franc/GitHub/sensible-docs-docs-test-hardening.

Pre-existing issues (from #737) found by the PR #727 security review, split out on request.

- [x] Scrub as its own CI step (`scrub.sh`), upload only after it succeeds; a cancelled or timed-out run can't upload Doc Detective's plain-text password.
- [x] `extract()` polls with a 240 s deadline instead of the SDK's endless `wait_for`; step timeout 18 min, job 25.
- [x] `SENSIBLE_TEST_EMAIL` added to `secrets.txt`.
- [x] Python dependencies pinned with hashes (`requirements.in` → `requirements.txt`), versions at least two weeks old.
- [x] Actions pinned to SHAs; `persist-credentials: false`; only the push step gets the token.
- [x] Envelope fingerprint read only from bot comments (a public comment could suppress the next warning).
- [ ] Proposal only, not implemented (ReadMe bidirectional sync must stay): refuse `runShell`/`runCode`/`httpRequest` steps in docs pages before Doc Detective runs.
- [ ] After #727 merges: its workflow uses the same requirements.txt, so it gets the pins automatically; pin check passes once both are on v0.
