# Webflow Blog Post Link Audit — sensible-configuration-library

**Search term:** `sensible-configuration-library`  
**Grep script:** `python3 .claude/skills/update-webflow-blog-posts/grep_posts.py <api-response.txt> "sensible-configuration-library" --links-only`  
**Collection:** Blog Posts (`65176057cde9c5589dd547d2`) on sensible-website (`6033da353ede9143c0c56ff8`)  
**Replacement rules:**
- GitHub links ending in `.pdf` → upload to Webflow CDN, replace href
- All other GitHub config-library links → replace with `https://www.sensible.so/configuration-library`
- Posts with a Prerequisites section → normalize to delivery orders template format (see SKILL.md)

---

## Resumption context

**Next post to process: [2/22]** — "How to extract data from insurance declaration pages with Sensible"  
Slug: `how-to-extract-data-from-insurance-declaration-pages-with-sensible` | ID: `69cd60dca92a97423415aefe`

**Do NOT use the saved bulk-fetch response file as the source of truth for body content.** It was fetched at session start and is stale — posts already updated will have old content there. Always re-fetch each post's current body from Webflow via `list_collection_items` with the slug filter before making changes.

**Pending publishes:** All updates so far are staged drafts in Webflow (not yet live). The live site still shows original content. Publish separately when the full batch is reviewed and approved.

**Flags requiring user decisions before processing:**
- [4/22] "Introducing email data extraction" — 10 specific subdirectory links; user may want to keep some specific rather than replacing all with homepage
- [20/22] "Extracting data from rate confirmations" — has a deep link to `ch_robinson.json#L532`; replacing with homepage loses the line-level specificity
- [22/22] "Introducing the Sensible configuration library" — post is *about* the config library; GitHub link may be intentional

**PDF upload pattern (for posts with `.pdf` links):**
1. `curl -L -o /tmp/<name>.pdf <github-raw-url>` then `md5sum /tmp/<name>.pdf`
2. MCP: `data_assets_tool > create_asset` with site_id `6033da353ede9143c0c56ff8`, file_name, file_hash
3. `python3 .claude/skills/update-webflow-blog-posts/upload_pdf_to_webflow.py /tmp/<name>.pdf --upload-url <url> --upload-details '<json>' --asset-id <id> --hosted-url <url>`
4. Replace GitHub URL with `hostedUrl` in post body

**Body file convention:** Save `bodies/<slug>-original.html` before any edit, `bodies/<slug>-updated.html` after `replace_in_body.py`. Use these for Webflow push and rollback.

---

## Posts (22 total)

- [x] **[1/22] How to extract data from cyber insurance quotes with Sensible**  
  ID: `69cd7daa04a65e810e6c0dcc`  
  Slug: `how-to-extract-data-from-cyber-insurance-quotes-with-sensible`  
  Config links replaced: `github.com/sensible-hq/sensible-configuration-library` → `sensible.so/configuration-library` ✓ (2026-07-15T19:49:07Z)  
  PDF uploaded: `beazley-cyber-quote-sample.pdf` → asset ID `6a57e6c26607f5fc29f2c883`  
  Webflow CDN URL: `https://cdn.prod.website-files.com/6033da353ede9143c0c56ff8/6a57e6c26607f5fc29f2c883_beazley-cyber-quote-sample.pdf`  
  Prerequisites normalized to delivery orders template ✓ (2026-07-15T21:14:43Z)  
  Bodies: `bodies/cyber-insurance-quotes-original.html` / `bodies/cyber-insurance-quotes-updated.html`  
  Status: **COMPLETE** — staged draft in Webflow, not yet published to live site

- [ ] **[2/22] How to extract data from insurance declaration pages with Sensible**  
  ID: `69cd60dca92a97423415aefe`  
  Slug: `how-to-extract-data-from-insurance-declaration-pages-with-sensible`  
  Config links (1): `github.com/.../Insurance/Policy%20Declaration%20Pages` → `sensible.so/configuration-library`

- [ ] **[3/22] How to capture the long tail when extracting data from paystubs**  
  ID: `68b4ca6b64e27f40075a6a74`  
  Slug: `paystubs-long-tail`  
  Config links (1): `github.com/.../templates` → `sensible.so/configuration-library`

- [ ] **[4/22] Introducing email data extraction**  
  ID: `686af2773c6c59ff5fbf9f15`  
  Slug: `introducing-email-data-extraction`  
  Config links (10): all point to specific subdirectories (Bank Statements, Healthcare, Pay Stubs, Driver License, ACORD Forms, Loss Runs, Policy Declaration Pages, Tax Forms, etc.)  
  ⚠️ FLAG: 10 specific subdirectory links — user may want to keep some specific rather than replacing all with homepage. Review each before approving.

- [ ] **[5/22] How to extract data from employment verification forms with Sensible**  
  ID: `68484c1bb88d34cd472a0fac`  
  Slug: `how-to-extract-data-from-employment-verification-forms-with-sensible`  
  Config links (3): root + Financial Services + Employment Verification

