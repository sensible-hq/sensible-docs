import os
import shutil
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import check_drift  # noqa: E402

REAL_ROOT = Path(__file__).resolve().parents[4]
VALE = os.environ.get("VALE_BIN") or shutil.which("vale") or (
    str(Path.home() / ".local/bin/vale") if (Path.home() / ".local/bin/vale").exists() else None
)
needs_vale = pytest.mark.skipif(VALE is None, reason="vale binary not installed")

PINNED = "https://github.com/errata-ai/Google/releases/download/v0.7.1/Google.zip"

VALE_INI = f"""\
StylesPath = .github/styles
MinAlertLevel = suggestion
Packages = {PINNED}

[*.md]
BasedOnStyles = Vale, Sensible
"""

RULE = """\
extends: existence
message: "Don't use '%s'."
level: warning
tokens:
  - foobar
"""

GUIDE = """\
# Rules

Intro text.

## No foobar

Do not write foobar.

- Avoid: "the foobar method"
- Prefer: "the baz method"

## Be nice

**Tone:** Be nice.

```markdown
## Not a heading, it is in a code block
```
"""

REGISTRY = {
    "guide_dir": ".claude/style-guide",
    "scan": ["rules.md"],
    "example_markers": {"fail": ["Avoid"], "pass": ["Prefer"]},
    "google": {"overrides": {}},
    "not_rules": [{"at": "rules.md#be-nice", "reason": "container"}],
    "rules": [
        {"id": "r-foobar", "at": "rules.md#no-foobar", "vale": "Sensible.NoFoobar"},
        {"id": "r-tone", "at": "rules.md#be-nice", "item": "Tone", "human": "judgment"},
    ],
}


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path):
    write(tmp_path / ".vale.ini", VALE_INI)
    write(tmp_path / ".github/styles/Sensible/NoFoobar.yml", RULE)
    write(tmp_path / ".claude/style-guide/rules.md", GUIDE)
    write(tmp_path / check_drift.FIXTURES_REL / "NoFoobar/fail.md", "Call foobar now.\n")
    write(tmp_path / check_drift.FIXTURES_REL / "NoFoobar/pass.md", "Call baz now.\n")
    save_registry(tmp_path, REGISTRY)
    return tmp_path


def save_registry(root: Path, reg: dict):
    write(root / check_drift.REGISTRY_REL, yaml.safe_dump(reg, sort_keys=False))


def load_registry(root: Path) -> dict:
    return yaml.safe_load((root / check_drift.REGISTRY_REL).read_text())


def run(root):
    problems, _ = check_drift.check(root, VALE)
    return problems


def codes(problems):
    return sorted({p.split(":", 1)[0] for p in problems})


# ---------------------------------------------------------------- pure helpers


def test_github_slug():
    assert check_drift.github_slug("Explicit subjects — avoid passive voice") == \
        "explicit-subjects--avoid-passive-voice"
    assert check_drift.github_slug("Describing the `id` parameter for methods") == \
        "describing-the-id-parameter-for-methods"
    assert check_drift.github_slug("Intro paragraph (no heading)") == "intro-paragraph-no-heading"


def test_parse_skips_code_blocks_and_finds_items(tmp_path):
    write(tmp_path / "g.md", GUIDE)
    units = check_drift.parse_guide_file(tmp_path / "g.md", "g.md")
    locs = [u.location for u in units]
    assert "g.md#no-foobar" in locs
    assert "g.md#be-nice item='Tone'" in locs
    assert not any("not-a-heading" in loc for loc in locs)


def test_table_rows_skip_header(tmp_path):
    write(tmp_path / "g.md", "## Terms\n\n| Concept | Use | Avoid |\n| --- | --- | --- |\n"
          '| App | "the app" | "the UI", "the dashboard" |\n')
    units = check_drift.parse_guide_file(tmp_path / "g.md", "g.md")
    rows = [u for u in units if u.kind == "row"]
    assert [r.key for r in rows] == ["App"]
    fails, passes = check_drift.extract_examples(rows[0], ["Avoid"], ["Prefer"], {"fail": [2], "pass": [1]})
    assert fails == ["the UI", "the dashboard"]
    assert passes == ["the app"]


