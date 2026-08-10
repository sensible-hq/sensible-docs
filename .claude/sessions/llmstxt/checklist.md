# llms.txt — remaining work

- [ ] **Generate `llmstxt.md` instead of `llms.txt`** — update the sync script to output `llmstxt.md`, place it in a docs category as a hidden page, and author a redirect to it from ReadMe's dashboard. Workaround: ReadMe doesn't support serving a raw `llms.txt` natively, so the file must be an `.md` page with a redirect.
- [ ] **Test `check_links.py`** — add unit tests mocking `urllib.request.urlopen`. Cases to cover: 200 passes, 404 fails, 429 is skipped, network errors are reported, duplicate URLs are only checked once.
- [ ] **End-to-end testing plan before production** — run file I/O scenarios on this branch to verify the GH action triggers and generates the correct output PR. Requires a branch-scoped duplicate of `sync-llmstxt.yml` that triggers on push to this branch (instead of `v0` paths), so tests don't pollute the real sync. Scenarios to cover:
  - Add a new topic `.md` + slug in `_order.yaml` → entry appears
  - Delete a slug from `_order.yaml` (leave the `.md`) → entry disappears
  - Delete both slug and `.md` → entry disappears
  - Add a slug with no corresponding `.md` → entry absent, `--check` reports stale slug
  - Add a `.md` with no `metadata.description` → entry absent or clearly flagged
  - Add a new category with 0 visible pages → section omitted
  - Add a new category with 1 visible page → section appears
  - Delete all pages from a category → section disappears
  - Update `metadata.description` in frontmatter + touch `_order.yaml` → description updates
  - Add `hidden: true` to a page + touch `_order.yaml` → entry disappears
  - Remove `hidden: true` + touch `_order.yaml` → entry reappears
