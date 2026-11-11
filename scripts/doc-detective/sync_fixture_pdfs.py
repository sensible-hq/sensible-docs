#!/usr/bin/env python3
"""Keep fixture copies of docs PDFs identical to the docs PDFs.

Fixture reference documents live in scripts/test/fixture_pdfs/, apart from assets/pdfs/, which holds only
PDFs the docs show. When a fixture uses a docs PDF, the fixture folder has a copy with the same file name,
and assets/pdfs/ is the source of truth: this script rewrites any copy whose bytes differ.

Usage:
  sync_fixture_pdfs.py           rewrite drifted copies, and print each one
  sync_fixture_pdfs.py --check   only report them; exit 1 if any differ

.github/workflows/sync-fixture-pdfs.yml runs it when a push to v0 changes assets/pdfs/, and opens or
updates a PR with the rewritten copies. Does nothing if the fixture folder doesn't exist.
"""

import argparse
import os
import shutil
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS_DIR = os.path.join(REPO_ROOT, "assets", "pdfs")
FIXTURE_DIR = os.path.join(REPO_ROOT, "scripts", "test", "fixture_pdfs")


def drifted(docs_dir=DOCS_DIR, fixture_dir=FIXTURE_DIR):
    """File names in both folders whose bytes differ, sorted."""
    if not os.path.isdir(fixture_dir) or not os.path.isdir(docs_dir):
        return []
    names = sorted(set(os.listdir(fixture_dir)) & set(os.listdir(docs_dir)))
    return [n for n in names if os.path.isfile(os.path.join(docs_dir, n))
            and _read(os.path.join(docs_dir, n)) != _read(os.path.join(fixture_dir, n))]


def _read(path):
    # Bytes, not filecmp: filecmp caches by size and modification time, so a same-size file rewritten
    # within the same timestamp tick would still compare as different
    with open(path, "rb") as f:
        return f.read()


def sync(docs_dir=DOCS_DIR, fixture_dir=FIXTURE_DIR):
    """Copy each drifted docs PDF over its fixture copy. Returns the names it rewrote."""
    names = drifted(docs_dir, fixture_dir)
    for name in names:
        shutil.copyfile(os.path.join(docs_dir, name), os.path.join(fixture_dir, name))
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="Report drifted copies without rewriting them; exit 1 if any")
    args = parser.parse_args()
    names = drifted() if args.check else sync()
    rel = os.path.relpath(FIXTURE_DIR, REPO_ROOT)
    for name in names:
        print(f"{'DRIFT' if args.check else 'SYNCED'} {rel}/{name} from assets/pdfs/{name}")
    if args.check and names:
        print(f"{len(names)} fixture PDF(s) differ from assets/pdfs. Run: python3 scripts/doc-detective/sync_fixture_pdfs.py", file=sys.stderr)
        return 1
    if not names:
        print(f"PASS every PDF in {rel} that has a namesake in assets/pdfs matches it", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
