---
name: update-webflow-blog-posts
description: Audit and update Webflow blog post bodies: replace GitHub config-library links, upload PDF assets to Webflow CDN, and normalize prerequisites sections. Use when asked to do a link audit, replace GitHub links in blog posts, upload PDFs to Webflow, or standardize blog post prerequisites sections.
argument-hint: [--site-id <id>] [--collection-id <id>] [--search <term>]
allowed-tools: Bash, Read, Write, mcp__webflow__data_cms_tool, mcp__webflow__data_assets_tool
---

# Update Webflow Blog Posts

Orchestration skill for auditing and updating Webflow blog post bodies. Handles:
- Grepping post bodies for any pattern (GitHub links, outdated URLs, etc.)
- Uploading PDF assets to Webflow CDN (two-step: MCP create_asset → S3 upload)
- Replacing links with per-post blocking approval before any Webflow write
- Normalizing prerequisites sections against the delivery orders post template

For the actual Webflow CMS reads/writes, follow the patterns in the global `bulk-cms-update` skill (`~/.claude/skills/bulk-cms-update/SKILL.md`): always use Webflow MCP tools, never direct API calls, always show a diff and get explicit approval before calling `update_collection_items`.

## Defaults (sensible-website)

- Site ID: `6033da353ede9143c0c56ff8`
- Blog Posts collection ID: `65176057cde9c5589dd547d2`
- Prerequisites template: the "How to extract data from delivery orders with Sensible" post
  (slug: `how-to-extract-data-from-delivery-orders-with-sensible`)

## Body files

All post body HTML files live in `bodies/` in this directory — NOT in `/tmp`. This makes them durable across sessions and available for rollback.

Naming convention:
- `bodies/<post-slug>-original.html` — body fetched from Webflow before any edits (rollback target)
- `bodies/<post-slug>-updated.html` — body after replacements, ready to push

Before pushing any update, always verify `bodies/<post-slug>-original.html` exists. If you need to revert, re-push the original body via `update_collection_items`.

## Scripts

All Python operations go through scripts in this directory — do NOT write inline Python in bash heredocs.

| Script | Purpose |
|--------|---------|
| `grep_posts.py` | Search post bodies (or any field) for a string/regex; extract matching URLs |
| `upload_pdf_to_webflow.py` | Step 2 of PDF upload: POST file to S3 presigned URL from create_asset |

### grep_posts.py quick reference

```bash
# Find posts with a search term, show surrounding context
python3 .claude/skills/update-webflow-blog-posts/grep_posts.py <api-response.txt> "search term"

# Extract only URLs containing the search term (deduped per post)
python3 .claude/skills/update-webflow-blog-posts/grep_posts.py <api-response.txt> "search term" --links-only

# Use regex
python3 .claude/skills/update-webflow-blog-posts/grep_posts.py <api-response.txt> "\.pdf\"" --regex

# Search a different field
python3 .claude/skills/update-webflow-blog-posts/grep_posts.py <api-response.txt> "term" --field post-summary
```

The api-response.txt is the saved output of a `list_collection_items` MCP call (the tool-result envelope format).

### upload_pdf_to_webflow.py quick reference

Step 1 (MCP): Call `data_assets_tool > create_asset` with site_id, file_name, and MD5 file_hash.
Step 2 (script): Pass the response fields to the script:

```bash
python3 .claude/skills/update-webflow-blog-posts/upload_pdf_to_webflow.py /tmp/file.pdf \
  --upload-url "<uploadUrl from create_asset>" \
  --upload-details '<uploadDetails JSON from create_asset>' \
  --asset-id "<id from create_asset>" \
  --hosted-url "<hostedUrl from create_asset>"
```

Get the MD5 first: `md5sum /tmp/file.pdf`

## Workflow: Link Audit and Replacement Loop

### Phase 1 — Save post data

Fetch all posts from the collection and save the raw MCP response to a local file (don't re-fetch repeatedly):

```
data_cms_tool > list_collection_items (limit: 100)
→ save response to /tmp/webflow-posts-<date>.txt
```

### Phase 2 — Grep for target links

Run `grep_posts.py` with `--links-only` to get a clean per-post link inventory.
Save output to a file (e.g. `/tmp/grep-results.txt`) and reference it in the checklist.

### Phase 3 — For each matching post (blocking loop)

For each post in the grep results:

1. **Fetch current body from Webflow** (not from the saved file — the body may have changed since the bulk fetch).
2. **Categorize links**:
   - PDF links (URL ends in `.pdf`) → upload to Webflow CDN first, then replace href
   - Other links → replace with target URL (e.g. `https://www.sensible.so/configuration-library`)
3. **Check prerequisites** (if post has a Prerequisites section) → compare against delivery orders template format; flag differences.
4. **Print diff** — show every changed line with old → new. Print the full proposed prerequisites section if it changed.
5. **Wait for approval** — do NOT call `update_collection_items` until user types "approve" (or "skip" to skip).
6. **Push to Webflow** on approval.
7. **Mark done in checklist**.

### Phase 4 — Checklist

Track progress in `checklist.md` in this directory. Update it after each post is processed.

## PDF Upload Flow (detail)

```
1. Download PDF locally if not already present
   curl -L -o /tmp/<filename>.pdf <url>

2. Get MD5:
   md5sum /tmp/<filename>.pdf

3. MCP: data_assets_tool > create_asset
   { site_id, file_name, file_hash: <md5> }
   → returns: uploadUrl, uploadDetails, id, hostedUrl

4. Script: upload_pdf_to_webflow.py
   (uses curl multipart POST to S3)
   → prints ASSET_ID and HOSTED_URL on success

5. Replace original URL with hostedUrl in post body
```

## Prerequisites Normalization

The delivery orders post is the template for what prerequisites should look like.
Fetch it fresh from Webflow before comparing:

```
data_cms_tool > list_collection_items
  slug: how-to-extract-data-from-delivery-orders-with-sensible
```

Template structure (6 bullets):
1. Sign up for a Sensible account (link to app.sensible.so/register/)
2. After completing onboarding, click Document types → Create new document type. In the dialog
3. Name the document type `<doc_type_slug>`
4. Upload the [example document](<webflow-cdn-url> target="_blank").
5. Leave all defaults as-is except ensure "Auto-generate configuration" is disabled
6. Click **Create** to create the document type and enter the SenseML editor.

Key differences from older blog post format:
- Steps are separate `<li>` items (not one large bullet)
- PDF link uses `target="_blank"` and anchor text "example document"
- PDF link points to Webflow CDN, not raw GitHub
- Ends with "enter the SenseML editor"

Only update prerequisites if the post has a Prerequisites section AND a PDF sample document that can be hosted on Webflow CDN. Otherwise note it as a flag for manual review.
