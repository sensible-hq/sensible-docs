#!/usr/bin/env python3
"""Which style rules fire while Claude Code writes docs, what the agent does about each, and whether
the change sticks. Reads local Claude Code transcripts; commits only counts.

  python3 scripts/style/rule_usage.py collect [--week 2026-W46] [--projects DIR] [--no-git]
  python3 scripts/style/rule_usage.py report [--html PATH] [--summary] [--report-url URL]

collect  Reads the transcripts of sensible-docs and its worktrees (~/.claude/projects/
         -home-franc-GitHub-sensible-docs*, but not -gen, -sandbox, or -private, which are other repos)
         for one ISO week (Monday to Sunday, UTC; default: the last complete week), and writes
         style-rules/usage/<week>.json. Claude Code deletes transcripts after 30 days, so run it within
         three weeks; the weekly files keep the history.
report   Renders every committed week as one HTML report (and, with --summary, a Markdown summary).

A firing is one alert from a rule on one file in one session: a write-time hook denial (PreToolUse), a
hook report after an edit (PostToolUse), an alert the hook let through after repeated denials, an
alert from the old PR-wide Vale hook, or a judge.py verdict. The hook repeats an alert after every
edit, and the transcript stores each hook output more than once, so firings are deduplicated per
session, file, rule, message, and line.

Outcomes, per firing:
  acted     the agent edited the file later in the session, and no later report repeats the alert
  ignored   the alert was still reported after the agent's last edit to the file, or it never edited it
  reverted  acted, but Vale flags the same rule and message on the file on the default branch today
  pushback  acted, and Frances's next message reads as a correction ("put it back", "revert", "don't change")
  unknown   a judge verdict or PR-wide alert on a file the session never edited again

The repo is public, so the weekly file holds rule ids, docs paths, outcomes, and counts: never message
text. Pushback excerpts appear only in a local report (--local-excerpts).
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
USAGE = ROOT / "style-rules/usage"
PROJECTS = Path.home() / ".claude/projects"
PROJECT_RE = re.compile(r"^-home-[^-]+-GitHub-sensible-docs(?:-(?!gen\b|gen-|sandbox|private).+)?$")
GUIDE_RE = re.compile(r"/\.claude/(?:style-guide|preferences)/([^/]+\.md)$")
DOC_RE = re.compile(r"(?:^|/)(docs/.+\.mdx?)$")
# vale_gate.py describe(): "  line 12: Sensible.EmDash: message"
GATE_LINE = re.compile(r"^\s*line (\d+): ([\w.-]+): (.+)$", re.M)
# Vale --output=line: "path:12:5:Sensible.EmDash:message"
VALE_LINE = re.compile(r"^(\S[^\n]*?\.mdx?):(\d+):\d+:([\w.-]+):(.+)$", re.M)
# judge.py: "docs/x.md:12: violation: sensible-filler filler, p(violation) 0.91: '...'"
JUDGE_LINE = re.compile(r"^(\S[^\n]*?\.mdx?):(\d+): (violation|unsure)(?: \(advisory\))?: ([\w-]+)", re.M)
PUSHBACK = re.compile(r"\b(revert|undo|put (?:it|that|them) back|change (?:it|that) back|don'?t change|do not change|"
                      r"leave (?:it|that) (?:as|alone)|keep the original|why did you (?:change|rewrite)|that was (?:fine|right))\b", re.I)


def project_dirs(base: Path = PROJECTS) -> list[Path]:
    return sorted(d for d in base.iterdir() if d.is_dir() and PROJECT_RE.match(d.name)) if base.is_dir() else []


def doc_path(path: str) -> str | None:
    m = DOC_RE.search(path or "")
    return m.group(1) if m else None


def registry_ids() -> dict:
    """Vale check or rule id -> registry rule id."""
    out = {}
    for r in yaml.safe_load((ROOT / "style-rules/registry.yaml").read_text()) or []:
        out[r["id"]] = r["id"]
        for v in (r.get("enforced_by") or {}).get("vale") or []:
            out[v] = r["id"]
    out["sensible-code-fences"] = "sensible-code-fences"
    return out


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(text_of(c.get("text") if isinstance(c, dict) and "text" in c else c.get("content") if isinstance(c, dict) else c)
                         for c in content)
    return ""


def typed_message(o: dict) -> str | None:
    """The text of a message Frances typed, or None for tool results, hook text, and harness messages."""
    if o.get("type") != "user" or o.get("isMeta") or o.get("isSidechain"):
        return None
    c = (o.get("message") or {}).get("content")
    if isinstance(c, list):
        if any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c):
            return None
        c = text_of(c)
    if not isinstance(c, str) or c.lstrip().startswith("<"):
        return None
    return c


def parse_session(lines: list[str]) -> dict:
    """Events in one transcript, in order: edits, reports (alerts on a file), guide reads, typed messages."""
    tool_files, events = {}, []
    for raw in lines:
        try:
            o = json.loads(raw)
        except json.JSONDecodeError:
            continue
        ts = o.get("timestamp") or ""
        msg = o.get("message") if isinstance(o.get("message"), dict) else {}
        if o.get("type") == "assistant":
            for c in msg.get("content") or []:
                if not isinstance(c, dict) or c.get("type") != "tool_use":
                    continue
                inp = c.get("input") or {}
                fp = inp.get("file_path") or ""
                tool_files[c.get("id")] = fp
                if c.get("name") in ("Edit", "Write", "MultiEdit") and doc_path(fp):
                    events.append({"kind": "edit", "file": doc_path(fp), "ts": ts, "tool": c.get("id")})
                if c.get("name") == "Read" and GUIDE_RE.search(fp):
                    events.append({"kind": "read", "guide": GUIDE_RE.search(fp).group(1), "ts": ts})
        typed = typed_message(o)
        if typed is not None:
            events.append({"kind": "message", "text": typed, "ts": ts})
        a = o.get("attachment") if isinstance(o.get("attachment"), dict) else None
        if a:
            text = text_of(a.get("content")) + "\n" + json.dumps(a.get("blockingError") or "") + "\n" + str(a.get("stdout") or "")
            text = text.replace("\\n", "\n")
            file = doc_path(tool_files.get(a.get("toolUseID"), ""))
            if "Vale flagged" in text or "Possible problems for Jev to judge" in text:
                source = "post"
            elif "vale_gate let this edit through" in text:
                source = "let-through"
            elif "in the docs this PR changes" in text:
                source = "pr-hook"
            else:
                source = None
            if source:
                events += alerts_from(text, file, source, ts)
        if o.get("type") == "user":
            for c in msg.get("content") or [] if isinstance(msg.get("content"), list) else []:
                if not isinstance(c, dict) or c.get("type") != "tool_result":
                    continue
                text = text_of(c.get("content"))
                file = doc_path(tool_files.get(c.get("tool_use_id"), ""))
                if "breaks a house style rule" in text:
                    events += alerts_from(text, file, "deny", ts)
                elif re.search(r"\d+ Jev calls", text):
                    events += alerts_from(text, None, "judge", ts)
    return {"events": events}


def alerts_from(text: str, file: str | None, source: str, ts: str) -> list[dict]:
    out = []
    for m in GATE_LINE.finditer(text):
        if file:
            out.append({"kind": "alert", "source": source, "file": file, "line": int(m.group(1)), "check": m.group(2),
                        "message": m.group(3).strip(), "ts": ts})
    for m in VALE_LINE.finditer(text):
        f = doc_path(m.group(1)) or file
        if f:
            out.append({"kind": "alert", "source": source, "file": f, "line": int(m.group(2)), "check": m.group(3),
                        "message": m.group(4).strip(), "ts": ts})
    if source == "judge":
        for m in JUDGE_LINE.finditer(text):
            f = doc_path(m.group(1))
            if f:
                out.append({"kind": "alert", "source": "judge", "file": f, "line": int(m.group(2)), "check": m.group(4),
                            "message": m.group(3), "ts": ts})
    return out


def firings(session: dict) -> list[dict]:
    """Deduplicated firings with outcomes (before the git check). Alert text never leaves this function
    except as the check and the Vale message, which come from the rules, not from Frances."""
    ev = session["events"]
    seen = {}
    for i, e in enumerate(ev):
        if e["kind"] != "alert":
            continue
        k = (e["file"], e["check"], e["message"], e["line"])
        if k not in seen:
            seen[k] = {**e, "first": i}
        seen[k]["last"] = i
    out = []
    for (file, check, message, line), f in seen.items():
        later_edits = [i for i, e in enumerate(ev) if e["kind"] == "edit" and e["file"] == file and i > f["first"]]
        # Reports on this file after the agent's last edit following the alert
        repeated = later_edits and f["last"] > later_edits[-1]
        if f["source"] in ("judge", "pr-hook") and not later_edits:
            outcome = "unknown"  # these report on whole pages or PRs, not on the agent's own change
        elif later_edits and not repeated:
            outcome = "acted"
        else:
            outcome = "ignored"
        nxt = next((e for e in ev[(later_edits[0] if later_edits else f["first"]) + 1:] if e["kind"] == "message"), None)
        pushback = bool(outcome == "acted" and nxt and PUSHBACK.search(nxt["text"]))
        out.append({"file": file, "check": check, "message": message, "line": line, "source": f["source"], "ts": f["ts"],
                    "outcome": outcome, "pushback": pushback, "pushback_text": nxt["text"][:300] if pushback else None})
    return out


def vale_on_default_branch(file: str, base: str, cache: dict) -> set:
    """(check, message) pairs Vale reports on the file as it is on the default branch."""
    if file in cache:
        return cache[file]
    out = set()
    shown = subprocess.run(["git", "-C", str(ROOT), "show", f"{base}:{file}"], capture_output=True, text=True)
    if shown.returncode == 0:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import test_rules
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / Path(file).name
            p.write_text(shown.stdout)
            res = subprocess.run([test_rules.vale(), "--config", str(ROOT / ".vale.ini"), "--output=JSON", str(p)],
                                 capture_output=True, text=True)
            try:
                out = {(a["Check"], a["Message"]) for v in json.loads(res.stdout or "{}").values() for a in v}
            except json.JSONDecodeError:
                pass
    cache[file] = out
    return out


def week_bounds(week: str | None, now: datetime.datetime | None = None) -> tuple[str, datetime.datetime, datetime.datetime]:
    """(name, start, end) of an ISO week, UTC. Default: the last complete week before now."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if week:
        y, w = week.split("-W")
        start = datetime.datetime.fromisocalendar(int(y), int(w), 1).replace(tzinfo=datetime.timezone.utc)
    else:
        monday = (now - datetime.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        start = monday - datetime.timedelta(days=7)
    iso = start.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}", start, start + datetime.timedelta(days=7)


