"""Portfolio claim: the documents (configs and page ranges) a portfolio extraction finds.

Runs a portfolio extraction of the test's document, segmented the way the test says
("segment_documents_with", the API parameter), and compares the documents exactly. The doc types are
either private fixtures or the page's own samples, each in a sample doc type. Fingerprinting uses no
LLM, so there's no judge and no envelope.

    {/* code test {"testId": "...", "segment_documents_with": "fingerprints"} */}
    {/* inline document */}
    {/* fixture {"name": "<doc type name>"} */}     repeatable; or inline configs with "doc_type" and "config"
    {/* expect {"compare": "documents", "documents": [["<config>", firstPage, lastPage], ...]} */}
    {/* code test end */}

Pages are printed (1-based) page numbers, to match the page's prose; [] means no documents. A test of
the page's own samples can leave out "documents" and take them from its {/* inline output */}.
"""

from .. import markup, samples, settings
from ..errors import DOCS_MALFORMED, SEGMENTS_DRIFT, CodeTestError
from ..reports.parts import e, restored_note
from .common import check_document, fixture_warnings, require_document

NAME = "documents"
LABEL = "portfolio documents"
RECORD_KEY = "segments"


def parse_expect(options, test_id, where):
    return options.get("documents")  # None: take them from the inline output; check() checks them


def validate(test, seen, where):
    require_document(test, seen, where)
    if not test.segment_documents_with or bool(test.fixtures) == bool(test.inline_configs) or test.config:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: an expect with compare \"documents\" needs \"segment_documents_with\", and either fixtures "
                            f"or inline configs with \"doc_type\" and \"config\" ({where})")
    if test.fixtures and test.output:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: a fixture test takes its expected documents from expect, not an inline output ({where})")
    if test.expect is None and not test.output:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: expect has no \"documents\" and there's no <!-- inline output --> to take them from ({where})")


def check(test):
    """(None, expected documents as [[config, firstPage, lastPage], ...])."""
    where = f"{test.file}, line {test.line}"
    for sample in test.inline_configs:
        markup.parse_block(test, "config", sample["text"], sample["line"], sample["shift"], True)
    expect = test.expect
    if expect is None:
        # The page's documented response: its documents' configs and page ranges are the claim
        output = markup.parse_block(test, "output", test.output, test.output_line, 0, False)
        documents = output.get("documents") if isinstance(output, dict) else None
        if not isinstance(documents, list) or not all(isinstance(d, dict) and {"configuration", "startPage", "endPage"} <= set(d) for d in documents):
            raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: the inline output needs a \"documents\" list whose items have configuration, startPage, and endPage ({where})")
        expect = [[d["configuration"], d["startPage"] + 1, d["endPage"] + 1] for d in documents]
    if not isinstance(expect, list) or not all(
        isinstance(d, list) and len(d) == 3 and isinstance(d[0], str)
        and all(type(n) is int and n >= 1 for n in d[1:]) and d[1] <= d[2] for d in expect
    ):
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: expect's documents must be a list of [config, firstPage, lastPage] with 1-based pages, firstPage <= lastPage ({where})")
    names = {sample["config"] for sample in test.inline_configs}
    unknown = sorted({d[0] for d in expect} - names) if test.inline_configs else []
    if unknown:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: the expected documents name config {unknown[0]!r}, which no inline config has ({where})")
    for name in test.fixtures:
        markup.fixture_files(name)  # raises DOCS_MALFORMED if the fixture is missing
        markup.fixture_references(name)  # or has no reference document
    return None, expect


def _actual(documents):
    return sorted([[d.get("configuration"), d["startPage"] + 1, d["endPage"] + 1] for d in documents], key=lambda d: (d[1], d[2]))


def _compare(expected, actual, extraction_id):
    if actual != sorted(expected, key=lambda d: (d[1], d[2])):
        fmt = lambda docs: "; ".join(f"{c} pages {a}-{b}" for c, a, b in docs) or "no documents"
        raise CodeTestError(SEGMENTS_DRIFT, f"the page claims {fmt(expected)}, but Sensible returned {fmt(actual)} (extraction {extraction_id})")


def run(rec, test, client, **_):
    _, expected = check(test)
    check_document(client, test.document_url)
    if test.inline_configs:
        return _run_samples(rec, test, client, expected)
    doc_types, editors = [], []
    for name in test.fixtures:
        refs = markup.fixture_references(name)
        doc_type, config_name, restored = client.ensure_fixture(*markup.fixture_files(name), refs)
        doc_types.append(doc_type)
        editors.append({"fixture": name, "url": markup.editor_url(doc_type, config_name, refs[0]["name"])})
        rec["warnings"] += [{"source": "fixture", "text": f"{name}: {w}"} for w in restored]
    extraction_id, documents = client.extract_portfolio(test.document_url, doc_types, f"ci__{test.test_id}")
    actual = _actual(documents)
    rec["segments"] = {
        "fixtures": list(test.fixtures),
        **({"table": test.table, "row": test.row} if test.row else {}),
        "document_types": doc_types,
        "editors": editors,
        "extraction_id": extraction_id,
        "expected": expected,
        "actual": actual,
    }
    _compare(expected, actual, extraction_id)


