#!/usr/bin/env python3
"""Page gate: checks what readers see on docs pages, and each folder's _order.yaml.

The behavior is specified in SPEC.md next to this file; tests.yaml is the
acceptance test. Python 3 stdlib plus PyYAML.
"""

import argparse
import json
import os
import posixpath
import re
import sys

import yaml

ALPHABETICAL_FILE = "scripts/gates/page/alphabetical-folders.yaml"
HEADER = "Sensible uses JSON5 to support in-line comments"
LANGUAGES = {
    "json", "xml", "yaml", "yml", "txt", "bash", "shell", "curl", "node",
    "python", "mermaid", "",
}
ERROR, WARNING, STRICT = "error", "warning", "strict"
SEVERITY = {
    "unreadable": ERROR,
    "todo": ERROR,
    "draft-link": ERROR,
    "fence-language": ERROR,
    "fence-unclosed": ERROR,
    "json-line-comment": STRICT,
    "output-comment": STRICT,
    "json5-header-missing": STRICT,
    "json5-header-repeated": STRICT,
    "json5-comment-repeated": WARNING,
    "order-missing": ERROR,
    "order-bad-yaml": ERROR,
    "order-duplicate": ERROR,
    "order-stale": STRICT,
    "order-unlisted": STRICT,
    "order-unsorted": STRICT,
}

OPEN_FENCE = re.compile(r"^\s*(`{3,})(.*)$")
TODO = re.compile(r"(?<!\w)(TODO|FIXME|TBD)(?!\w)")
DRAFT_LINK = re.compile(r"doc:(draft-[\w-]+)")
WS = re.compile(r"\s+")


class CantRun(Exception):
    pass


def is_draft(name):
    return name.startswith("draft-")


def slug_of(relpath):
    """Slug of a page at a repo-relative path."""
    folder, name = posixpath.split(relpath)
    if name == "index.md":
        return posixpath.basename(folder)
    return name[:-3]


# --- Reading a page ---------------------------------------------------------


def scan_markdown(lines):
    """Split a page into lines of visible text and code blocks.

    Returns (kinds, visible, blocks):
      kinds[i]   'text' or 'code' (fence lines and code contents)
      visible[i] the line's visible text (HTML comments blanked with spaces)
      blocks     list of dicts: open (0-based line), close (or None), lang, body (list of line indexes)
    """
    kinds, visible, blocks = [], [], []
    in_comment = False
    block = None
    for i, line in enumerate(lines):
        if block is not None:
            kinds.append("code")
            visible.append(line)
            n = len(block["ticks"])
            m = re.match(r"^\s*(`+)\s*$", line)
            if m and len(m.group(1)) >= n:
                block["close"] = i
                block = None
            else:
                block["body"].append(i)
            continue
        if not in_comment:
            m = OPEN_FENCE.match(line)
            if m:
                info = m.group(2).strip()
                block = {
                    "open": i,
                    "close": None,
                    "ticks": m.group(1),
                    "lang": info.split()[0] if info else "",
                    "body": [],
                }
                blocks.append(block)
                kinds.append("code")
                visible.append(line)
                continue
        # Ordinary text: blank out HTML comments.
        out = []
        pos = 0
        while pos < len(line):
            if in_comment:
                end = line.find("-->", pos)
                if end < 0:
                    out.append(" " * (len(line) - pos))
                    pos = len(line)
                else:
                    out.append(" " * (end + 3 - pos))
                    pos = end + 3
                    in_comment = False
            else:
                start = line.find("<!--", pos)
                if start < 0:
                    out.append(line[pos:])
                    pos = len(line)
                else:
                    out.append(line[pos:start])
                    out.append(" " * 4)
                    pos = start + 4
                    in_comment = True
        kinds.append("text")
        visible.append("".join(out))
    return kinds, visible, blocks


def label_of(block, kinds, visible):
    """True when the block's label marks it as output."""
    i = block["open"] - 1
    while i >= 0:
        if kinds[i] == "code":
            return False
        if visible[i].strip():
            text = re.sub(r"[*_#]", "", visible[i]).strip()
            if text.endswith(":"):
                text = text[:-1].strip()
            return text.lower() in ("output", "example output")
        i -= 1
    return False


