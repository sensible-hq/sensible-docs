"""Read a docs page's test markup: Doc Detective UI tests and code tests.

UI tests use Doc Detective's own syntax, and Doc Detective runs them:

    <!-- test {"testId": "app_document_types_page", "description": "..."} -->
    <!-- step {...} -->
    <!-- test end -->

Code tests use their own wrapper, and code_tests.py runs them. Inside it, markers point at the
example's parts:

    <!-- code test {"testId": "extract_auto_insurance_anyco", "description": "..."} -->
    <!-- example document -->                       the next line's link is the example document
    <!-- example document {"from": "<testId>"} -->  or reuse another code test's document
    <!-- example config -->                         the next code block is the config
    <!-- example config {"fragment": "field"} -->   or a one-field excerpt, run wrapped in {"fields": [...]}
    <!-- example output -->                         the next code block is the documented output
    <!-- code test end -->

For claims about portfolio segmentation (fingerprints), a code test can run committed fixtures
instead of a code block, and compare page ranges instead of parsed_document:

    <!-- code test {"testId": "...", "description": "...", "segment": "fingerprints"} -->
    <!-- example document -->
    <!-- example config {"fixture": "<dir>/<doctype>"} -->   a doc type and its config, from the test fixtures; repeatable
    <!-- example output {"compare": "documents", "expect": [["<config>", firstPage, lastPage], ...]} -->
    <!-- code test end -->

Pages in `expect` are printed (1-based) page numbers, to match the page's prose; [] means no documents.

A table of claims gets one tag, and one table test checks it, with a row entry for each of its rows
(like a Doc Detective test and its steps). The table itself has no markers, so it reads as usual:

    <!-- table {"tableId": "portfolio_failures"} -->
    | ... | ... |
    <!-- table test {"testId": "portfolio_failures_tests", "table": "portfolio_failures", "segment": "fingerprints"} -->
    <!-- example document -->                       or {"from": "<testId>"}
    <!-- row {"rowId": "last_test_fails", "config": {"fixture": "<dir>/<doctype>"}, "expect": [...]} -->
    <!-- table test end -->

The tag and the test must name each other, and the test needs one row entry per table row, in the
table's order: adding or deleting a row without updating the test fails the run. Row content isn't
compared; the tag is the hint that the table and the test change together.

Test IDs must be unique across both kinds of test on a page.
"""

import json
import re
from dataclasses import dataclass, field

from . import jsonish, settings
from .errors import DOCS_MALFORMED, CodeTestError

UI_TEST_RE = re.compile(r"<!--\s*test\s+(\{.*?\})\s*-->(.*?)<!--\s*test end\s*-->", re.S)
CODE_TEST_RE = re.compile(r"<!--\s*code test\s+(\{.*?\})\s*-->(.*?)<!--\s*code test end\s*-->", re.S)
STEP_RE = re.compile(r"<!--\s*step\s+\{")
MARKER_RE = re.compile(r"<!--\s*example\s+(config|document|output)\s*(\{.*?\})?\s*-->", re.S)
FENCE_RE = re.compile(r"\s*```[a-zA-Z0-9]*\n(.*?)\n```", re.S)
# First Markdown link on the next non-blank line, for example the example document's download link
LINK_RE = re.compile(r"\s*[^\n]*?\]\((https?://[^)\s]+)\)")
TEST_ID_RE = re.compile(r"^[a-z0-9_]+$")


@dataclass
class UiTest:
    test_id: str
    description: str
    line: int
    steps: int = 0  # <!-- step --> comments, so a report can tell when Doc Detective skipped one


@dataclass
class CodeTest:
    test_id: str
    description: str
    file: str
    line: int
    config: str = ""  # the text uploaded to Sensible
    config_line: int = 0  # line before the block's first line
    output: str = ""
    output_line: int = 0
    output_span: tuple = (0, 0)  # character offsets of the output block's text in the page
    document_url: str = ""
    document_from: str = ""  # another code test whose document this one reuses
    fragment: bool = False  # the config is a one-field excerpt, wrapped for the run
    segment: str = ""  # "fingerprints": a portfolio extraction that segments with fingerprints
    fixtures: list = field(default_factory=list)  # "<dir>/<doctype>" names from settings.TEST_FIXTURES_DIR
    compare: str = ""  # "documents": compare portfolio page ranges with `expect`, not parsed_document
    expect: object = None
    table: str = ""  # the tagged table this test's row belongs to
    row: str = ""  # "<n>: <rowId>", the row of that table this test checks


