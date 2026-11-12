"""Classification claim: which files Sensible classifies, sent with which content types.

Sends each file to the classify endpoint with its content type, restricted to the test's fixture doc
type, and checks whether Sensible classified it as that doc type. The fixture's description is what
Sensible classifies by. No extraction, no LLM judge (classification is the product's own LLM call; its
answer is the claim), no envelope.

    <!-- code test {"testId": "classify_...", "description": "..."} -->
    <!-- fixture {"name": "<doc type name>"} -->
    <!-- expect {"compare": "classification", "requests": [
        {"file": "<file in the fixture's folder>" or "docs_pdf": "<file name in assets/pdfs>",
         "as": "xlsx", "classified": true or false}, ...]} -->
    <!-- code test end -->

Each request gives its content type as `as`, a file extension that stands for that extension's MIME
type (settings.REFERENCE_CONTENT_TYPES), or as `content_type`, the MIME type itself, for one with no
extension there. `label` (optional) names the request in reports.
"""

import json
import os
import shlex

from .. import markup, settings
from ..errors import CLASSIFICATION_DRIFT, DOCS_MALFORMED, CodeTestError
from ..reports.parts import chip, e, restored_note
from .common import fixture_warnings

NAME = "classification"
LABEL = "classification"
RECORD_KEY = "classification"


# `as`: a short name for a request's content type, the file extension it belongs to
CONTENT_TYPE_NAMES = {ext.lstrip("."): mime for ext, mime in settings.REFERENCE_CONTENT_TYPES.items()}


def _content_type(r):
    """A request's MIME type, from `as` or `content_type` (exactly one), or None if neither is valid."""
    if ("as" in r) == ("content_type" in r):
        return None
    if "as" in r:
        return CONTENT_TYPE_NAMES.get(r["as"]) if isinstance(r["as"], str) else None
    return r["content_type"] if isinstance(r["content_type"], str) and r["content_type"] else None


def parse_expect(options, test_id, where):
    requests = options.get("requests")
    if set(options) - {"compare", "requests"} or not isinstance(requests, list) or not requests or not all(
        isinstance(r, dict) and sum(k in r for k in markup.DOCUMENT_KEYS) == 1 and _content_type(r)
        and isinstance(r.get("classified"), bool) and isinstance(r.get("label", ""), str)
        and set(r) <= {*markup.DOCUMENT_KEYS, "as", "content_type", "classified", "label"}
        for r in requests
    ):
        raise CodeTestError(DOCS_MALFORMED, f"{test_id}: a \"classification\" expect needs only \"requests\": "
                            f"[{{\"file\": \"<file in the fixture's folder>\" or \"docs_pdf\": \"<file name in assets/pdfs>\", "
                            f"\"as\": one of {', '.join(CONTENT_TYPE_NAMES)} (or \"content_type\": \"<MIME type>\"), "
                            f"\"classified\": true or false, \"label\": \"...\" (optional)}}] ({where})")
    # Expand `as`, so the rest of the run (the request, the curl command, the report) sees the MIME type
    return {"requests": [{**{k: v for k, v in r.items() if k != "as"}, "content_type": _content_type(r)} for r in requests]}


def validate(test, seen, where):
    if seen - {"expect", "fixture"} or test.segment_documents_with or len(test.fixtures) != 1:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: a \"classification\" expect needs exactly one <!-- fixture --> (the doc type to classify as) "
                            f"and sends the files in its requests, so the test takes no inline document, config, output, or segment_documents_with ({where})")


def check(test):
    where = f"{test.file}, line {test.line}"
    folder = markup.fixture_dir(test.fixtures[0])  # raises DOCS_MALFORMED if the fixture is missing
    for request in test.expect["requests"]:
        try:
            markup.document_path(request, folder)
        except ValueError as e:
            raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: request {e} ({where})")
    markup.fixture_files(test.fixtures[0])
    markup.fixture_references(test.fixtures[0])  # or has no reference document
    return None, test.expect


def curl_command(path, doc_type, content_type, file):
    """The request a classification run sends, as a curl command to run from the repo root. Every value
    from the page is shell-quoted; the key stays an environment variable, never its value."""
    from urllib.parse import urlencode

    url = f"{settings.api()}{path}?{urlencode({'document_types': doc_type})}"
    return (f"curl -s -w '\\nHTTP %{{http_code}}\\n' -X POST {shlex.quote(url)} "
            f'-H "Authorization: Bearer ${settings.sensible_key_var()}" '
            f"-H {shlex.quote('Content-Type: ' + content_type)} --data-binary {shlex.quote('@' + file)}")


