"""Parse the JSON in docs code blocks: JSON plus comments, trailing commas (configs only), and `...`."""

import json
import re

# A bare `...` in a documented output block becomes this string while parsing
ELLIPSIS = "__ELLIPSIS__"
TRAILING_COMMA = re.compile(r",(\s*[}\]])")


def is_ellipsis(value):
    """`...` (bare or as a string) or "…" means "don't check this" in a documented output."""
    return value in (ELLIPSIS, "...", "…")


class SyntaxIssue(Exception):
    def __init__(self, message, line):
        super().__init__(message)
        self.line = line


def strip_json5(text, trailing_commas=True):
    """Remove /* */ and // comments and trailing commas, leaving strings intact.

    Removed comments keep their newlines, so parse errors report the right line. With
    trailing_commas=False, a trailing comma raises SyntaxIssue instead of being removed.

    A bare `...` becomes the ELLIPSIS string. In an object's key position it becomes an
    `"__ELLIPSIS__": null` member, which drop_ellipsis_keys removes after parsing.
    """
    out = []
    stack = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if text.startswith("...", i):
            previous = "".join(out).rstrip()[-1:]
            key_position = bool(stack) and stack[-1] == "{" and previous in ("{", ",")
            out.append(f'"{ELLIPSIS}": null' if key_position else f'"{ELLIPSIS}"')
            i += 3
        elif c in "{[":
            stack.append(c)
            out.append(c)
            i += 1
        elif c in "}]":
            if stack:
                stack.pop()
            out.append(c)
            i += 1
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i : j + 1])
            i = j + 1
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end == -1:
                raise SyntaxIssue("unclosed /* comment", text.count("\n", 0, i) + 1)
            out.append("\n" * text.count("\n", i, end))
            i = end + 2
        elif text.startswith("//", i):
            end = text.find("\n", i)
            i = n if end == -1 else end
        else:
            out.append(c)
            i += 1
    stripped = "".join(out)
    if not trailing_commas:
        match = TRAILING_COMMA.search(stripped)
        if match:
            raise SyntaxIssue("trailing comma", stripped.count("\n", 0, match.start()) + 1)
    return TRAILING_COMMA.sub(r"\1", stripped)


def _strict_pairs(pairs):
    keys = [k for k, _ in pairs if k != ELLIPSIS]
    duplicates = sorted({k for k in keys if keys.count(k) > 1})
    if duplicates:
        raise ValueError(f"duplicate key {json.dumps(duplicates[0])}")
    return dict(pairs)


def _reject_constant(name):
    raise ValueError(f"{name} isn't valid JSON")


def drop_ellipsis_keys(value):
    if isinstance(value, dict):
        return {k: drop_ellipsis_keys(v) for k, v in value.items() if k != ELLIPSIS}
    if isinstance(value, list):
        return [drop_ellipsis_keys(v) for v in value]
    return value


def parse_block(text, trailing_commas=True):
    """Parse a docs code block, raising SyntaxIssue with a line number relative to the block.

    Rejects duplicate keys and NaN/Infinity. trailing_commas=False is for output blocks:
    Sensible never outputs trailing commas.
    """
    stripped = strip_json5(text, trailing_commas)
    try:
        value = json.loads(stripped, object_pairs_hook=_strict_pairs, parse_constant=_reject_constant)
    except json.JSONDecodeError as e:
        raise SyntaxIssue(e.msg, e.lineno)
    except ValueError as e:
        raise SyntaxIssue(str(e), None)
    return drop_ellipsis_keys(value)


def has_bare_ellipsis(text):
    return ELLIPSIS in strip_json5(text) and ELLIPSIS not in text
