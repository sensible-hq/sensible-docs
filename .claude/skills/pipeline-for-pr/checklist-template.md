# Checklist: pipeline for sensible#<engine-pr>

Claude Code session name: <session-name>
Claude Code session ID: <session-id>
Engine PR: sensible-hq/sensible#<engine-pr>
Docs branch: <branch, once step 4 creates it>
Docs PR: <sensible-docs#number, once step 4 opens it>

Tick an item only when its skill has run and Frances has replied to the report. Under each step, record what it produced. A skipped step gets a `- Skipped: <reason>` line. `scripts/pipeline/step_evidence.py` reads this file, so keep each field's name and colon, and list every session's ID on the session ID line, separated by commas.

- [ ] **1. Research the PR** (`update-docs-from-pr` steps 1–2)
  - Merged into the engine's default branch, or still in an open PR:
  - Affected pages:
  - Existing docs PR, if any:
  - Extractor directories:
- [ ] **2. Upload the extractor** (`upload-pr-extractor`, or adapted)
  - Sensible app URLs:
  - Config Frances settled on:
- [ ] **3. Comment the example config** (`json5-commenter`)
  - Draft: `drafts/<engine-pr>-example.md`
  - Frances approved the comments:
- [ ] **4. Write the example page** (`create-docs-example`)
  - Page:
  - Docs PR opened:
- [ ] **5. Draft the docs** (`update-docs-from-pr` from step 3)
  - Pages changed:
  - Vale and Jev judge results:
- [ ] **6. Extract testable claims** (`extract-testable-claims`)
  - Claims Frances picked:
  - Records: `scripts/doc-detective/testable-claims/pr-<docs-pr>-<feature>/`
- [ ] **7. Add tests** (`add-doc-tests`)
  - Tests added, or why not:
- [ ] **8. Hand off for merge**
  - Frances merged the docs PR:
  - `close-docs-pr` ran:
