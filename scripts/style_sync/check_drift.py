#!/usr/bin/env python3
"""Check for drift between the style guide and the Vale rules.

Reads scripts/style_sync/registry.yaml, which links each style-guide rule
(in .claude/style-guide/) to its enforcement, and checks that:

  * every custom Vale rule (.github/styles/Sensible/*.yml) is referenced by the
    registry, and every Vale target the registry names exists and is enabled
    (agent-only rules must instead be off: agent_lines.py runs them);
  * every guide location in the registry still resolves, and every guide rule
    found by the registry's convention has an entry;
  * every custom Vale rule has at least one failing and one passing test case,
    and each test case behaves as expected when run through Vale. Test cases
    come from fixtures (fixtures/<Rule>/fail*.md, pass*.md) and from the
    Avoid/Prefer examples in the guide itself;
  * .vale.ini pins its packages, and the registry's record of the Google
    overrides matches .vale.ini.

Exit codes: 0 = no drift, 1 = drift found, 2 = the check itself could not run.
Prints one line per problem. Deterministic: no network, no LLM.
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = SCRIPT_DIR.parents[1]
REGISTRY_REL = "scripts/style_sync/registry.yaml"
FIXTURES_REL = "scripts/style_sync/fixtures"
STYLES_REL = ".github/styles"
CUSTOM_STYLE = "Sensible"
ENFORCEMENTS = ("vale", "human", "none-yet")
VOCAB_CHECKS = {"accept": "Vale.Terms", "reject": "Vale.Avoid"}


class CheckError(Exception):
    """The check could not run (bad registry, Vale missing, and so on)."""


# --------------------------------------------------------------------------
# Markdown parsing
# --------------------------------------------------------------------------

FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
BOLD_LEAD_RE = re.compile(r"^\*\*([^*]+?)\*\*(:?)")
QUOTED_RE = re.compile(r"[\"“]([^\"“”]+)[\"”]")


def github_slug(text: str) -> str:
    """Anchor GitHub generates for a heading."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> text
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


@dataclass
class Unit:
    """A rule-shaped unit of a guide file: heading, bold lead, or table row."""

    kind: str  # "heading" | "item" | "row"
    file: str
    anchor: str
    key: str  # heading text, bold-lead text, or first table cell
    line: int
    level: int = 0
    body: list = field(default_factory=list)  # (line_no, text) owned by this unit
    cells: list = field(default_factory=list)  # table cells for rows

    @property
    def location(self) -> str:
        loc = f"{self.file}#{self.anchor}"
        if self.kind == "item":
            loc += f" item={self.key!r}"
        elif self.kind == "row":
            loc += f" row={self.key!r}"
        return loc


def parse_guide_file(path: Path, name: str) -> list[Unit]:
    """Split a markdown file into headings, bold-lead items and table rows.

    Lines inside fenced code blocks and blockquotes are never rule units.
    A unit's body runs until the next unit of any kind starts.
    """
    units: list[Unit] = []
    slug_counts: dict[str, int] = {}
    fence: tuple[str, int] | None = None
    current_heading: Unit | None = None
    current: Unit | None = None
    table_line = 0  # 0 = not in a table; else number of table lines seen so far

    for no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if fence is not None or not raw.strip().startswith("|"):
            table_line = 0
        m = FENCE_RE.match(raw)
        if fence is None and m:
            fence = (m.group(1)[0], len(m.group(1)))
            if current:
                current.body.append((no, raw))
            continue
        if fence is not None:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] \
                    and not m.group(2).strip():
                fence = None
            if current:
                current.body.append((no, raw))
            continue

        h = HEADING_RE.match(raw)
        if h:
            text = h.group(2)
            base = github_slug(text)
            n = slug_counts.get(base, 0)
            slug_counts[base] = n + 1
            anchor = base if n == 0 else f"{base}-{n}"
            current_heading = Unit("heading", name, anchor, text, no, level=len(h.group(1)))
            units.append(current_heading)
            current = current_heading
            continue

        b = BOLD_LEAD_RE.match(raw)
        if b and current_heading is not None:
            text = b.group(1).strip()
            if text.endswith((":", ".")) or b.group(2):
                key = text.rstrip(":.").strip()
                current = Unit("item", name, current_heading.anchor, key, no)
                units.append(current)
                current.body.append((no, raw))
                continue

        stripped = raw.strip()
        if stripped.startswith("|") and current_heading is not None:
            table_line += 1
            # Line 1 is the header row and line 2 the separator; data rows follow.
            if table_line > 2:
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                units.append(Unit("row", name, current_heading.anchor, cells[0], no, cells=cells))
            continue

        if current:
            current.body.append((no, raw))
    return units


