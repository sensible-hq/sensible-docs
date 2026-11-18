#!/usr/bin/env python3
"""Judge docs pages against the judgment rules in style-rules/judgment/, with Jev.

  python3 scripts/style/judge.py <file> [...] [--base REF] [--rules id,...] [--dry-run] [--json]

For each rule, code finds candidates (the spec's check.find), Jev answers the spec's multiple-choice
question about each one, and code decides (the spec's check.verdicts):

  violation  Jev picked a choice listed under verdicts.violation with confidence >= 0.70
  unsure     it picked a violation choice with lower confidence; reported, never a pass
  review     it picked a choice listed under verdicts.review; worth a look, not a failure
  ok         anything else

A rule only fails the run once calibration has earned it trust: on its labeled cases, at least 90% of
the violations it flagged were real (precision) and it found at least half of the labeled violations
(recall), over at least 6 labeled cases with at least 3 violations. See calibrate.py. Other rules report
as advisory.

--base REF compares with REF, which the diff detectors need (added tables, added headings, changed
links, added-only patterns); without it they're skipped. --dry-run lists candidates without calling Jev.

Exit codes: 0 no trusted violations, 1 trusted violations, 3 Jev unavailable (fails closed).
"""
import argparse
import concurrent.futures
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "style-rules/judgment"
THRESHOLD = 0.70
TRUST = 0.90
MIN_CASES, MIN_VIOLATIONS = 6, 3  # fewer labeled cases than this can't earn trust
MAX_STATE = 6000
FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*([\w+-]*)")
HEADING = re.compile(r"^(#{1,6})\s+(.*)")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'`*\[(])")
LINK = re.compile(r"\]\(((?:doc|reference|ref):[^)\s]+)\)")


# ------------------------------------------------------------------ page model

def parse(text: str) -> dict:
    """Blocks with 1-based start lines: prose paragraphs, headings, tables, and code blocks."""
    lines = text.splitlines()
    i, blocks, title = 0, [], ""
    if lines and lines[0].strip() == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), 0)
        try:
            title = str((yaml.safe_load("\n".join(lines[1:end])) or {}).get("title") or "")
        except yaml.YAMLError:
            pass
        i = end + 1
    para, para_start = [], 0

    def flush():
        nonlocal para
        if para:
            blocks.append({"kind": "prose", "line": para_start, "text": "\n".join(para)})
            para = []

    while i < len(lines):
        line = lines[i]
        m = FENCE.match(line)
        if m:
            flush()
            start, marker = i, m.group(1)
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(marker):
                i += 1
            blocks.append({"kind": "code", "lang": m.group(2).lower(), "line": start + 1,
                           "text": "\n".join(lines[start + 1:i])})
            i += 1
            continue
        h = HEADING.match(line)
        if h:
            flush()
            blocks.append({"kind": "heading", "level": len(h.group(1)), "line": i + 1, "text": h.group(2).strip()})
        elif line.lstrip().startswith("|"):
            flush()
            start = i
            while i + 1 < len(lines) and lines[i + 1].lstrip().startswith("|"):
                i += 1
            blocks.append({"kind": "table", "line": start + 1, "text": "\n".join(lines[start:i + 1]),
                           "end": i + 1})
        elif not line.strip() or line.strip().startswith("<!--"):
            flush()
        else:
            if not para:
                para_start = i + 1
            para.append(line)
        i += 1
    flush()
    return {"title": title, "blocks": blocks, "lines": lines}


def sentences(block: dict) -> list[tuple[int, str]]:
    """(line, sentence) for a prose block."""
    text, out, pos = block["text"], [], 0
    for m in list(SENTENCE_END.finditer(text)) + [None]:
        end = m.start() if m else len(text)
        if text[pos:end].strip():
            out.append((block["line"] + text[:pos].count("\n"), text[pos:end].strip()))
        pos = m.end() if m else len(text)
    return out


def prose_only(s: str) -> str:
    """Text for pattern matching: inline code removed, so `key` in code isn't a hit."""
    return re.sub(r"`[^`]*`", "", s)


