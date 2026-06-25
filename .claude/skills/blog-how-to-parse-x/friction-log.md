# Friction Log: blog-how-to-parse-x

Running record of skill failures, near-misses, and friction points. Each entry has a root cause and a proposed fix so patterns become improvements to the skill or template.

---

## 2026-06-22 — All output blocks were wrong on first draft

**What happened:** The delivery orders draft was written with fully invented output blocks — wrong date, wrong port, wrong values, wrong format (`"LOS ANGELES, CA"` instead of `{"type": "string", "value": "Rotterdam"}`), wrong units (`"kg"` vs `"kilograms"`).

**Root cause:** Output blocks were written before any extraction was run. The skill wired testing as a post-draft checklist item, not as a prerequisite to writing output blocks. There was no constraint preventing imagination from filling in the blanks.

**Secondary cause:** The Sensible API wraps all values in `{"type": "...", "value": "..."}` objects — this wasn't in the template or style guide, so the format was guessed incorrectly.

**Fix needed in skill (Step 4):** Upload the config and run a live extraction *before* writing any output block. Output blocks must come from real API responses, never from inference.

**Fix needed in template:** Add a note that string outputs are always `{"type": "string", "value": "..."}` — not bare strings — so the format is never guessed wrong again.

**Fix needed in template:** App link from `upload_pr_extractor.py` should be printed to terminal only, not embedded in the draft.

---

## 2026-06-22 — Field summary flattened sections into top-level fields

**What happened:** The first field inventory table listed all fields at the same level — `goods.description_of_goods`, `goods.weight`, etc. appeared as rows alongside `departure` and `port_of_discharge`. The fact that `goods` is a `sections` field (a repeating structure containing sub-fields) was not visible.

**Root cause:** The summary format didn't account for the structural difference between top-level fields and section sub-fields.

**Fix needed in skill (Step 3):** Split the inventory into two blocks — "Top-level fields" and one block per sections field (e.g., "`goods` — sections field"). Sub-fields belong under their parent sections block, not in the main table.

---

## 2026-06-22 — Config files saved as plain JSON, stripping inline comments

**What happened:** The skill saved SenseML configs to disk as plain JSON — no inline comments. The blog post draft's code blocks were enriched by json5-commenter separately. Two divergent artifacts, no single source of truth.

**Root cause:** The skill had no step to sync the enriched draft back to the config files. Enrichment ran on the draft only; the config files were written from the raw input and never updated.

**Fix in skill (Step 6.5):** After json5-commenter enriches the draft, extract the "Putting it all together" code block and overwrite the combined post config file. The draft is the source of truth — one enrichment pass covers both.

---

## 2026-06-22 — Second config upload errors on golden re-upload

**What happened:** Running `upload_pr_extractor.py` a second time on the same document type (to publish the trimmed "Putting it all together" config) failed with `HTTP 400: the name is already in use` on the golden upload step. The script exited with an error, obscuring the fact that the config itself was published successfully and the app URL was still valid.

**Root cause:** `upload_golden` treats both POST and PUT failure as fatal (`sys.exit(1)`). But when the same PDF is uploaded a second time for a different config, the golden name collision is expected and harmless — the file is already on the server and fully usable.

**Fix in script (`upload_pr_extractor.py`):** When both POST and PUT fail on the golden upload, print a warning and return instead of exiting. The golden already exists; the app URL at the end is still correct.

---

## 2026-06-24 — Wrong Sensible app URL printed (full config, not combined)

**What happened:** The URL printed after Step 4 points to the original full config extraction. The writer needs the URL for the trimmed "Putting it all together" config — the one that actually matches what's in the post.

**Root cause:** SKILL.md has no step to upload the combined config after Step 6.5 and get its URL. The combined config is extracted to a file but never pushed to Sensible, so there's no app link for it.

**Fix needed in skill (Step 6.5):** After extracting the combined config from the draft, run `upload_and_extract.py` on it with a distinct config name (e.g., `[doc-type-slug]_blog`), save the output, and print that URL to the user as the verifiable app link for the post.

---

## 2026-06-24 — Sensible app URL not surfaced to user after extraction

**What happened:** `upload_and_extract.py` printed the Sensible app URL at the end of its output. Claude read it in the tool result but never relayed it to the user — the URL was silently consumed and the skill moved on to drafting.

**Root cause:** SKILL.md says "Print the Sensible app URL the script emits to the terminal for the writer to verify (do NOT embed it in the draft)" but gives no explicit checkpoint. Claude can process the tool result and continue to the next step without producing any user-facing output.

**Fix needed in skill (Step 4):** Add an explicit mandatory stop immediately after the script call: parse the URL from the script output and output it to the user in a response before continuing. Phrase it as a blocking checkpoint — "output the URL to the user, then proceed to Step 5."

---

## 2026-06-25 — Notion page missing all code blocks after HTML comments

**What happened:** Draft v2 of the Form 1004 blog post was pushed to Notion with `<!-- CONFIG:START -->` and `<!-- CONFIG:END -->` HTML comment markers in the content. Notion's markdown parser doesn't support HTML comments — it silently dropped all content after the first `<!-- ... -->` tag, which meant every code block in the bottom half of the page (the "Putting it all together" section and everything after it) was missing.

**Root cause:** The draft markdown uses HTML comments as extraction markers for `extract_config_from_draft.py`. These are never visible to a reader of the `.md` file (rendered as nothing in most markdown tools), but Notion's parser treats them as invalid syntax and truncates the page there.

**Fix needed in skill (Step 8):** Before passing draft content to any Notion tool, preprocess the content to strip all `<!-- ... -->` HTML comments — these are build-tool markers, not reader-visible content:

```bash
python3 -c "
import re
content = open('drafts/blog-[doc-type-slug].md').read()
content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
print(content)
" > /tmp/[doc-type-slug]_notion_content.txt
```

Then pass `/tmp/[doc-type-slug]_notion_content.txt` as the page content, not the raw draft.

---

## 2026-06-22 — Only one goods section returned (couldn't show two objects)

**What happened:** The template rule says "at least two objects per array field." The example document had only one cargo line item, so the goods array had one object. The rule couldn't be satisfied.

**Root cause:** Template rule was written without accounting for documents that genuinely have one repeating item.

**Fix needed in template:** Soften the rule — "show at least two objects *if present in the document*; if the document has only one, show it and note that the config handles multiple."