def extract_examples(unit: Unit, fail_markers, pass_markers, columns=None):
    """Return (fail_examples, pass_examples) found in a unit.

    Prose units: list items or lines that start with a marker word followed
    by a colon, e.g. `- Avoid: "x", "y"`. Every double-quoted string on the
    line is one example; with no quotes, the rest of the line is the example.

    Table rows: quoted strings in the column(s) named by `columns`.
    """
    fails: list[str] = []
    passes: list[str] = []
    if unit.kind == "row":
        if columns:
            for idx in columns.get("fail", []):
                if idx < len(unit.cells):
                    fails += QUOTED_RE.findall(unit.cells[idx])
            for idx in columns.get("pass", []):
                if idx < len(unit.cells):
                    passes += QUOTED_RE.findall(unit.cells[idx])
        return fails, passes

    marker_re = re.compile(
        r"^\s*(?:[-*+]\s+)?\**(" + "|".join(re.escape(m) for m in fail_markers + pass_markers)
        + r")\**\s*:\s*\**\s*(.+)$"
    )
    in_fence = False
    for _, line in unit.body:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = marker_re.match(line)
        if not m:
            continue
        found = QUOTED_RE.findall(m.group(2)) or [m.group(2).strip()]
        (fails if m.group(1) in fail_markers else passes).extend(found)
    return fails, passes


# --------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------


@dataclass
class Location:
    file: str
    anchor: str
    item: str | None = None
    row: str | None = None

    def __str__(self):
        s = f"{self.file}#{self.anchor}"
        if self.item:
            s += f" item={self.item!r}"
        if self.row:
            s += f" row={self.row!r}"
        return s


def parse_location(spec: dict) -> Location:
    at = spec.get("at")
    if not isinstance(at, str) or "#" not in at:
        raise ValueError(f"'at' must look like 'file.md#anchor', got {at!r}")
    file, anchor = at.split("#", 1)
    return Location(file, anchor, spec.get("item"), spec.get("row"))


def find_unit(units_by_file: dict, loc: Location) -> Unit | None:
    for u in units_by_file.get(loc.file, []):
        if u.anchor != loc.anchor:
            continue
        if loc.item is not None:
            if u.kind == "item" and u.key == loc.item:
                return u
        elif loc.row is not None:
            if u.kind == "row" and u.key == loc.row:
                return u
        elif u.kind == "heading":
            return u
    return None


def as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


# --------------------------------------------------------------------------
# Vale config
# --------------------------------------------------------------------------


def read_vale_ini(path: Path) -> configparser.ConfigParser:
    cp = configparser.ConfigParser(interpolation=None, strict=False)
    cp.optionxform = str  # keep rule-name case
    text = path.read_text(encoding="utf-8")
    cp.read_string("[__global__]\n" + text)
    return cp


def md_section(cp: configparser.ConfigParser) -> str | None:
    for name in ("*.md", "*.{md}", "*"):
        if cp.has_section(name):
            return name
    return None


def target_check_name(target: str) -> str:
    """Map a registry vale target to the check name Vale reports."""
    if target.startswith("vocab:"):
        kind = target.rsplit("/", 1)[-1].removesuffix(".txt")
        return VOCAB_CHECKS.get(kind, target)
    return target


def target_exists(root: Path, target: str) -> bool:
    styles = root / STYLES_REL
    if target.startswith("vocab:"):
        rel = target[len("vocab:"):]
        if not rel.endswith(".txt"):
            rel += ".txt"
        vocab, _, kind = rel.partition("/")
        return (styles / "config" / "vocabularies" / vocab / kind).is_file() \
            and kind.removesuffix(".txt") in VOCAB_CHECKS
    style, _, rule = target.partition(".")
    if not rule:
        return False
    if style == "Vale":
        return rule in {"Terms", "Avoid", "Spelling", "Repetition"}
    return (styles / style / f"{rule}.yml").is_file()