def test_extract_examples_from_prose(tmp_path):
    write(tmp_path / "g.md", GUIDE)
    unit = next(u for u in check_drift.parse_guide_file(tmp_path / "g.md", "g.md")
                if u.anchor == "no-foobar")
    assert check_drift.extract_examples(unit, ["Avoid"], ["Prefer"]) == (["the foobar method"], ["the baz method"])


@pytest.mark.parametrize("pkg,pinned", [
    ("Google", False),
    ("https://github.com/errata-ai/Google/releases/latest/download/Google.zip", False),
    (PINNED, True),
])
def test_package_pinning(tmp_path, pkg, pinned):
    write(tmp_path / ".vale.ini", f"Packages = {pkg}\n")
    problems = check_drift.check_packages(check_drift.read_vale_ini(tmp_path / ".vale.ini"))
    assert (problems == []) is pinned


# ---------------------------------------------------------------- end to end


@needs_vale
def test_clean_repo_has_no_drift(repo):
    assert run(repo) == []


@needs_vale
def test_orphan_vale_rule(repo):
    write(repo / ".github/styles/Sensible/Unmapped.yml", RULE)
    problems = run(repo)
    assert "ORPHAN-VALE-RULE: Sensible.Unmapped has no registry entry" in problems


@needs_vale
def test_registry_target_missing(repo):
    reg = load_registry(repo)
    reg["rules"].append({"id": "r-ghost", "vale": "Sensible.Ghost", "basis": "x"})
    save_registry(repo, reg)
    assert any(p.startswith("MISSING-VALE-RULE: rule r-ghost") for p in run(repo))


@needs_vale
def test_dangling_anchor_after_heading_rename(repo):
    guide = repo / ".claude/style-guide/rules.md"
    guide.write_text(guide.read_text().replace("## No foobar", "## Never foobar"))
    problems = run(repo)
    assert any(p.startswith("DANGLING: rule r-foobar") for p in problems)
    assert any(p.startswith("UNMAPPED-GUIDE-RULE: rules.md#never-foobar") for p in problems)


@needs_vale
def test_dangling_item(repo):
    guide = repo / ".claude/style-guide/rules.md"
    guide.write_text(guide.read_text().replace("**Tone:**", "**Voice:**"))
    problems = run(repo)
    assert any(p.startswith("DANGLING: rule r-tone") for p in problems)


@needs_vale
def test_unmapped_guide_rule(repo):
    guide = repo / ".claude/style-guide/rules.md"
    guide.write_text(guide.read_text() + "\n## Brand new rule\n\nText.\n")
    assert codes(run(repo)) == ["UNMAPPED-GUIDE-RULE"]


@needs_vale
def test_fixture_stops_triggering(repo):
    write(repo / check_drift.FIXTURES_REL / "NoFoobar/fail.md", "Call baz now.\n")
    problems = run(repo)
    assert problems == [
        "TEST-FAIL: scripts/style_sync/fixtures/NoFoobar/fail.md should trigger Sensible.NoFoobar but does not"
    ]


@needs_vale
def test_rule_change_breaks_guide_example(repo):
    write(repo / ".github/styles/Sensible/NoFoobar.yml", RULE.replace("foobar", "quux"))
    problems = run(repo)
    assert any("example 'the foobar method' should trigger Sensible.NoFoobar" in p for p in problems)
    assert any("fixtures/NoFoobar/fail.md should trigger" in p for p in problems)


@needs_vale
def test_pass_example_that_triggers(repo):
    write(repo / check_drift.FIXTURES_REL / "NoFoobar/pass.md", "foobar\n")
    assert any("pass.md should not trigger Sensible.NoFoobar" in p for p in run(repo))


@needs_vale
def test_known_gap_silences_example(repo):
    reg = load_registry(repo)
    guide = repo / ".claude/style-guide/rules.md"
    guide.write_text(guide.read_text().replace('- Avoid: "the foobar method"',
                                               '- Avoid: "the foobar method", "the fubar method"'))
    assert any("'the fubar method'" in p for p in run(repo))
    reg["rules"][0]["known_gaps"] = ["the fubar method"]
    save_registry(repo, reg)
    assert run(repo) == []


