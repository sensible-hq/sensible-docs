#!/usr/bin/env python3
"""One map of every style rule: the registry, the Jev judgment specs, and the Vale rules.

  python3 scripts/style/rule_map.py hierarchy [--check] [--html PATH]
  python3 scripts/style/rule_map.py coverage

hierarchy  writes style-rules/HIERARCHY.md: every rule grouped by scope (general, page-type,
           construct), with how it's enforced and where it's stated. --check exits 1 if the file is
           stale instead of writing it. --html also writes a standalone HTML report.
coverage   lists sentences in the style guides, templates, preferences, and skills that read like a rule
           but have no <!-- rule: --> marker in their section: candidates to register. skill_rules.py
           judges whether a skill section restates a registered rule; this catches rules nobody registered.

Enforcement is derived from each entry's enforced_by, never stored: Vale, Jev, script, manual (a
judgment spec a person applies), or prose (the guide is the only carrier).
"""
import argparse
import configparser
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "style-rules/registry.yaml"
SPECS = ROOT / "style-rules/judgment"
HIERARCHY = ROOT / "style-rules/HIERARCHY.md"
STYLES = ROOT / ".github/styles"
GUIDES = [".claude/style-guide", ".claude/preferences"]
SCOPES = ("general", "page-type", "construct")
SCOPE_TITLES = {"general": "General: every docs page", "page-type": "Page type: one kind of page",
                "construct": "Construct: one element, term, or parameter"}
MARKER = re.compile(r"<!--\s*rule:\s*[a-z0-9-]+\s*-->")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
RULE_LIKE = re.compile(
    r"^\s*(?:[-*]\s+|\d+\.\s+)?(?:\*\*[^*]*\*\*:?\s*)?"
    r"(Do not|Don't|Never|Always|Avoid|Prefer|Use|Write|Keep|Lead with|Start with|Put|Link|Name|Capitalize|State|"
    r"Describe|Mark|Omit|Make sure|Must|Only)\b(?!:)")


def load_registry() -> list[dict]:
    return yaml.safe_load(REGISTRY.read_text()) or []


def load_specs() -> dict:
    return {p.stem: yaml.safe_load(p.read_text()) for p in sorted(SPECS.glob("*.yaml"))}


def trusted(spec: dict) -> bool:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import judge
    return judge.trusted(spec)


def enforcement(entry: dict, specs: dict | None = None) -> list[str]:
    """How a rule is checked, from enforced_by: Vale, Jev, script, manual, or prose."""
    enf = entry.get("enforced_by") or {}
    out = []
    if enf.get("vale"):
        out.append("Vale")
    for spec_path in enf.get("judgment") or []:
        spec = (specs or {}).get(Path(spec_path).stem) or {}
        out.append("manual" if ((spec.get("check") or {}).get("find") or {}).get("kind") == "manual" else "Jev")
    if enf.get("script"):
        out.append("script")
    return out or ["prose"]


def active_package_rules() -> list[tuple[str, str]]:
    """(rule, level) for each Google or Vale package rule that runs on docs pages ([*.md] in .vale.ini)."""
    ini = configparser.ConfigParser(strict=False, interpolation=None)
    ini.optionxform = str
    ini.read_string("[root]\n" + (ROOT / ".vale.ini").read_text())
    off = {k for k, v in ini["*.md"].items() if v.strip().upper() == "NO"}
    out = []
    for path in sorted((STYLES / "Google").glob("*.yml")):
        name = f"Google.{path.stem}"
        if name in off:
            continue
        level = (yaml.safe_load(path.read_text()) or {}).get("level", "warning")
        out.append((name, level))
    return out


def guide_files() -> list[Path]:
    """Style guides, templates, preferences, and the repo's skills."""
    return [p for d in GUIDES for p in sorted((ROOT / d).glob("*.md"))] + sorted(ROOT.glob(".claude/skills/*/SKILL.md"))


def coverage() -> list[tuple[str, int, str]]:
    """(file, line, text) for rule-like sentences with no rule marker in their section (under the same heading)."""
    out = []
    for path in guide_files():
        lines = path.read_text().splitlines()
        in_fence, para = False, []

        def flush():
            if para and not any(MARKER.search(t) for _, t in para):
                for n, t in para:
                    if RULE_LIKE.match(t) and not t.lstrip().startswith("|"):
                        out.append((str(path.relative_to(ROOT)), n, t.strip()))
            para.clear()

        for n, line in enumerate(lines, 1):
            if FENCE.match(line):
                flush()
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if line.startswith("#"):
                flush()
            else:
                para.append((n, line))
        flush()
    return out


def rows(registry: list[dict], specs: dict) -> list[dict]:
    out = []
    for r in registry:
        enf = r.get("enforced_by") or {}
        spec = specs.get(r["id"])
        how = enforcement(r, specs)
        detail = list(enf.get("vale") or []) + [s.split()[0].split("/")[-1] for s in enf.get("script") or []]
        if spec and "Jev" in how:
            detail.append("Jev " + ("trusted" if trusted(spec) else "advisory"))
        out.append({"id": r["id"], "scope": r.get("scope", "?"), "applies_to": r.get("applies_to", ""),
                    "statement": r.get("statement", ""), "kind": r.get("kind", ""), "gate": r.get("gate", ""),
                    "how": how, "detail": detail,
                    "stated_in": sorted({Path(s["file"]).name for s in r.get("stated_in") or []})})
    return out


def grouped(items: list[dict]) -> dict:
    groups = {s: {} for s in SCOPES}
    for x in items:
        groups.setdefault(x["scope"], {}).setdefault(x["applies_to"] or "", []).append(x)
    return groups