def scan_json(block, lines):
    """Tokenize a JSON block.

    Returns (line_comments, block_comments, key_comments):
      line_comments  0-based line indexes with a // comment
      block_comments list of (line, text)
      key_comments   list of (line, key, text)
    """
    body = block["body"]
    line_comments = []
    block_comments = []
    key_comments = []
    last_key = None  # (line, key)
    pending_string = None  # (line, content) of the last string, to see if it's a key
    in_block = None  # (start line, list of chars)
    for li in body:
        line = lines[li]
        pos = 0
        n = len(line)
        while pos < n:
            if in_block is not None:
                end = line.find("*/", pos)
                if end < 0:
                    in_block[1].append(line[pos:])
                    pos = n
                else:
                    in_block[1].append(line[pos:end])
                    pos = end + 2
                    start_line, parts = in_block
                    text = WS.sub(" ", "".join(parts)).strip()
                    block_comments.append((start_line, text))
                    if last_key is not None and last_key[0] == start_line:
                        key_comments.append((start_line, last_key[1], text))
                    in_block = None
                continue
            c = line[pos]
            if c in "\"'":
                j = pos + 1
                content = []
                while j < n:
                    if line[j] == "\\" and j + 1 < n:
                        content.append(line[j:j + 2])
                        j += 2
                        continue
                    if line[j] == c:
                        break
                    content.append(line[j])
                    j += 1
                pending_string = (li, "".join(content))
                pos = j + 1
                continue
            if line.startswith("/*", pos):
                in_block = (li, [])
                pos += 2
                pending_string = None
                continue
            if line.startswith("//", pos):
                line_comments.append(li)
                pos = n
                pending_string = None
                continue
            if c == ":" and pending_string is not None:
                last_key = pending_string
                pending_string = None
            elif not c.isspace():
                pending_string = None
            pos += 1
        if in_block is not None:
            in_block[1].append("\n")
    if in_block is not None:  # never closes: runs to the end of the block
        start_line, parts = in_block
        text = WS.sub(" ", "".join(parts)).strip()
        block_comments.append((start_line, text))
        if last_key is not None and last_key[0] == start_line:
            key_comments.append((start_line, last_key[1], text))
    return line_comments, block_comments, key_comments


def check_page(root, relpath, problems):
    full = os.path.join(root, *relpath.split("/"))
    try:
        with open(full, "rb") as f:
            data = f.read()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        problems.add((relpath, None, "unreadable", None))
        return
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = [l[:-1] if l.endswith("\r") else l for l in text.split("\n")]
    if lines and lines[-1] == "" and text.endswith("\n"):
        lines.pop()

    def add(i, rule, subject=None):
        problems.add((relpath, i + 1, rule, subject))

    kinds, visible, blocks = scan_markdown(lines)

    for i, v in enumerate(visible):
        for m in TODO.finditer(v):
            add(i, "todo", m.group(1))
        for m in DRAFT_LINK.finditer(v):
            add(i, "draft-link", m.group(1))

    header_seen = False
    first_commented_done = False
    earlier_keys = set()  # (key, text) from earlier config blocks
    for b in blocks:
        if b["lang"] not in LANGUAGES:
            add(b["open"], "fence-language", b["lang"])
        if b["close"] is None:
            add(b["open"], "fence-unclosed")
        if b["lang"] != "json":
            continue
        line_comments, block_comments, key_comments = scan_json(b, lines)
        for li in line_comments:
            add(li, "json-line-comment")
        if label_of(b, kinds, visible):
            if block_comments:
                add(block_comments[0][0], "output-comment")
            continue
        # Config block.
        headers = [li for li, t in block_comments if t == HEADER]
        if block_comments and not first_commented_done:
            first_commented_done = True
            if not headers:
                add(b["open"], "json5-header-missing")
        if headers:
            if header_seen:
                add(headers[0], "json5-header-repeated")
            elif len(headers) > 1:
                add(headers[1], "json5-header-repeated")
            header_seen = True
        for li, key, t in key_comments:
            if (key, t) in earlier_keys:
                add(li, "json5-comment-repeated", key)
        earlier_keys.update((key, t) for _, key, t in key_comments)


# --- _order.yaml ------------------------------------------------------------


def title_of(full, fallback):
    try:
        with open(full, "rb") as f:
            text = f.read().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return fallback
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.split("\n")
    if not lines or lines[0].rstrip("\r").strip() != "---":
        return fallback
    for j in range(1, len(lines)):
        if lines[j].rstrip("\r").strip() == "---":
            try:
                meta = yaml.safe_load("\n".join(lines[1:j]))
            except yaml.YAMLError:
                return fallback
            if isinstance(meta, dict):
                t = meta.get("title")
                if isinstance(t, str) and t:
                    return t
            return fallback
    return fallback


def folder_members(root, folder):
    """Map member name -> (kind, full path of the page or the subfolder's index.md)."""
    full = os.path.join(root, *folder.split("/"))
    members = {}
    for name in sorted(os.listdir(full)):
        p = os.path.join(full, name)
        if os.path.isdir(p):
            if not is_draft(name):
                members[name] = os.path.join(p, "index.md")
        elif os.path.isfile(p) and name.endswith(".md") and name != "index.md":
            slug = name[:-3]
            if not is_draft(slug):
                members[slug] = p
    return members


