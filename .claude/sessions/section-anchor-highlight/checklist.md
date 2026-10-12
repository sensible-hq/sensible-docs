# Session: section-anchor-highlight

Claude Code session name: section anchor highlight
Claude Code session ID: 7af18af7-ddad-4787-abd1-949eefd2e211

Source PRs: sensible-hq/sensible#3470 (engine: metadata.anchor on section output), sensible-hq/sensible-app#1881 (viewer: "Show section anchors" Options toggle)

- [x] Read both PRs
- [x] Identify affected docs: sections/index.md `display` row only (withMetadata output is undocumented, so #3470 has no standalone doc impact)
- [x] Load style guide + editorial preferences
- [x] Edit sections/index.md display row
- [x] Style/glossary check (vale CLI: no findings on edited line; MCP unavailable)
- [x] Commit, push, open PR
- [ ] After merge: run close-docs-pr

## Round 2: centralize Options UI info in color.md (user request)
- [x] Add `# Options` section to color.md (one H2 per menu item) + screenshot ui_viewer_options.png (screenshots/ and final/)
- [x] Add Violet box (section anchor) to color table; note dotted boxes need Show unextracted lines
- [x] Move Validate fingerprints text + screenshot from fingerprint.md to color.md; leave link
- [x] Replace sections/index.md display-row UI text with link to color.md#show-section-anchors
- [ ] Decide whether to retitle color.md (currently "Source text traceability")
