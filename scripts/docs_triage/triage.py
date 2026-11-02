#!/usr/bin/env python3
"""Label merged sensible-hq/sensible PRs that need docs (docs_needed_ai) or may need them (docs_triage_ai).

Jev (TypeSafe's judge model) answers each question in criteria.md as a yes/no score (noul)
about one PR: its title, description, changed files, and a diff excerpt. `decide` turns the
scores into one of the two labels, or none; criteria.md describes the rule.

  python3 scripts/docs_triage/triage.py --dry-run              # score PRs merged in the last 4 days
  python3 scripts/docs_triage/triage.py --dry-run --pr 3474    # score specific PRs
  python3 scripts/docs_triage/triage.py                        # also apply the labels
  python3 scripts/docs_triage/triage.py --issues               # open sensible-docs issues instead

--issues opens one sensible-docs issue per docs_needed_ai PR and one issue for the run's
docs_triage_ai PRs, and labels nothing. It's for running locally with your own gh login, until
the workflow has a token that can read sensible. sensible-docs is public, so the issues name
only PR numbers and the question that flagged each one: never titles or descriptions.

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
DOCS_REPO = "sensible-hq/sensible-docs"
NEEDED = "docs_needed_ai"
TRIAGE = "docs_triage_ai"
AI_LABELS = {NEEDED, TRIAGE}
# A PR that already carries any of these has been labeled, by a human or by this script.
DOCS_LABELS = AI_LABELS | {"doc_changes_needed", "docs_done", "docs_dont_publicly_doc", "docs_future_not_yet_blocked"}
BOT_AUTHORS = {"dependabot", "dependabot[bot]", "github-actions", "github-actions[bot]", "app/dependabot"}

JEV_API = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL = "jev-latest"

TRIAGE_THRESHOLD = 0.70  # any trigger at or above this: the PR gets at least docs_triage_ai
NEEDED_THRESHOLD = 0.90  # a confident trigger at or above this can earn docs_needed_ai
CLEAR = 0.30             # docs_needed_ai also needs every exclusion below this
# Triggers precise enough for docs_needed_ai. T-api, T-behavior, and T-output catch real docs
# work too, but they're where most false positives come from, so alone they only earn triage.
CONFIDENT_TRIGGERS = ("T-config", "T-inputs", "T-models")
# Exclusions that rule a PR out. The other X-* questions only keep it out of docs_needed_ai.
HARD_EXCLUSIONS = ("X-internal",)

HERE = Path(__file__).resolve().parent
DOCS_ROOT = HERE.parent.parent
CRITERION = re.compile(r"^\s*-\s+\[([TX]-[\w-]+)\]\s+(.+?)\s*$")

# Files whose diffs say nothing about docs: extractor goldens, OCR caches, lockfiles, binaries.
SKIP_FILE = re.compile(r"^(extraction-cache/|extractors/.*/goldens/|test-cache/|pnpm-lock\.yaml$|.*\.snap$|.*\.(pdf|png|jpe?g|tiff?|csv|xlsx?|xlsm|xlsb)$)")
# Diff excerpts lead with the files that most often mean docs: the config schema, then the API.
PRIORITY = ["src/engine/__generated__/", "src/engine/types.ts", "src/api/", "src/engine/"]
# PR descriptions sometimes name the label outright; Jev must not see the answer.
LABEL_MENTION = re.compile(r"doc_changes_needed|docs_done|docs_dont_publicly_doc|docs_future_not_yet_blocked|docs_triage_ai|docs_needed_ai|docs?[_ -]needed", re.I)

IN_CI = bool(os.environ.get("GITHUB_ACTIONS"))


class JevUnavailable(RuntimeError):
    """Jev couldn't score a PR (no key, network or HTTP error, or a missing answer).

    The script fails closed on this: the PR gets no label and the run exits nonzero.
    """


# ── criteria and decision ────────────────────────────────────────────────────

def load_criteria(path: Path = HERE / "criteria.md") -> dict:
    """Read the Jev questions from a criteria file.

    Args:
        path: a Markdown file with one question per line, like `- [T-config] The PR adds ...`.
            Lines that don't match are ignored.

    Returns:
        {criterion id: question text}, in file order.
    """
    return {m.group(1): m.group(2) for line in path.read_text().splitlines() if (m := CRITERION.match(line))}


def decide(scores: dict, triage_threshold: float = TRIAGE_THRESHOLD) -> str | None:
    """Turn Jev's scores for one PR into a label.

    Args:
        scores: {criterion id: noul score from 0 to 1}, for every T-* and X-* question.
        triage_threshold: the score a trigger needs for docs_triage_ai.

    Returns:
        NEEDED when a confident trigger is at or above NEEDED_THRESHOLD and every exclusion is
        below CLEAR; TRIAGE when any trigger is at or above triage_threshold and no hard
        exclusion is; otherwise None.
    """
    triggers = {k: v for k, v in scores.items() if k.startswith("T-")}
    exclusions = {k: v for k, v in scores.items() if k.startswith("X-")}
    if max(triggers.values(), default=0) < triage_threshold:
        return None
    if any(exclusions.get(k, 0) >= triage_threshold for k in HARD_EXCLUSIONS):
        return None
    confident = any(triggers.get(k, 0) >= NEEDED_THRESHOLD for k in CONFIDENT_TRIGGERS)
    if confident and all(v < CLEAR for v in exclusions.values()):
        return NEEDED
    return TRIAGE


# ── what Jev sees ────────────────────────────────────────────────────────────

def public_endpoints(root: Path = DOCS_ROOT) -> list:
    """List the operations in the published OpenAPI specs.

    Jev uses this list to tell public endpoints from ones only the Sensible app calls.

    Args:
        root: the sensible-docs checkout; specs are read from reference/openapi_*.json.

    Returns:
        Sorted strings like `POST /extract/{document_type}`.
    """
    out = set()
    for spec in sorted((root / "reference").glob("openapi_*.json")):
        for path, ops in json.loads(spec.read_text()).get("paths", {}).items():
            out.update(f"{m.upper()} {path}" for m in ops if m != "parameters")
    return sorted(out)


def redact(text: str) -> str:
    """Drop every line that names a docs label, so Jev doesn't see the answer.

    Args:
        text: a PR description.

    Returns:
        The description without those lines.
    """
    return "\n".join(line for line in text.splitlines() if not LABEL_MENTION.search(line))


def _rank(path: str) -> int:
    """Sort key for diff excerpts: lower ranks are shown first.

    Args:
        path: a changed file's path in sensible.

    Returns:
        The index of the first PRIORITY prefix the path starts with; otherwise one past the
        end, plus one more for test files.
    """
    for i, prefix in enumerate(PRIORITY):
        if path.startswith(prefix):
            return i
    return len(PRIORITY) + ("test" in path)


def build_state(pr: dict, files: list, endpoints: list, budget: int = 14000, per_file: int = 4000) -> str:
    """Build the text Jev judges for one PR.

    Args:
        pr: the GitHub pull request object (number, title, body).
        files: the GitHub pulls/files list for the PR (filename and patch for each file).
        endpoints: public API operations, from `public_endpoints`.
        budget: the most characters of diff to include, across all files.
        per_file: the most characters of diff to include from one file.

    Returns:
        The title, the redacted description, the changed files (goldens, caches, and lockfiles
        omitted), the public endpoints, and a diff excerpt that starts with the schema and API.
    """
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
    """Map a criterion id to a Jev question key, which allows only letters, digits, and `_`.

    Args:
        cid: a criterion id such as `T-config`.

    Returns:
        The id with every other character replaced by `_`, such as `T_config`.
    """
    return re.sub(r"[^A-Za-z0-9_]", "_", cid)


def ask_jev(state: str, criteria: dict) -> dict:
    """Ask Jev every question about one PR.

    Args:
        state: the PR text, from `build_state`.
        criteria: {criterion id: question}, from `load_criteria`.

    Returns:
        {criterion id: noul score from 0 to 1}.

    Raises:
        JevUnavailable: no TYPESAFE_API_KEY, a network or HTTP error, or an unanswered question.
            The message never includes the response body.
    """
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
    """Call the GitHub REST API through `gh api`.

    Args:
        path: the API path, such as `repos/sensible-hq/sensible/pulls/1`.
        method: the HTTP method.
        fields: form fields, sent with `-f`.

    Returns:
        The parsed JSON response, or None for an empty one.

    Raises:
        RuntimeError: the call failed. gh's stderr is dropped because it can quote private data.
    """
    cmd = ["gh", "api", "-X", method, path]
    for k, v in (fields or {}).items():
        cmd += ["-f", f"{k}={v}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        raise RuntimeError(f"gh api {method} {path} failed")
    return json.loads(res.stdout) if res.stdout.strip() else None


def merged_since(since: dt.datetime) -> list:
    """Find the sensible PRs merged at or after a time.

    Args:
        since: a UTC datetime.

    Returns:
        GitHub search results (issue objects with number, labels, and user), every page.
    """
    q = f"repo:{REPO} is:pr is:merged merged:>={since.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    items, page = [], 1
    while True:
        res = gh(f"search/issues?q={urllib.parse.quote(q)}&per_page=100&page={page}")
        items += res["items"]
        if len(res["items"]) < 100:
            return items
        page += 1


def pr_files(number: int) -> list:
    """List a PR's changed files with their patches.

    GitHub leaves out the patch for binary and very large files, and returns at most 3000 files.

    Args:
        number: the sensible PR number.

    Returns:
        GitHub pulls/files objects (filename, patch, and so on).
    """
    files, page = [], 1
    while page <= 30:
        batch = gh(f"repos/{REPO}/pulls/{number}/files?per_page=100&page={page}")
        files += batch
        if len(batch) < 100:
            break
        page += 1
    return files


def label_was_removed(number: int) -> bool:
    """Check whether a human has taken an AI label off this PR, so the script doesn't put it back.

    Args:
        number: the sensible PR number.

    Returns:
        True if the PR's events include removing docs_needed_ai or docs_triage_ai.
    """
    page = 1
    while True:
        events = gh(f"repos/{REPO}/issues/{number}/events?per_page=100&page={page}")
        if any(e.get("event") == "unlabeled" and (e.get("label") or {}).get("name") in AI_LABELS for e in events):
            return True
        if len(events) < 100:
            return False
        page += 1


def candidate(issue: dict) -> bool:
    """Decide whether a merged PR should be scored at all.

    Args:
        issue: a GitHub issue object for the PR (labels, user).

    Returns:
        False if the PR already has a docs label or a bot opened it; otherwise True.
    """
    labels = {lbl["name"] for lbl in issue.get("labels", [])}
    return not labels & DOCS_LABELS and (issue.get("user") or {}).get("login") not in BOT_AUTHORS


# ── sensible-docs issues (--issues) ──────────────────────────────────────────

def top_trigger(scores: dict) -> str:
    """Name the trigger that scored highest, for an issue to say why a PR was flagged.

    Args:
        scores: {criterion id: noul score} for one PR.

    Returns:
        A trigger id such as `T-config`. Ids are safe to publish; scores and PR text aren't.
    """
    return max((k for k in scores if k.startswith("T-")), key=lambda k: scores[k])


def has_docs_issue(number: int) -> bool:
    """Check whether any sensible-docs issue, open or closed, already mentions this PR.

    That covers the issues this script opens, earlier triage issues, and the issues the
    close-docs-pr skill opens, which all write the PR as `sensible-hq/sensible#N` or `sensible#N`.

    Args:
        number: the sensible PR number.

    Returns:
        True if an issue mentions it.
    """
    for ref in (f"sensible#{number}", f"{REPO}#{number}"):
        q = f'repo:{DOCS_REPO} is:issue "{ref}"'
        if gh(f"search/issues?q={urllib.parse.quote(q)}&per_page=1")["total_count"] > 0:
            return True
    return False


def needed_issue(number: int, scores: dict) -> tuple:
    """Write the issue for one docs_needed_ai PR.

    Args:
        number: the sensible PR number.
        scores: Jev's scores for it.

    Returns:
        (title, body). Neither includes the PR's title or description, because the issue is public.
    """
    title = f"Docs needed (AI): sensible#{number}"
    body = (f"Jev is confident that {REPO}#{number} needs docs (strongest signal: `{top_trigger(scores)}`, "
            f"see `scripts/docs_triage/criteria.md`).\n\n"
            f"Opened by `scripts/docs_triage/triage.py --issues`. If no docs are needed, label the PR "
            f"`docs_dont_publicly_doc` or close this as not planned.")
    return title, body


def triage_issue(flagged: dict, since: str, until: str) -> tuple:
    """Write the one issue that lists a run's docs_triage_ai PRs.

    Args:
        flagged: {PR number: Jev's scores} for every PR the run triaged.
        since: the start of the run's merge window, as YYYY-MM-DD.
        until: the end of the window, as YYYY-MM-DD.

    Returns:
        (title, body), with a checkbox per PR. Neither includes PR titles or descriptions.
    """
    title = f"Docs triage (AI): {len(flagged)} sensible PRs merged {since} to {until}"
    lines = [f"- [ ] {REPO}#{n} (`{top_trigger(s)}`)" for n, s in sorted(flagged.items())]
    body = ("Jev thinks these PRs may need docs, but isn't confident. For each, decide and label the PR "
            "(`doc_changes_needed`, `docs_dont_publicly_doc`, or nothing), then tick it.\n\n"
            + "\n".join(lines)
            + "\n\nOpened by `scripts/docs_triage/triage.py --issues`; see `scripts/docs_triage/criteria.md`.")
    return title, body


def open_issue(title: str, body: str) -> str:
    """Open a sensible-docs issue.

    Args:
        title: the issue title.
        body: the issue body, in Markdown.

    Returns:
        The new issue's URL.
    """
    return gh(f"repos/{DOCS_REPO}/issues", "POST", {"title": title, "body": body})["html_url"]


# ── main ─────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    """Score PRs, label them, and print a summary.

    Args:
        argv: command-line arguments; None reads sys.argv.

    Returns:
        The exit code: 0, or 1 if any PR couldn't be scored.
    """
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since-days", type=float, default=4,
                    help="look back this many days (default 4: the gap between the Monday and Thursday runs)")
    ap.add_argument("--pr", type=int, action="append", help="score these PRs instead of searching")
    ap.add_argument("--dry-run", action="store_true", help="score and report, but don't label")
    ap.add_argument("--threshold", type=float, default=TRIAGE_THRESHOLD, help="trigger score for docs_triage_ai")
    ap.add_argument("--issues", action="store_true",
                    help="open sensible-docs issues instead of labeling sensible PRs (with --dry-run, print them)")
    args = ap.parse_args(argv)
    now = dt.datetime.now(dt.timezone.utc)
    since = now - dt.timedelta(days=args.since_days)

    criteria, endpoints = load_criteria(), public_endpoints()
    if args.pr:
        issues = [gh(f"repos/{REPO}/issues/{n}") for n in args.pr]
    else:
        issues = [i for i in merged_since(since) if candidate(i)]

    labeled = {NEEDED: [], TRIAGE: []}
    all_scores = {}
    passed, skipped, failed = [], [], []
    for issue in issues:
        n = issue["number"]
        try:
            if not args.pr and (label_was_removed(n) or (args.issues and has_docs_issue(n))):
                skipped.append(n)
                continue
            pr = gh(f"repos/{REPO}/pulls/{n}")
            scores = ask_jev(build_state(pr, pr_files(n), endpoints), criteria)
        except (JevUnavailable, RuntimeError) as e:
            failed.append(n)
            print(f"#{n}: not scored" + ("" if IN_CI else f" ({e})"))
            continue
        label = decide(scores, args.threshold)
        if not IN_CI:
            top = ", ".join(f"{k}={v:.2f}" for k, v in sorted(scores.items(), key=lambda kv: -kv[1])[:3])
            print(f"#{n} {label or 'none':15s} {pr['title'][:70]}  [{top}]")
        if label:
            if not args.dry_run and not args.issues:
                gh(f"repos/{REPO}/issues/{n}/labels", "POST", {"labels[]": label})
            labeled[label].append(n)
            all_scores[n] = scores
        else:
            passed.append(n)

    if args.issues:
        drafts = [needed_issue(n, all_scores[n]) for n in labeled[NEEDED]]
        if labeled[TRIAGE]:
            drafts.append(triage_issue({n: all_scores[n] for n in labeled[TRIAGE]},
                                       since.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")))
        for title, body in drafts:
            print(f"\nwould open: {title}\n{body}" if args.dry_run else f"opened: {open_issue(title, body)}")

    verb = ("would open issues for" if args.issues else "would label") if args.dry_run else \
           ("opened issues for" if args.issues else "labeled")
    print(f"\n{len(issues)} PRs considered: {verb} {NEEDED} {labeled[NEEDED]} and {TRIAGE} {labeled[TRIAGE]}; "
          f"{len(passed)} not flagged, {len(skipped)} skipped (AI label removed, or already in an issue), "
          f"{len(failed)} not scored {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