@dataclass
class Page:
    path: str
    ui_tests: list = field(default_factory=list)
    code_tests: dict = field(default_factory=dict)  # test ID -> CodeTest, in page order


def _line(text, offset):
    return text.count("\n", 0, offset) + 1


def _test_header(text, match, path, kind):
    line = _line(text, match.start())
    try:
        header = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        raise CodeTestError(DOCS_MALFORMED, f"{path}, line {line}: the {kind} comment isn't valid JSON ({e.msg})")
    test_id = header.get("testId", "")
    if not TEST_ID_RE.match(test_id):
        raise CodeTestError(DOCS_MALFORMED, f"{path}, line {line}: testId {test_id!r} must be lowercase letters, digits, and underscores")
    return test_id, header.get("description", ""), line


def wrap_field_fragment(text):
    """Turn a one-field excerpt ("{ ... },") into a runnable config, keeping comments and layout."""
    body = text.rstrip()
    if body.endswith(","):
        body = body[:-1]
    return '{\n  "fields": [\n' + body + "\n  ]\n}"


def _code_test(text, match, path):
    test_id, description, line = _test_header(text, match, path, "code test")
    test = CodeTest(test_id, description, path, line)
    header = json.loads(match.group(1))
    test.segment = header.get("segment", "")
    if test.segment not in ("", "fingerprints"):
        raise CodeTestError(DOCS_MALFORMED, f"{test_id}: unknown segment {test.segment!r}; use \"fingerprints\" ({path}, line {line})")
    body, offset = match.group(2), match.start(2)
    seen = set()
    for marker in MARKER_RE.finditer(body):
        role = marker.group(1)
        options = json.loads(marker.group(2)) if marker.group(2) else {}
        seen.add(role)
        where = f"{path}, line {_line(text, offset + marker.start())}"
        if role == "document":
            if options.get("from"):
                test.document_from = options["from"]
                continue
            link = LINK_RE.match(body, marker.end())
            if not link:
                raise CodeTestError(DOCS_MALFORMED, f"{test_id}: <!-- example document --> isn't followed by a line with a link ({where})")
            test.document_url = link.group(1)
            continue
        if role == "config" and "fixture" in options:
            test.fixtures.append(options["fixture"])
            continue
        if role == "output" and "compare" in options:
            if options["compare"] != "documents":
                raise CodeTestError(DOCS_MALFORMED, f"{test_id}: unknown compare {options['compare']!r}; use \"documents\" ({where})")
            test.compare, test.expect = options["compare"], options.get("expect")
            continue
        fence = FENCE_RE.match(body, marker.end())
        if not fence:
            raise CodeTestError(DOCS_MALFORMED, f"{test_id}: <!-- example {role} --> isn't followed by a code block ({where})")
        start = offset + fence.start(1)
        if role == "config":
            fragment = options.get("fragment")
            if fragment not in (None, "field"):
                raise CodeTestError(DOCS_MALFORMED, f"{test_id}: unknown config fragment {fragment!r}; use \"field\" ({where})")
            test.fragment = fragment == "field"
            test.config = wrap_field_fragment(fence.group(1)) if test.fragment else fence.group(1)
            test.config_line = text.count("\n", 0, start)
        else:
            test.output = fence.group(1)
            test.output_line = text.count("\n", 0, start)
            test.output_span = (start, offset + fence.end(1))
    missing = {"config", "document", "output"} - seen
    if test.compare == "documents" and (test.segment != "fingerprints" or not test.fixtures or test.config):
        raise CodeTestError(DOCS_MALFORMED, f"{test_id}: compare \"documents\" needs \"segment\": \"fingerprints\" and fixture configs only ({path}, line {line})")
    if missing:
        raise CodeTestError(DOCS_MALFORMED, f"{test_id}: missing <!-- example {'/'.join(sorted(missing))} --> ({path}, line {line})")
    return test


