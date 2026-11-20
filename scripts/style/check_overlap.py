#!/usr/bin/env python3
"""Find style rules in style-rules/registry.yaml that duplicate, overlap, or contradict each other.

  python3 scripts/style/check_overlap.py [--jev] [--rules id,...] [--involving id,...] [--report FILE]

Three layers, cheapest first:

  fixtures  (deterministic) Run every Vale fixture in style-rules/tests/ and look at alerts from
            registered Vale rules that aren't under test. A `pass` line, which shows correct text for
            one rule, flagged by another rule is a contradiction: the house example breaks a house
            rule. A `fail` line flagged by another rule is an overlap. When the other rule is a
            judgment rule, its Vale pattern only finds candidates, so the hit is marked (detector):
            worth a look, weaker than a hard contradiction.
  wording   (deterministic) Pairs of rules whose statements and stated_in quotes share most of their
            content words. Cheap and noisy; it finds restatements, not conflicts.
  jev       (near-deterministic, --jev) Ask Jev two yes-or-no questions about each pair: do they ask
            for the same thing, and can following one break the other. Each pair is asked in both
            orders and the two answers are averaged, because Jev leans toward whatever comes first; a
            pair whose two orders disagree is reported as unstable rather than trusted.

The wording and Jev layers compare only rules that share a kind of text in their registry `applies`
list (whole-page matches every kind), because rules that never see the same text can't conflict.
Jev answers are cached by request in --cache, so a weekly run only asks about pairs where a rule's
wording changed since the last run.

A pair you've ruled on goes in style-rules/overlaps.yaml with a verdict and a hash of both statements.
Editing either rule's statement changes the hash, so the pair comes back for review. A rule that wins
a deliberate conflict lists the loser under `overrides` in the registry; that pair is never reported
as a contradiction.

A pair recorded with verdict `unreviewed` is a known backlog item: it's listed in the report but
doesn't fail the run. Exits 1 when any layer reports a pair that isn't recorded at all. Set JEV_RECORD / JEV_REPLAY as for jev.py.
"""
import argparse
import concurrent.futures
import hashlib
import itertools
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev  # noqa: E402
from test_rules import MARK, RULES, vale  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "style-rules/registry.yaml"
SETTLED = ROOT / "style-rules/overlaps.yaml"
TESTS = ROOT / "style-rules/tests"

WORDING_MIN = 0.3  # Jaccard similarity of content words
NOUL_YES = 0.7
UNSTABLE = 0.35  # gap between the two orders' answers

STOP = set("""a an the and or but not no nor of to in on for with as at by from into than then that this
these those it its is are be been being do does don't doesn't use used using when where which who what
how if so such any each every one only also more most other same can may must should never always
don't isn't aren't you your their there here just like about over under before after per via""".split())

QUESTIONS = {
    "same": ("Do Rule 1 and Rule 2 ask for the same thing, so that text that follows one rule also "
             "follows the other?",
             {"true": "The rules restate one requirement, or one is a narrower case of the other.",
              "false": "The rules require different things, even if they're about related topics."}),
    "conflict": ("Could a writer produce a sentence, heading, or code block where following Rule 1 means "
                 "breaking Rule 2?",
                 {"true": "Some text exists where the two rules can't both be followed.",
                  "false": "Any text can follow both rules at once."}),
}
CACHE = ROOT / ".cache/rule-overlap.json"


def load_rules(only=None):
    rules = yaml.safe_load(REGISTRY.read_text()) or []
    return [r for r in rules if not only or r["id"] in only]


def text_of(rule):
    """The rule as a reader meets it: its statement plus every place it's stated in prose."""
    quotes = [s.get("quote", "") for s in rule.get("stated_in") or []]
    return " ".join([rule.get("statement", "")] + quotes)


def shares_text(ra, rb):
    a, b = set(ra.get("applies") or []), set(rb.get("applies") or [])
    return bool(a & b) or "whole-page" in a | b


def candidate_pairs(by_id):
    return [(a, b) for a, b in itertools.combinations(sorted(by_id), 2) if shares_text(by_id[a], by_id[b])]


def pair_key(a, b):
    return tuple(sorted((a, b)))


def pair_hash(ra, rb):
    first, second = sorted((ra, rb), key=lambda r: r["id"])
    return hashlib.sha256((first.get("statement", "") + "\n" + second.get("statement", "")).encode()).hexdigest()[:12]