def collect(week: str | None, dirs: list[Path], base: str | None, now: datetime.datetime | None = None) -> dict:
    name, since, until = week_bounds(week, now)
    lo, hi = since.isoformat()[:19], until.isoformat()[:19]
    ids = registry_ids()
    all_firings, reads, sessions = [], collections.Counter(), 0
    for d in dirs:
        for f in sorted(d.rglob("*.jsonl")):
            if datetime.datetime.fromtimestamp(f.stat().st_mtime, datetime.timezone.utc) < since:
                continue
            lines = f.read_text(errors="replace").splitlines()
            s = parse_session(lines)
            evs = [e for e in s["events"] if lo <= e.get("ts", "")[:19] < hi]
            if not evs:
                continue
            sessions += 1
            for e in evs:
                if e["kind"] == "read":
                    reads[e["guide"]] += 1
            sid = hashlib.sha256(str(f).encode()).hexdigest()[:8]
            for x in firings({"events": evs}):
                all_firings.append({**x, "session": sid})
    cache = {}
    for x in all_firings:
        if base and x["outcome"] == "acted" and x["source"] != "judge":
            x["reverted"] = (x["check"], x["message"]) in vale_on_default_branch(x["file"], base, cache)
        else:
            x["reverted"] = False
    rules = {}
    for x in all_firings:
        rid = ids.get(x["check"], x["check"])
        r = rules.setdefault(rid, {"checks": set(), "firings": 0, "acted": 0, "ignored": 0, "unknown": 0, "reverted": 0, "pushback": 0})
        r["checks"].add(x["check"])
        r["firings"] += 1
        r[x["outcome"]] += 1
        r["reverted"] += x["reverted"]
        r["pushback"] += x["pushback"]
    return {"week": name, "from": since.date().isoformat(), "to": (until - datetime.timedelta(days=1)).date().isoformat(),
            "sessions": sessions, "default_branch": base,
            "rules": {k: {**v, "checks": sorted(v["checks"])} for k, v in sorted(rules.items())},
            "guide_reads": dict(sorted(reads.items())),
            # Public: rule, file, source, outcome. No message text from Frances or the agent.
            "firings": [{k: x[k] for k in ("session", "file", "check", "source", "outcome", "reverted", "pushback")} for x in all_firings],
            "_local": [x for x in all_firings if x["pushback"]]}


