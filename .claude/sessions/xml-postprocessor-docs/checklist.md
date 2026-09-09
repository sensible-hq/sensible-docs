# Checklist — xml-postprocessor-docs

Session name: xml-postprocessor-docs
Session ID: 39002c4a-a0d9-4424-a091-89a35b61577a

---

- [x] Create postprocessors/ category directory structure
  - [x] postprocessors/index.md (parent overview page)
  - [x] postprocessors/jsonlogic-postprocessor.md (renamed from postprocessor.md)
  - [x] postprocessors/xml-postprocessor.md (new, for PR 3461)
  - [x] postprocessors/_order.yaml
- [x] Update docs/Senseml reference/_order.yaml (postprocessor → postprocessors)
- [x] Delete old postprocessor.md
- [x] Rebase onto origin/v0 (in progress — conflict in jsonlogic-postprocessor.md frontmatter, resolved)
- [x] Write .claude-session for this worktree
- [x] Rename brief to brief-postprocessors.md (naming pattern: brief-<slug>.md)
- [x] Update xml-postprocessor.md example with real golden from sensible-hq/sensible#3461 (CH Robinson rate confirmation)
- [x] Push postprocessor_xml config to Frances's Sensible account for SenseML editor review
- [ ] Obtain CH Robinson PDF + screenshot for doc assets (postprocessor_xml.png, postprocessor_xml.pdf)
- [ ] Replace example PDF with a redacted version (current example PDF is not yet redacted)
- [ ] Rerun style guides on updated pages
- [ ] Verify rendered XML string output examples actually display with surrounding `"` in ReadMe
- [ ] Finish rebase and force-push to PR #715
- [ ] Consider: rename "JsonLogic postprocessor" → "JSON postprocessor"
- [ ] Verify: does `keepParsedDocument: false` actually disable Excel output and human review for the XML postprocessor?
- [ ] Verify in codebase: `content` behavior — "A scalar value becomes text content. An element object becomes a nested child element. An array produces a sequence of child elements." Confirm each claim against xml.ts implementation. (copied from JsonLogic page — needs confirmation against codebase)
- [ ] Add to docs-from-PR skills: guidance on how to handle provenance/traceability — i.e., how to trace claims back to the sensible codebase (e.g., parameter names, defaults, behavior) rather than trusting PR descriptions alone
- [ ] Search all doc topics for mentions of "postprocessor" — update cross-references, descriptions, and links to reflect the new postprocessors/ structure and the addition of the XML type
- [ ] Audit docs that mention output formats and output schemas — update to reflect XML postprocessor as a new output option
  - Anywhere that describes the API output schema (parsed_document shape, postprocessorOutput, field types, Excel) may need updating
  - May need a new concept topic: "Output formats / output schemas" covering parsed_document, postprocessorOutput (JsonLogic and XML variants), Excel — so individual pages can link out instead of re-explaining inline

---

Notes:
- Redirect needed: /docs/postprocessor → /docs/postprocessors (Frances adding separately)
- Config in SenseML editor: https://app.sensible.so/editor/?d=postprocessor_xml&c=all
- Brief naming convention: brief-<slug>.md (not <slug>.md)
