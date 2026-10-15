"""Compare a documented output with Sensible's parsed_document.

Every key and value the docs show must agree; keys the docs leave out are ignored. `...` marks
what not to check: a value, an object member, or the rest of an array ([a, b, ...] or
[a, ..., z]). An array without `...` must match in full.
"""

import json
from typing import NamedTuple

from .jsonish import is_ellipsis

# A key the docs show that parsed_document doesn't have
MISSING = object()


class Diff(NamedTuple):
    path: tuple  # into the documented output, so a fix can be applied there
    expected: object
    actual: object  # MISSING if parsed_document has no such key


def diffs(expected, actual, path=()):
    """Every place where what the docs show disagrees with `actual`."""
    if is_ellipsis(expected):
        return []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [Diff(path, expected, actual)]
        found = []
        for key, value in expected.items():
            if key not in actual:
                found.append(Diff(path + (key,), value, MISSING))
            else:
                found += diffs(value, actual[key], path + (key,))
        return found
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return [Diff(path, expected, actual)]
        cut = next((i for i, e in enumerate(expected) if is_ellipsis(e)), None)
        if cut is None:
            if len(actual) != len(expected):
                return [Diff(path, expected, actual)]
            pairs = [(i, i) for i in range(len(expected))]
        else:
            head = list(range(cut))
            tail = [i for i in range(cut + 1, len(expected)) if not is_ellipsis(expected[i])]
            if len(actual) < len(head) + len(tail):
                return [Diff(path, expected, actual)]
            offset = len(actual) - len(expected)
            pairs = [(i, i) for i in head] + [(i, i + offset) for i in tail]
        return [d for i, j in pairs for d in diffs(expected[i], actual[j], path + (i,))]
    if isinstance(expected, bool) or isinstance(actual, bool):
        # In Python, True == 1 and False == 0. JSON booleans and numbers must not match.
        if type(expected) is type(actual) and expected == actual:
            return []
    elif isinstance(expected, float) or isinstance(actual, float):
        if isinstance(actual, (int, float)) and abs(expected - actual) < 1e-9:
            return []
    elif expected == actual:
        return []
    return [Diff(path, expected, actual)]


def coverage(expected, actual, path=(), notes=None):
    """What the comparison didn't check: `...` markers, shortened arrays, and keys the docs leave out.

    Returns {"skipped": [paths], "abbreviated": [(path, shown, total)], "extra_top_level": [keys],
    "extra_nested": count}.
    """
    if notes is None:
        notes = {"skipped": [], "abbreviated": [], "extra_top_level": [], "extra_nested": 0}
    if is_ellipsis(expected):
        notes["skipped"].append(path)
    elif isinstance(expected, dict) and isinstance(actual, dict):
        extra = [k for k in actual if k not in expected]
        if path:
            notes["extra_nested"] += len(extra)
        else:
            notes["extra_top_level"] += extra
        for k in expected:
            if k in actual:
                coverage(expected[k], actual[k], path + (k,), notes)
    elif isinstance(expected, list) and isinstance(actual, list):
        cut = next((i for i, e in enumerate(expected) if is_ellipsis(e)), None)
        if cut is None:
            pairs = list(zip(range(len(expected)), range(len(actual)))) if len(expected) == len(actual) else []
        else:
            shown = [i for i, e in enumerate(expected) if not is_ellipsis(e)]
            notes["abbreviated"].append((path, len(shown), len(actual)))
            offset = len(actual) - len(expected)
            pairs = [(i, i) for i in shown if i < cut] + [(i, i + offset) for i in shown if i > cut]
            pairs = [(i, j) for i, j in pairs if 0 <= j < len(actual)]
        for i, j in pairs:
            coverage(expected[i], actual[j], path + (i,), notes)
    return notes


def leaf_paths(value, path=()):
    """The path of every leaf (scalar or `...`) in a documented output."""
    if isinstance(value, dict) and value:
        for k, v in value.items():
            yield from leaf_paths(v, path + (k,))
    elif isinstance(value, list) and value:
        for i, v in enumerate(value):
            yield from leaf_paths(v, path + (i,))
    else:
        yield path


def value_at(obj, path):
    for segment in path:
        try:
            obj = obj[segment]
        except (KeyError, IndexError, TypeError):
            return MISSING
    return obj


def typed_field_path(expected, path):
    """The path of the innermost documented object with a "type" key that contains `path`.

    That object is the whole typed field (for example {source, value, unit, type}), which the judge
    needs to compare value and source together. Falls back to `path` itself.
    """
    for end in range(len(path), -1, -1):
        node = value_at(expected, path[:end])
        if isinstance(node, dict) and "type" in node:
            return path[:end]
    return path


def format_path(path):
    return "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in path)


def describe(diff):
    if diff.actual is MISSING:
        return f"{format_path(diff.path)}: missing from actual output"
    return f"{format_path(diff.path)}: expected {json.dumps(diff.expected)}, got {json.dumps(diff.actual)}"


def apply_fixes(expected, fixes):
    """A copy of `expected` with each mismatched value replaced by the actual value."""
    fixed = json.loads(json.dumps(expected))
    for diff in fixes:
        if not diff.path:
            return diff.actual
        parent = fixed
        for step in diff.path[:-1]:
            parent = parent[step]
        if diff.actual is MISSING:
            del parent[diff.path[-1]]
        else:
            parent[diff.path[-1]] = diff.actual
    return fixed