def target_enabled(cp: configparser.ConfigParser, target: str) -> bool:
    section = md_section(cp)
    if section is None:
        return False
    if target.startswith("vocab:"):
        vocab = target[len("vocab:"):].split("/", 1)[0]
        vocabs = [v.strip() for v in cp.get("__global__", "Vocab", fallback="").split(",")]
        based = [s.strip() for s in cp.get(section, "BasedOnStyles", fallback="").split(",")]
        check = target_check_name(target)
        explicit = cp.get(section, check, fallback=None)
        if explicit is not None:
            return explicit.strip().upper() != "NO" and vocab in vocabs
        return vocab in vocabs and "Vale" in based
    explicit = cp.get(section, target, fallback=None)
    if explicit is not None:
        return explicit.strip().upper() != "NO"
    style = target.split(".", 1)[0]
    based = [s.strip() for s in cp.get(section, "BasedOnStyles", fallback="").split(",")]
    return style in based


PINNED_RE = re.compile(r"^https?://.*/(?:releases/download/v?\d[^/]*/|archive/(?:refs/tags/)?v?\d)")


def check_packages(cp: configparser.ConfigParser) -> list[str]:
    problems = []
    raw = cp.get("__global__", "Packages", fallback="")
    for pkg in [p.strip() for p in raw.split(",") if p.strip()]:
        if not PINNED_RE.match(pkg):
            problems.append(
                f"UNPINNED-PACKAGE: .vale.ini package {pkg!r} is not pinned to a release; "
                "`vale sync` installs whatever version is latest"
            )
    return problems


# --------------------------------------------------------------------------
# Running Vale
# --------------------------------------------------------------------------


def run_vale(vale: str, root: Path, checks: set[str], vocabs: list[str], files: list[Path]) -> dict:
    """Run Vale on files with only `checks` enabled; return {path: [check, ...]}."""
    if not files:
        return {}
    with tempfile.TemporaryDirectory() as tmp:
        ini = Path(tmp) / "vale.ini"
        lines = [
            f"StylesPath = {(root / STYLES_REL).as_posix()}",
            "MinAlertLevel = suggestion",
        ]
        if vocabs:
            lines.append("Vocab = " + ", ".join(vocabs))
        lines += ["", "[*.md]", "BasedOnStyles ="]
        lines += [f"{c} = YES" for c in sorted(checks)]
        ini.write_text("\n".join(lines) + "\n", encoding="utf-8")
        cmd = [vale, "--no-global", "--no-exit", f"--config={ini}", "--output=JSON"]
        cmd += [str(f) for f in files]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp, timeout=300)
        except FileNotFoundError as exc:
            raise CheckError(f"vale binary not found: {vale}") from exc
        try:
            data = json.loads(proc.stdout or "{}")
        except json.JSONDecodeError as exc:
            raise CheckError(
                f"vale did not return JSON (exit {proc.returncode}): "
                f"{(proc.stderr or proc.stdout).strip()[:500]}"
            ) from exc
        if not isinstance(data, dict):
            raise CheckError(f"unexpected vale output: {str(data)[:200]}")
    result: dict[str, list[str]] = {}
    for path, alerts in data.items():
        result[str(Path(path).resolve())] = [a.get("Check", "") for a in alerts]
    return result


# --------------------------------------------------------------------------
# Main check
# --------------------------------------------------------------------------


@dataclass
class TestCase:
    rules: list[str]  # check names; a fail case must trigger at least one
    expect: str  # "fail" | "pass"
    source: str  # human-readable origin
    path: Path


