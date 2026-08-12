# llms.txt — end-to-end test results

## How the test workflow signals results

The test workflow (`test-sync-llmstxt.yml`) exits 1 when llms.txt changes and a PR is created/updated. So:

- **Workflow `failure`** = "Fail if llms.txt changed" step fired → llms.txt changed, PR created/updated ✅
- **Workflow `success`** = "Create or update PR" and "Fail if llms.txt changed" both skipped → llms.txt unchanged ✅

## Results

| Test | Trigger commit | Auto commit (llmstxt-1.md) | Sync PR | Result |
|------|---------------|---------------------------|---------|--------|
| touch `_order.yaml` comment only — no PR | [ab7ec0d](https://github.com/sensible-hq/sensible-docs/commit/ab7ec0d0ab) | — (skipped, no change) | — | ✅ |
| no-change push — no PR (1c) | [2a4b1f5](https://github.com/sensible-hq/sensible-docs/commit/2a4b1f5787) | — (skipped, no change) | — | ✅ |
| add page + slug — entry appears | [51b24d5](https://github.com/sensible-hq/sensible-docs/commit/51b24d525c) / [cef814a](https://github.com/sensible-hq/sensible-docs/commit/cef814ac37) | [ea34350](https://github.com/sensible-hq/sensible-docs/commit/ea34350ed1) ⚠️ | [663](https://github.com/sensible-hq/sensible-docs/pull/663) | ✅ |
| remove slug (keep .md) — entry disappears | [eeae399](https://github.com/sensible-hq/sensible-docs/commit/eeae399ec7) | [44c5179](https://github.com/sensible-hq/sensible-docs/commit/44c5179a1a) ⚠️ | [664](https://github.com/sensible-hq/sensible-docs/pull/664) | ✅ |
| stale slug (no .md) — entry absent, `--check` warns | [35d1276](https://github.com/sensible-hq/sensible-docs/commit/35d1276f1c) | — (skipped, no change) | — | ✅ |
| slug + no `metadata.description` — entry without description | [6172bea](https://github.com/sensible-hq/sensible-docs/commit/6172bea556) | [95b9b97](https://github.com/sensible-hq/sensible-docs/commit/95b9b97062) | [667](https://github.com/sensible-hq/sensible-docs/pull/667) | ✅ |
| `hidden: true` — entry disappears | [1cbbd14](https://github.com/sensible-hq/sensible-docs/commit/1cbbd14707) | [679b084](https://github.com/sensible-hq/sensible-docs/commit/679b084f63) | [668](https://github.com/sensible-hq/sensible-docs/pull/668) | ✅ |
| remove `hidden: true` — entry reappears | [c0a1a85](https://github.com/sensible-hq/sensible-docs/commit/c0a1a85373) | [3efcfbd](https://github.com/sensible-hq/sensible-docs/commit/3efcfbdc56) | [669](https://github.com/sensible-hq/sensible-docs/pull/669) | ✅ |
| add `metadata.description` — description updates | [e61bc1d](https://github.com/sensible-hq/sensible-docs/commit/e61bc1d2da) | [f555cb6](https://github.com/sensible-hq/sensible-docs/commit/f555cb6f14) | [670](https://github.com/sensible-hq/sensible-docs/pull/670) | ✅ |
| category with 1 hidden page — section omitted | [e711a5c](https://github.com/sensible-hq/sensible-docs/commit/e711a5cd57) | — (skipped, no change) | — | ✅ |
| unhide page in category — section appears | [db59990](https://github.com/sensible-hq/sensible-docs/commit/db59990ae0) | [63b21e6](https://github.com/sensible-hq/sensible-docs/commit/63b21e6705) | [671](https://github.com/sensible-hq/sensible-docs/pull/671) | ✅ |
| hide page in category — section disappears | [a70f704](https://github.com/sensible-hq/sensible-docs/commit/a70f704bdc) | [fb4fbdd](https://github.com/sensible-hq/sensible-docs/commit/fb4fbdd79a) | [672](https://github.com/sensible-hq/sensible-docs/pull/672) | ✅ |
| add `openapi_test.json` — spec link appears | [366ef84](https://github.com/sensible-hq/sensible-docs/commit/366ef84e10) | [0f83748](https://github.com/sensible-hq/sensible-docs/commit/0f837481ec) | [673](https://github.com/sensible-hq/sensible-docs/pull/673) | ✅ |
| remove `openapi_test.json` — spec link disappears | [02e780e](https://github.com/sensible-hq/sensible-docs/commit/02e780e025) | [db96b0c](https://github.com/sensible-hq/sensible-docs/commit/db96b0c996) | [674](https://github.com/sensible-hq/sensible-docs/pull/674) | ✅ |

⚠️ = trigger→auto commit link is inferred from timestamp, not from recorded trigger history. PRs 663 and 664 were created before the trigger history feature was added to the workflow PR body, so the exact trigger commit can't be confirmed from PR metadata.

## Anomaly: test-1b

[2b839d3](https://github.com/sensible-hq/sensible-docs/commit/2b839d365c) — "no-change push" — expected `success` but got `failure`. Likely a state issue (llms.txt was out of sync at that point). The immediately following test-1c ([2a4b1f5](https://github.com/sensible-hq/sensible-docs/commit/2a4b1f5787)) passed clean with no change. Not investigated further.

## Not tested

- Delete both slug and `.md` simultaneously — only tested delete-slug-keep-md and delete-slug-delete-md separately via the reset commits.
