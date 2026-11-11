"""Where a test run's evidence comes from: the commit, whether the tested files had uncommitted
changes, when it ran, and against which Sensible environment. Reports and saved results carry it,
so a reader can tell whether a saved report matches the page next to it."""

import json
import os
import subprocess
from datetime import datetime, timezone

from . import settings

# Uncommitted changes here mean the run tested something no commit has: the page, the tooling, or test files
TESTED_PATHS = ["scripts/doc-detective", "scripts/test"]
# Except the saved evidence and the tooling's docs, which a run writes or which change nothing it runs
# (keep in step with NOT_TOOLING in plan_runs.py; a unit test checks it)
NOT_TESTED = [
    "scripts/doc-detective/reports",
    "scripts/doc-detective/sample-reports",
    "scripts/doc-detective/README.md",
    "scripts/doc-detective/TEST-MATRIX.md",
]
FILE = "provenance.json"


def _git(*args):
    try:
        out = subprocess.run(["git", *args], capture_output=True, text=True, cwd=settings.REPO_ROOT, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.strip()


def provenance(page_path):
    """{"commit", "uncommitted", "tested_at", "environment"}. commit is "unknown" outside a git checkout."""
    status = _git("status", "--porcelain", "--", page_path, *TESTED_PATHS, *(f":(exclude){p}" for p in NOT_TESTED))
    return {
        "commit": _git("rev-parse", "--short=9", "HEAD") or "unknown",
        "uncommitted": bool(status),
        "tested_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "environment": settings.env(),
    }


def for_run(output_dir, page_path):
    """The run's provenance, computed once and kept in output_dir/provenance.json, so the report header
    and the saved results agree, and both describe the tree before anything was saved."""
    path = os.path.join(output_dir, FILE)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            saved = json.load(f)
        if saved.get("page") == page_path:
            return {k: v for k, v in saved.items() if k != "page"}
    prov = provenance(page_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"page": page_path, **prov}, f, indent=2)
    return prov


def describe(prov):
    """One line for a report header."""
    changes = " (with uncommitted changes)" if prov["uncommitted"] else ""
    return f"{prov['tested_at']} · commit {prov['commit']}{changes} · Sensible {prov['environment']}"