def md_cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def hierarchy_md(registry: list[dict], specs: dict) -> str:
    items = rows(registry, specs)
    counts = {s: sum(1 for x in items if x["scope"] == s) for s in SCOPES}
    by_how = {}
    for x in items:
        for h in x["how"]:
            by_how[h] = by_how.get(h, 0) + 1
    pkg = active_package_rules()
    gaps = coverage()
    out = ["# Style rule hierarchy", "",
           "Generated by `python3 scripts/style/rule_map.py hierarchy` from `registry.yaml`, the Jev specs in "
           "`judgment/`, and `.vale.ini`. Don't edit it by hand; `check_registry.py` fails when it's stale.", "",
           f"{len(items)} registered rules: " + ", ".join(f"{counts[s]} {s}" for s in SCOPES) + ". Enforced by: "
           + ", ".join(f"{n} {h}" for h, n in sorted(by_how.items())) + ". "
           f"Plus {len(pkg)} Google package rules that run on every page, and {len(gaps)} rule-like sentences "
           "in the guides with no registry entry (`rule_map.py coverage`).", "",
           "Enforcement: **Vale** matches a pattern; **Jev** judges each candidate a detector finds (trusted rules can "
           "fail a run, advisory rules only report); **script** is a repo check; **manual** is a judgment a person "
           "applies; **prose** means the guide is the only carrier.", ""]
    for scope, groups in grouped(items).items():
        out += [f"## {SCOPE_TITLES.get(scope, scope)}", ""]
        for applies, members in sorted(groups.items()):
            if applies:
                out += [f"### {applies[0].upper() + applies[1:]}", ""]
            out += ["| rule | statement | enforced by | gate | stated in |", "| ---- | --------- | ----------- | ---- | --------- |"]
            for x in sorted(members, key=lambda x: x["id"]):
                how = ", ".join(x["how"]) + (f" ({', '.join(x['detail'])})" if x["detail"] else "")
                out.append(f"| `{x['id']}` | {md_cell(x['statement'])} | {md_cell(how)} | {x['gate'] or ''} | "
                           f"{md_cell(', '.join(x['stated_in']))} |")
            out.append("")
    out += ["## Google package rules", "",
            "Third-party rules from Vale's Google package that run on every docs page and aren't in the registry. "
            "A registered rule that names one (`enforced_by.vale`) is listed above instead.", "",
            "| rule | level |", "| ---- | ----- |"]
    claimed = {v for r in registry for v in (r.get("enforced_by") or {}).get("vale") or []}
    out += [f"| `{n}` | {lvl} |" for n, lvl in pkg if n not in claimed]
    out.append("")
    return "\n".join(out)


def hierarchy_html(registry: list[dict], specs: dict) -> str:
    import report_html as h
    items = rows(registry, specs)
    sections = []
    how_chip = {"Vale": "pass", "Jev": "judge", "script": "info", "manual": "warn", "prose": "warn"}
    for scope, groups in grouped(items).items():
        body = []
        for applies, members in sorted(groups.items()):
            if applies:
                body.append(f"<h3>{h.e(applies)}</h3>")
            body.append(h.table(["Rule", "Statement", "Enforced by", "Gate", "Stated in"], [
                [f"<code>{h.e(x['id'])}</code>", h.e(x["statement"]),
                 " ".join(f'<span class="chip {how_chip.get(k, "info")}">{h.e(k)}</span>' for k in x["how"])
                 + (f'<br><span class="muted">{h.e(", ".join(x["detail"]))}</span>' if x["detail"] else ""),
                 h.e(x["gate"] or ""), h.e(", ".join(x["stated_in"]))] for x in sorted(members, key=lambda x: x["id"])]))
        n = sum(len(m) for m in groups.values())
        sections.append(h.card(f"{SCOPE_TITLES.get(scope, scope)} ({n})", "".join(body), open_=True))
    claimed = {v for r in registry for v in (r.get("enforced_by") or {}).get("vale") or []}
    pkg = [(n, lvl) for n, lvl in active_package_rules() if n not in claimed]
    sections.append(h.card(f"Google package rules ({len(pkg)})", h.table(["Rule", "Level"], [[f"<code>{h.e(n)}</code>", h.e(l)] for n, l in pkg]),
                           "Third-party rules that run on every docs page and aren't in the registry.", open_=False))
    gaps = coverage()
    sections.append(h.card(f"Unregistered rule-like sentences ({len(gaps)})",
                           h.table(["File", "Line", "Text"], [[h.e(f), str(n), h.e(t[:200])] for f, n, t in gaps]),
                           "Sentences in the style guides that read like a rule, with no rule marker in their section. "
                           "Register the real rules; the rest are guidance.", open_=False))
    return h.page("Style rule hierarchy", f"{len(items)} registered rules, grouped by how far each reaches", sections)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["hierarchy", "coverage"])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--html")
    a = ap.parse_args(argv)
    registry, specs = load_registry(), load_specs()
    if a.command == "coverage":
        gaps = coverage()
        for f, n, t in gaps:
            print(f"{f}:{n}: {t[:140]}")
        print(f"{len(gaps)} rule-like sentences with no rule marker")
        return 0
    text = hierarchy_md(registry, specs)
    if a.html:
        import report_html
        report_html.write(Path(a.html), hierarchy_html(registry, specs))
    if a.check:
        if not HIERARCHY.is_file() or HIERARCHY.read_text() != text:
            print("style-rules/HIERARCHY.md is stale: run python3 scripts/style/rule_map.py hierarchy")
            return 1
        return 0
    HIERARCHY.write_text(text)
    print(f"wrote {HIERARCHY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main())
