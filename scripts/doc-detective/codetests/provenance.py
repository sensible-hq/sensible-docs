"""Where a test run's evidence comes from: the commit, whether the tested files had uncommitted
changes, when it ran, and against which Sensible environment. Reports and saved results carry it,
so a reader can tell whether a saved report matches the page next to it."""

import subprocess
from datetime import datetime, timezone

from . import settings

# Uncommitted changes here mean the run tested something no commit has: the page, the tooling, or test files
TESTED_PATHS = ["scripts/doc-detective", "scripts/test"]


def _git(*args):
    try:
        out = subprocess.run(["git", *args], capture_output=True, text=True, cwd=settings.REPO_ROOT, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.strip()


def provenance(page_path):
    """{"commit", "uncommitted", "tested_at", "environment"}. commit is "unknown" outside a git checkout."""
    status = _git("status", "--porcelain", "--", page_path, *TESTED_PATHS)
    return {
        "commit": _git("rev-parse", "--short=9", "HEAD") or "unknown",
        "uncommitted": bool(status),
        "tested_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "environment": settings.env(),
    }


def describe(prov):
    """One line for a report header."""
    changes = " (with uncommitted changes)" if prov["uncommitted"] else ""
    return f"{prov['tested_at']} · commit {prov['commit']}{changes} · Sensible {prov['environment']}"
