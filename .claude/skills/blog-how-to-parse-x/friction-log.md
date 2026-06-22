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

## 2026-06-22 — Only one goods section returned (couldn't show two objects)

**What happened:** The template rule says "at least two objects per array field." The example document had only one cargo line item, so the goods array had one object. The rule couldn't be satisfied.

**Root cause:** Template rule was written without accounting for documents that genuinely have one repeating item.

**Fix needed in template:** Soften the rule — "show at least two objects *if present in the document*; if the document has only one, show it and note that the config handles multiple."
