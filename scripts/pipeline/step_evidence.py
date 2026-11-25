#!/usr/bin/env python3
"""Check the evidence that a pipeline-for-pr step ran, from the session transcript, the repo, and the checklist.

The agent running the pipeline doesn't judge its own work here: this script reads what happened and prints an
evidence block with a link for each check, which the handoff report carries. What each step needs is in
.claude/skills/pipeline-for-pr/evidence.yaml; the design is in design/pipeline-step-evidence/design.md.

Usage:
  step_evidence.py --checklist <checklist.md> [--transcript <session.jsonl>] [--step N] [--json]

Reads the transcript of every session ID on the checklist, found under ~/.claude/projects/ or, with --transcript,
beside that file. Exits 0 when every check passes, 1 when any is missing or unverified, 2 on bad input.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / ".claude/skills/pipeline-for-pr/evidence.yaml"
BASE = os.environ.get("PIPELINE_BASE_REF", "origin/v0")
DOCS_REPO = os.environ.get("DOCS_REPO", "sensible-hq/sensible-docs")

HEADER_RE = re.compile(r"^# Checklist: pipeline for sensible#(\d+)", re.M)
STEP_RE = re.compile(r"^- \[([ xX])\] \*\*(\d+)\.\s*(.*?)\*\*")
FIELD_RE = re.compile(r"^(\s+)- ([^:]+?):(.*)$")
PLACEHOLDER_RE = re.compile(r"<[a-z][a-z -]*>|<[^>]*once step")
READ_CMD_RE = r"(?:^|[;&|(]|\n)\s*(cat|less|more|bat)\s+(-\S+\s+)*['\"]?\S*{path}"  # whole-file reads only, not sed/head/tail


@dataclass
class Result:
    status: str  # pass, missing, unverified
    label: str
    detail: str = ""
    link: str = ""


@dataclass
class Event:
    ts: datetime
    file: Path
    line: int
    kind: str  # read, bash, skill, text
    value: str

    @property
    def link(self) -> str:
        return f"{self.file}:{self.line}"


# --- checklist ---------------------------------------------------------------------------------------------

@dataclass
class Step:
    number: int
    title: str
    ticked: bool
    line: int
    fields: list  # (name, filled, line)
    skipped: bool


def header_value(text: str, name: str) -> str | None:
    m = re.search(rf"^{re.escape(name)}:\s*(.*)$", text, re.M)
    if not m or not m.group(1).strip() or PLACEHOLDER_RE.search(m.group(1)):
        return None
    return m.group(1).strip()


def parse_checklist(path: Path) -> dict:
    text = path.read_text()
    m = HEADER_RE.search(text)
    if not m:
        raise ValueError(f"{path} isn't a pipeline-for-pr checklist")
    lines = text.splitlines()
    steps: list[Step] = []
    for i, line in enumerate(lines, 1):
        sm = STEP_RE.match(line)
        if sm:
            steps.append(Step(int(sm.group(2)), sm.group(3).strip(), sm.group(1) != " ", i, [], False))
            continue
        fm = FIELD_RE.match(line)
        if fm and steps:
            indent, name, value = len(fm.group(1)), fm.group(2).strip(), fm.group(3).strip()
            nxt = lines[i] if i < len(lines) else ""
            nested = len(nxt) - len(nxt.lstrip()) > indent and nxt.strip().startswith("-")
            filled = bool(value) and not PLACEHOLDER_RE.search(value) or nested
            if name.lower() == "skipped":
                steps[-1].skipped = filled
            else:
                steps[-1].fields.append((name, filled, i))
    pr = header_value(text, "Docs PR")
    ids = header_value(text, "Claude Code session ID") or ""
    return {
        "path": path,
        "engine_pr": m.group(1),
        "docs_pr": (re.search(r"#(\d+)", pr or "") or [None, None])[1],
        "branch": (header_value(text, "Docs branch") or "").strip("`") or None,
        "session_ids": [s.strip() for s in ids.split(",") if s.strip()],
        "steps": steps,
    }


def current_step(checklist: dict) -> Step | None:
    return next((s for s in checklist["steps"] if not s.ticked and not s.skipped), None)


# --- transcript --------------------------------------------------------------------------------------------

def parse_ts(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def load_events(paths: list[Path]) -> list[Event]:
    events = []
    for path in paths:
        try:
            handle = path.open()
        except OSError:
            continue
        with handle:
            for n, raw in enumerate(handle, 1):
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") != "assistant":
                    continue
                ts = parse_ts(rec.get("timestamp"))
                content = (rec.get("message") or {}).get("content") or []
                if ts is None or not isinstance(content, list):
                    continue
                for item in content:
                    if item.get("type") == "text":
                        events.append(Event(ts, path, n, "text", item.get("text", "")))
                    elif item.get("type") == "tool_use":
                        inp = item.get("input") or {}
                        kind, value = {
                            # A Read with offset or limit saw part of the file, so it isn't a read of the skill.
                            "Read": ("partial_read" if inp.get("offset") or inp.get("limit") else "read",
                                     inp.get("file_path", "")),
                            "Bash": ("bash", inp.get("command", "")),
                            "Skill": ("skill", inp.get("skill", "")),
                        }.get(item.get("name"), (None, None))
                        if kind:
                            events.append(Event(ts, path, n, kind, value or ""))
    events.sort(key=lambda e: e.ts)
    return events


def transcripts(checklist: dict, transcript: Path | None) -> list[Path]:
    """This session's transcript, plus the transcript of every session ID on the checklist. Without a transcript
    path, IDs are looked up under ~/.claude/projects/."""
    if transcript:
        paths = [transcript.parent / f"{sid}.jsonl" for sid in checklist["session_ids"]] + [transcript]
    else:
        projects = Path(os.environ.get("CLAUDE_PROJECTS_DIR", Path.home() / ".claude/projects"))
        paths = [p for sid in checklist["session_ids"] for p in sorted(projects.glob(f"*/{sid}.jsonl"))]
    return list(dict.fromkeys(paths))


def is_read(event: Event, path: str) -> bool:
    skill = path.split("/")[2] if path.startswith(".claude/skills/") else None
    if event.kind == "read":
        return event.value.endswith("/" + path) or event.value == path
    if event.kind == "bash":
        return bool(re.search(READ_CMD_RE.format(path=re.escape(path)), event.value))
    return event.kind == "skill" and skill is not None and event.value.split(":")[-1] == skill


def step_windows(spec: dict, events: list[Event], upto: int) -> dict[int, tuple[datetime | None, Event | None]]:
    """For each step, when its window opens and the read that opened it. A step's read only counts after the
    previous step's window opened, so a later step can't reuse an earlier step's read of the same file."""
    windows, start = {}, None
    for n in sorted(k for k in spec if k <= upto):
        path = next((c["path"] for c in spec[n] if c["kind"] == "read"), None)
        hit = None
        if path:
            hit = next((e for e in events if (start is None or e.ts > start) and is_read(e, path)), None)
        if hit:
            start = hit.ts
        windows[n] = (start, hit)
    return windows