def check(root: Path, vale: str | None, registry_path: Path | None = None) -> tuple[list[str], dict]:
    root = root.resolve()
    registry_path = registry_path or root / REGISTRY_REL
    try:
        reg = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CheckError(f"cannot read registry {registry_path}: {exc}") from exc
    if not isinstance(reg, dict):
        raise CheckError("registry must be a mapping")

    problems: list[str] = []
    stats = {"entries": 0, "draft": 0, "vale": 0, "human": 0, "none-yet": 0, "tests": 0}

    guide_dir = root / reg.get("guide_dir", ".claude/style-guide")
    scan = reg.get("scan") or []
    markers = reg.get("example_markers") or {}
    fail_markers = markers.get("fail", ["Avoid"])
    pass_markers = markers.get("pass", ["Prefer"])
    tables = reg.get("tables") or {}

    # Parse every scanned guide file.
    units_by_file: dict[str, list[Unit]] = {}
    for name in scan:
        p = guide_dir / name
        if not p.is_file():
            problems.append(f"MISSING-GUIDE-FILE: registry scans {name} but it does not exist")
            continue
        units_by_file[name] = parse_guide_file(p, name)

    def lookup(spec, where) -> Unit | None:
        try:
            loc = parse_location(spec)
        except ValueError as exc:
            problems.append(f"SCHEMA: {where}: {exc}")
            return None
        if not (guide_dir / loc.file).is_file():
            problems.append(f"DANGLING: {where}: guide file {loc.file} does not exist")
            return None
        if loc.file not in units_by_file:
            units_by_file[loc.file] = parse_guide_file(guide_dir / loc.file, loc.file)
        unit = find_unit(units_by_file, loc)
        if unit is None:
            hint = ""
            if loc.item is None and loc.row is None:
                for line in (guide_dir / loc.file).read_text(encoding="utf-8").splitlines():
                    h = HEADING_RE.match(line)
                    if h and github_slug(h.group(2)) == loc.anchor:
                        hint = (" (the heading text exists but sits inside a code block;"
                                " check for a nested or unclosed ``` fence above it)")
                        break
            problems.append(f"DANGLING: {where}: {loc} not found in the guide{hint}")
        return unit

    # Candidate rule units by convention.
    table_anchors = set()
    for t in tables:
        table_anchors.add(t)
    candidates: dict[str, Unit] = {}
    for name, units in units_by_file.items():
        for u in units:
            if u.kind == "heading":
                if u.level not in (2, 3) or f"{u.file}#{u.anchor}" in table_anchors:
                    continue
            elif u.kind == "row":
                if f"{u.file}#{u.anchor}" not in table_anchors:
                    continue
            candidates[u.location] = u

    covered: set[str] = set()

    # not_rules: acknowledged candidates that are not rules.
    for i, nr in enumerate(reg.get("not_rules") or []):
        where = f"not_rules[{i}] ({nr.get('at')})"
        if not nr.get("reason"):
            problems.append(f"SCHEMA: {where}: missing 'reason'")
        unit = lookup(nr, where)
        if unit is not None:
            covered.add(unit.location)

    # Rule entries.
    cp = read_vale_ini(root / ".vale.ini")
    seen_ids: set[str] = set()
    tests: list[TestCase] = []
    custom_targets: set[str] = set()
    tmp_examples = Path(tempfile.mkdtemp(prefix="style_sync_"))
    example_count = 0

    # Agent-only rules are off in .vale.ini on purpose; agent_lines.py runs them.
    agent_only = reg.get("agent_only_rules") or []
    if not isinstance(agent_only, list) or not all(isinstance(r, str) for r in agent_only):
        problems.append("SCHEMA: agent_only_rules must be a list of rule names")
        agent_only = []
    for r in agent_only:
        if not target_exists(root, r):
            problems.append(f"MISSING-VALE-RULE: agent_only_rules: target {r!r} does not exist")
        elif target_enabled(cp, r):
            problems.append(
                f"AGENT-ONLY-ENABLED: {r} is agent-only but enabled for *.md in .vale.ini, "
                "so it flags human-written lines too"
            )

    try:
        for i, entry in enumerate(reg.get("rules") or []):
            stats["entries"] += 1
            eid = entry.get("id")
            where = f"rule {eid or f'#{i}'}"
            if not eid:
                problems.append(f"SCHEMA: rules[{i}]: missing 'id'")
            elif eid in seen_ids:
                problems.append(f"SCHEMA: {where}: duplicate id")
            seen_ids.add(eid)
            if entry.get("status") == "draft":
                stats["draft"] += 1

            kinds = [k for k in ENFORCEMENTS if k in entry]
            if len(kinds) != 1:
                problems.append(
                    f"SCHEMA: {where}: needs exactly one of {', '.join(ENFORCEMENTS)}; has {kinds or 'none'}"
                )
                continue
            kind = kinds[0]
            stats[kind] += 1
            if kind == "human" and not entry.get("human"):
                problems.append(f"SCHEMA: {where}: 'human' needs a short reason")

            unit = None
            if "at" in entry:
                unit = lookup(entry, where)
                if unit is not None:
                    if unit.location in covered:
                        problems.append(f"SCHEMA: {where}: {unit.location} is mapped more than once")
                    covered.add(unit.location)
            elif kind != "vale" or not entry.get("basis"):
                problems.append(f"SCHEMA: {where}: needs 'at' (guide location), or 'vale' plus 'basis'")

            if kind != "vale":
                continue

            targets = as_list(entry["vale"])
            checks = []
            for t in targets:
                if not isinstance(t, str) or not target_exists(root, t):
                    problems.append(f"MISSING-VALE-RULE: {where}: target {t!r} does not exist")
                    continue
                if t not in agent_only and not target_enabled(cp, t):
                    problems.append(f"DISABLED-VALE-RULE: {where}: target {t!r} is not enabled for *.md in .vale.ini")
                if t.startswith(f"{CUSTOM_STYLE}."):
                    custom_targets.add(t)
                checks.append(target_check_name(t))
            if not checks or unit is None:
                continue

            # Guide examples become test cases.
            columns = None
            if unit.kind == "row":
                columns = tables.get(f"{unit.file}#{unit.anchor}") or {}
            fails, passes = extract_examples(unit, fail_markers, pass_markers, columns)
            gaps = set(as_list(entry.get("known_gaps")))
            for expect, examples in (("fail", fails), ("pass", passes)):
                for ex in examples:
                    if expect == "fail" and ex in gaps:
                        continue
                    example_count += 1
                    p = tmp_examples / f"ex{example_count:04d}.md"
                    p.write_text(ex + "\n", encoding="utf-8")
                    tests.append(TestCase(checks, expect, f"{unit.location} example {ex!r}", p))
            for g in sorted(gaps - set(fails)):
                problems.append(f"STALE-KNOWN-GAP: {where}: known_gaps entry {g!r} is no longer an Avoid example")

        # Every custom Vale rule needs a registry entry.
        custom_dir = root / STYLES_REL / CUSTOM_STYLE
        custom_rules = sorted(f"{CUSTOM_STYLE}.{p.stem}" for p in custom_dir.glob("*.yml"))
        for r in custom_rules:
            if r not in custom_targets:
                problems.append(f"ORPHAN-VALE-RULE: {r} has no registry entry")

        # Fixtures.
        fixtures_dir = root / FIXTURES_REL
        if fixtures_dir.is_dir():
            for d in sorted(p for p in fixtures_dir.iterdir() if p.is_dir()):
                rule = f"{CUSTOM_STYLE}.{d.name}"
                if rule not in custom_rules:
                    problems.append(f"ORPHAN-FIXTURE: {FIXTURES_REL}/{d.name} has no matching rule {rule}")
                    continue
                for f in sorted(d.glob("*.md")):
                    if f.name.startswith("fail"):
                        tests.append(TestCase([rule], "fail", f"{FIXTURES_REL}/{d.name}/{f.name}", f))
                    elif f.name.startswith("pass"):
                        tests.append(TestCase([rule], "pass", f"{FIXTURES_REL}/{d.name}/{f.name}", f))

        for r in custom_rules:
            have = {t.expect for t in tests if r in t.rules and len(t.rules) == 1}
            for expect in ("fail", "pass"):
                if expect not in have:
                    problems.append(
                        f"NO-TESTS: {r} has no {expect} test (add {FIXTURES_REL}/{r.split('.', 1)[1]}/{expect}.md "
                        "or an Avoid/Prefer example in its guide section)"
                    )

        # Run Vale on all test cases at once; filter alerts by check name.
        stats["tests"] = len(tests)
        if tests:
            if not vale:
                raise CheckError("vale binary not found; install Vale or pass --vale")
            all_checks = {c for t in tests for c in t.rules}
            vocabs = [v.strip() for v in cp.get("__global__", "Vocab", fallback="").split(",") if v.strip()]
            results = run_vale(vale, root, all_checks, vocabs, [t.path for t in tests])
            for t in tests:
                fired = set(results.get(str(t.path.resolve()), [])) & set(t.rules)
                if t.expect == "fail" and not fired:
                    problems.append(f"TEST-FAIL: {t.source} should trigger {' or '.join(t.rules)} but does not")
                elif t.expect == "pass" and fired:
                    problems.append(f"TEST-FAIL: {t.source} should not trigger {', '.join(sorted(fired))} but does")
    finally:
        shutil.rmtree(tmp_examples, ignore_errors=True)

    # Guide rules found by convention that have no entry.
    for loc, u in sorted(candidates.items(), key=lambda kv: (kv[1].file, kv[1].line)):
        if loc not in covered:
            problems.append(f"UNMAPPED-GUIDE-RULE: {loc} (line {u.line}) has no registry entry")

    # Google package: overrides recorded vs .vale.ini, and pinning.
    google = reg.get("google") or {}
    section = md_section(cp)
    actual = {}
    if section:
        for k, v in cp.items(section):
            if k.startswith("Google."):
                actual[k] = v.strip().upper()
    recorded = {k: str(v).upper() if not isinstance(v, bool) else ("YES" if v else "NO")
                for k, v in (google.get("overrides") or {}).items()}
    for k in sorted(set(actual) | set(recorded)):
        if actual.get(k) != recorded.get(k):
            problems.append(
                f"GOOGLE-OVERRIDES: .vale.ini has {k} = {actual.get(k, '(unset)')} but the registry records "
                f"{recorded.get(k, '(unset)')}"
            )
    problems += check_packages(cp)

    return sorted(set(problems), key=problems.index), stats


