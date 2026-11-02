#!/usr/bin/env python3
"""Flag merged sensible-hq/sensible PRs that may need docs, by adding the docs_triage_ai label.

Jev (TypeSafe's judge model) answers each question in criteria.md as a yes/no score (noul)
about one PR: its title, description, changed files, and a diff excerpt. A PR gets the label
when any T-* trigger scores at or above the threshold and neither X-* exclusion does.

  python3 scripts/docs_triage/triage.py --dry-run              # score PRs merged in the last 4 days
  python3 scripts/docs_triage/triage.py --dry-run --pr 3474    # score specific PRs
  python3 scripts/docs_triage/triage.py                        # also apply the label

Needs GH_TOKEN (or a logged-in gh) with read access to sensible's contents and write access to
its pull requests, and TYPESAFE_API_KEY.

sensible-docs is public and sensible is private, so in GitHub Actions this script prints only
counts and PR numbers: no titles, scores, or error text, which could quote private code.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = "sensible-hq/sensible"
LABEL = "docs_triage_ai"
# A PR that already carries any of these has had a human docs decision.
DOCS_LABELS = {LABEL, "doc_changes_needed", "docs_done", "docs_dont_publicly_doc", "docs_future_not_yet_blocked"}
BOT_AUTHORS = {"dependabot", "dependabot[bot]", "github-actions", "github-actions[bot]", "app/dependabot"}

JEV_API = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL = "jev-latest"
THRESHOLD = 0.70

HERE = Path(__file__).resolve().parent
DOCS_ROOT = HERE.parent.parent
CRITERION = re.compile(r"^\s*-\s+\[([TX]-[\w-]+)\]\s+(.+?)\s*$")

# Files whose diffs say nothing about docs: extractor goldens, OCR caches, lockfiles, binaries.
SKIP_FILE = re.compile(r"^(extraction-cache/|extractors/.*/goldens/|test-cache/|pnpm-lock\.yaml$|.*\.snap$|.*\.(pdf|png|jpe?g|tiff?|csv|xlsx?|xlsm|xlsb)$)")
# Diff excerpts lead with the files that most often mean docs: the config schema, then the API.
PRIORITY = ["src/engine/__generated__/", "src/engine/types.ts", "src/api/", "src/engine/"]
# PR descriptions sometimes name the label outright; Jev must not see the answer.
LABEL_MENTION = re.compile(r"doc_changes_needed|docs_done|docs_dont_publicly_doc|docs_future_not_yet_blocked|docs_triage_ai|docs?[_ -]needed", re.I)

IN_CI = bool(os.environ.get("GITHUB_ACTIONS"))


class JevUnavailable(RuntimeError):
    pass


# ── criteria and decision ────────────────────────────────────────────────────

def load_criteria(path: Path = HERE / "criteria.md") -> dict:
    """{id: question} from lines like `- [T-config] The PR adds ...`."""
    return {m.group(1): m.group(2) for line in path.read_text().splitlines() if (m := CRITERION.match(line))}


def needs_triage(scores: dict, threshold: float = THRESHOLD) -> bool:
    triggered = any(v >= threshold for k, v in scores.items() if k.startswith("T-"))
    excluded = any(v >= threshold for k, v in scores.items() if k.startswith("X-"))
    return triggered and not excluded


# ── what Jev sees ────────────────────────────────────────────────────────────

def public_endpoints(root: Path = DOCS_ROOT) -> list:
    """`METHOD /path` for every operation in the published OpenAPI specs."""
    out = set()
    for spec in sorted((root / "reference").glob("openapi_*.json")):
        for path, ops in json.loads(spec.read_text()).get("paths", {}).items():
            out.update(f"{m.upper()} {path}" for m in ops if m != "parameters")
    return sorted(out)


def redact(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not LABEL_MENTION.search(line))


def _rank(path: str) -> int:
    for i, prefix in enumerate(PRIORITY):
        if path.startswith(prefix):
            return i
    return len(PRIORITY) + ("test" in path)


def build_state(pr: dict, files: list, endpoints: list, budget: int = 14000, per_file: int = 4000) -> str:
    """The text Jev judges. `files` is the GitHub pulls/files list (filename, patch)."""
    shown = [f for f in files if not SKIP_FILE.match(f["filename"])]
    out = [f"PR #{pr['number']}: {pr['title']}", "", "Description:",
           redact((pr.get("body") or "(none)").strip())[:3000], "",
           f"Changed files ({len(files)}; {len(files) - len(shown)} golden/cache/lock files omitted):"]
    out += [f"  {f['filename']}" for f in shown[:80]]
    out += ["", "Public API endpoints (documented at docs.sensible.so):"] + [f"  {e}" for e in endpoints]
    out += ["", "Diff excerpt:"]
    used = 0
    for f in sorted(shown, key=lambda f: _rank(f["filename"])):
        if used >= budget:
            break
        chunk = f"--- {f['filename']}\n{f.get('patch') or '(no patch: binary or too large)'}\n"[:min(per_file, budget - used)]
        out.append(chunk)
        used += len(chunk)
    return "\n".join(out)


# ── Jev ──────────────────────────────────────────────────────────────────────

def _key(cid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", cid)  # Jev question ids must be plain keys


def ask_jev(state: str, criteria: dict) -> dict:
    """{criterion id: noul score}. Raises JevUnavailable; never guesses a pass or fail."""
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        raise JevUnavailable("TYPESAFE_API_KEY is not set")
    body = {"state": state, "model": JEV_MODEL,
            "questions": {_key(c): {"type": "noul", "instructions": q} for c, q in criteria.items()}}
    req = urllib.request.Request(JEV_API, data=json.dumps(body).encode(), method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "sensible-docs-triage"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise JevUnavailable(f"HTTP {e.code}") from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise JevUnavailable(f"network: {e}") from None
    back = {_key(c): c for c in criteria}
    scores = {back[k]: a["noul"] for k, a in (resp.get("answers") or {}).items() if k in back and a.get("type") == "noul"}
    if set(scores) != set(criteria):
        raise JevUnavailable("Jev did not answer every question")
    return scores


# ── GitHub ───────────────────────────────────────────────────────────────────

def gh(path: str, method: str = "GET", fields: dict | None = None):
    cmd = ["gh", "api", "-X", method, path]
    for k, v in (fields or {}).items():
        cmd += ["-f", f"{k}={v}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        raise RuntimeError(f"gh api {method} {path} failed")  # stderr can quote private data; drop it
    return json.loads(res.stdout) if res.stdout.strip() else None


def merged_since(since: dt.datetime) -> list:
    q = f"repo:{REPO} is:pr is:merged merged:>={since.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    items, page = [], 1
    while True:
        res = gh(f"search/issues?q={urllib.parse.quote(q)}&per_page=100&page={page}")
        items += res["items"]
        if len(res["items"]) < 100:
            return items
        page += 1


def pr_files(number: int) -> list:
    files, page = [], 1
    while page <= 30:  # GitHub returns at most 3000 files
        batch = gh(f"repos/{REPO}/pulls/{number}/files?per_page=100&page={page}")
        files += batch
        if len(batch) < 100:
            break
        page += 1
    return files


def label_was_removed(number: int) -> bool:
    """A human took docs_triage_ai off this PR before; don't put it back."""
    page = 1
    while True:
        events = gh(f"repos/{REPO}/issues/{number}/events?per_page=100&page={page}")
        if any(e.get("event") == "unlabeled" and (e.get("label") or {}).get("name") == LABEL for e in events):
            return True
        if len(events) < 100:
            return False
        page += 1


