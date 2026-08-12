# llms.txt — remaining work

- [ ] **Generate `llmstxt.md` instead of `llms.txt`** — update the sync script to output `llmstxt.md`, place it in a docs category as a hidden page, and author a redirect to it from ReadMe's dashboard. Workaround: ReadMe doesn't support serving a raw `llms.txt` natively, so the file must be an `.md` page with a redirect.
- [ ] **Test `check_links.py`** — add unit tests mocking `urllib.request.urlopen`. Cases to cover: 200 passes, 404 fails, 429 is skipped, network errors are reported, duplicate URLs are only checked once.
- [x] **End-to-end testing plan before production** — see `test-results.md` for full evidence with commit links. All scenarios passed. Two gaps: (1) trigger→auto commit links for PRs 663/664 are inferred from timestamp, not recorded metadata (workflow didn't have trigger history feature yet); (2) "delete both slug and .md simultaneously" was not tested as a single commit. Neither is a blocker.