def load_weeks() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(USAGE.glob("*.json"))]


def render_html(weeks: list[dict], local: list[dict] | None = None) -> str:
    import report_html as h
    ids = set(registry_ids().values())
    totals = {}
    for w in weeks:
        for rid, v in w["rules"].items():
            t = totals.setdefault(rid, collections.Counter())
            t.update({k: v[k] for k in ("firings", "acted", "ignored", "unknown", "reverted", "pushback")})
    rows = []
    for rid, t in sorted(totals.items(), key=lambda x: -x[1]["firings"]):
        acted = t["acted"]
        kept = acted - t["reverted"] - t["pushback"]
        rows.append([f"<code>{h.e(rid)}</code>" + ("" if rid in ids else ' <span class="muted">not in the registry</span>'),
                     str(t["firings"]), str(acted), str(t["ignored"]), str(t["unknown"]), str(t["reverted"]), str(t["pushback"]),
                     h.chip("pass" if acted and kept / acted >= 0.8 else ("warn" if acted else "info"), f"{kept / acted:.0%}" if acted else "n/a")])
    never = sorted(ids - set(totals))
    by_week = [[h.e(w["week"]), str(w["sessions"]), str(sum(v["firings"] for v in w["rules"].values())),
                str(sum(v["acted"] for v in w["rules"].values())), str(sum(v["reverted"] + v["pushback"] for v in w["rules"].values()))]
               for w in weeks]
    reads = collections.Counter()
    for w in weeks:
        reads.update(w.get("guide_reads") or {})
    sections = [
        h.card("Rules that fired", h.table(["Rule", "Firings", "Acted", "Ignored", "Unknown", "Reverted", "Pushback", "Kept"], rows) if rows else "<p>No firings.</p>",
               "Kept: of the firings the agent acted on, the share that wasn't reverted on the default branch or pushed back on. "
               "Ignored can be right: the hook asks the agent to leave false positives and say why.", open_=True),
        h.card(f"Registered rules that never fired ({len(never)})", "<p>" + ", ".join(f"<code>{h.e(r)}</code>" for r in never) + "</p>",
               "Not necessarily dead: prose rules never fire, and a rule writers already follow fires rarely. Compare with the weekly "
               "cleanup's corpus counts.", open_=False),
        h.card("Weeks", h.table(["Week", "Sessions", "Firings", "Acted", "Reverted or pushed back"], by_week), open_=False),
        h.card("Style guides loaded", h.table(["Guide", "Reads"], [[h.e(g), str(n)] for g, n in reads.most_common()]),
               "A weak signal: reading a guide loads every rule in it at once.", open_=False),
    ]
    if local:
        sections.append(h.card("Pushback (local only)", h.table(["Rule", "File", "Next message"], [
            [f"<code>{h.e(x['check'])}</code>", h.e(x["file"]), h.e(x["pushback_text"] or "")] for x in local]),
            "From your transcripts. This section is never committed or uploaded.", open_=True))
    span = f"{weeks[0]['week']} to {weeks[-1]['week']}" if weeks else "no weeks yet"
    return h.page("Style rule usage", f"Claude Code sessions in sensible-docs, {span}", sections)