def added_lines(path: Path, base: str | None) -> set[int] | None:
    """Lines added or changed since base, or None without a base. A new file is all added."""
    if not base:
        return None
    rel = str(path.relative_to(ROOT))
    if subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{base}:{rel}"], capture_output=True).returncode:
        return set(range(1, len(path.read_text().splitlines()) + 1))
    out = subprocess.run(["git", "-C", str(ROOT), "diff", "-U0", base, "--", rel], capture_output=True, text=True).stdout
    lines = set()
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", out, re.M):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        lines.update(range(start, start + count))
    return lines


def removed_links(path: Path, base: str) -> set[str]:
    rel = str(path.relative_to(ROOT))
    out = subprocess.run(["git", "-C", str(ROOT), "diff", "-U0", base, "--", rel], capture_output=True, text=True).stdout
    return {t for line in out.splitlines() if line.startswith("-") for t in LINK.findall(line)}


# ------------------------------------------------------------------ detectors

def matches_path(rel: str, find: dict) -> bool:
    inc = find.get("paths") or ["**"]
    exc = find.get("exclude_paths") or []
    return any(fnmatch.fnmatch(rel, p) for p in inc) and not any(fnmatch.fnmatch(rel, p) for p in exc)


def find_candidates(spec: dict, path: Path, page: dict, base: str | None) -> tuple[list[dict], str | None]:
    """(candidates, reason skipped). A candidate: line, text (what Jev judges), context."""
    find = spec["check"]["find"]
    kind = find["kind"]
    rel = str(path.relative_to(ROOT))
    if not matches_path(rel, find):
        return [], None
    added = added_lines(path, base)
    blocks = page["blocks"]
    out = []

    if kind == "manual":
        return [], f"manual: {find.get('note', '')}"
    if kind in ("added-tables", "added-headings", "changed-links") or find.get("added_only"):
        if added is None:
            return [], "needs --base"

    if kind == "sentences":
        pat = re.compile(find["pattern"], re.I)
        exc = re.compile(find["exclude"], re.I) if find.get("exclude") else None
        for b in blocks:
            if b["kind"] != "prose":
                continue
            for line, s in sentences(b):
                if find.get("added_only") and line not in added:
                    continue
                t = prose_only(s)
                m = pat.search(t)
                if m and not (exc and exc.search(t)):
                    out.append({"line": line, "text": s, "context": b["text"], "mark": m.group(0)})
    elif kind == "first-sentence":
        b = next((b for b in blocks if b["kind"] == "prose" and not b["text"].startswith("**Note:**")), None)
        if b and sentences(b):
            line, s = sentences(b)[0]
            out.append({"line": line, "text": s, "context": b["text"]})
    elif kind == "section-openers":
        pat = re.compile(find["pattern"], re.I)
        seen = set()
        for k, b in enumerate(blocks):
            if b["kind"] != "heading" or re.search(r"parameters|examples?|notes|syntax", b["text"], re.I):
                continue
            # Only prose directly under the heading; a subheading in between starts another section.
            nxt = blocks[k + 1] if k + 1 < len(blocks) and blocks[k + 1]["kind"] == "prose" else None
            if nxt and sentences(nxt) and nxt["line"] not in seen:
                seen.add(nxt["line"])
                line, s = sentences(nxt)[0]
                if pat.search(prose_only(s)):
                    out.append({"line": line, "text": s, "context": f"## {b['text']}\n\n{nxt['text']}"})
    elif kind == "vale":
        exe = next((c for c in ("vale", str(Path.home() / ".local/bin/vale"))
                    if subprocess.run(["sh", "-c", f'command -v "{c}"'], capture_output=True).stdout or Path(c).is_file()), None)
        if not exe:
            return [], "Vale isn't installed"
        res = subprocess.run([exe, "--config", str(ROOT / ".vale.ini"), "--output=JSON", "--minAlertLevel=suggestion",
                              "--filter=.Name in " + json.dumps(find.get("checks") or [find["check"]]), str(path)],
                             capture_output=True, text=True, cwd=ROOT)
        try:
            alerts = [a for v in json.loads(res.stdout or "{}").values() for a in v]
        except json.JSONDecodeError:
            alerts = []
        seen = set()
        for a in alerts:
            for b in blocks:
                if b["kind"] != "prose":
                    continue
                for line, s in sentences(b):
                    if a["Match"] in s and line <= a["Line"] <= line + s.count("\n") and (line, s) not in seen:
                        seen.add((line, s))
                        out.append({"line": line, "text": s, "context": b["text"], "mark": a["Match"]})
    elif kind == "added-tables":
        for b in blocks:
            header = b["text"].splitlines()[0] if b["kind"] == "table" else ""
            if b["kind"] == "table" and b["line"] in added and not re.match(r"^\|\s*(key|id)\s*\|", header, re.I):
                out.append({"line": b["line"], "text": b["text"], "context": b["text"]})
    elif kind == "added-headings":
        for k, b in enumerate(blocks):
            if b["kind"] != "heading" or b["line"] not in added or b["text"].lower().startswith("example"):
                continue
            body = []
            for x in blocks[k + 1:]:
                if x["kind"] == "heading" and x["level"] <= b["level"]:
                    break
                body.append(x)
            if sum(x["kind"] == "prose" for x in body) < 3 and not any(x["kind"] in ("table", "code") for x in body):
                text = "#" * b["level"] + " " + b["text"] + "\n\n" + "\n\n".join(x["text"] for x in body)
                out.append({"line": b["line"], "text": text, "context": text})
    elif kind == "changed-links":
        gone = removed_links(path, base)
        if gone:
            for b in blocks:
                if b["kind"] != "prose":
                    continue
                for line, s in sentences(b):
                    targets = LINK.findall(s)
                    if line in added and targets and not set(targets) & gone:
                        out.append({"line": line, "text": s, "context": b["text"],
                                    "note": f"previous link targets on this page: {', '.join(sorted(gone))}"})
    elif kind == "json-blocks":
        pat = re.compile(find["pattern"], re.S)
        for b in blocks:
            if b["kind"] == "code" and b["lang"] in ("json", "json5") and pat.search(b["text"]):
                out.append({"line": b["line"], "text": b["text"], "context": b["text"]})
    elif kind == "examples-section":
        start = next((k for k, b in enumerate(blocks) if b["kind"] == "heading" and b["text"].lower() in ("examples", "example")), None)
        if start is not None:
            level = blocks[start]["level"]
            section = []
            for b in blocks[start + 1:]:
                if b["kind"] == "heading" and b["level"] <= level:
                    break
                section.append(b)
            heads = [b for b in section if b["kind"] == "heading"]
            if len(heads) >= 2:
                summary = []
                for b in section:
                    if b["kind"] == "heading":
                        summary.append("#" * b["level"] + " " + b["text"])
                    elif b["kind"] == "prose":
                        summary.append(b["text"])
                text = "\n\n".join(summary)
                out.append({"line": blocks[start]["line"], "text": text, "context": text})
    else:
        return [], f"unknown detector {kind}"
    return out, None


