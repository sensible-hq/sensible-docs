# readme-metrics checklist

Claude Code session name: readme-metrics
Claude Code session ID: 79acfabe-a332-4530-86b6-e04cdc9dc6d5
Started: 2026-10-01

## Context

- ReadMe Developer Metrics API (`metrics.readme.io/v2/...`) rejects `README_API_KEY` with "upgrade to enterprise" on every endpoint tested (pageview/top, pageview/total, search/top-search-terms, thumb/worst, thumb/average). Dashboard shows top pages; API does not.
- Exploring a weekly automated screenshot (Playwright) of the dashboard top-pages view as a workaround.

## Tasks

- [ ] Fix `vale` MCP server startup (failed at session start with `Executable not found in $PATH: node`)
  - [ ] Run `/mcp` and reconnect `vale`; if it connects, the failure was transient — done
  - [ ] If it fails again, change `"command": "node"` for `vale` in `~/.claude.json` to `/home/franc/.nvm/versions/node/v24.15.0/bin/node` (note: must update on nvm version change)
  - [ ] Check `vale-mcp` (npx, failed with `CONNECTION_CLOSED`) — likely a separate issue; same absolute-path fix for `npx` if needed
- [ ] Weekly ReadMe top-pages screenshot automation — blocked on: dashboard URL, login method (email/password vs SSO), screenshot-only vs JSON capture