def parse_page(path):
    """Read a page's UI tests and code tests, and check the markup rules."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    page = Page(path)
    ids = {}  # test ID -> line where it's first defined

    def claim(test_id, line):
        if test_id in ids:
            raise CodeTestError(DOCS_MALFORMED, f"{path}: testId {test_id!r} is used on line {ids[test_id]} and line {line}; test IDs must be unique on a page")
        ids[test_id] = line

    for match in UI_TEST_RE.finditer(text):
        test_id, description, line = _test_header(text, match, path, "test")
        if MARKER_RE.search(match.group(2)):
            raise CodeTestError(DOCS_MALFORMED, f"{path}, line {line}: {test_id} has <!-- example ... --> markers inside a Doc Detective <!-- test -->; wrap a code test in <!-- code test --> instead")
        claim(test_id, line)
        page.ui_tests.append(UiTest(test_id, description, line, len(STEP_RE.findall(match.group(2)))))

    code_spans = []
    for match in CODE_TEST_RE.finditer(text):
        test = _code_test(text, match, path)
        claim(test.test_id, test.line)
        page.code_tests[test.test_id] = test
        code_spans.append((match.start(), match.end()))

    code_spans += [(m.start(), m.end()) for m in TABLE_TEST_RE.finditer(text)]
    for marker in MARKER_RE.finditer(text):
        if not any(start <= marker.start() < end for start, end in code_spans):
            raise CodeTestError(DOCS_MALFORMED, f"{path}, line {_line(text, marker.start())}: <!-- example {marker.group(1)} --> is outside any <!-- code test -->")

    _table_tests(text, path, page, claim)

    for test in page.code_tests.values():
        if test.document_from:
            source = page.code_tests.get(test.document_from)
            if not source or not source.document_url:
                raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: <!-- example document {{\"from\": \"{test.document_from}\"}} --> names no code test with its own document link")
            test.document_url = source.document_url
    return page


def check_syntax(test):
    """Return (config, documented output) parsed, or raise DOCS_MALFORMED with the doc line of the problem.

    Configs may have comments and trailing commas (Sensible accepts them). Output blocks may have
    comments and `...`, but not trailing commas (Sensible never outputs them).
    """
    if test.compare == "documents":
        expect = test.expect
        if not isinstance(expect, list) or not all(
            isinstance(d, list) and len(d) == 3 and isinstance(d[0], str) and all(isinstance(n, int) and n >= 1 for n in d[1:]) for d in expect
        ):
            raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: expect must be a list of [config, firstPage, lastPage] with 1-based pages ({test.file}, line {test.line})")
        for name in test.fixtures:
            fixture_files(name)  # raises DOCS_MALFORMED if the fixture is missing
            fixture_references(name)  # or has no reference document
        return None, expect
    parsed = {}
    for role, text, line, trailing_commas in (("config", test.config, test.config_line, True), ("output", test.output, test.output_line, False)):
        try:
            parsed[role] = jsonish.parse_block(text, trailing_commas)
        except jsonish.SyntaxIssue as e:
            # A wrapped field fragment has 2 lines of wrapper above the doc's text
            shift = -2 if role == "config" and test.fragment else 0
            where = f"line {line + e.line + shift}" if e.line else f"{role} block at line {line}"
            raise CodeTestError(DOCS_MALFORMED, f"{role} block: {e} ({test.file}, {where})")
    return parsed["config"], parsed["output"]


def fixture_files(name):
    """The doc type file and the single config file of fixture "<dir>/<doctype>"."""
    import glob
    import os

    directory, _, doctype = name.rpartition("/")
    base = os.path.join(settings.TEST_FIXTURES_DIR, directory)
    doctype_file = os.path.join(base, f"{doctype}.doctype.json")
    configs = glob.glob(os.path.join(base, f"{glob.escape(doctype)}.*.config.json"))
    if not directory or not os.path.exists(doctype_file) or len(configs) != 1:
        raise CodeTestError(DOCS_MALFORMED, f"fixture {name!r}: expected {os.path.relpath(doctype_file, settings.REPO_ROOT)} and exactly one {doctype}.<config>.config.json beside it")
    config = os.path.basename(configs[0])[len(doctype) + 1:-len(".config.json")]
    # Fixtures live in the shared test account; the prefix marks them so nobody deletes them in the app by accident
    if not doctype.startswith(settings.FIXTURE_PREFIX) or not config.startswith(settings.FIXTURE_PREFIX):
        raise CodeTestError(DOCS_MALFORMED, f"fixture {name!r}: the doc type and config names must start with {settings.FIXTURE_PREFIX!r} (found {doctype!r}, {config!r})")
    return doctype_file, configs[0]


def fixture_references(name):
    """The reference documents of fixture "<dir>/<doctype>", from <dir>/manifest.json.

    Every fixture doc type needs at least one, so it can be opened in the SenseML editor. Each is
    {"name", "pdf" (repo-relative), "configuration"}, in the contract-test manifest's shape."""
    import os

    directory, _, doctype = name.rpartition("/")
    _, config_file = fixture_files(name)
    config = os.path.basename(config_file)[len(doctype) + 1:-len(".config.json")]
    manifest_file = os.path.join(settings.TEST_FIXTURES_DIR, directory, "manifest.json")
    try:
        with open(manifest_file, encoding="utf-8") as f:
            manifest = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise CodeTestError(DOCS_MALFORMED, f"fixture {name!r}: can't read {os.path.relpath(manifest_file, settings.REPO_ROOT)} ({e})")
    entry = next((d for d in manifest.get("document_types", []) if d.get("doctype") == f"{doctype}.doctype.json"), None)
    refs = (entry or {}).get("references") or []
    if not refs:
        raise CodeTestError(DOCS_MALFORMED, f"fixture {name!r}: needs at least one reference document in {os.path.relpath(manifest_file, settings.REPO_ROOT)}, so it can be opened in the SenseML editor")
    for ref in refs:
        if not ref.get("name", "").startswith(settings.FIXTURE_PREFIX):
            raise CodeTestError(DOCS_MALFORMED, f"fixture {name!r}: reference document {ref.get('name')!r} must start with {settings.FIXTURE_PREFIX!r}")
        if ref.get("configuration") != config:
            raise CodeTestError(DOCS_MALFORMED, f"fixture {name!r}: reference document {ref['name']!r} must use config {config!r}, not {ref.get('configuration')!r}")
        if not os.path.exists(os.path.join(settings.REPO_ROOT, ref.get("pdf", ""))):
            raise CodeTestError(DOCS_MALFORMED, f"fixture {name!r}: reference document PDF {ref.get('pdf')!r} doesn't exist")
    return refs