# --- checks ------------------------------------------------------------------------------------------------

class Missing(Exception):
    pass


def fill(template: str, checklist: dict, regex: bool = False) -> str:
    def sub(m):
        value = checklist.get(m.group(1))
        if value is None:
            raise Missing(f"no {m.group(1).replace('_', ' ')} on the checklist yet")
        return re.escape(value) if regex else value
    return re.sub(r"\{(engine_pr|docs_pr|branch)\}", sub, template)


def git(*args, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True)


def main_root(path: Path) -> Path:
    out = git("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=path.parent)
    return Path(out.stdout.strip()).parent if out.returncode == 0 else path.parent


def worktree_for(root: Path, branch: str) -> Path | None:
    out = git("worktree", "list", "--porcelain", cwd=root).stdout
    for block in out.split("\n\n"):
        if f"branch refs/heads/{branch}" in block:
            return Path(block.splitlines()[0].removeprefix("worktree "))
    return None


def check(c: dict, ctx: dict) -> Result:
    kind, checklist, start = c["kind"], ctx["checklist"], ctx["start"]
    try:
        if kind == "read":
            label = f"Read `{c['path']}`"
            hit = ctx["read_hit"]
            if not hit:
                return Result("missing", label, "no read of the skill file in this step's part of the transcript")
            return Result("pass", label, hit.ts.strftime("%Y-%m-%d %H:%M UTC"), hit.link)

        if kind == "bash":
            pattern = re.compile(fill(c["pattern"], checklist, regex=True))
            hit = next((e for e in ctx["events"] if e.kind == "bash" and (start is None or e.ts >= start)
                        and pattern.search(e.value)), None)
            if not hit:
                return Result("missing", c["label"], f"no command matching `{pattern.pattern}` during this step")
            command = " ".join(hit.value.split())
            return Result("pass", c["label"], f"`{command[:70]}{'…' if len(command) > 70 else ''}`", hit.link)

        if kind == "file":
            root = ctx["main"] if c.get("root", "main") == "main" else ctx["worktree"]
            if root is None:
                raise Missing("the docs branch has no worktree yet")
            matches = sorted(glob.glob(str(root / fill(c["path"], checklist))))
            if not matches:
                return Result("missing", c["label"], f"no file matching `{fill(c['path'], checklist)}`")
            if "contains" not in c:
                return Result("pass", c["label"], f"{len(matches)} file(s)", f"{matches[0]}:1")
            pattern = re.compile(c["contains"])
            for match in matches:
                for n, line in enumerate(Path(match).read_text(errors="replace").splitlines(), 1):
                    if pattern.search(line):
                        return Result("pass", c["label"], "", f"{match}:{n}")
            return Result("missing", c["label"], f"no line matching `{c['contains']}`", f"{matches[0]}:1")

        if kind == "commit":
            branch = fill("{branch}", checklist)
            out = git("log", "--format=%h%x09%cI%x09%s", f"{BASE}..{branch}", "--", c["path"], cwd=ctx["main"])
            if out.returncode != 0:
                raise Missing(f"git couldn't read `{BASE}..{branch}`")
            for row in out.stdout.splitlines():
                sha, when, subject = row.split("\t", 2)
                if start is None or datetime.fromisoformat(when) >= start:
                    return Result("pass", c["label"], f"{sha} {subject}", f"git show {sha}")
            return Result("missing", c["label"], f"no commit on `{branch}` touching `{c['path']}` during this step")

        if kind == "pr_body":
            pr = fill("{docs_pr}", checklist)
            pattern = re.compile(fill(c["pattern"], checklist, regex=True))
            try:
                out = subprocess.run(["gh", "pr", "view", pr, "--repo", DOCS_REPO, "--json", "body,url"],
                                     capture_output=True, text=True, timeout=20)
                data = json.loads(out.stdout) if out.returncode == 0 else None
            except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
                data = None
            if data is None:
                raise Missing(f"`gh pr view {pr}` failed")
            if pattern.search(data.get("body") or ""):
                return Result("pass", c["label"], "", data.get("url", ""))
            return Result("missing", c["label"], f"PR body doesn't match `{pattern.pattern}`", data.get("url", ""))

        if kind == "checklist":
            step = ctx["step"]
            empty = [(name, line) for name, filled, line in step.fields if not filled]
            label = "Checklist fields filled"
            if not empty:
                return Result("pass", label, f"{len(step.fields)} field(s)", f"{checklist['path']}:{step.line}")
            names = "; ".join(name for name, _ in empty)
            return Result("missing", label, f"empty: {names}", f"{checklist['path']}:{empty[0][1]}")

        raise ValueError(f"unknown check kind {kind!r}")
    except Missing as e:
        return Result("unverified", c.get("label") or f"Read `{c.get('path')}`", str(e))


def evaluate(checklist_path: Path, transcript: Path | None, step_number: int | None = None) -> dict:
    spec = {int(k): v for k, v in yaml.safe_load(SPEC.read_text()).items()}
    checklist = parse_checklist(checklist_path)
    step = (next((s for s in checklist["steps"] if s.number == step_number), None) if step_number
            else current_step(checklist))
    if step is None:
        return {"step": None, "results": []}
    events = load_events(transcripts(checklist, transcript))
    windows = step_windows(spec, events, step.number)
    start, hit = windows.get(step.number, (None, None))
    main = main_root(checklist_path)
    ctx = {"checklist": checklist, "events": events, "start": start, "read_hit": hit, "step": step, "main": main,
           "worktree": worktree_for(main, checklist["branch"]) if checklist["branch"] else None}
    results = [check(c, ctx) for c in spec.get(step.number, [])]
    return {"step": step.number, "title": step.title, "results": results}


ICON = {"pass": "✅", "missing": "❌", "unverified": "⚠️"}


def evidence_id(outcome: dict) -> str:
    payload = json.dumps([outcome["step"], [asdict(r) for r in outcome["results"]]], sort_keys=True)
    return f"evidence-id: step {outcome['step']} · {hashlib.sha256(payload.encode()).hexdigest()[:10]}"


def render(outcome: dict) -> str:
    lines = [f"**Step {outcome['step']} evidence: {outcome['title']}**, checked by `scripts/pipeline/step_evidence.py`",
             ""]
    for r in outcome["results"]:
        parts = [f"{ICON[r.status]} {r.label}"] + [p for p in (r.detail, f"`{r.link}`" if r.link else "") if p]
        lines.append("- " + " · ".join(parts))
    lines += ["", evidence_id(outcome)]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--checklist", type=Path, required=True)
    ap.add_argument("--transcript", type=Path)
    ap.add_argument("--step", type=int)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        outcome = evaluate(args.checklist.resolve(), args.transcript and args.transcript.resolve(), args.step)
    except (OSError, ValueError, yaml.YAMLError) as e:
        print(e, file=sys.stderr)
        return 2
    if outcome["step"] is None:
        print("Every step is ticked or skipped.")
        return 0
    if args.json:
        print(json.dumps({**outcome, "results": [asdict(r) for r in outcome["results"]],
                          "evidence_id": evidence_id(outcome)}, indent=2))
    else:
        print(render(outcome))
    return 0 if all(r.status == "pass" for r in outcome["results"]) else 1


if __name__ == "__main__":
    sys.exit(main())
