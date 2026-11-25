import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import metrics as M  # noqa: E402

CLAUDE = "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"


# ---------- pure logic ----------

@pytest.mark.parametrize("text, expected", [
    ("see https://github.com/sensible-hq/sensible/pull/3519", [("sensible", 3519)]),
    ("sensible-hq/sensible-app#120 and sensible#7", [("sensible", 7), ("sensible-app", 120)]),
    ("sensible-docs#12 is not backend", []),
    ("closes #812", []),
    ("sensible#1 sensible#1", [("sensible", 1)]),
    ("doc: thing (sensible#3519, #3533)", [("sensible", 3519), ("sensible", 3533)]),
    ("Based on sensible-hq/sensible#3190, #3237, and #3240.",
     [("sensible", 3190), ("sensible", 3237), ("sensible", 3240)]),
    ("Run `/update-docs-from-pr 3235 3220`", [("sensible", 3220), ("sensible", 3235)]),
    ("sensible#5 fixes docs #812", [("sensible", 5)]),
])
def test_backend_refs(text, expected):
    assert M.backend_refs(text) == expected


@pytest.mark.parametrize("path, expected", [
    ("docs/Senseml reference/ocr.md", True),
    ("reference/extraction.json", True),
    ("reference/extraction/post-extract.md", False),
    ("reference/sub/x.json", False),
    ("assets/images/final/x.png", False),
    (".claude/sessions/x/checklist.md", False),
    ("docs/_order.yaml", False),
])
def test_is_doc_file(path, expected):
    assert M.is_doc_file(path) is expected


def test_is_claude_commit():
    assert M.is_claude_commit("Fix thing" + CLAUDE)
    assert M.is_claude_commit("x\n\nco-authored-by: claude <a@b>")
    assert not M.is_claude_commit("Update conditional.md")
    assert not M.is_claude_commit("Mention Co-Authored-By: Claude in prose")


def c(sha, claude, docs=True):
    return {"sha": sha, "claude": claude, "doc_files": ["docs/a.md"] if docs else [], "doc_lines": 1}


def test_draft_is_first_doc_commit_only():
    # Later Claude commits are revisions (often dictated), never part of the draft.
    commits = [c("0", True, docs=False), c("1", True), c("2", True), c("3", False)]
    assert M.draft_commit(commits) == "1"


def test_no_draft_when_first_doc_commit_is_human():
    assert M.draft_commit([c("1", False), c("2", True), c("3", True)]) is None


def test_no_draft_without_doc_commits():
    assert M.draft_commit([c("1", True, docs=False)]) is None


def test_post_draft_commits_counts_doc_commits_only():
    commits = [c("1", True), c("2", False, docs=False), c("3", False), c("4", True)]
    assert M.post_draft_commits(commits, "1") == 2
    assert M.post_draft_commits(commits, None) == 0


def test_survival_multiset_and_whitespace():
    draft = {"docs/a.md": ["The same sentence twice.", "  The same sentence twice.",
                           "A sentence to be reworded.", "", "A sentence that moves."]}
    net = {"docs/a.md": ["A sentence that moves.", "The same sentence twice.", "A reworded sentence."]}
    # one copy survives (only one in net), blank ignored, the moved line survives
    assert M.survival(draft, net) == (2, 4)


def test_survival_ignores_trivial_lines():
    draft = {"docs/a.md": ["```", "| --- | --- |", "}", "A real sentence of content."]}
    assert M.survival(draft, {"docs/a.md": ["```", "| --- | --- |", "}"]}) == (0, 1)


def test_survival_does_not_count_lines_already_on_the_page():
    # The net diff doesn't add this line (it was already in the file), so it can't survive.
    draft = {"docs/a.md": ['    "type": "string",']}
    assert M.survival(draft, {"docs/a.md": []}) == (0, 1)


def test_word_survival_counts_reworded_words_not_rows():
    draft = {"docs/a.md": ["| thorough | Claude 5.5 Sonnet |"]}
    net = {"docs/a.md": ["| thorough | Claude Sonnet 5.5 |"]}
    kept, total = M.word_survival(draft, net)
    assert total == 7 and kept == 6
    assert M.survival(draft, net) == (0, 1)


def test_word_survival_missing_file():
    assert M.word_survival({"docs/a.md": ["two words"]}, {}) == (0, 2)


def test_survival_deleted_file():
    assert M.survival({"docs/a.md": ["Content that got cut."]}, {}) == (0, 1)


def test_pooled_weights_by_size():
    rows = [M.PRMetrics(1, "t", "after", "", "", "", doc_lines=10, revision_lines=10),
            M.PRMetrics(2, "t", "after", "", "", "", doc_lines=90, revision_lines=0),
            M.PRMetrics(3, "t", "after", "", "", "", doc_lines=50, revision_lines=None)]
    assert M.pooled(rows, "revision_lines", "doc_lines") == 10.0
    assert M.pooled([], "revision_lines", "doc_lines") is None


def test_fix_overlap_ignores_trivial_lines():
    added = {"docs/a.md": ["| --- | --- |", "```", "The default value is 10 pages."]}
    deleted = {"docs/a.md": ["| --- | --- |", "```", "The default value is 10 pages."],
               "docs/b.md": ["The default value is 10 pages."]}
    assert M.fix_overlap(added, deleted) == 1


def test_period_and_per100():
    cut = datetime(2026, 10, 27, tzinfo=timezone.utc)
    assert M.period(datetime(2026, 10, 26, tzinfo=timezone.utc), cut) == "before"
    assert M.period(cut, cut) == "after"
    assert M.per100(3, 150) == 2.0
    assert M.per100(3, 0) is None
    assert M.per100(None, 10) is None