def editor_url(doctype, config, reference):
    """The SenseML editor, opened on a fixture's config and reference document."""
    from urllib.parse import urlencode

    return "https://app.sensible.so/editor/?" + urlencode({"d": doctype, "c": config, "g": reference})


TABLE_TAG_RE = re.compile(r"<!--\s*table\s+(\{.*?\})\s*-->", re.S)
TABLE_TEST_RE = re.compile(r"<!--\s*table test\s+(\{.*?\})\s*-->(.*?)<!--\s*table test end\s*-->", re.S)
ROW_RE = re.compile(r"<!--\s*row\s+(\{.*?\})\s*-->", re.S)
TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")


def _table_rows(text, tag_end):
    """Number of data rows in the Markdown table that follows a table tag."""
    lines = text[tag_end:].split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i + 1 >= len(lines) or not TABLE_LINE_RE.match(lines[i]) or not set(lines[i + 1].replace("|", "").strip()) <= set("-: ") or not lines[i + 1].strip():
        return None
    rows = 0
    for line in lines[i + 2:]:
        if not TABLE_LINE_RE.match(line):
            break
        rows += 1
    return rows


def _json(text, where, kind):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise CodeTestError(DOCS_MALFORMED, f"{where}: the {kind} comment isn't valid JSON ({e.msg})")


