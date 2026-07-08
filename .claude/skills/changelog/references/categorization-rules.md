# PR Categorization Rules

Derived from Frances's past calls in #documentation threads. Use these when annotating release PRs with `document / investigate / skip`.

---

## skip

Apply these without needing to ask:

- **Bug fixes** — any PR described as a fix, correction, or repair with no new user-facing behavior. Frances's phrasing: "bug fix, no docs", "this seems like a bug fix?"
- **Infra / internal tooling** — deploy scripts, stack migrations, CI changes, Lambda internals, per-stage/per-region resource moves
- **Dependency bumps and security patches** — dependabot PRs, `pnpm audit` fixes, package version upgrades
- **Backend-only wiring** — things like denormalizing data onto DynamoDB, refactoring error dispatch, internal queue changes with no API surface change
- **Named-customer-specific** — e.g. adding a specific customer's SAML SSO provider, toggling a feature per-account via internal CLI
- **"Still in progress / open PR"** — Frances's signal: "still in progress", "open PR", "won't announce till it's fixed"
- **Small UI polish** — Frances's phrasing: "too small a UI change / bug fix", "too small a change to SenseML JSON editing"
- **Internal access grants** — granting specific engineers console or accounts-manager access

---

## investigate

Use when you're uncertain, or when the PR is user-facing but scope/readiness is unclear:

- **Feature needs Horacio confirmation** — Frances often checks whether something is intentionally public before documenting it. Signal: "is this a bug fix?", "assuming no update necessary?"
- **"No public docs for now"** — feature exists but isn't being surfaced yet (e.g. classifyAndQuery). Flag as investigate so it doesn't get lost.
- **"Save for next changelog"** — Frances defers items explicitly; treat these as investigate, not skip. They're not dropped.
- **Email processor behavior changes** — this feature area is actively being documented and user-facing changes are often worth at least a mention
- **New UI affordances** — Cmd+click shortcuts, toggles, bulk actions — small but user-facing; check if worth a brief mention

---

## document in changelog

- Clear new user-facing feature with existing or in-progress public docs
- New method, operator, or parameter with a reference page
- Already documented by Frances (note "already docs'd <date>" in the annotation)
- UI feature significant enough to warrant a changelog section on its own

---

## General signals from Frances's comments

| Frances's phrasing | Call |
|---|---|
| "bug fix" / "this is a bug fix?" | skip |
| "internal/backend changes" | skip |
| "save for next changelog" | investigate |
| "no public docs for now" | investigate (don't lose it) |
| "too small a UI change" | skip |
| "still in progress (open PR)" | skip |
| "checked w/ Horacio, no update necessary" | skip |
| "not surfacing X yet" | investigate |
| "covered by last month" | skip |
