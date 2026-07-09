# Subskill: Structural Check

Verifies changelog draft structure after the docs-checker terminology pass. Catches missing doc links and wrong image format.

**Long-term direction:** As more entry types accumulate, promote these templates into a `references/entry-templates/` directory with one file per section type. A template-first workflow would make steps 1–2 below largely automatic.

---

## Entry template

Use this stub when drafting each section. Fill in the bracketed parts; the example sentences show the expected pattern and voice.

```markdown
## [New feature | Improvement | UX improvement | UX improvements | Deprecation]: [short title]

Sensible released [feature name], which [what it does in one clause]. 
You can now [primary action a user takes with this feature] — for example, [concrete use case]. 
[Optional: what problem it solves, or what it replaces.]
For more information, see [Topic name](doc:slug).
```

**Example (filled in):**

```markdown
## New feature: Today operator for JsonLogic

Sensible released the new Today operator for [JsonLogic](doc:jsonlogic).
The operator returns the current UTC date as a `YYYY-MM-DD` string and takes no arguments.
Combine it with the existing Date Shift operator to compute dates relative to today — for example,
a contract expiration date one year from the current date — without hardcoding a date in your config.
For more information, see [JsonLogic](doc:jsonlogic).
```

---

---

## Step 1 — Doc links

Every section must link to at least one relevant published doc page using readme short-link format:
- `docs/` pages → `[text](doc:slug)`
- `reference/` pages → `[text](reference:slug)`

For each section in the draft:
1. Identify the primary feature being described.
2. Check whether a doc link exists in the section body.
3. If a link is missing, find the relevant local file:
   ```bash
   find /home/franc/GitHub/sensible-docs/docs -iname "*<slug>*" | grep -v ".claude"
   ```
4. If a doc page exists: add a `[text](doc:slug)` link — use "For more information, see [X](doc:x)" as a closing sentence if no natural inline placement exists.
5. If no doc page exists: add a comment `<!-- DOC LINK NEEDED: no public page for [feature] -->` so it's visible in the readme.io draft.

---

## Step 2 — Image format

Images must use JSX `<Image>` syntax, **not** markdown `![alt](url)`:

```jsx
<Image alt="Click to enlarge" border={false} src="URL" />
```

Scan the draft for any markdown image syntax `![` and replace with `<Image>`.

---

## Step 3 — Image source

Images must be hosted in the sensible-docs repo:
```
https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/<filename>
```

If a screenshot exists in a PR or Notion but hasn't been moved to the repo yet, do **not** use the raw GitHub asset URL (these expire). Instead replace with:
```
<!-- SCREENSHOT NEEDED: source <url> -->
```

---

## Step 4 — Report

List every section and its status:

```
Doc links:
  ✓ Actor attribution → doc:extraction
  ✓ Region as image → doc:region, doc:images
  ✗ Bulk actions — no public page (comment added)

Images:
  ✓ No markdown image syntax found
  ✗ Word wrap entry: markdown image replaced with comment (src not hosted)
```