def summary(weeks: list[dict], report_url: str | None) -> str:
    w = weeks[-1] if weeks else None
    lines = ["## Style rule usage", ""]
    if report_url:
        lines += [f"**[Open the full HTML report]({report_url})** (opens in the browser; you need to be signed in to GitHub)", ""]
    if not w:
        return "\n".join(lines + ["No weekly usage files yet."])
    f = sum(v["firings"] for v in w["rules"].values())
    lines += [f"Latest week {w['week']}: {w['sessions']} sessions, {f} firings across {len(w['rules'])} rules, "
              f"{sum(v['acted'] for v in w['rules'].values())} acted on, "
              f"{sum(v['reverted'] + v['pushback'] for v in w['rules'].values())} reverted or pushed back."]
    return "\n".join(lines)


def git_base() -> str | None:
    for ref in ("origin/v0", "v0"):
        if subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", "-q", ref], capture_output=True).returncode == 0:
            return ref
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["collect", "report"])
    ap.add_argument("--week", help="ISO week such as 2026-W46 (default: the last complete week)")
    ap.add_argument("--projects", help="a transcripts directory to read instead of ~/.claude/projects/<sensible-docs*>")
    ap.add_argument("--no-git", action="store_true", help="skip the reverted check against the default branch")
    ap.add_argument("--html")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--report-url")
    ap.add_argument("--local-excerpts", action="store_true", help="collect: also write the pushback excerpts to a local HTML report")
    a = ap.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    if a.command == "collect":
        dirs = [Path(a.projects)] if a.projects else project_dirs()
        data = collect(a.week, dirs, None if a.no_git else git_base())
        local = data.pop("_local")
        USAGE.mkdir(parents=True, exist_ok=True)
        out = USAGE / f"{data['week']}.json"
        out.write_text(json.dumps(data, indent=1) + "\n")
        print(f"wrote {out.relative_to(ROOT)}: {data['sessions']} sessions, {len(data['firings'])} firings, "
              f"{len(data['rules'])} rules, {len(local)} with pushback")
        if a.local_excerpts or a.html:
            import report_html
            path = Path(a.html or Path(tempfile.gettempdir()) / "style-rule-usage-local.html")
            report_html.write(path, render_html(load_weeks(), local))
            print(f"local report (with pushback excerpts): {path}")
        return 0
    weeks = load_weeks()
    if a.html:
        import report_html
        report_html.write(Path(a.html), render_html(weeks))
    if a.summary:
        print(summary(weeks, a.report_url))
    return 0


if __name__ == "__main__":
    sys.exit(main())
