#!/usr/bin/env python3
"""
publish_to_notion.py — Push a blog draft to Notion as a versioned child page.

Usage:
    python3 .claude/skills/blog-how-to-parse-x/publish_to_notion.py \
        --draft drafts/blog-residential-appraisal-reports.md \
        --parent-id 38ac7dd4-9788-81a0-9ff1-ce6b59651538

Requires:
    NOTION_API_KEY environment variable — a Notion internal integration token.
    Create one at https://www.notion.so/my-integrations, then share the target
    page with the integration.

Creates "Draft vN — YYYY-MM-DD" as a child page under --parent-id.
Strips HTML comments before parsing. Preserves code block content verbatim,
including all /* */ inline comments.
"""

import argparse
import os
import re
import sys
from datetime import date

import requests

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
MAX_TEXT_LEN = 2000  # Notion rich_text element character limit


# ── Auth ───────────────────────────────────────────────────────────────────────

def _headers() -> dict:
    key = os.environ.get("NOTION_API_KEY", "").strip()
    if not key:
        sys.exit("Error: NOTION_API_KEY environment variable is not set.\n"
                 "Create an integration at https://www.notion.so/my-integrations")
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


# ── Rich text helpers ──────────────────────────────────────────────────────────

def _parse_inline(text: str) -> list[dict]:
    """
    Convert markdown inline formatting to Notion rich_text elements.
    Handles **bold**, `inline code`, and [link](url).
    """
    pattern = re.compile(
        r'(\*\*(.+?)\*\*)'                 # **bold**
        r'|(`([^`\n]+)`)'                  # `code`
        r'|(\[([^\]]+)\]\(([^)]+)\))'     # [text](url)
    )
    result = []
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            result.extend(_split_plain(text[pos:m.start()]))
        if m.group(1):  # bold
            result.append({"type": "text", "text": {"content": m.group(2)},
                           "annotations": {"bold": True}})
        elif m.group(3):  # inline code
            result.append({"type": "text", "text": {"content": m.group(4)},
                           "annotations": {"code": True}})
        elif m.group(5):  # link
            result.append({"type": "text",
                           "text": {"content": m.group(6), "link": {"url": m.group(7)}}})
        pos = m.end()
    if pos < len(text):
        result.extend(_split_plain(text[pos:]))
    return result or [{"type": "text", "text": {"content": ""}}]


def _split_plain(text: str) -> list[dict]:
    """Split plain text into ≤2000-char chunks (Notion limit per rich_text element)."""
    chunks = []
    while text:
        chunks.append({"type": "text", "text": {"content": text[:MAX_TEXT_LEN]}})
        text = text[MAX_TEXT_LEN:]
    return chunks


def _chunk_code(content: str) -> list[dict]:
    """Split code content into ≤2000-char rich_text elements."""
    chunks = []
    while content:
        chunks.append({"type": "text", "text": {"content": content[:MAX_TEXT_LEN]}})
        content = content[MAX_TEXT_LEN:]
    return chunks or [{"type": "text", "text": {"content": ""}}]


# ── Block builders ─────────────────────────────────────────────────────────────

def _heading(text: str, level: int) -> dict:
    t = f"heading_{min(level, 3)}"
    return {"type": t, t: {"rich_text": _parse_inline(text)}}


def _paragraph(text: str) -> dict:
    return {"type": "paragraph", "paragraph": {"rich_text": _parse_inline(text)}}


def _bullet(text: str) -> dict:
    return {"type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": _parse_inline(text)}}


def _code(content: str, language: str) -> dict:
    # Normalize language: Notion doesn't know json5
    lang = "json" if language in ("json5", "json") else (language or "plain text")
    return {"type": "code", "code": {"rich_text": _chunk_code(content), "language": lang}}


def _divider() -> dict:
    return {"type": "divider", "divider": {}}


# ── Markdown parser ────────────────────────────────────────────────────────────

def _preprocess(content: str) -> str:
    """Strip <!-- HTML comments --> — Notion drops all content after the first one."""
    return re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)