def _table_tests(text, path, page, claim):
    """Read table tags and table tests; expand each row entry into a CodeTest."""
    tables = {}
    for tag in TABLE_TAG_RE.finditer(text):
        where = f"{path}, line {_line(text, tag.start())}"
        table_id = _json(tag.group(1), where, "table").get("tableId", "")
        if not TEST_ID_RE.match(table_id):
            raise CodeTestError(DOCS_MALFORMED, f"{where}: tableId {table_id!r} must be lowercase letters, digits, and underscores")
        if table_id in tables:
            raise CodeTestError(DOCS_MALFORMED, f"{where}: tableId {table_id!r} is used twice")
        rows = _table_rows(text, tag.end())
        if rows is None:
            raise CodeTestError(DOCS_MALFORMED, f"{where}: <!-- table {{\"tableId\": \"{table_id}\"}} --> isn't followed by a Markdown table")
        tables[table_id] = rows

    tested = set()
    for match in TABLE_TEST_RE.finditer(text):
        test_id, description, line = _test_header(text, match, path, "table test")
        header = json.loads(match.group(1))
        where = f"{path}, line {line}"
        table_id = header.get("table", "")
        if table_id not in tables:
            raise CodeTestError(DOCS_MALFORMED, f"{test_id}: no <!-- table {{\"tableId\": \"{table_id}\"}} --> on the page ({where})")
        if table_id in tested:
            raise CodeTestError(DOCS_MALFORMED, f"{test_id}: table {table_id!r} already has a table test ({where})")
        tested.add(table_id)
        body, offset = match.group(2), match.start(2)
        document = MARKER_RE.search(body)
        if not document or document.group(1) != "document":
            raise CodeTestError(DOCS_MALFORMED, f"{test_id}: a table test needs <!-- example document --> before its rows ({where})")
        options = json.loads(document.group(2)) if document.group(2) else {}
        document_url, document_from = "", options.get("from", "")
        if not document_from:
            link = LINK_RE.match(body, document.end())
            if not link:
                raise CodeTestError(DOCS_MALFORMED, f"{test_id}: <!-- example document --> isn't followed by a line with a link ({where})")
            document_url = link.group(1)
        entries = list(ROW_RE.finditer(body))
        if len(entries) != tables[table_id]:
            raise CodeTestError(DOCS_MALFORMED, f"{test_id}: table {table_id!r} has {tables[table_id]} row(s) but its test has {len(entries)} row entr{'y' if len(entries) == 1 else 'ies'}. Add or remove row entries so there's one per table row, in the table's order ({where})")
        for n, entry in enumerate(entries, start=1):
            entry_where = f"{path}, line {_line(text, offset + entry.start())}"
            row = _json(entry.group(1), entry_where, "row")
            row_id = row.get("rowId", "")
            if not TEST_ID_RE.match(row_id):
                raise CodeTestError(DOCS_MALFORMED, f"{test_id}: rowId {row_id!r} must be lowercase letters, digits, and underscores ({entry_where})")
            config = row.get("config") or {}
            if "fixture" not in config:
                raise CodeTestError(DOCS_MALFORMED, f"{test_id}: row {row_id} needs \"config\": {{\"fixture\": \"<dir>/<doctype>\"}} ({entry_where})")
            test = CodeTest(f"{test_id}__{row_id}", f"{description} (row {n}: {row_id})" if description else f"row {n}: {row_id}",
                            path, _line(text, offset + entry.start()))
            test.segment = header.get("segment", "")
            test.fixtures = [config["fixture"]]
            test.compare, test.expect = row.get("compare", "documents"), row.get("expect")
            test.document_url, test.document_from = document_url, document_from
            test.table, test.row = table_id, f"{n}: {row_id}"
            if test.compare != "documents" or test.segment != "fingerprints":
                raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: table test rows support \"segment\": \"fingerprints\" with compare \"documents\" ({entry_where})")
            claim(test.test_id, test.line)
            page.code_tests[test.test_id] = test

    untested = sorted(set(tables) - tested)
    if untested:
        raise CodeTestError(DOCS_MALFORMED, f"{path}: tagged table(s) without a table test: {', '.join(untested)}")
