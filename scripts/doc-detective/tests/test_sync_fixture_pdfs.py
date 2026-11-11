"""Fixture copies of docs PDFs stay identical to assets/pdfs (sync_fixture_pdfs.py)."""

import os
import re
import tempfile
import unittest

import sync_fixture_pdfs as sfp


class SyncTest(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.docs, self.fixtures = os.path.join(d.name, "docs"), os.path.join(d.name, "fixtures")
        os.makedirs(self.docs)
        os.makedirs(self.fixtures)

    def write(self, folder, name, data):
        with open(os.path.join(folder, name), "wb") as f:
            f.write(data)

    def read(self, folder, name):
        with open(os.path.join(folder, name), "rb") as f:
            return f.read()

    def test_rewrites_only_drifted_namesakes(self):
        self.write(self.docs, "a.pdf", b"new")
        self.write(self.fixtures, "a.pdf", b"old")
        self.write(self.docs, "b.pdf", b"same")
        self.write(self.fixtures, "b.pdf", b"same")
        self.write(self.docs, "docs_only.pdf", b"x")
        self.write(self.fixtures, "fixture_only.pdf", b"y")
        self.assertEqual(sfp.drifted(self.docs, self.fixtures), ["a.pdf"])
        self.assertEqual(sfp.sync(self.docs, self.fixtures), ["a.pdf"])
        self.assertEqual(self.read(self.fixtures, "a.pdf"), b"new")
        self.assertEqual(self.read(self.fixtures, "fixture_only.pdf"), b"y")
        self.assertFalse(os.path.exists(os.path.join(self.fixtures, "docs_only.pdf")))
        self.assertEqual(sfp.drifted(self.docs, self.fixtures), [])

    def test_compares_bytes_not_size_or_time(self):
        self.write(self.docs, "a.pdf", b"abc")
        self.write(self.fixtures, "a.pdf", b"abd")
        self.assertEqual(sfp.drifted(self.docs, self.fixtures), ["a.pdf"])

    def test_no_fixture_folder_does_nothing(self):
        self.assertEqual(sfp.sync(self.docs, os.path.join(self.fixtures, "missing")), [])

    def test_workflow_runs_on_docs_pdf_changes_and_syncs_the_fixture_folder(self):
        path = os.path.join(sfp.REPO_ROOT, ".github", "workflows", "sync-fixture-pdfs.yml")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.assertIn('- "assets/pdfs/**"', text)
        self.assertIn(os.path.relpath(sfp.FIXTURE_DIR, sfp.REPO_ROOT), text)
        self.assertTrue(re.search(r"python3 scripts/doc-detective/sync_fixture_pdfs\.py", text))


if __name__ == "__main__":
    unittest.main()
