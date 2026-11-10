# Sensible Docs — Method and Parameter Names in Prose

**Identifiers in prose:** Write method, parameter, and preprocessor names as spaced Title Case in running text — never as backtick-wrapped camelCase or snake_case. The backtick form is for the parameter table's key column and code blocks only.

Link method and preprocessor names on first mention per page; subsequent mentions use plain Title Case with no link. Parameters don't have dedicated pages so don't link them.

Always include the type descriptor word ("method", "parameter", "preprocessor") alongside the name — never use a bare name alone.

- Wrong: "If you set Height, then..."
- Right: "If you set the Height parameter, then..."

This rule applies to all inline body text — except the first column of a parameter reference table, where the raw key (`` `camelCase` `` or `` `snake_case` ``) is the correct form.

| Wrong | Guides & reference docs | Blog posts |
| ----- | ----------------------- | ---------- |
| the `` `queryGroup` `` method | the `[Query Group](doc:query-group)` method | the `[Query Group](https://docs.sensible.so/docs/query-group)` method |
| the `` `mergeLines` `` preprocessor | the `[Merge Lines](doc:merge-lines)` preprocessor | the `[Merge Lines](https://docs.sensible.so/docs/merge-lines)` preprocessor |
| the `` `source_ids` `` parameter | the Source IDs parameter | the Source IDs parameter |
| the `` `extra_data` `` field | the Extra Data field | the Extra Data field |