# ------------------------------------------------------------------ judging

def state_for(page: dict, rel: str, cand: dict) -> str:
    parts = [f"Page: {page['title'] or rel}", f"File: {rel}"]
    if cand.get("note"):
        parts.append(f"Note: {cand['note']}")
    if cand["context"] != cand["text"]:
        parts.append(f"Context:\n{cand['context']}")
    parts.append(f"Marked text:\n{cand['text']}" + (f"\n(marked phrase: {cand['mark']})" if cand.get("mark") else ""))
    return "\n\n".join(parts)[:MAX_STATE]


def key(rid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", rid)


def verdict(spec: dict, answer: dict) -> str:
    v = spec["check"].get("verdicts") or {}
    choice, conf = answer.get("choice"), answer.get("confidence", 0)
    if choice in (v.get("violation") or []):
        return "violation" if conf >= THRESHOLD else "unsure"
    if choice in (v.get("review") or []):
        return "review"
    return "ok"


def trusted(spec: dict) -> bool:
    """Calibration earned trust: flagged violations are almost always real (precision), and the rule
    finds at least half of the labeled violations (recall)."""
    cal = spec.get("calibration") or {}
    return (cal.get("precision", 0) >= TRUST and cal.get("recall", 0) >= 0.5
            and cal.get("cases", 0) >= MIN_CASES and cal.get("violations", 0) >= MIN_VIOLATIONS)


def load_specs(only: set | None = None) -> dict:
    specs = {}
    for p in sorted(SPECS.glob("*.yaml")):
        d = yaml.safe_load(p.read_text())
        if not only or d["id"] in only:
            specs[d["id"]] = d
    return specs


def judge(files: list[Path], specs: dict, base: str | None = None, dry_run: bool = False, workers: int = 8) -> dict:
    """Run every rule on every file. Returns {results, skipped, usage, calls}."""
    groups, skipped = {}, []
    for path in files:
        page = parse(path.read_text())
        rel = str(path.relative_to(ROOT))
        for rid, spec in specs.items():
            cands, why = find_candidates(spec, path, page, base)
            if why and not any(x["rule"] == rid and x["reason"] == why for x in skipped if why.startswith("manual")):
                skipped.append({"rule": rid, "path": rel, "reason": why})
            for c in cands:
                state = state_for(page, rel, c)
                g = groups.setdefault(state, {"path": rel, "line": c["line"], "text": c["text"], "rules": []})
                if rid not in g["rules"]:
                    g["rules"].append(rid)
    results, usage, calls = [], {"input_tokens": 0, "output_tokens": 0}, 0
    if dry_run:
        for g in groups.values():
            results += [{"rule": r, "path": g["path"], "line": g["line"], "text": g["text"], "verdict": "candidate"}
                        for r in g["rules"]]
        return {"results": results, "skipped": skipped, "usage": usage, "calls": 0}

    def ask(item):
        state, g = item
        q = {key(r): jev.choice_question(specs[r]["check"]["question"]["ask"], specs[r]["check"]["question"]["criteria"])
             for r in g["rules"]}
        return state, g, jev.call(state, q)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for state, g, resp in pool.map(ask, groups.items()):
            calls += 1
            for k in usage:
                usage[k] += (resp.get("usage") or {}).get(k, 0)
            for r in g["rules"]:
                ans = (resp.get("answers") or {}).get(key(r)) or {}
                results.append({"rule": r, "path": g["path"], "line": g["line"], "text": g["text"],
                                "choice": ans.get("choice"), "confidence": ans.get("confidence"),
                                "verdict": verdict(specs[r], ans), "trusted": trusted(specs[r]),
                                "fix": specs[r].get("fix"), "model": resp.get("model")})
    return {"results": results, "skipped": skipped, "usage": usage, "calls": calls}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--base")
    ap.add_argument("--rules")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--all", action="store_true", help="also print ok results")
    a = ap.parse_args(argv)
    specs = load_specs(set(a.rules.split(",")) if a.rules else None)
    files = [Path(f).resolve() for f in a.files]
    try:
        out = judge(files, specs, a.base, a.dry_run)
    except jev.JevUnavailable as e:
        print(f"judge: Jev unavailable: {e}", file=sys.stderr)
        return 3
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        for r in sorted(out["results"], key=lambda r: (r["path"], r["line"], r["rule"])):
            if r["verdict"] == "ok" and not a.all:
                continue
            tag = r["verdict"] + ("" if r.get("trusted", True) or r["verdict"] == "candidate" else " (advisory)")
            conf = f" {r['choice']} {r['confidence']:.2f}" if r.get("choice") else ""
            print(f"{r['path']}:{r['line']}: {tag}: {r['rule']}{conf}: {r['text'][:120]!r}")
            if r["verdict"] in ("violation", "unsure") and r.get("fix"):
                print(f"    fix: {r['fix']}")
        for s in out["skipped"]:
            if s["reason"] != "needs --base" or a.base:
                print(f"skipped {s['rule']} on {s['path']}: {s['reason']}")
        n = {v: sum(r["verdict"] == v for r in out["results"]) for v in ("violation", "unsure", "review", "ok", "candidate")}
        print(f"{out['calls']} Jev calls, {out['usage']['input_tokens']} input tokens (${jev.cost(out['usage']):.4f}); "
              + ", ".join(f"{k} {v}" for k, v in n.items() if v))
    failing = [r for r in out["results"] if r["verdict"] == "violation" and r.get("trusted")]
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
