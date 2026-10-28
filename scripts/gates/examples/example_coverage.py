#!/usr/bin/env python3
"""Example-coverage gate: checks that changed SenseML examples are covered by a code test.

Behavior is defined by SPEC.md in this folder; tests.yaml is the acceptance test.

    example_coverage.py --base DIR --head DIR [--json] [--print-tests]
"""

import argparse
import json
import os
import re
import sys

FENCE_OPEN = re.compile(r"^\s*(`{3,})(.*)$")
FENCE_CLOSE = re.compile(r"^\s*(`{3,})\s*$")
TEST_ID = re.compile(r"^[a-z0-9_]+$")
CONFIG_KEYS = {"fields", "method", "preprocessors", "postprocessor", "computed_fields", "fingerprint", "sections"}
OUTPUT_LABELS = {"output", "example output"}


class Comment:
    def __init__(self, start, end, line, text):
        self.start = start  # offset of "<!--"
        self.end = end  # offset just past "-->"
        self.line = line  # 1-based line of "<!--"
        self.text = text


class Block:
    def __init__(self, line, fence_start, ticks, info):
        self.line = line  # 1-based line of the opening fence
        self.fence_start = fence_start  # offset of the opening fence line's start
        self.ticks = ticks
        self.info = info
        self.language = info.split()[0] if info.split() else ""
        self.body = []
        self.above = None  # the comment directly above, if any


class CodeTest:
    def __init__(self, opening, header):
        self.opening = opening
        self.header = header
        self.closing = None
        self.limit = None  # offset where the test's inside ends
        self.unclosed = False
        self.test_id = None
        try:
            parsed = json.loads(header) if header else None
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            tid = parsed.get("testId")
            if isinstance(tid, str) and TEST_ID.match(tid):
                self.test_id = tid

    def contains(self, comment):
        return self.opening.end <= comment.start and comment.end <= self.limit


# --- Reading a page ----------------------------------------------------------


def scan(text):
    """Returns (blocks, comments, label_lines, closing_fence_lines) for a page's text."""
    lines = text.split("\n")
    blocks, comments = [], []
    stripped = []  # each line with comments removed (code block lines as is)
    closing = set()  # 0-based indexes of closing fence lines
    open_block = None
    comment_start = comment_line = None
    offset = 0
    for i, raw in enumerate(lines):
        line = raw[:-1] if raw.endswith("\r") else raw
        base = offset
        offset += len(raw) + 1
        if open_block is not None:
            m = FENCE_CLOSE.match(line)
            if m and len(m.group(1)) >= open_block.ticks:
                closing.add(i)
                open_block = None
            else:
                open_block.body.append(line)
            stripped.append(line)
            continue
        col = 0
        if comment_start is not None:
            j = line.find("-->")
            if j < 0:
                stripped.append("")
                continue
            end = base + j + 3
            comments.append(Comment(comment_start, end, comment_line, text[comment_start + 4 : end - 3].strip()))
            comment_start = None
            col = j + 3
        else:
            m = FENCE_OPEN.match(line)
            if m:
                open_block = Block(i + 1, base, len(m.group(1)), m.group(2).strip())
                blocks.append(open_block)
                stripped.append(line)
                continue
        pieces = []
        while True:
            k = line.find("<!--", col)
            if k < 0:
                pieces.append(line[col:])
                break
            pieces.append(line[col:k])
            e = line.find("-->", k + 4)
            if e < 0:
                comment_start, comment_line = base + k, i + 1
                break
            start, end = base + k, base + e + 3
            comments.append(Comment(start, end, i + 1, text[start + 4 : end - 3].strip()))
            col = e + 3
        stripped.append("".join(pieces))
    # A comment that never closes is dropped: it can't be directly above anything.

    for b in blocks:
        before = [c for c in comments if c.end <= b.fence_start]
        if before and text[before[-1].end : b.fence_start].strip() == "":
            b.above = before[-1]
    return blocks, comments, stripped, closing


