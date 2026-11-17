#!/usr/bin/env python3
"""Check that style-rules/registry.yaml and the files it links still agree.

  python3 scripts/style/check_registry.py

The registry records, for each rule, its deterministic carriers (Vale rules, scripts, judgment specs)
and its probabilistic carriers (the guides, templates, and skills that state it in prose). This script
fails when the two sides drift apart:

  - a stated_in quote no longer appears in its file
  - a stated_in file has no <!-- rule: <id> --> marker for that rule, or a marker names an unknown rule
    or a file the rule doesn't list
  - a Sensible.* Vale rule has no registry entry, or an entry names a Vale rule, script, judgment
    spec, or fixture that doesn't exist
  - a deterministic rule has no carrier or no fixture, or a judgment spec lacks a required field or
    quotes its source file wrongly

Exits 1 on any problem.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "style-rules/registry.yaml"
STYLES = ROOT / ".github/styles"
MARKER = re.compile(r"<!--\s*rule:\s*([a-z0-9-]+)\s*-->")
KINDS = {"deterministic", "judgment", "prose"}
GATES = {"block", "warn", "report"}
JUDGMENT_FIELDS = ("id", "source", "applies", "check", "examples")


def norm(text: str) -> str:
    """Whitespace-collapsed text, so a reflowed paragraph still matches its quote."""
    return re.sub(r"\s+", " ", text).strip()


def vale_rule_exists(name: str) -> bool:
    style, _, rule = name.partition(".")
    return (STYLES / style / f"{rule}.yml").is_file()


def check(registry: list[dict]) -> list[str]:
    problems = []
    ids = [r.get("id") for r in registry]
    for dup in {i for i in ids if ids.count(i) > 1}:
        problems.append(f"duplicate id: {dup}")
    by_id = {r["id"]: r for r in registry if r.get("id")}
    claimed_vale = set()

    for r in registry:
        rid = r.get("id", "?")
        kind = r.get("kind")
        if kind not in KINDS:
            problems.append(f"{rid}: kind must be one of {sorted(KINDS)}")
        if not r.get("statement"):
            problems.append(f"{rid}: no statement")
        enf = r.get("enforced_by") or {}
        for name in enf.get("vale") or []:
            claimed_vale.add(name)
            if not vale_rule_exists(name):
                problems.append(f"{rid}: Vale rule {name} doesn't exist")
        for script in enf.get("script") or []:
            if not (ROOT / script.split()[0]).is_file():
                problems.append(f"{rid}: script {script} doesn't exist")
        for spec in enf.get("judgment") or []:
            path = ROOT / spec
            if not path.is_file():
                problems.append(f"{rid}: judgment spec {spec} doesn't exist")
                continue
            data = yaml.safe_load(path.read_text()) or {}
            missing = [f for f in JUDGMENT_FIELDS if f not in data]
            if missing:
                problems.append(f"{rid}: judgment spec {spec} lacks {', '.join(missing)}")
            if data.get("id") != rid:
                problems.append(f"{rid}: judgment spec {spec} has id {data.get('id')}")
            src = data.get("source") or {}
            if src.get("file"):
                src_path = ROOT / src["file"]
                if not src_path.is_file():
                    problems.append(f"{rid}: judgment spec source {src['file']} doesn't exist")
                elif norm(src.get("quote", "")) not in norm(src_path.read_text()):
                    problems.append(f"{rid}: judgment spec quote not found in {src['file']}: {src.get('quote', '')[:70]}")
        carriers = (enf.get("vale") or []) + (enf.get("script") or [])
        if kind == "deterministic":
            if not carriers:
                problems.append(f"{rid}: deterministic but no Vale rule or script")
            if r.get("gate") not in GATES:
                problems.append(f"{rid}: gate must be one of {sorted(GATES)}")
            fixture = r.get("fixture")
            if enf.get("vale") and not fixture:
                problems.append(f"{rid}: Vale rule with no fixture")
            if fixture and not (ROOT / fixture).is_file():
                problems.append(f"{rid}: fixture {fixture} doesn't exist")
        if kind == "judgment" and not enf.get("judgment"):
            problems.append(f"{rid}: judgment but no judgment spec")
        for s in r.get("stated_in") or []:
            path = ROOT / s.get("file", "")
            if not path.is_file():
                problems.append(f"{rid}: stated_in file {s.get('file')} doesn't exist")
                continue
            text = path.read_text()
            if norm(s.get("quote", "")) not in norm(text):
                problems.append(f"{rid}: quote not found in {s['file']}: {s.get('quote', '')[:70]}")
            if rid not in MARKER.findall(text):
                problems.append(f"{rid}: no <!-- rule: {rid} --> marker in {s['file']}")

    for path in sorted((STYLES / "Sensible").glob("*.yml")):
        name = f"Sensible.{path.stem}"
        if name not in claimed_vale:
            problems.append(f"{name}: no registry entry")

    for path in sorted(ROOT.glob(".claude/**/*.md")) + sorted(ROOT.glob("style-rules/**/*.md")):
        if "/sessions/" in str(path) or "/tests/" in str(path):
            continue
        rel = str(path.relative_to(ROOT))
        for rid in MARKER.findall(path.read_text()):
            if rid not in by_id:
                problems.append(f"{rel}: marker names unknown rule {rid}")
            elif rel not in [s.get("file") for s in by_id[rid].get("stated_in") or []]:
                problems.append(f"{rel}: marker for {rid}, but the registry doesn't list this file")
    return problems


def main():
    registry = yaml.safe_load(REGISTRY.read_text()) or []
    problems = check(registry)
    for p in problems:
        print(p)
    kinds = {k: sum(1 for r in registry if r.get("kind") == k) for k in sorted(KINDS)}
    print(f"{len(registry)} rules ({', '.join(f'{n} {k}' for k, n in kinds.items())}), {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
