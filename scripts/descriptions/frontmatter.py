"""
Shared helpers for reading and writing YAML front matter in docs/ and reference/.

excerpt is the source of truth for SEO descriptions; metadata.description is
derived from it. In reference/, both fields are optional: a missing key means
the field was intentionally omitted, so only keys that exist but are empty
count as missing.
"""

import re
from pathlib import Path
from typing import Iterator, NamedTuple

import yaml

SCRIPT_DIR = Path(__file__).parent.resolve()
MAX_LENGTH = 160

_CLOSING_FENCE = re.compile(r"\n---\s*(\n|$)")


def find_repo_root() -> Path:
    candidate = SCRIPT_DIR.parent.parent
    if (candidate / "docs").is_dir():
        return candidate
    cwd = Path.cwd()
    if (cwd / "docs").is_dir():
        return cwd
    raise SystemExit("Could not find repo root (expected docs/ directory)")


def load_ignore_list() -> set[str]:
    ignore_file = SCRIPT_DIR / "description_ignore.txt"
    if not ignore_file.exists():
        return set()
    return {
        line.strip()
        for line in ignore_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


class Split(NamedTuple):
    text: str  # front matter between the fences, without the leading "---"
    closing: int  # index of the newline before the closing fence
    body: int  # index where the body starts, after the closing fence line


def split(content: str) -> Split | None:
    if not content.startswith("---"):
        return None
    end = _CLOSING_FENCE.search(content, 3)
    if not end:
        return None
    return Split(content[3 : end.start()], end.start(), end.end())


class Doc(NamedTuple):
    path: Path
    fm: dict | None  # None if there's no front matter or it doesn't parse
    error: str | None  # YAML error, if the front matter doesn't parse
    content: str
    body: int


def read(path: Path) -> Doc:
    # newline="" keeps CRLF in bodies intact when the file is written back.
    content = path.open(encoding="utf-8", newline="").read()
    parts = split(content)
    if parts is None:
        return Doc(path, None, None, content, 0)
    try:
        fm = yaml.safe_load(parts.text) or {}
    except yaml.YAMLError as e:
        return Doc(path, None, str(e), content, parts.body)
    if not isinstance(fm, dict):
        return Doc(path, None, "Front matter is not a mapping", content, parts.body)
    return Doc(path, fm, None, content, parts.body)


def dump(fm: dict) -> str:
    # width=inf keeps every value on one line. Wrapped values are easy to break
    # when the file is edited elsewhere (see the go-live.md incident).
    return yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False, width=float("inf"))


def write(doc: Doc, fm: dict) -> None:
    fm = with_required_keys(fm)
    doc.path.open("w", encoding="utf-8", newline="").write(f"---\n{dump(fm)}---\n{doc.content[doc.body:]}")


def iter_docs(repo_root: Path, dirs: tuple[str, ...] = ("docs",)) -> Iterator[tuple[Path, str]]:
    """Yield (path, repo-relative path) for each .md file, skipping the ignore list."""
    ignore = load_ignore_list()
    for d in dirs:
        for path in sorted((repo_root / d).glob("**/*.md")):
            rel = path.relative_to(repo_root).as_posix()
            if rel not in ignore:
                yield path, rel


def is_reference(rel: str) -> bool:
    return rel.startswith("reference/")


def get_description(fm: dict) -> str | None:
    metadata = fm.get("metadata")
    return metadata.get("description") if isinstance(metadata, dict) else None


def has_description_key(fm: dict) -> bool:
    metadata = fm.get("metadata")
    return isinstance(metadata, dict) and "description" in metadata


def _blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def missing_field(rel: str, fm: dict) -> str | None:
    """Return the field that needs generated text ("excerpt" or "metadata.description"), or None."""
    if fm.get("hidden"):
        return None
    if not is_reference(rel):
        return "excerpt" if _blank(fm.get("excerpt")) else None
    if "excerpt" in fm:
        return "excerpt" if _blank(fm["excerpt"]) else None
    if has_description_key(fm) and _blank(get_description(fm)):
        return "metadata.description"
    return None


def _insert_after(d: dict, after: str, key: str, value) -> dict:
    """Return d with key set, inserted after the `after` key if key is new (else appended)."""
    if key in d:
        return {**d, key: value}
    out = {}
    for k, v in d.items():
        out[k] = v
        if k == after:
            out[key] = value
    out.setdefault(key, value)
    return out


def with_required_keys(fm: dict) -> dict:
    """Return fm with hidden: false added if absent, in ReadMe's usual key order.

    docs/ pages also need a title, but it isn't invented here; check_excerpt.py reports it.
    """
    if "hidden" in fm:
        return fm
    after = next((k for k in ("deprecated", "excerpt", "title") if k in fm), None)
    return _insert_after(fm, after, "hidden", False)


def set_excerpt(fm: dict, excerpt: str) -> dict:
    """Return fm with excerpt set, inserting the key after title if it's absent."""
    return _insert_after(fm, "title", "excerpt", excerpt)


def set_description(fm: dict, description: str) -> dict:
    """Return fm with metadata.description set, creating the block in ReadMe's usual shape."""
    metadata = fm.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {"title": "", "description": description, "robots": "index"}
    else:
        metadata = _insert_after(metadata, "title", "description", description)
    return {**fm, "metadata": metadata}