def _run_samples(rec, test, client, expected):
    """The page's own samples: each sample's config in a sample doc type, run together as a portfolio.
    Sensible validates each config on upload, so a sample with invalid syntax fails."""
    types, editors = {}, {}
    for sample in test.inline_configs:
        name = f"{samples.prefix(test.file)}{test.test_id}__{sample['doc_type']}"
        if name not in types:
            types[name] = samples.create(client, name, sample["config"], sample["text"], test.document_url)
        else:
            client.publish_config(types[name][0], sample["config"], sample["text"])
        editors[sample["config"]] = markup.editor_url(name, sample["config"], types[name][1])
    extraction_id, documents = client.extract_portfolio(test.document_url, list(types), f"ci__{test.test_id}",
                                                        environment=settings.ENVIRONMENT)
    actual = _actual(documents)
    rec["segments"] = {
        "fixtures": [],
        "samples": [{"doc_type": s["doc_type"], "config": s["config"], "editor": editors[s["config"]]} for s in test.inline_configs],
        "document_types": list(types),
        "extraction_id": extraction_id,
        "expected": expected,
        "actual": actual,
    }
    _compare(expected, actual, extraction_id)


def sample_doc_types(test):
    base = f"{samples.prefix(test.file)}{test.test_id}"
    return list(dict.fromkeys(f"{base}__{s['doc_type']}" for s in test.inline_configs))


def probeable(test):
    return False


def shows_document(rec):
    return not rec.get("segments", {}).get("editors")  # fixture tests link each fixture to the editor, which has the document


def _fmt(docs):
    return "; ".join(f"{c} pages {s}-{e}" for c, s, e in docs) or "no documents"


def text(rec):
    seg = rec.get("segments")
    if not seg:
        return []
    lines = [f"{rec['test_id']}: portfolio segments (fingerprints, compared exactly)" + (f", table {seg.get('table')} row {seg['row']}" if seg.get("row") else "")]
    if seg.get("samples"):
        lines.append(f"  Samples: {', '.join(x['config'] for x in seg['samples'])}  (extraction {seg['extraction_id']})")
        lines += [f"  Editor: {x['editor']}" for x in seg["samples"] if x.get("editor")]
        lines.append("  (Editor links show the latest run's configs: each run deletes and recreates the sample doc types.)")
    else:
        lines.append(f"  Fixtures: {', '.join(seg['fixtures'])}  (extraction {seg['extraction_id']})")
    lines += [f"  Editor: {x['url']}" for x in seg.get("editors", [])]
    lines.append(f"  Page claims: {_fmt(seg['expected'])}")
    lines.append(f"  Sensible:    {_fmt(seg['actual'])}")
    return lines + fixture_warnings(rec)


def html(rec, links):
    seg = rec.get("segments")
    if not seg:
        return []

    def docs(items):
        return "<br>".join(f"<code>{e(c)}</code> pages {s}–{n}" for c, s, n in items) or '<span class="muted">no documents</span>'

    link = f"https://app.sensible.so/extraction/?e={seg['extraction_id']}"
    out = ["<h3>Portfolio segments</h3>"]
    if seg.get("row"):
        out.append(f'<p>Checks row <strong>{e(seg["row"])}</strong> of table <code>{e(seg.get("table", ""))}</code>.</p>')
    out.append('<p class="muted">Fingerprint claim, compared exactly: no LLM fields, so no judge and no envelope.</p>')
    out.append('<table><tr><th>Page claims</th><th>Sensible returned</th></tr>'
               f'<tr><td>{docs(seg["expected"])}</td><td>{docs(seg["actual"])}</td></tr></table>')
    editors = {x["fixture"]: x["url"] for x in seg.get("editors", [])}

    def fixture(name):
        editor = f' (<a href="{e(editors[name])}">open in the SenseML editor</a>)' if name in editors else ""
        return f"<code>{e(name)}</code>{editor}"

    if seg.get("samples"):
        def sample(x):
            editor = f' (<a href="{e(x["editor"])}">open in the SenseML editor</a>)' if x.get("editor") else ""
            return f"<code>{e(x['config'])}</code>{editor}"
        out.append(f'<p class="muted">The page\'s own samples: {", ".join(sample(x) for x in seg["samples"])}, each in its own doc type. '
                   f'Extraction: <a href="{e(link)}">{e(seg["extraction_id"])}</a> (test account).</p>')
        out.append(f'<p class="muted">{e(samples.LINKS_NOTE)}</p>')
    else:
        out.append(f'<p class="muted">Fixtures: {", ".join(fixture(x) for x in seg["fixtures"])}. '
                   f'Extraction: <a href="{e(link)}">{e(seg["extraction_id"])}</a> (test account).</p>')
    return out + restored_note(rec, ". Check whether someone edited it in the app:")


def details(test, rec):
    seg = rec.get("segments")
    if not seg:
        return f"{test.test_id}: portfolio documents"
    pages = ", ".join(f"pages {s}–{n}" for _, s, n in seg["expected"]) or "no documents"
    if seg.get("row"):
        number, _, row_id = seg["row"].partition(": ")
        return f"Row {number} ({row_id}): {pages}"
    return f"{test.test_id}: {pages}"


def checked(test, rec):
    return details(test, rec) if rec.get("segments") else ""
