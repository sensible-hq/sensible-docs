#!/usr/bin/env python3
"""Build first-lines-draft.md: for each page in pages.json, the current excerpt, any ui-docs
short description, and the first 150 words of the page body.

Deterministic. Word counting rules (see the draft header): code blocks, images, tables, diagrams,
and HTML/JSX blocks become markers like [table] and don't count; link URLs are dropped (link text
kept); headings keep their text and are prefixed with "#"s; list items keep their text.

Usage (from the repo root): python3 .claude/sessions/seo/build_first_lines.py
"""
import json
import re
import subprocess
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCE = HERE / "pages.json"  # page list snapshot from PR #758's keywords-draft.md
OUT = HERE / "first-lines-draft.md"
PROPOSALS = HERE / "proposals.json"  # optional: proposed openings, keyed by page number
WORDS = 150

# ui-docs branch (PR #660): method id -> draft page number, for methods that are in the draft
UI_DOCS_REF = "origin/ui-docs"
UI_DOCS_PAGES = {"intersection": 10, "box": None, "checkbox": None, "nearestCheckbox": None}


def parse_source():
    """Return (groups, pages) in draft order from pages.json: groups = [(group_title, [n, ...])]."""
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    groups, pages = [], {}
    for g in data["groups"]:
        groups.append((g["title"], [p["n"] for p in g["pages"]]))
        for p in g["pages"]:
            pages[p["n"]] = {"title": p["title"], "path": p["path"]}
    return groups, pages


def read_page(rel):
    raw = (REPO / rel).read_text(encoding="utf-8").replace("\r\n", "\n")
    _, fm_text, body = raw.split("---", 2)
    fm = yaml.safe_load(fm_text) or {}
    if "api" in fm:  # spec-generated reference page
        spec = json.loads((REPO / "reference" / fm["api"]["file"]).read_text(encoding="utf-8"))
        for item in spec["paths"].values():
            for op in item.values():
                if isinstance(op, dict) and op.get("operationId") == fm["api"]["operationId"]:
                    return None, op.get("description") or "", "OpenAPI operation description"
    return fm.get("excerpt"), body, "page body"


def to_blocks(md):
    """Turn markdown into a list of (kind, text) blocks in reading order."""
    blocks, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            lang = s[3:].strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            blocks.append(("marker", "[diagram]" if lang == "mermaid" else "[code block]"))
            i = j + 1
            continue
        if s.startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            blocks.append(("marker", "[table]"))
            i = j
            continue
        if re.match(r"^<(Table|table|Image|img|Cards?|div|Callout|br)\b", s):
            tag = re.match(r"^<(\w+)", s).group(1)
            if s.endswith("/>") or tag in ("br", "img", "Image"):
                blocks.append(("marker", "[image]" if tag in ("Image", "img") else "")) if tag != "br" else None
                i += 1
                continue
            j = i + 1
            while j < len(lines) and f"</{tag}>" not in lines[j]:
                j += 1
            blocks.append(("marker", "[table]" if tag.lower() == "table" else f"[{tag}]"))
            i = j + 1
            continue
        if re.match(r"^!\[[^\]]*\]\([^)]*\)\s*$", s):
            blocks.append(("marker", "[image]"))
            i += 1
            continue
        if not s:
            i += 1
            continue
        if s.startswith("#"):
            blocks.append(("heading", s))
        elif re.match(r"^([*-]|\d+\.)\s", s):
            blocks.append(("item", s))
        else:
            blocks.append(("para", s))
        i += 1
    return [b for b in blocks if b and b[1]]


def clean(text):
    text = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "[image]", text)  # linked image
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "[image]", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # links -> text
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\\", "")
    return re.sub(r"\s+", " ", text).strip()


def first_words(md, limit=WORDS):
    """Return (rendered lines, words counted, truncated?)."""
    out, count = [], 0
    for kind, text in to_blocks(md):
        if kind == "marker":
            out.append(text)
            continue
        t = clean(text)
        words = t.split()
        prefix_words = 0
        if kind == "heading":
            prefix_words = 1  # the '#' marker isn't a word
        content = words[prefix_words:]
        if count + len(content) > limit:
            keep = limit - count
            cut = " ".join(words[: prefix_words + keep]) + " …"
            if kind == "heading":
                hashes, _, rest = cut.partition(" ")
                cut = f"`{hashes}` {rest}"
            out.append(cut)
            return out, limit, True
        if kind == "heading":
            hashes, _, rest = t.partition(" ")
            t = f"`{hashes}` {rest}"  # keep page headings from becoming draft headings
        out.append(t)
        count += len(content)
    return out, count, False


