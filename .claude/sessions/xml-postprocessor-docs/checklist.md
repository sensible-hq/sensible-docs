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
- [ ] Finish rebase and force-push to PR #715
- [ ] Consider: rename "JsonLogic postprocessor" → "JSON postprocessor"

---

Notes:
- Redirect needed: /docs/postprocessor → /docs/postprocessors (Frances adding separately)
- Config in SenseML editor: https://app.sensible.so/editor/?d=postprocessor_xml&c=all
- Brief naming convention: brief-<slug>.md (not <slug>.md)
