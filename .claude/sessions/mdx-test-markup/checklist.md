# mdx-test-markup checklist

- Session: xlsb continuation (2ee92462-6c8b-42e1-bea3-6b1926a1caf5)
- Worktree: `~/GitHub/sensible-docs-mdx-test-markup`, branch `fe_mdx_test_markup`

Edits in the ReadMe editor saved Supported file types' HTML comments as MDX comments, test markup included, so the runner stopped seeing its tests. Frances chose to read both forms and to author in MDX from now on, keeping markup short because agents can read it in the page's HTML.

- [x] `markup.read_page`: MDX comments outside code fences read as HTML comments, same length, so offsets and line numbers still match the saved page; `parse_page`, `should_run`, and the planner's markup scan use it; `check_secrets` reads page variables in either form
- [x] Planner check fails when a listed page has no test markup
- [x] README and docstring examples in MDX; README says why, and asks for short markup
- [x] Doc Detective 4.38.1's markdown file type already reads `{/* test */}`, `{/* step */}`, and `{/* test end */}`, so UI tests can be MDX too
- [ ] After merge: CI run of file-types.md on v0, then the doc-test evidence comment on #815 and #812, and on issue #818
- [ ] #749's add-doc-tests skill: switch its examples to MDX and add the brevity guidance
- [ ] Runner error messages still name markers in HTML form (`<!-- fixture -->`); both forms are read, so they stay accurate
