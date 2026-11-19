"""Evidence records: the committed proof for a record-only claim, one the page doesn't run.

A record-only claim has no test markup on its page. Its section carries one comment listing the claim
IDs it covers, and each ID has a record in evidence/<page slug>/<claim_id>.json (shape:
schemas/evidence.schema.json) with the configs, documents, and responses it cites in files/ beside it.
TEST-MATRIX.md lists every record; to_sqlite() loads them into a database with one table per level of
the record, keyed by the record's own IDs.

Usage:
  codetests/evidence.py check [DIR]   validate every record (schema, file hashes, IDs, page comments)
  codetests/evidence.py stale [DAYS]  print a GitHub warning for each record whose newest run is older
                                      than DAYS (default 183); always exits 0
  codetests/evidence.py sqlite FILE   write every record to a new SQLite database
"""

import datetime
import hashlib
import json
import os
import re
import sqlite3
import sys

if __name__ == "__main__":
    sys.path[:0] = [os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".deps"),
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

import jsonschema  # noqa: E402

from codetests import markup, settings  # noqa: E402

EVIDENCE_DIR = os.path.join(settings.HERE, "evidence")
STALE_DAYS = 183
# <!-- tested claims {"ids": [...]} -->, or the MDX form, which markup.read_page converts
POINTER_RE = re.compile(r"<!--\s*tested claims\s+(\{.*?\})\s*-->", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)

# One table per level of a record. Every column is a scalar; expected and actual are JSON text.
SQLITE_TABLES = """
CREATE TABLE claims (
  claim_id TEXT PRIMARY KEY, schema_version INTEGER NOT NULL, page TEXT NOT NULL, section TEXT NOT NULL,
  claim TEXT NOT NULL, claim_kind TEXT NOT NULL, verdict TEXT NOT NULL,
  bug_summary TEXT, bug_status TEXT, bug_link TEXT,
  page_change_summary TEXT, page_change_commit TEXT, page_change_pr TEXT,
  approved_by TEXT NOT NULL, approved_on TEXT NOT NULL, notes TEXT, record_path TEXT NOT NULL
);
CREATE TABLE files (sha256 TEXT PRIMARY KEY, path TEXT NOT NULL);
CREATE TABLE runs (
  claim_id TEXT NOT NULL REFERENCES claims, run_id TEXT NOT NULL, role TEXT NOT NULL, purpose TEXT NOT NULL,
  environment TEXT NOT NULL, account TEXT NOT NULL, ran_on TEXT NOT NULL, engine_commit TEXT, engine_note TEXT NOT NULL,
  doc_type TEXT NOT NULL, extraction_id TEXT,
  config_sha256 TEXT NOT NULL REFERENCES files, document_sha256 TEXT NOT NULL REFERENCES files,
  response_sha256 TEXT REFERENCES files,
  PRIMARY KEY (claim_id, run_id)
);
CREATE TABLE run_fields (
  claim_id TEXT NOT NULL, run_id TEXT NOT NULL, field TEXT NOT NULL, expected TEXT, actual TEXT,
  PRIMARY KEY (claim_id, run_id, field), FOREIGN KEY (claim_id, run_id) REFERENCES runs
);
"""


def schema():
    with open(os.path.join(settings.SCHEMAS_DIR, "evidence.schema.json"), encoding="utf-8") as f:
        return json.load(f)


def page_slug(page):
    """Same naming as saved reports (test_matrix.slug)."""
    return re.sub(r"[^a-z0-9]+", "-", page[:-3].lower() if page.endswith(".md") else page.lower()).strip("-")


def load_all(evidence_dir=EVIDENCE_DIR):
    """[(path, record)] for every record, sorted by page, then claim ID."""
    found = []
    if not os.path.isdir(evidence_dir):
        return found
    for folder in sorted(os.listdir(evidence_dir)):
        full = os.path.join(evidence_dir, folder)
        if not os.path.isdir(full):
            continue
        for name in sorted(os.listdir(full)):
            if name.endswith(".json"):
                path = os.path.join(full, name)
                with open(path, encoding="utf-8") as f:
                    found.append((path, json.load(f)))
    return sorted(found, key=lambda pr: (pr[1].get("page", ""), pr[1].get("claim_id", "")))


def pointers(page_path):
    """{claim_id: section heading} from a page's tested-claims comments. A comment belongs to the
    nearest heading above it."""
    text = markup.read_page(page_path)
    headings = [(m.start(), m.group(2)) for m in HEADING_RE.finditer(text)]
    found = {}
    for m in POINTER_RE.finditer(text):
        ids = json.loads(m.group(1)).get("ids", [])
        section = next((h for start, h in reversed(headings) if start < m.start()), "")
        for claim_id in ids:
            found[claim_id] = section
    return found


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def files_of(record):
    """Every file a record cites, as {"path", "sha256"} objects."""
    return [run[role] for run in record["runs"] for role in ("config", "document", "response") if role in run]


