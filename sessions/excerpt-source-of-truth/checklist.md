# Session: excerpt-source-of-truth

Branch: refactor/excerpt-source-of-truth
PR: (pending)

## Tasks

- [x] Create `check_excerpt.py` — flags docs/ files missing/empty excerpt; skips reference/ missing key
- [x] Create `add_excerpt.py` — writes generated text to excerpt (insert or update)
- [x] Create `sync_description.py` — copies excerpt → metadata.description (always overwrites, excerpt wins)
- [x] Update workflow — checks excerpt, generates to excerpt, syncs description unconditionally, gates PR on git diff
- [x] Write pytest suite (15 tests, all passing) for the three new scripts
- [ ] Open PR
- [ ] Verify workflow fires and creates a PR after merge

## Test plan

- [x] check_excerpt: docs/ file missing excerpt key → flagged
- [x] check_excerpt: docs/ file with empty excerpt → flagged
- [x] check_excerpt: docs/ file with excerpt → passes
- [x] check_excerpt: hidden docs/ file → skipped
- [x] check_excerpt: reference/ file missing excerpt key → skipped (silent)
- [x] check_excerpt: reference/ file with empty excerpt → flagged
- [x] add_excerpt: updates existing excerpt in-place
- [x] add_excerpt: inserts excerpt after title when key absent
- [x] add_excerpt: replaces empty excerpt
- [x] add_excerpt: returns False on file with no front matter
- [x] sync_description: copies excerpt → metadata.description when stale
- [x] sync_description: inserts metadata.description when key absent
- [x] sync_description: no-op when already in sync
- [x] sync_description: skips file with no excerpt
- [x] sync_description: dry-run does not write
- [ ] Workflow: triggers on push to v0, creates PR for file missing excerpt
