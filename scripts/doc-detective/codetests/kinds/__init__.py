"""Claim kinds: what a code test claims about Sensible, and how to check it. One module per kind.

A code test's kind is its {/* expect {"compare": "<kind>"} */} (no expect: "output", the page's
documented output). Everything that differs by kind lives in its module, so adding a kind is a new
module, its record section's schema (schemas/kinds/<kind>.schema.json), and one line in KINDS below.
markup.py, runner.py, record.py, the reports, and test_matrix.py look the kind up here instead of
branching on it. tests/test_kinds.py registers a made-up kind to check that nothing else is needed.

Each module defines:

  NAME                         the kind, as written in "compare" and saved in each record's "kind"
  LABEL                        what TEST-MATRIX.md calls it
  RECORD_KEY                   the record section it fills, shaped by schemas/kinds/<NAME>.schema.json;
                               None for a kind whose fields are the record's own ("output")
  parse_expect(options, test_id, where)
                               the expect marker's options, checked; becomes test.expect. Raise
                               DOCS_MALFORMED for bad options ("output" has no expect marker)
  validate(test, seen, where)  the markup rules for the whole test: which markers it needs and allows
                               (`seen` is the set of marker roles in it). Raise DOCS_MALFORMED
  check(test)                  parse and check what the test runs, before any network call: returns
                               (config, expected), or raises DOCS_MALFORMED with the page line
  run(rec, test, client, **options)
                               run the test, fill the record's section, and raise CodeTestError on a
                               failed claim. `options` are the judge settings, which only "output" uses
  sample_doc_types(test)       the doc types in the test account named for this test, which persist
                               until its next run ([] if none); cleanup keeps these and deletes the rest
  probeable(test)              whether --probe-blank can rerun it on a blank page
  shows_document(rec)          whether report.html shows the example document's link above the section
  text(rec)                    the plain-text summary lines for the section
  html(rec, links)             report.html's section, as a list of HTML strings. `links` is a
                               reports.html.Links: repo-relative paths as links from the report
  details(test, rec)           report.html's link text for the test: what it checked, unique to the test
  checked(test, rec)           the CI summary's "Checked" cell
"""

from . import classification, documents, fingerprint, output

KINDS = {kind.NAME: kind for kind in (output, documents, fingerprint, classification)}
# The values an expect marker's "compare" can take: every kind but the default
COMPARES = tuple(name for name in KINDS if name != output.NAME)


def of(test):
    """The kind module of a markup.CodeTest."""
    return KINDS[test.compare or output.NAME]


def of_record(rec):
    """The kind module of a code-test record."""
    return KINDS[rec["kind"]]