def lex_json(body):
    """Returns (content, key names) for a JSON block's body."""
    s = body
    n = len(s)
    tokens = []  # (kind, text, name)
    i = 0
    while i < n:
        c = s[i]
        if c == '"' or c == "'":
            j = i + 1
            closed = False
            while j < n:
                ch = s[j]
                if ch == "\n":
                    break
                if ch == "\\" and j + 1 < n and s[j + 1] != "\n":
                    j += 2
                    continue
                if ch == c:
                    j += 1
                    closed = True
                    break
                j += 1
            j = min(j, n)
            tok = s[i:j]
            name = tok[1:-1] if closed else tok[1:]
            tokens.append(("str", tok, name))
            i = j
        elif s.startswith("/*", i):
            j = s.find("*/", i + 2)
            i = n if j < 0 else j + 2
        elif s.startswith("//", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
        elif c.isspace():
            i += 1
        else:
            tokens.append(("ch", c, None))
            i += 1
    keys = set()
    for a, b in zip(tokens, tokens[1:]):
        if a[0] == "str" and b == ("ch", ":", None):
            keys.add(a[2])
    return "".join(t[1] for t in tokens), keys


def says_output(label):
    s = re.sub(r"[*_#]", "", label).strip()
    if s.endswith(":"):
        s = s[:-1]
    return s.lower() in OUTPUT_LABELS


def label_of(block, stripped, closing):
    i = block.line - 2
    while i >= 0:
        if stripped[i].strip():
            return None if i in closing else stripped[i]
        i -= 1
    return None


def is_marker(text):
    return text.startswith("inline config") or text.startswith("inline output")


def exemption(comment):
    """Returns None if the comment isn't an exemption, else its reason ('' for none)."""
    if comment is None:
        return None
    t = comment.text
    if t == "no code test":
        return ""
    if t.startswith("no code test:"):
        return " ".join(t[len("no code test:") :].split())
    return None


def is_test_opening(text):
    if text == "code test end" or not text.startswith("code test"):
        return False
    return len(text) == 9 or text[9].isspace()


class Page:
    def __init__(self, text):
        self.text = text
        blocks, comments, stripped, closing = scan(text)
        self.comments = comments
        self.blocks = blocks
        self.json_blocks = []
        for b in blocks:
            if b.language != "json":
                continue
            b.content, keys = lex_json("\n".join(b.body))
            above = b.above.text if b.above else ""
            if above.startswith("inline output"):
                b.kind = "output"
            elif above.startswith("inline config"):
                b.kind = "config"
            elif (lbl := label_of(b, stripped, closing)) is not None and says_output(lbl):
                b.kind = "output"
            elif keys & CONFIG_KEYS and "parsed_document" not in keys:
                b.kind = "config"
            else:
                b.kind = "plain"
            self.json_blocks.append(b)
        self.tests = []
        current = None
        for c in comments:
            if c.text == "code test end":
                if current is not None:
                    current.closing = c
                    current.limit = c.start
                    current = None
            elif is_test_opening(c.text):
                if current is not None:
                    current.unclosed = True
                    current.limit = c.start
                current = CodeTest(c, c.text[9:].strip())
                self.tests.append(current)
        if current is not None:
            current.unclosed = True
            current.limit = len(text)

    def test_for(self, comment):
        for t in self.tests:
            if t.contains(comment):
                return t
        return None


# --- Checking ----------------------------------------------------------------


def read_text(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return text[1:] if text.startswith("\ufeff") else text


def list_pages(root):
    docs = os.path.join(root, "docs")
    pages = []
    if not os.path.isdir(docs):
        return pages
    for dirpath, dirnames, filenames in os.walk(docs):
        dirnames.sort()
        for name in filenames:
            if name.endswith(".md"):
                full = os.path.join(dirpath, name)
                pages.append(os.path.relpath(full, root).replace(os.sep, "/"))
    return sorted(pages)


def check_page(path, text, base_text, problems, covering):
    """Checks one changed head page. Returns the number of changed example blocks."""

    def report(line, rule, severity, subject=None):
        problems.append({"path": path, "line": line, "rule": rule, "severity": severity, "subject": subject})

    page = Page(text)
    base_pool = []
    if base_text is not None:
        base_pool = [b.content for b in Page(base_text).json_blocks]

    changed = []
    for b in page.json_blocks:
        if b.content in base_pool:
            base_pool.remove(b.content)
        elif b.kind != "plain":
            changed.append(b)

    # Code test markup
    seen_ids = set()
    for t in page.tests:
        if t.test_id is None:
            report(t.opening.line, "test-markup", "error", "header")
        if t.unclosed:
            report(t.opening.line, "test-markup", "error", "unclosed")
        if t.test_id is not None:
            if t.test_id in seen_ids:
                report(t.opening.line, "test-markup", "error", "duplicate-id")
            seen_ids.add(t.test_id)
    below = {id(b.above): b for b in page.blocks if b.above is not None}
    for c in page.comments:
        if not is_marker(c.text):
            continue
        t = page.test_for(c)
        if t is None:
            report(c.line, "test-markup", "error", "marker-outside-test")
        elif id(c) not in below:
            report(c.line, "test-markup", "error", "marker-without-block")

    # Changed example blocks
    covering_tests = set()
    for b in changed:
        reason = exemption(b.above)
        if reason is not None:
            if reason:
                report(b.line, "exempt", "warning", reason)
            else:
                report(b.line, "exempt-no-reason", "error")
            continue
        t = page.test_for(b.above) if b.above is not None and is_marker(b.above.text) else None
        if t is not None and t.test_id is not None and not t.unclosed:
            covering_tests.add(id(t))
            continue
        report(b.line, "config-untested" if b.kind == "config" else "output-untested", "error")

    # Covering tests
    for t in page.tests:
        if t.test_id is None or t.unclosed:
            continue
        own = text[t.opening.start : t.closing.end]
        if id(t) in covering_tests or base_text is None or own not in base_text:
            covering.add((path, t.test_id))
    return len(changed)


def run(base, head):
    problems, covering = [], set()
    changed_blocks = 0
    for path in list_pages(head):
        if os.path.basename(path).startswith("draft-"):
            continue
        text = read_text(os.path.join(head, path))
        if text is None:
            problems.append({"path": path, "line": None, "rule": "unreadable", "severity": "error", "subject": None})
            continue
        base_path = os.path.join(base, path)
        base_text = read_text(base_path) if os.path.isfile(base_path) else None
        if base_text is not None and base_text == text:
            continue
        changed_blocks += check_page(path, text, base_text, problems, covering)
    problems.sort(key=lambda p: (p["path"], p["line"] is not None, p["line"] or 0, p["rule"], p["subject"] or ""))
    return problems, sorted(covering), changed_blocks


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check that changed SenseML examples have a code test.")
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--print-tests", action="store_true")
    args = parser.parse_args(argv)
    if not os.path.isdir(args.base):
        print(f"example_coverage: base isn't a folder: {args.base}", file=sys.stderr)
        return 2
    if not os.path.isdir(os.path.join(args.head, "docs")):
        print(f"example_coverage: head has no docs/ folder: {args.head}", file=sys.stderr)
        return 2

    problems, covering, changed_blocks = run(args.base, args.head)
    errors = sum(1 for p in problems if p["severity"] == "error")
    warnings = len(problems) - errors

    if args.print_tests:
        if args.json:
            print(json.dumps([{"path": p, "testId": t} for p, t in covering], indent=2))
        else:
            for p, t in covering:
                print(f"{p}\t{t}")
    elif args.json:
        print(json.dumps(problems, indent=2, ensure_ascii=False))
    else:
        for p in problems:
            loc = p["path"] if p["line"] is None else f"{p['path']}:{p['line']}"
            sub = f": {p['subject']}" if p["subject"] is not None else ""
            print(f"{loc}: {p['severity']}: {p['rule']}{sub}")
        print(
            f"example coverage: {errors} error(s), {warnings} warning(s), "
            f"{changed_blocks} changed block(s), {len(covering)} test(s)"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