def candidate(issue: dict) -> bool:
    labels = {lbl["name"] for lbl in issue.get("labels", [])}
    return not labels & DOCS_LABELS and (issue.get("user") or {}).get("login") not in BOT_AUTHORS


# ── main ─────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since-days", type=float, default=4,
                    help="look back this many days (default 4: the gap between the Monday and Thursday runs)")
    ap.add_argument("--pr", type=int, action="append", help="score these PRs instead of searching")
    ap.add_argument("--dry-run", action="store_true", help="score and report, but don't label")
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    args = ap.parse_args(argv)

    criteria, endpoints = load_criteria(), public_endpoints()
    if args.pr:
        issues = [gh(f"repos/{REPO}/issues/{n}") for n in args.pr]
    else:
        since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.since_days)
        issues = [i for i in merged_since(since) if candidate(i)]

    flagged, passed, skipped, failed = [], [], [], []
    for issue in issues:
        n = issue["number"]
        try:
            if not args.pr and label_was_removed(n):
                skipped.append(n)
                continue
            pr = gh(f"repos/{REPO}/pulls/{n}")
            scores = ask_jev(build_state(pr, pr_files(n), endpoints), criteria)
        except (JevUnavailable, RuntimeError) as e:
            failed.append(n)
            print(f"#{n}: not scored" + ("" if IN_CI else f" ({e})"))
            continue
        hit = needs_triage(scores, args.threshold)
        if not IN_CI:
            top = ", ".join(f"{k}={v:.2f}" for k, v in sorted(scores.items(), key=lambda kv: -kv[1])[:3])
            print(f"#{n} {'FLAG' if hit else 'pass'}  {pr['title'][:70]}  [{top}]")
        if hit:
            if not args.dry_run:
                gh(f"repos/{REPO}/issues/{n}/labels", "POST", {"labels[]": LABEL})
            flagged.append(n)
        else:
            passed.append(n)

    verb = "would label" if args.dry_run else "labeled"
    print(f"\n{len(issues)} PRs considered: {verb} {len(flagged)} {flagged}, {len(passed)} not flagged, "
          f"{len(skipped)} skipped (label removed by a human), {len(failed)} not scored {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
