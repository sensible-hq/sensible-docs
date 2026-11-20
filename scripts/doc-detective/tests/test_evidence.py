"""Evidence records (codetests/evidence.py): validation, page comments, staleness, the matrix, SQLite."""

import copy
import datetime
import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
import unittest

import test_matrix
from codetests import evidence, markup

PAGE = """# Parameters

| key | value | description |
| --- | --- | --- |
| ocrIfMissing | Match | If Sensible doesn't find the text, it OCRs every page. |

{/* tested claims {"ids": ["ocr_if_missing_every_page"]} */}

# Examples

<!-- tested claims {"ids": ["ocr_if_missing_example"]} -->
"""

CONFIG = b'{"fields": []}'
DOCUMENT = b"%PDF-1.4 fake"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def record(page, claim_id="ocr_if_missing_every_page", section="Parameters", ran_on="2026-11-19"):
    return {
        "schema_version": 1,
        "claim_id": claim_id,
        "docs_pr": 825,
        "page": page,
        "section": section,
        "claim": "If Sensible doesn't find the text, it OCRs every page.",
        "claim_kind": "scope and order",
        "verdict": "holds_with_bug",
        "bug": {"summary": "Also OCRs pages Page Range excluded", "status": "not_reported"},
        "runs": [
            {"run_id": "test", "role": "test", "purpose": "the claim", "environment": "production", "account": "docs_test",
             "ran_on": ran_on, "engine": {"note": "accepts ocrIfMissing"}, "doc_type": "claims_t2_test",
             "extraction_id": "a2c51a98-98cc-457e-b42e-ce4331199c04",
             "config": {"path": "files/config.json", "sha256": digest(CONFIG)},
             "document": {"path": "files/doc.pdf", "sha256": digest(DOCUMENT)},
             "fields": [{"field": "total_premium", "expected": 6109, "actual": 6109},
                        {"field": "agency_ref", "expected": None, "actual": None}]},
            {"run_id": "control", "role": "control", "purpose": "no preprocessor", "environment": "production",
             "account": "docs_test", "ran_on": "2026-11-01", "engine": {"note": "accepts ocrIfMissing"},
             "doc_type": "claims_t2_ctrl", "config": {"path": "files/config.json", "sha256": digest(CONFIG)},
             "document": {"path": "files/doc.pdf", "sha256": digest(DOCUMENT)},
             "fields": [{"field": "total_premium", "expected": None, "actual": None}]},
        ],
        "approval": {"by": "Frances Elliott", "date": "2026-11-19"},
    }


class EvidenceTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        self.page = "docs/ocr-preprocessor.md"
        os.makedirs(os.path.join(self.root, "docs"))
        with open(os.path.join(self.root, self.page), "w", encoding="utf-8") as f:
            f.write(PAGE)
        self.dir = os.path.join(self.root, "testable-claims")
        self.folder = os.path.join(self.dir, "pr-825-ocr-if-missing")
        os.makedirs(os.path.join(self.folder, "files"))
        for name, data in (("config.json", CONFIG), ("doc.pdf", DOCUMENT)):
            with open(os.path.join(self.folder, "files", name), "wb") as f:
                f.write(data)

    def save(self, rec, name=None):
        path = os.path.join(self.folder, name or f"{rec['claim_id']}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rec, f)
        return path

    def check(self):
        return evidence.check(self.dir, repo_root=self.root)

    def test_a_good_record_passes(self):
        self.save(record(self.page))
        self.assertEqual(self.check(), {})

    def test_pointer_comments_belong_to_the_heading_above_in_either_comment_form(self):
        self.assertEqual(evidence.pointers(os.path.join(self.root, self.page)),
                         {"ocr_if_missing_every_page": "Parameters", "ocr_if_missing_example": "Examples"})

    def test_runners_ignore_the_pointer_comment(self):
        page = markup.parse_page(os.path.join(self.root, self.page))
        self.assertEqual((page.ui_tests, page.code_tests), ([], {}))

    def test_schema_errors_are_reported(self):
        bad = record(self.page)
        bad["verdict"] = "probably"
        del bad["approval"]
        self.save(bad)
        errors = next(iter(self.check().values()))
        self.assertTrue(any("verdict" in e for e in errors))
        self.assertTrue(any("approval" in e for e in errors))

    def test_a_changed_file_fails_its_hash(self):
        self.save(record(self.page))
        with open(os.path.join(self.folder, "files", "doc.pdf"), "ab") as f:
            f.write(b"edited")
        self.assertIn("files/doc.pdf doesn't match its sha256", next(iter(self.check().values())))

    def test_the_page_must_list_the_claim_in_its_section(self):
        self.save(record(self.page, section="Examples"))
        self.save(record(self.page, claim_id="not_on_page"))
        found = {os.path.basename(p): e for p, e in self.check().items()}
        self.assertEqual(found["ocr_if_missing_every_page.json"], ['the page lists ocr_if_missing_every_page under "Parameters", not "Examples"'])
        self.assertEqual(found["not_on_page.json"], ["no tested-claims comment on the page lists not_on_page"])

    def test_file_name_must_be_the_claim_id(self):
        self.save(record(self.page), name="other.json")
        self.assertIn("file name isn't ocr_if_missing_every_page.json", next(iter(self.check().values())))

    def test_folder_is_the_docs_pr_then_the_feature(self):
        for bad in ("pr-825", "pr-900-ocr-if-missing", "pr-825_ocr", "PR-825-ocr"):
            folder = os.path.join(self.dir, bad)
            shutil.copytree(os.path.join(self.folder, "files"), os.path.join(folder, "files"))
            path = os.path.join(folder, "ocr_if_missing_every_page.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(record(self.page), f)
            self.assertTrue(any("isn't pr-825-<feature>" in e for e in self.check()[path]), bad)
            shutil.rmtree(folder)

    def test_one_folder_per_pr(self):
        self.save(record(self.page))
        folder = os.path.join(self.dir, "pr-825-other")
        shutil.copytree(os.path.join(self.folder, "files"), os.path.join(folder, "files"))
        path = os.path.join(folder, "ocr_if_missing_example.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record(self.page, claim_id="ocr_if_missing_example", section="Examples"), f)
        self.assertIn("docs PR #825 also has records in pr-825-ocr-if-missing; one folder per PR", self.check()[path])

    def test_one_pr_folder_can_hold_several_pages(self):
        other_page = "docs/other.md"
        with open(os.path.join(self.root, other_page), "w", encoding="utf-8") as f:
            f.write('# Other\n\n<!-- tested claims {"ids": ["other_claim"]} -->\n')
        self.save(record(self.page))
        self.save(dict(record(other_page, claim_id="other_claim", section="Other")))
        self.assertEqual(self.check(), {})

    def test_stale_uses_the_newest_run(self):
        # "recent" has one old run and one recent one; "old" has only old runs
        recent = record(self.page, ran_on="2026-01-01")
        old = copy.deepcopy(recent)
        old["runs"][1]["ran_on"] = "2026-02-01"
        found = evidence.stale([("recent", recent), ("old", old)], today=datetime.date(2026, 11, 19))
        self.assertEqual([p for p, _ in found], ["old"])

    def test_matrix_lists_each_record(self):
        self.save(record(self.page))
        rows = [l for l in test_matrix.evidence_rows(self.dir) if l.startswith("| #")]
        self.assertEqual(len(rows), 1)
        self.assertIn("| #825 | ocr-preprocessor.md | Parameters | `ocr_if_missing_every_page` | scope and order |", rows[0])
        self.assertIn("| holds with bug | 2026-11-19, 2 runs, production (docs test account), [record](", rows[0])

    def test_matrix_says_when_there_are_none(self):
        self.assertEqual(test_matrix.evidence_rows(self.dir)[-1], "None yet.")

    def test_every_record_loads_into_sqlite_with_one_row_per_level(self):
        first = record(self.page)
        second = copy.deepcopy(first)
        second["claim_id"], second["section"] = "ocr_if_missing_example", "Examples"
        second["page_change"] = {"summary": "Reworded the row", "commit": "c8c5ede36"}
        self.save(first)
        self.save(second)
        self.assertEqual(self.check(), {})
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON")
        evidence.to_sqlite(evidence.load_all(self.dir), conn, self.dir)
        count = lambda t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        self.assertEqual((count("claims"), count("runs"), count("run_fields"), count("files")), (2, 4, 6, 2))
        # expected and actual keep their JSON types, null included
        self.assertEqual(conn.execute("SELECT expected, actual FROM run_fields WHERE run_id='test' AND field='agency_ref' AND claim_id=?",
                                      (first["claim_id"],)).fetchone(), ("null", "null"))
        self.assertEqual(conn.execute("SELECT page_change_commit FROM claims WHERE claim_id='ocr_if_missing_example'").fetchone(), ("c8c5ede36",))
        self.assertEqual(conn.execute("PRAGMA foreign_key_check").fetchall(), [])


class RealRecordsTest(unittest.TestCase):
    def test_every_committed_record_passes(self):
        self.assertEqual(evidence.check(), {})


if __name__ == "__main__":
    unittest.main()