def parse_blocks(content: str) -> list[dict]:
    """Parse preprocessed markdown into Notion block dicts."""
    blocks = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        # Fenced code block — consume all lines until closing fence verbatim
        if line.startswith('```'):
            lang = line[3:].strip() or 'plain text'
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append(_code('\n'.join(code_lines), lang))
            i += 1
            continue

        # Headings
        if line.startswith('#### '):
            blocks.append(_heading(line[5:], 3))
        elif line.startswith('### '):
            blocks.append(_heading(line[4:], 3))
        elif line.startswith('## '):
            blocks.append(_heading(line[3:], 2))
        elif line.startswith('# '):
            blocks.append(_heading(line[2:], 1))
        # Horizontal rule
        elif line.strip() == '---':
            blocks.append(_divider())
        # Bullet list (- or *)
        elif re.match(r'^[-*] ', line):
            blocks.append(_bullet(line[2:]))
        # Numbered list — render as bullets for review copy
        elif re.match(r'^\d+\. ', line):
            blocks.append(_bullet(re.sub(r'^\d+\. ', '', line)))
        # Blank line — skip (Notion handles spacing)
        elif not line.strip():
            pass
        # Paragraph
        else:
            blocks.append(_paragraph(line))

        i += 1

    return blocks


# ── Notion API ─────────────────────────────────────────────────────────────────

def _get_child_version(parent_id: str) -> int:
    """Return the highest existing Draft vN version number under parent_id (0 if none)."""
    url = f"{NOTION_API}/blocks/{parent_id}/children"
    resp = requests.get(url, headers=_headers(), params={"page_size": 100})
    resp.raise_for_status()
    versions = []
    for block in resp.json().get("results", []):
        if block.get("type") == "child_page":
            m = re.match(r"Draft v(\d+)", block["child_page"].get("title", ""))
            if m:
                versions.append(int(m.group(1)))
    return max(versions, default=0)


def _create_child_page(parent_id: str, title: str) -> str:
    """Create an empty child page under parent_id. Returns the new page ID."""
    resp = requests.post(
        f"{NOTION_API}/pages",
        headers=_headers(),
        json={
            "parent": {"type": "page_id", "page_id": parent_id},
            "properties": {
                "title": {"title": [{"type": "text", "text": {"content": title}}]}
            },
        },
    )
    resp.raise_for_status()
    return resp.json()["id"]


def _append_blocks(page_id: str, blocks: list[dict]) -> None:
    """Append blocks to a page in batches of 100 (Notion API limit)."""
    url = f"{NOTION_API}/blocks/{page_id}/children"
    total = len(blocks)
    for start in range(0, total, 100):
        batch = blocks[start:start + 100]
        resp = requests.patch(url, headers=_headers(), json={"children": batch})
        if not resp.ok:
            print(f"  Error on batch {start//100 + 1}: {resp.status_code} — {resp.text[:300]}",
                  file=sys.stderr)
            resp.raise_for_status()
        end = min(start + 100, total)
        print(f"  Appended blocks {start + 1}–{end} of {total}")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--draft", required=True, help="Path to draft .md file")
    ap.add_argument("--parent-id", required=True,
                    help="Notion page ID of the main Content Tracker entry for this post")
    args = ap.parse_args()

    # Read and preprocess draft
    draft_path = args.draft
    if not os.path.exists(draft_path):
        sys.exit(f"Error: draft file not found: {draft_path}")
    content = open(draft_path).read()
    content = _preprocess(content)

    # Auto-version: find highest existing Draft vN child, increment
    current_version = _get_child_version(args.parent_id)
    version = current_version + 1
    today = date.today().strftime("%Y-%m-%d")
    title = f"Draft v{version} — {today}"  # em dash
    print(f"Target parent: {args.parent_id}")
    print(f"Creating child page: {title!r}")

    # Parse markdown to blocks
    blocks = parse_blocks(content)
    print(f"Parsed {len(blocks)} blocks from {draft_path}")

    # Create child page
    page_id = _create_child_page(args.parent_id, title)
    print(f"Created page: {page_id}")

    # Append all blocks
    _append_blocks(page_id, blocks)

    clean_id = page_id.replace("-", "")
    print(f"\nDone → https://notion.so/{clean_id}")


if __name__ == "__main__":
    main()