def load_settled(by_id, known=None):
    """Pairs ruled on whose statements haven't changed since, and pairs whose statements have."""
    settled, stale = {}, []
    entries = yaml.safe_load(SETTLED.read_text()) if SETTLED.exists() else None
    for e in entries or []:
        a, b = e["pair"]
        if known and (a in known and b in known) and (a not in by_id or b not in by_id):
            continue  # a rule outside --rules; not this run's business
        if a not in by_id or b not in by_id:
            stale.append(f"{a} / {b}: settled pair names a rule the registry doesn't have")
            continue
        if e.get("hash") != pair_hash(by_id[a], by_id[b]):
            stale.append(f"{a} / {b}: a statement changed since the pair was settled ({e.get('verdict')})")
            continue
        settled[pair_key(a, b)] = e
    return settled, stale


def overrides(by_id):
    return {pair_key(r["id"], o) for r in by_id.values() for o in r.get("overrides") or []}


# ---------------------------------------------------------------- fixtures

def fixture_findings(by_id):
    """(rule a, rule b, kind, evidence) for fixture lines flagged by a registered rule not under test."""
    check_to_rule = {}
    for r in by_id.values():
        for name in (r.get("enforced_by") or {}).get("vale") or []:
            check_to_rule.setdefault(name, r["id"])
    exe = vale()
    out = []
    for path in sorted(TESTS.glob("*.md")):
        text = path.read_text()
        m = RULES.search(text)
        if not m:
            continue
        under_test = {x.strip() for x in m.group(1).split(",") if x.strip()}
        owners = {check_to_rule[c] for c in under_test if c in check_to_rule}
        if not owners:
            continue
        res = subprocess.run([exe, "--config", str(ROOT / ".vale.ini"), "--output=JSON",
                              "--minAlertLevel=suggestion", str(path.relative_to(ROOT))],
                             cwd=ROOT, capture_output=True, text=True)
        try:
            alerts = [a for v in json.loads(res.stdout or "{}").values() for a in v]
        except json.JSONDecodeError:
            continue
        lines = text.splitlines()
        for a in alerts:
            other = check_to_rule.get(a["Check"])
            if not other or a["Check"] in under_test or other in owners:
                continue
            line = lines[a["Line"] - 1]
            mark = MARK.search(line)
            if not mark:
                continue
            kind = "contradiction" if (mark.group(1) or mark.group(2)) == "pass" else "overlap"
            if by_id[other].get("gate") == "judge":
                kind += " (detector)"  # the other rule's Vale pattern only finds candidates for Jev
            for owner in owners:
                out.append((owner, other, kind, f"{path.name}:{a['Line']} {a['Check']}: {line.strip()[:80]}"))
    return out


# ---------------------------------------------------------------- wording

def words(text):
    found = (w.rstrip(".-") for w in re.findall(r"[a-z][a-z0-9.'-]+", text.lower()))
    return {w for w in found if w not in STOP and len(w) > 2}


def wording_findings(by_id):
    bags = {rid: words(text_of(r)) for rid, r in by_id.items()}
    out = []
    for a, b in candidate_pairs(by_id):
        union = bags[a] | bags[b]
        if not union:
            continue
        sim = len(bags[a] & bags[b]) / len(union)
        if sim >= WORDING_MIN:
            out.append((a, b, "similar wording", f"{sim:.2f} shared: {', '.join(sorted(bags[a] & bags[b])[:8])}"))
    return out


# ---------------------------------------------------------------- jev

def request(first, second):
    state = f"Two style rules for software documentation.\n\nRule 1: {text_of(first)}\n\nRule 2: {text_of(second)}"
    qs = {k: {"type": "noul", "instructions": q, "criteria": c} for k, (q, c) in QUESTIONS.items()}
    return state, qs


def ask(first, second):
    state, qs = request(first, second)
    resp = jev.call(state, qs)
    return {k: float(resp["answers"][k]["noul"]) for k in QUESTIONS}