def test_parse_diff_filters_doc_files_and_handles_new_and_deleted():
    diff = "\n".join([
        "diff --git a/docs/a.md b/docs/a.md", "--- a/docs/a.md", "+++ b/docs/a.md",
        "@@ -1 +1 @@", "-old", "+new",
        "diff --git a/docs/new.md b/docs/new.md", "--- /dev/null", "+++ b/docs/new.md",
        "@@ -0,0 +1 @@", "+fresh",
        "diff --git a/scripts/x.py b/scripts/x.py", "--- a/scripts/x.py", "+++ b/scripts/x.py",
        "@@ -1 +1 @@", "-a", "+b",
        "diff --git a/docs/gone.md b/docs/gone.md", "--- a/docs/gone.md", "+++ /dev/null",
        "@@ -1 +0,0 @@", "-bye",
    ])
    added, deleted = M.parse_diff(diff)
    assert added == {"docs/a.md": ["new"], "docs/new.md": ["fresh"]}
    assert deleted == {"docs/a.md": ["old"], "docs/gone.md": ["bye"]}


def test_report_flags_small_samples():
    rows = [M.PRMetrics(1, "t", "before", "2026-01-01", "2026-01-02", "sensible#1", doc_lines=10),
            M.PRMetrics(2, "t", "after", "2026-11-01", "2026-11-02", "sensible#2", doc_lines=20,
                        fix_window="open")]
    out = M.render_report(rows, "tag", datetime(2026, 10, 27, tzinfo=timezone.utc), excluded=[9])
    assert "Small sample" in out
    assert "| #2 | after |" in out
    assert "0, open" in out
    assert "change no doc files: #9" in out


# ---------- end to end on a throwaway repo ----------

def sh(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def commit(repo, files, msg):
    for path, text in files.items():
        p = repo / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    sh(repo, "add", "-A")
    sh(repo, "commit", "-q", "-m", msg)
    return sh(repo, "rev-parse", "HEAD")


class FakeGitHub:
    def backend_merged_at(self, repo, number):
        return "2026-11-01T00:00:00Z"


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    sh(r, "init", "-q", "-b", "v0")
    sh(r, "config", "user.email", "t@t")
    sh(r, "config", "user.name", "t")
    commit(r, {"docs/a.md": "# A\n\nExisting intro paragraph stays.\n"}, "base")
    return r


def test_measure_pr_end_to_end(repo, monkeypatch):
    sh(repo, "checkout", "-q", "-b", "feat")
    commit(repo, {"docs/a.md": "# A\n\nExisting intro paragraph stays.\n"
                               "The new parameter defaults to five pages.\n"
                               "It applies to every document type.\n"
                               "A sentence the human will rewrite.\n"}, "draft" + CLAUDE)
    commit(repo, {"scripts/t.py": "x\n"}, "test script" + CLAUDE)
    commit(repo, {"docs/a.md": "# A\n\nExisting intro paragraph stays.\n"
                               "The new parameter defaults to five pages.\n"
                               "It applies to every document type.\n"
                               "The human rewrote this sentence.\n"}, "copy edit")
    head = commit(repo, {"docs/a.md": "# A\n\nExisting intro paragraph stays.\n"
                                      "The new parameter defaults to ten pages.\n"
                                      "It applies to every document type.\n"
                                      "The human rewrote this sentence.\n"}, "fix default" + CLAUDE)
    sh(repo, "checkout", "-q", "v0")
    sh(repo, "merge", "-q", "--squash", "feat")
    sh(repo, "commit", "-q", "-m", "Feature (#10)")
    merge = sh(repo, "rev-parse", "HEAD")
    fix = commit(repo, {"docs/a.md": "# A\n\nExisting intro paragraph stays.\n"
                                     "The new parameter defaults to ten pages.\n"
                                     "It applies to PDFs only.\n"
                                     "The human rewrote this sentence.\n"}, "Fix scope (#11)")

    git = M.Git(repo)
    monkeypatch.setattr(git, "fetch_pr", lambda n: head)
    pr = {"number": 10, "title": "doc: param (sensible#5)", "body": "",
          "createdAt": "2026-11-02T00:00:00Z", "mergedAt": "2026-11-03T00:00:00Z",
          "mergeCommit": {"oid": merge}}
    m = M.measure_pr(git, FakeGitHub(), pr, datetime(2026, 10, 27, tzinfo=timezone.utc))

    assert m.period == "after"
    assert m.backend == "sensible#5"
    assert m.doc_lines == 3          # three lines added to docs/a.md, net
    assert m.new_pages == 0
    assert m.commits == 4
    assert m.human_commits == 1
    assert m.human_doc_lines == 2    # one line replaced
    assert m.draft_lines == 3
    assert m.post_draft_commits == 2
    # 19 draft words; lost: "five", and all of the rewritten sentence but "human"
    assert (m.draft_words_kept, m.draft_words) == (13, 19)
    assert m.revision_lines == 4         # human rewrite (2) + dictated fix (2)
    assert m.revision_lines_claude == 2
    assert m.draft_survival == pytest.approx(0.333, abs=0.001)  # only "every document type" survived
    assert m.lag_days == 2.0

    later = {"number": 11, "title": "", "body": "", "createdAt": "2026-11-04T00:00:00Z",
             "mergedAt": "2026-11-05T00:00:00Z", "mergeCommit": {"oid": fix}}
    M.attach_fixes(git, [m], [pr, later], now=datetime(2026, 11, 6, tzinfo=timezone.utc))
    assert m.fixes == 1
    assert m.fix_prs == "#11"
    assert m.fix_window == "open"