def run(rec, test, client, **_):
    _, expect = check(test)
    name = test.fixtures[0]
    refs = markup.fixture_references(name)
    doctype_file, config_file = markup.fixture_files(name)
    doc_type, config_name, restored = client.ensure_fixture(doctype_file, config_file, refs)
    rec["warnings"] += [{"source": "fixture", "text": f"{name}: {w}"} for w in restored]
    with open(doctype_file, encoding="utf-8") as f:
        description = (json.load(f).get("schema") or {}).get("description", "")
    runs = []
    folder = markup.fixture_dir(name)
    for request in expect["requests"]:
        path = markup.document_path(request, folder)
        file = os.path.relpath(path, settings.REPO_ROOT)  # repo-relative, for the record, the curl, and report links
        status, text, got = client.classify(path, request["content_type"], doc_type)
        runs.append({
            "file": file, "content_type": request["content_type"], "label": request.get("label", ""),
            "expected": request["classified"], "actual": got == doc_type, "http_status": status,
            "response": settings.redact(" ".join(text.split()))[:300],
            "curl": curl_command("/classify", doc_type, request["content_type"], file),
        })
    rec["classification"] = {
        "fixture": name, "editor": markup.editor_url(doc_type, config_name, refs[0]["name"]),
        "doc_type_description": description, "runs": runs,
    }
    wrong = [r for r in runs if r["actual"] != r["expected"]]
    if wrong:
        say = lambda r: (f"{r['file']} sent as {r['content_type']}: the page claims Sensible "
                         f"{'classifies' if r['expected'] else 'does not classify'} it, but it "
                         f"{'did' if r['actual'] else 'did not'} (HTTP {r['http_status']}: {r['response'][:120]})")
        raise CodeTestError(CLASSIFICATION_DRIFT, "; ".join(say(r) for r in wrong))


def sample_doc_types(test):
    return []


def probeable(test):
    return False


def shows_document(rec):
    return False  # the files it sends are in the section's table


def text(rec):
    cl = rec.get("classification")
    if not cl:
        return []
    lines = [f"{rec['test_id']}: classification (compared exactly), fixture {cl['fixture']}", f"  Editor: {cl['editor']}"]
    for run in cl["runs"]:
        label = f" ({run['label']})" if run["label"] else ""
        lines.append(f"  {run['file']} as {run['content_type']}{label}: page claims {'classified' if run['expected'] else 'not classified'}; "
                     f"Sensible {'classified' if run['actual'] else 'not classified'}  (HTTP {run['http_status']})")
        lines.append(f"    $ {run['curl']}")
    return lines + fixture_warnings(rec)


def html(rec, links):
    cl = rec.get("classification")
    if not cl:
        return []
    out = ["<h3>Classification</h3>",
           f'<p>Each row sends a file to the classify endpoint with a content type, restricted to the fixture doc type '
           f'<code>{e(cl["fixture"])}</code> (<a href="{e(cl["editor"])}">open in the SenseML editor</a>, test account). '
           f'Sensible classifies by its description: <em>{e(cl["doc_type_description"])}</em></p>',
           '<p class="muted">Compared exactly: Sensible\'s answer is the claim, so no judge and no envelope. '
           'File links are relative to this report, so they open from a local checkout. Run the curl commands from the repo root.</p>',
           "<table><tr><th>File</th><th>Sent as</th><th>Page claims</th><th>Sensible</th><th>Response</th></tr>"]
    for run in cl["runs"]:
        verdict = lambda yes: "classified" if yes else "not classified"
        ok = "pass" if run["actual"] == run["expected"] else "fail"
        label = f'<br><span class="muted">{e(run["label"])}</span>' if run["label"] else ""
        link = f'<a href="{e(links.repo(run["file"]))}"><code>{e(os.path.basename(run["file"]))}</code></a>'
        out.append(f'<tr><td>{link}{label}</td><td><code>{e(run["content_type"])}</code></td>'
                   f'<td>{verdict(run["expected"])}</td><td>{chip(ok, verdict(run["actual"]))}</td>'
                   f'<td><span class="muted">HTTP {run["http_status"]}</span><br><code>{e(run["response"][:160])}</code></td></tr>')
        out.append(f'<tr><td colspan="5"><pre>{e(run["curl"])}</pre></td></tr>')
    out.append("</table>")
    return out + restored_note(rec)


def details(test, rec):
    cl = rec.get("classification")
    if not cl:
        return f"{test.test_id}: classification"
    yes = sum(r["expected"] for r in cl["runs"])
    return f"{test.test_id}: classification, {yes} classified and {len(cl['runs']) - yes} not"


def checked(test, rec):
    return details(test, rec) if rec.get("classification") else ""