def jev_findings(by_id, workers=8, cache_path=None, stats=None):
    """Jev's verdicts on every candidate pair. Answers are reused from cache_path while both rules' text
    and the questions are unchanged, so only new or reworded pairs cost a call."""
    pairs = candidate_pairs(by_id)
    jobs = [(a, b) for a, b in pairs] + [(b, a) for a, b in pairs]
    cache = json.loads(cache_path.read_text()) if cache_path and cache_path.exists() else {}
    keys = {j: jev.digest(dict(zip(("state", "questions"), request(by_id[j[0]], by_id[j[1]])))) for j in jobs}
    todo = [j for j in jobs if keys[j] not in cache]
    with concurrent.futures.ThreadPoolExecutor(workers) as pool:
        for j, ans in zip(todo, pool.map(lambda p: ask(by_id[p[0]], by_id[p[1]]), todo)):
            cache[keys[j]] = ans
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        live = {keys[j] for j in jobs}
        cache_path.write_text(json.dumps({k: v for k, v in cache.items() if k in live}, indent=0, sort_keys=True))
    if stats is not None:
        stats.update(pairs=len(pairs), calls=len(todo), cached=len(jobs) - len(todo))
    answers = {j: cache[keys[j]] for j in jobs}
    out = []
    for a, b in pairs:
        fwd, back = answers[(a, b)], answers[(b, a)]
        for k, label in (("same", "duplicate"), ("conflict", "contradiction")):
            mean, gap = (fwd[k] + back[k]) / 2, abs(fwd[k] - back[k])
            if gap >= UNSTABLE and max(fwd[k], back[k]) >= NOUL_YES:
                out.append((a, b, f"unstable {label}", f"Jev {fwd[k]:.2f} one way, {back[k]:.2f} the other"))
            elif mean >= NOUL_YES:
                out.append((a, b, label, f"Jev {mean:.2f} ({fwd[k]:.2f} / {back[k]:.2f})"))
    return out


# ---------------------------------------------------------------- report

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--jev", action="store_true", help="also ask Jev about every pair of rules")
    ap.add_argument("--rules", help="comma-separated rule ids to limit the run to")
    ap.add_argument("--report", help="write a Markdown report to this file")
    ap.add_argument("--no-fixtures", action="store_true", help="skip the Vale fixture layer")
    ap.add_argument("--cache", default=str(CACHE), help="Jev answer cache (default .cache/rule-overlap.json)")
    ap.add_argument("--involving", help="comma-separated rule ids; report only pairs that include one")
    args = ap.parse_args(argv)

    by_id = {r["id"]: r for r in load_rules(set(args.rules.split(",")) if args.rules else None)}
    settled, stale = load_settled(by_id, {r["id"] for r in load_rules()})
    won = overrides(by_id)

    found = [] if args.no_fixtures else fixture_findings(by_id)
    found += wording_findings(by_id)
    stats = {}
    if args.jev:
        try:
            found += jev_findings(by_id, cache_path=Path(args.cache), stats=stats)
        except jev.JevUnavailable as e:
            print(f"check_overlap: Jev unavailable, skipped: {e}", file=sys.stderr)

    if args.involving:
        keep = set(args.involving.split(","))
        found = [f for f in found if f[0] in keep or f[1] in keep]
    open_, backlog, quiet = [], [], 0
    seen = set()
    for a, b, kind, evidence in found:
        k = pair_key(a, b)
        if k in settled and settled[k].get("verdict") == "unreviewed":
            if (k, kind, evidence) not in seen:
                seen.add((k, kind, evidence))
                backlog.append((a, b, kind, evidence))
            continue
        if k in settled or (k in won and "contradiction" in kind):
            quiet += 1
            continue
        if (k, kind, evidence) in seen:
            continue
        seen.add((k, kind, evidence))
        open_.append((a, b, kind, evidence))

    def listing(items):
        return [f"- **{kind}**: `{a}` / `{b}` (hash {pair_hash(by_id[a], by_id[b])}): {ev}" for a, b, kind, ev in
                sorted(items, key=lambda f: (f[2] != "contradiction", "contradiction" not in f[2],
                                             "duplicate" not in f[2], f[0], f[1]))]
    lines = listing(open_) + [f"- **stale**: {s}" for s in stale]
    if backlog:
        lines += ["", f"Unreviewed backlog ({len(backlog)}), not failing the run:", ""] + listing(backlog)
    summary = (f"{len(by_id)} rules, {len(open_)} open findings, {len(backlog)} in the unreviewed backlog, "
               f"{len(stale)} stale settlements, "
               f"{quiet} settled or overridden; {len(candidate_pairs(by_id))} of "
               f"{len(by_id) * (len(by_id) - 1) // 2} pairs share a kind of text")
    if stats:
        summary += f"; Jev: {stats['calls']} calls, {stats['cached']} answers from cache"
    body = "\n".join(lines) or "Nothing to review."
    if args.report:
        Path(args.report).write_text(f"# Rule overlap report\n\n{summary}\n\n{body}\n")
    print(body)
    print(summary)
    return 1 if open_ or stale else 0


if __name__ == "__main__":
    sys.exit(main())