- [ ] **[6/22] How to extract data from CMS-1500 forms with Sensible**  
  ID: `6834e3538b72f426b66fef7b`  
  Slug: `how-to-extract-data-from-cms-1500-forms-with-sensible`  
  Config links (3): root + Healthcare + CMS 1500

- [ ] **[7/22] The opinionated guide to JsonLogic for transforming document data**  
  ID: `676065f09ed02c6c2ef6492c`  
  Slug: `opinionated-guide-to-jsonlogic-for-transforming-document-data`  
  Config links (1): `github.com/.../` (root with trailing slash)

- [ ] **[8/22] Import data from documents into Salesforce using Sensible and Zapier**  
  ID: `66db482abc5f75cbfcbfdf7d`  
  Slug: `import-data-from-documents-into-salesforce-using-sensible-and-zapier`  
  Config links (1): root

- [ ] **[9/22] How to extract data from rent rolls with LLMs and Sensible**  
  ID: `663e4b2314c5e1c698d4d80d`  
  Slug: `how-to-extract-data-from-rent-rolls-with-llms-and-sensible`  
  Config links (3): root + root/ + proptech subdirectory

- [ ] **[10/22] How to redact data, count items, and calculate values in documents using Sensible**  
  ID: `660453ed0ace39fb0fc8e083`  
  Slug: `transform-your-extracted-document-data-with-custom-logic`  
  Config links (1): root with trailing slash

- [ ] **[11/22] How to extract data from resumes with LLMs and Sensible**  
  ID: `65b139021db55585b5fa2990`  
  Slug: `how-to-extract-data-from-resumes-with-llms-and-sensible`  
  Config links (3): root + root/ + resume subdirectory

- [ ] **[12/22] How to extract data from bank statements with the Sensible Node SDK**  
  ID: `657b57fbf4465107ea3e5ff0`  
  Slug: `document-extraction-nodejs`  
  Config links (2): root + bank_statements subdirectory

- [ ] **[13/22] Guide to Using GPT-3 with Python**  
  ID: `6535a6df17ca225f10770e8f`  
  Slug: `guide-to-using-gpt-3-with-python`  
  Config links (2): root + bank_statements/bank_of_america subdirectory

- [ ] **[14/22] How to extract data from bank statements with Sensible**  
  ID: `65176057cde9c5589dd54a10`  
  Slug: `how-to-extract-data-from-bank-statements-with-sensible`  
  Config links (2): root/ + Bank Statements subdirectory

- [ ] **[15/22] Low-code document extraction: Import data from PDFs into your database using Zapier and Sensible**  
  ID: `65176057cde9c5589dd54a0f`  
  Slug: `low-code-pdf-to-database-with-zapier-and-sensible`  
  PDF links (1): `github.com/.../raw/main/tax_forms/1040/2021/1040_2021_sample.pdf` → upload to Webflow CDN  
  Config links (5): root + root/ + tax_forms subdirectories (2018, 2019, 2020) + Tax Forms template

- [ ] **[16/22] Sensible raises a $6.5MM seed round**  
  ID: `65176057cde9c5589dd54a0c`  
  Slug: `seed-funding`  
  Config links (1): root

- [ ] **[17/22] How to extract data from Explanation of Benefits documents**  
  ID: `65176057cde9c5589dd54a0b`  
  Slug: `how-to-extract-data-from-explanation-of-benefits-documents`  
  Config links (3): root/ + eobs subdirectory + Healthcare subdirectory

- [ ] **[18/22] How to extract data from closing disclosures**  
  ID: `65176057cde9c5589dd549be`  
  Slug: `how-to-extract-data-from-closing-disclosures`  
  Config links (4): root/ + root/tree/main/ + closing_disclosure + Real Estate template

- [ ] **[19/22] How to use GPT-4 to parse free-text documents**  
  ID: `65176057cde9c5589dd549dd`  
  Slug: `how-to-use-gpt-4-to-parse-free-text-documents`  
  Config links (1): root with trailing slash

- [ ] **[20/22] Extracting data from rate confirmations**  
  ID: `65176057cde9c5589dd549dc`  
  Slug: `extracting-data-from-rate-confirmations`  
  Config links (2): rate_confirmations subdirectory + deep link with line anchor (`ch_robinson.json#L532`)  
  ⚠️ FLAG: The `ch_robinson.json#L532` link points to a specific line in a specific file — replacing with the homepage loses that specificity. Decide: keep as-is, link to config library homepage, or find a better target.

- [ ] **[21/22] Debuting self-serve walkthroughs**  
  ID: `65176057cde9c5589dd54990`  
  Slug: `debuting-self-serve-walkthroughs`  
  Config links (1): root

- [ ] **[22/22] Introducing the Sensible configuration library**  
  ID: `65176057cde9c5589dd54943`  
  Slug: `introducing-the-sensible-configuration-library`  
  Config links (1): root  
  ⚠️ FLAG: This post is *about* the config library — the GitHub link may be intentional. Review before replacing.
