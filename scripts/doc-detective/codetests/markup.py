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

Test IDs must be unique across both kinds of test on a page.
"""

import json
import re
from dataclasses import dataclass, field

from . import jsonish
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

    for marker in MARKER_RE.finditer(text):
        if not any(start <= marker.start() < end for start, end in code_spans):
            raise CodeTestError(DOCS_MALFORMED, f"{path}, line {_line(text, marker.start())}: <!-- example {marker.group(1)} --> is outside any <!-- code test -->")

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