def ui_docs():
    """Return {page number: [(label, text)]} from the ui-docs branch."""
    found = {}
    try:
        raw = subprocess.run(["git", "show", f"{UI_DOCS_REF}:assets/ai/senseml-descriptions.json"],
                             cwd=REPO, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return found
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    raw = re.sub(r",\s*}", "}", raw)
    data = json.loads(raw)
    for method, n in UI_DOCS_PAGES.items():
        if n is None or method not in data:
            continue
        entry = data[method]
        desc = entry["description"] if isinstance(entry, dict) else entry
        found.setdefault(n, []).append(("`senseml-descriptions.json` description", desc))
        mini = subprocess.run(["git", "show", f"{UI_DOCS_REF}:assets/ai/mini-pages/{method}.md"],
                              cwd=REPO, capture_output=True, text=True)
        if mini.returncode == 0:
            paras = [p.strip() for p in mini.stdout.split("\n\n") if p.strip() and not p.strip().startswith(("#", "**", "```", "["))]
            if paras:
                found[n].append((f"`mini-pages/{method}.md` opening paragraph", paras[0]))
    return found


def main():
    groups, pages = parse_source()
    ui = ui_docs()
    proposals = {}
    if PROPOSALS.exists():
        proposals = {p["n"]: p for p in json.loads(PROPOSALS.read_text(encoding="utf-8"))}
    out = [
        "# First 150 words draft",
        "",
        "Goal: the first 150 words of each page's content explain exactly what the page covers, so human and",
        "agent readers can tell whether the page is for them.",
        "",
        "Generated by `build_first_lines.py` (deterministic; rerun to refresh). Per page:",
        "- **Current excerpt**: from frontmatter on this branch (PR #758 applies new excerpts; rerun after it merges).",
        "- **ui-docs short description**: from branch `ui-docs` (PR #660), only where that branch covers the page.",
        "- **First 150 words (current)**: the page body as plain text. Code blocks, images, tables, diagrams, and",
        "  HTML/JSX blocks appear as markers like `[table]` and don't count as words; link URLs are dropped;",
        "  headings keep their `#`s. `…` marks the 150-word cutoff. \"(entire page)\" means the page is shorter.",
        "- **Proposed opening**: a rewrite of the opening paragraph (from `proposals.json`), with the exact current",
        "  text it replaces, a rationale, and an independent rubric grade (criteria A and D; see `grades.md`).",
        "",
    ]
    for title, ns in groups:
        out += [f"## {title}", ""]
        for n in ns:
            p = pages[n]
            excerpt, body, source = read_page(p["path"])
            lines, count, truncated = first_words(body)
            rel = p["path"][len("docs/"):] if p["path"].startswith("docs/") else p["path"]
            out.append(f"### {n}. {p['title']}")
            out.append(f"File: `{rel}`")
            out.append("#### Current excerpt")
            out.append(excerpt if excerpt else "(none: spec-generated page)")
            for label, text in ui.get(n, []):
                out.append(f"#### ui-docs short description ({label})")
                out.append(text)
            note = f"{count} words" + ("" if truncated else ", entire page") + ("" if source == "page body" else f"; from {source}")
            out.append(f"#### First 150 words (current; {note})")
            out.extend(lines)
            prop = proposals.get(n)
            if prop:
                out.append(f"#### Proposed opening ({len(prop['proposed'].split())} words)")
                out.append(prop["proposed"])
                out.append(f"*Replaces:* \"{prop['replaces'][:200]}{'…' if len(prop['replaces']) > 200 else ''}\"")
                out.append(f"*Why:* {prop['rationale']}")
                if prop.get("grade"):
                    g = prop["grade"]
                    out.append(f"*Grade of proposed opening:* A {g['A']}, D {g['D']} (current: A {g['A_before']}, D {g['D_before']}). {g['note']}")
            out.append("")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}: {sum(len(ns) for _, ns in groups)} pages; ui-docs entries for {sorted(ui)}")


if __name__ == "__main__":
    main()
