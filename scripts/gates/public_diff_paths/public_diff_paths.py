#!/usr/bin/env python3
"""Fail a change that adds or changes a file at a path that never belongs in this public repo.

Spec: SPEC.md beside this file (tests.yaml is the acceptance test).

Usage: public_diff_paths.py --base REF --head REF [--repo DIR] [--denylist FILE]
Exit: 0 no forbidden path, 1 at least one, 2 couldn't run.
"""
import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

NAME = "public_diff_paths.py"
BUILTIN = ["**/runs/", "**/specs/", "**/design/docops/", "**/judges/*/labels/", "*.jsonl"]
DEFAULT_DENYLIST = Path(__file__).resolve().parent / "denylist.txt"


class CantRun(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise CantRun(message)


def git(repo, *args):
    res = subprocess.run(["git", "-C", str(repo), "-c", "core.quotePath=off", *args],
                         capture_output=True)
    return res.returncode, res.stdout


def read_denylist(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise CantRun(f"can't read denylist {path}: {exc.__class__.__name__}")
    patterns = []
    for n, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("/") or ".." in line.split("/"):
            raise CantRun(f"{path}:{n}: bad pattern: {line}")
        patterns.append(line)
    return patterns


def match_parts(pat, parts):
    """Do pattern components `pat` match path components `parts` exactly (with ** spanning)?"""
    if not pat:
        return not parts
    if pat[0] == "**":
        return any(match_parts(pat[1:], parts[i:]) for i in range(len(parts) + 1))
    return bool(parts) and fnmatch.fnmatchcase(parts[0], pat[0]) and match_parts(pat[1:], parts[1:])


def matches(pattern, path):
    parts = path.split("/")
    if "/" not in pattern:
        return fnmatch.fnmatchcase(parts[-1], pattern)
    if pattern.endswith("/"):
        pat = pattern.rstrip("/").split("/")
        # a folder pattern: some proper prefix of the path is the folder
        return any(match_parts(pat, parts[:k]) for k in range(1, len(parts)))
    return match_parts(pattern.split("/"), parts)


def changed_paths(repo, base, head):
    code, _ = git(repo, "rev-parse", "--git-dir")
    if code != 0:
        raise CantRun(f"not a git checkout: {repo}")
    for ref in (base, head):
        code, _ = git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
        if code != 0:
            raise CantRun(f"not a commit: {ref}")
    code, _ = git(repo, "merge-base", base, head)
    if code != 0:
        raise CantRun(f"no merge base: {base} and {head}")
    code, out = git(repo, "diff", "--name-only", "--no-renames", "--diff-filter=d", "-z",
                    f"{base}...{head}")
    if code != 0:
        raise CantRun(f"git diff failed: {base}...{head}")
    return sorted(p for p in out.decode("utf-8", "surrogateescape").split("\0") if p)


def main(argv):
    parser = Parser(prog=NAME)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--denylist", default=str(DEFAULT_DENYLIST))
    try:
        args = parser.parse_args(argv)
        patterns = BUILTIN + read_denylist(args.denylist)
        paths = changed_paths(args.repo, args.base, args.head)
    except CantRun as exc:
        sys.stderr.write(f"{NAME}: {exc}\n")
        return 2
    errors = 0
    for path in paths:
        hit = next((p for p in patterns if matches(p, path)), None)
        if hit is not None:
            errors += 1
            print(f"{path}: error: forbidden-path: {hit}")
    print(f"public diff paths: {errors} error(s), {len(paths)} changed path(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