def problems(path, record, repo_root=settings.REPO_ROOT, check_page=True):
    """What's wrong with one record: schema errors, a file missing or changed, a misplaced or misnamed
    file, or a page comment that doesn't list the claim in the record's section."""
    errors = [f"{e.json_path}: {e.message}" for e in jsonschema.Draft202012Validator(schema()).iter_errors(record)]
    if errors:
        return errors
    folder = os.path.dirname(path)
    if os.path.basename(path) != f"{record['claim_id']}.json":
        errors.append(f"file name isn't {record['claim_id']}.json")
    if os.path.basename(folder) != page_slug(record["page"]):
        errors.append(f"folder isn't {page_slug(record['page'])}")
    run_ids = [r["run_id"] for r in record["runs"]]
    if len(set(run_ids)) != len(run_ids):
        errors.append("run_id repeats")
    for f in files_of(record):
        full = os.path.join(folder, f["path"])
        if not os.path.isfile(full):
            errors.append(f"{f['path']} is missing")
        elif sha256(full) != f["sha256"]:
            errors.append(f"{f['path']} doesn't match its sha256")
    if check_page:
        page = os.path.join(repo_root, record["page"])
        if not os.path.isfile(page):
            errors.append(f"page {record['page']} doesn't exist")
        else:
            section = pointers(page).get(record["claim_id"])
            if section is None:
                errors.append(f"no tested-claims comment on the page lists {record['claim_id']}")
            elif section != record["section"]:
                errors.append(f"the page lists {record['claim_id']} under \"{section}\", not \"{record['section']}\"")
    return errors


def check(evidence_dir=EVIDENCE_DIR, repo_root=settings.REPO_ROOT, check_page=True):
    """{path: [problem]} for every record with a problem, plus claim IDs that repeat across records."""
    found = {}
    seen = {}
    for path, record in load_all(evidence_dir):
        errors = problems(path, record, repo_root, check_page)
        claim_id = record.get("claim_id")
        if claim_id in seen:
            errors.append(f"claim_id {claim_id} is also in {seen[claim_id]}")
        seen.setdefault(claim_id, path)
        if errors:
            found[path] = errors
    return found


def newest_run(record):
    return max(run["ran_on"] for run in record["runs"])


def stale(records, today=None, days=STALE_DAYS):
    """[(path, record)] whose newest run is more than `days` old."""
    today = today or datetime.date.today()
    limit = today - datetime.timedelta(days=days)
    return [(p, r) for p, r in records if datetime.date.fromisoformat(newest_run(r)) < limit]


def to_sqlite(records, conn, evidence_dir=EVIDENCE_DIR):
    """Load [(path, record)] into an open SQLite connection, creating the tables."""
    conn.executescript(SQLITE_TABLES)
    for path, r in records:
        bug, change, approval = r.get("bug", {}), r.get("page_change", {}), r["approval"]
        conn.execute("INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            r["claim_id"], r["schema_version"], r["page"], r["section"], r["claim"], r["claim_kind"], r["verdict"],
            bug.get("summary"), bug.get("status"), bug.get("link"),
            change.get("summary"), change.get("commit"), change.get("pr"),
            approval["by"], approval["date"], r.get("notes"), os.path.relpath(path, evidence_dir)))
        folder = os.path.relpath(os.path.dirname(path), evidence_dir)
        for f in files_of(r):
            conn.execute("INSERT OR IGNORE INTO files VALUES (?,?)", (f["sha256"], f"{folder}/{f['path']}"))
        for run in r["runs"]:
            conn.execute("INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                r["claim_id"], run["run_id"], run["role"], run["purpose"], run["environment"], run["account"],
                run["ran_on"], run["engine"].get("commit"), run["engine"]["note"], run["doc_type"],
                run.get("extraction_id"), run["config"]["sha256"], run["document"]["sha256"],
                run.get("response", {}).get("sha256")))
            for fld in run["fields"]:
                conn.execute("INSERT INTO run_fields VALUES (?,?,?,?,?)", (
                    r["claim_id"], run["run_id"], fld["field"], json.dumps(fld["expected"]), json.dumps(fld["actual"])))
    conn.commit()


def main(argv):
    command = argv[1] if len(argv) > 1 else None
    if command == "check":
        found = check(argv[2]) if len(argv) > 2 else check()
        for path, errors in found.items():
            for e in errors:
                print(f"FAIL {os.path.relpath(path, settings.REPO_ROOT)}: {e}", file=sys.stderr)
        if not found:
            print(f"PASS {len(load_all(argv[2] if len(argv) > 2 else EVIDENCE_DIR))} evidence records", file=sys.stderr)
        return 1 if found else 0
    if command == "stale":
        days = int(argv[2]) if len(argv) > 2 else STALE_DAYS
        for path, r in stale(load_all(), days=days):
            print(f"::warning file={os.path.relpath(path, settings.REPO_ROOT)}::Evidence for {r['claim_id']} is from "
                  f"{newest_run(r)}, more than {days} days ago. Rerun it, or record why it still holds.")
        return 0
    if command == "sqlite" and len(argv) > 2:
        if os.path.exists(argv[2]):
            print(f"{argv[2]} exists; give a new file", file=sys.stderr)
            return 1
        conn = sqlite3.connect(argv[2])
        to_sqlite(load_all(), conn)
        conn.close()
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