@needs_vale
def test_missing_tests(repo):
    shutil.rmtree(repo / check_drift.FIXTURES_REL)
    guide = repo / ".claude/style-guide/rules.md"
    guide.write_text(guide.read_text().replace('- Prefer: "the baz method"\n', ""))
    problems = run(repo)
    assert any(p.startswith("NO-TESTS: Sensible.NoFoobar has no pass test") for p in problems)
    assert not any("has no fail test" in p for p in problems)


@needs_vale
def test_orphan_fixture(repo):
    write(repo / check_drift.FIXTURES_REL / "Gone/fail.md", "x\n")
    assert any(p.startswith("ORPHAN-FIXTURE") for p in run(repo))


@needs_vale
def test_disabled_target(repo):
    write(repo / ".vale.ini", VALE_INI + "Sensible.NoFoobar = NO\n")
    assert any(p.startswith("DISABLED-VALE-RULE") for p in run(repo))


@needs_vale
def test_agent_only_rule_is_off_in_vale_ini_and_still_tested(repo):
    reg = load_registry(repo)
    reg["agent_only_rules"] = ["Sensible.NoFoobar"]
    save_registry(repo, reg)
    write(repo / ".vale.ini", VALE_INI + "Sensible.NoFoobar = NO\n")
    assert run(repo) == []
    # its fixtures still run, with the rule enabled explicitly
    write(repo / check_drift.FIXTURES_REL / "NoFoobar/pass.md", "Call foobar now.\n")
    assert codes(run(repo)) == ["TEST-FAIL"]


@needs_vale
def test_agent_only_rule_enabled_in_vale_ini(repo):
    reg = load_registry(repo)
    reg["agent_only_rules"] = ["Sensible.NoFoobar"]
    save_registry(repo, reg)
    assert codes(run(repo)) == ["AGENT-ONLY-ENABLED"]


@needs_vale
def test_agent_only_rule_missing(repo):
    reg = load_registry(repo)
    reg["agent_only_rules"] = ["Sensible.Nope"]
    save_registry(repo, reg)
    write(repo / ".vale.ini", VALE_INI + "Sensible.NoFoobar = NO\n")
    assert any(p.startswith("MISSING-VALE-RULE: agent_only_rules") for p in run(repo))


@needs_vale
def test_entry_needs_exactly_one_enforcement(repo):
    reg = load_registry(repo)
    reg["rules"][1]["none-yet"] = ""
    save_registry(repo, reg)
    assert any(p.startswith("SCHEMA: rule r-tone: needs exactly one") for p in run(repo))


@needs_vale
def test_google_override_mismatch_and_unpinned(repo):
    write(repo / ".vale.ini", VALE_INI.replace(PINNED, "Google") + "Google.Colons = NO\n")
    problems = run(repo)
    assert any(p.startswith("UNPINNED-PACKAGE") for p in problems)
    assert any(p.startswith("GOOGLE-OVERRIDES: .vale.ini has Google.Colons = NO") for p in problems)


@needs_vale
def test_main_exit_codes_and_report(repo, tmp_path, capsys):
    report = tmp_path / "report.md"
    args = ["--root", str(repo), "--vale", VALE, "--report-md", str(report)]
    assert check_drift.main(args) == 0
    assert "**Problems:** 0" in report.read_text()

    write(repo / ".github/styles/Sensible/Unmapped.yml", RULE)
    assert check_drift.main(args) == 1
    out = capsys.readouterr().out
    assert "ORPHAN-VALE-RULE: Sensible.Unmapped" in out
    assert "ORPHAN-VALE-RULE: Sensible.Unmapped" in report.read_text()


def test_main_reports_missing_vale(repo):
    assert check_drift.main(["--root", str(repo), "--vale", str(repo / "no-such-vale")]) == 2


@needs_vale
def test_real_registry_is_well_formed():
    """The checked-in registry has no schema errors or broken mappings.

    Content drift (TEST-FAIL, UNPINNED-PACKAGE, DANGLING, ...) is what the
    weekly job reports, so it is not asserted here.
    """
    problems, stats = check_drift.check(REAL_ROOT, VALE)
    assert [p for p in problems if p.startswith(("SCHEMA", "MISSING-VALE-RULE", "ORPHAN"))] == []
    assert stats["entries"] > 0


def test_review_table_is_current():
    import review_table
    assert review_table.main(["review_table.py", "--check"]) == 0, "run scripts/style_sync/review_table.py"