REPORT_TEMPLATE = """\
<!-- style-drift-report -->
## Style guide / Vale drift report

**Run:** {run}
**Commit:** `{commit}`
**Problems:** {count}
**Registry:** {entries} entries ({vale} Vale, {human} human, {none_yet} none-yet; {draft} still marked draft)
**Vale test cases run:** {tests}

### Problems

```text
{lines}
```

### How to resolve

This issue is opened and updated by `.github/workflows/style_drift.yml`. It never blocks docs work.
See `scripts/style_sync/README.md` for what each problem code means and how to fix it.
The issue closes automatically when a run finds no drift.
"""


def render_report(problems: list[str], stats: dict, run: str, commit: str) -> str:
    return REPORT_TEMPLATE.format(
        run=run or "(local run)",
        commit=commit or "(unknown)",
        count=len(problems),
        entries=stats.get("entries", 0),
        vale=stats.get("vale", 0),
        human=stats.get("human", 0),
        none_yet=stats.get("none-yet", 0),
        draft=stats.get("draft", 0),
        tests=stats.get("tests", 0),
        lines="\n".join(p.replace("```", "'''") for p in problems) or "(none)",
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="repository root")
    ap.add_argument("--registry", type=Path, help="registry file (default: scripts/style_sync/registry.yaml)")
    ap.add_argument("--vale", default=os.environ.get("VALE_BIN") or shutil.which("vale"),
                    help="path to the vale binary (default: vale on PATH)")
    ap.add_argument("--report-md", type=Path, help="also write a markdown issue body here")
    ap.add_argument("--run-url", default="", help="link to the CI run, for the report")
    ap.add_argument("--commit", default="", help="commit SHA, for the report")
    args = ap.parse_args(argv)

    try:
        problems, stats = check(args.root, args.vale, args.registry)
    except CheckError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for p in problems:
        print(p)
    print(
        f"-- {len(problems)} problem(s); {stats['entries']} registry entries "
        f"({stats['draft']} draft); {stats['tests']} Vale test case(s)",
        file=sys.stderr,
    )
    if args.report_md:
        args.report_md.write_text(render_report(problems, stats, args.run_url, args.commit), encoding="utf-8")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
