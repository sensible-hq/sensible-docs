"""What a run's evidence records about the tree it tested (codetests/provenance.py)."""

import os
import subprocess
import tempfile
import unittest

import plan_runs
from codetests import provenance, settings


class ProvenanceTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        root = self.dir.name
        saved = settings.REPO_ROOT
        settings.REPO_ROOT = root
        self.addCleanup(setattr, settings, "REPO_ROOT", saved)
        for args in (["init", "-q"], ["config", "user.email", "t@example.test"], ["config", "user.name", "t"]):
            subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
        self.write("docs/a.md", "page")
        self.write("scripts/doc-detective/run.sh", "run")
        subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "c"], cwd=root, check=True, capture_output=True)

    def write(self, path, text):
        full = os.path.join(self.dir.name, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(text)

    def test_clean_tree(self):
        prov = provenance.provenance("docs/a.md")
        self.assertFalse(prov["uncommitted"])
        self.assertEqual(len(prov["commit"]), 9)

    def test_saved_evidence_doesnt_count_as_uncommitted(self):
        self.write("scripts/doc-detective/reports/docs-a.html", "<html>")
        self.write("scripts/doc-detective/TEST-MATRIX.md", "# matrix")
        self.assertFalse(provenance.provenance("docs/a.md")["uncommitted"])

    def test_edited_page_or_tooling_counts(self):
        self.write("docs/a.md", "edited")
        self.assertTrue(provenance.provenance("docs/a.md")["uncommitted"])

    def test_for_run_computes_once_per_page(self):
        output = os.path.join(self.dir.name, "out")
        first = provenance.for_run(output, "docs/a.md")
        self.write("docs/a.md", "edited after the report was written")
        self.assertEqual(provenance.for_run(output, "docs/a.md"), first)
        # Another page's run recomputes: the page edited above now counts as uncommitted
        import json
        provenance.for_run(output, "docs/b.md")
        with open(os.path.join(output, provenance.FILE)) as f:
            self.assertEqual(json.load(f)["page"], "docs/b.md")

    def test_excludes_match_the_planners(self):
        self.assertEqual({p + "/**" if not p.endswith(".md") else p for p in provenance.NOT_TESTED}, set(plan_runs.NOT_TOOLING))