def check_folder(root, folder, alphabetical, problems):
    order_path = folder + "/_order.yaml"
    full_order = os.path.join(root, *order_path.split("/"))
    members = folder_members(root, folder)

    def add(rule, subject=None):
        problems.add((order_path, None, rule, subject))

    if not os.path.isfile(full_order):
        if members:
            add("order-missing")
        return
    try:
        with open(full_order, "rb") as f:
            entries = yaml.safe_load(f.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        add("order-bad-yaml")
        return
    if entries is None:
        entries = []
    if not isinstance(entries, list) or not all(isinstance(e, str) for e in entries):
        add("order-bad-yaml")
        return

    seen = set()
    kept = []  # entries in file order: not drafts, not stale, not repeats
    for e in entries:
        if is_draft(e):
            continue
        if e in seen:
            add("order-duplicate", e)
            continue
        seen.add(e)
        if e not in members:
            add("order-stale", e)
            continue
        kept.append(e)
    for m in members:
        if m not in seen:
            add("order-unlisted", m)

    if folder in alphabetical:
        keys = [title_of(members[e], e).lower() for e in kept]
        ordered = sorted(keys)
        for e, k, s in zip(kept, keys, ordered):
            if k != s:
                add("order-unsorted", e)
                break


# --- Command line -----------------------------------------------------------


def load_alphabetical(root):
    path = os.path.join(root, *ALPHABETICAL_FILE.split("/"))
    if not os.path.exists(path):
        return set()
    try:
        with open(path, "rb") as f:
            data = yaml.safe_load(f.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
        raise CantRun(f"{ALPHABETICAL_FILE}: can't read: {e}")
    if data is None:
        data = []
    if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
        raise CantRun(f"{ALPHABETICAL_FILE}: not a YAML list of strings")
    return {posixpath.normpath(x.replace("\\", "/")) for x in data}


def all_pages_and_folders(root):
    pages, folders = [], []
    docs = os.path.join(root, "docs")
    for dirpath, dirnames, filenames in os.walk(docs):
        dirnames.sort()
        rel = posixpath.join("docs", *os.path.relpath(dirpath, docs).split(os.sep)) \
            if os.path.relpath(dirpath, docs) != "." else "docs"
        folders.append(rel)
        for name in sorted(filenames):
            if name.endswith(".md") and os.path.isfile(os.path.join(dirpath, name)):
                pages.append(rel + "/" + name)
    return pages, folders


def select(root, paths):
    """Pages and folders to check for the PATH arguments."""
    pages, folders = [], []

    def add_folder(f):
        if (f == "docs" or f.startswith("docs/")) and os.path.isdir(os.path.join(root, *f.split("/"))):
            if f not in folders:
                folders.append(f)

    for p in paths:
        p = p.replace("\\", "/")
        if p.startswith("/"):
            continue
        p = posixpath.normpath(p)
        if not p.startswith("docs/"):
            continue
        name = posixpath.basename(p)
        full = os.path.join(root, *p.split("/"))
        if name.endswith(".md") and os.path.isfile(full) and p not in pages:
            pages.append(p)
        if name.endswith(".md") or name == "_order.yaml":
            parent = posixpath.dirname(p)
            add_folder(parent)
            if name == "index.md":
                add_folder(posixpath.dirname(parent))
    return pages, folders


def run(root, strict, paths):
    if not os.path.isdir(os.path.join(root, "docs")):
        raise CantRun(f"{os.path.join(root, 'docs')} isn't a folder")
    alphabetical = load_alphabetical(root)
    if paths:
        pages, folders = select(root, paths)
    else:
        pages, folders = all_pages_and_folders(root)
    problems = set()
    n_pages = 0
    for p in pages:
        if is_draft(slug_of(p)):
            continue
        n_pages += 1
        check_page(root, p, problems)
    for f in folders:
        check_folder(root, f, alphabetical, problems)

    out = []
    for path, line, rule, subject in problems:
        sev = SEVERITY[rule]
        if sev == STRICT:
            sev = ERROR if strict else WARNING
        out.append({"path": path, "line": line, "rule": rule, "severity": sev, "subject": subject})
    out.sort(key=lambda d: (d["path"], d["line"] is not None, d["line"] or 0,
                            d["rule"], d["subject"] is not None, d["subject"] or ""))
    return out, n_pages, len(folders)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check docs pages and _order.yaml files.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("paths", nargs="*", metavar="PATH")
    args = parser.parse_args(argv)
    try:
        problems, n_pages, n_folders = run(args.root, args.strict, args.paths)
    except CantRun as e:
        print(f"page gate: {e}", file=sys.stderr)
        return 2
    errors = sum(1 for p in problems if p["severity"] == ERROR)
    warnings = len(problems) - errors
    if args.json:
        print(json.dumps(problems, indent=2, ensure_ascii=False))
    else:
        for p in problems:
            loc = p["path"] + (f":{p['line']}" if p["line"] is not None else "")
            sub = f": {p['subject']}" if p["subject"] is not None else ""
            print(f"{loc}: {p['severity']}: {p['rule']}{sub}")
        print(f"page gate: {errors} error(s), {warnings} warning(s), "
              f"{n_pages} page(s), {n_folders} folder(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
