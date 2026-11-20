"""Standalone fingerprint claim: whether a fingerprint passes, as written and with tests broken.

In strict fingerprint mode, Sensible runs a config only if its fingerprint passes, so the extraction
completes with the config, or FAILS. Runs the page's config as written, then each variant with the
listed tests replaced by a match no document has, each in its own sample doc type. No LLM, so no
judge and no envelope.

    {/* code test {"testId": "..."} */}
    {/* inline document */}
    {/* inline config {"fragment": "fingerprint"} */}   or a whole config with a fingerprint
    {/* expect {"compare": "fingerprint", "passes": true, "variants": [{"break": [0], "passes": false}]} */}
    {/* code test end */}
"""

import copy
import json

from .. import markup, samples
from ..errors import DOCS_MALFORMED, EXTRACTION_ERROR, FINGERPRINT_DRIFT, CodeTestError
from ..reports.parts import chip, e
from .common import check_document, require_document, require_no_portfolio

NAME = "fingerprint"
LABEL = "fingerprint (strict mode)"
RECORD_KEY = "fingerprint"

# Replaces a test to break it on purpose: no document has this line
NO_MATCH = {"type": "includes", "text": "docs-ci: a line no document has"}


def parse_expect(options, test_id, where):
    variants = options.get("variants", [])
    if not isinstance(options.get("passes"), bool) or not isinstance(variants, list) or not all(
        isinstance(v, dict) and isinstance(v.get("passes"), bool) and isinstance(v.get("break"), list) and v["break"]
        and all(type(i) is int and i >= 0 for i in v["break"]) for v in variants
    ):
        raise CodeTestError(DOCS_MALFORMED, f"{test_id}: a \"fingerprint\" expect needs \"passes\": true or false, and optional \"variants\": "
                            f"[{{\"break\": [<test index>, ...], \"passes\": true or false}}] ({where})")
    return {"passes": options["passes"], "variants": variants}


def validate(test, seen, where):
    require_document(test, seen, where)
    require_no_portfolio(test, where)
    if not test.config or test.output:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: a \"fingerprint\" expect needs one <!-- inline config --> and no inline output ({where})")


def check(test):
    """(config, expect options)."""
    where = f"{test.file}, line {test.line}"
    config = markup.parse_block(test, "config", test.config, test.config_line, test.config_shift, True)
    tests = (config.get("fingerprint") or {}).get("tests") if isinstance(config, dict) else None
    if not isinstance(tests, list) or not tests:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: a \"fingerprint\" test's config needs fingerprint.tests ({where})")
    for variant in test.expect["variants"]:
        if max(variant["break"]) >= len(tests):
            raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: variant breaks test {max(variant['break'])}, but the fingerprint has {len(tests)} tests (0-based) ({where})")
    return config, test.expect


def run(rec, test, client, **_):
    config, expect = check(test)
    check_document(client, test.document_url)
    runs = []
    names = sample_doc_types(test)
    for n, variant in enumerate([{"break": [], "passes": expect["passes"]}] + expect["variants"]):
        text = test.config
        if variant["break"]:
            broken = copy.deepcopy(config)
            for i in variant["break"]:
                broken["fingerprint"]["tests"][i] = NO_MATCH
            text = json.dumps(broken, indent=2)
        name = names[n]
        _, reference = samples.create(client, name, test.test_id, text, test.document_url, {"fingerprint_mode": "strict"})
        result = client.extract_standalone(test.document_url, name, f"ci__{test.test_id}" + (f"__v{n}" if n else ""))
        if result.get("status") == "FAILED" and result.get("errors"):
            # A failing fingerprint fails with no errors; anything else is a different problem
            raise CodeTestError(EXTRACTION_ERROR, f"extraction {result.get('id')} failed: {json.dumps(result.get('errors'))[:300]}")
        passed = result.get("status") == "COMPLETE" and result.get("configuration") == test.test_id
        runs.append({"break": variant["break"], "expected": variant["passes"], "actual": passed, "extraction_id": result.get("id", ""),
                     "editor": markup.editor_url(name, test.test_id, reference)})
    rec["fingerprint"] = {"config": test.test_id, "runs": runs}
    wrong = [r for r in runs if r["actual"] != r["expected"]]
    if wrong:
        say = lambda r: ("as written" if not r["break"] else f"with tests {', '.join(map(str, r['break']))} broken") + \
            f": the page claims it {'passes' if r['expected'] else 'fails'}, but it {'passed' if r['actual'] else 'failed'} (extraction {r['extraction_id']})"
        raise CodeTestError(FINGERPRINT_DRIFT, "; ".join(say(r) for r in wrong))


def sample_doc_types(test):
    """One for the config as written, plus one per variant."""
    base = f"{samples.prefix(test.file)}{test.test_id}"
    return [base] + [f"{base}__v{n}" for n in range(1, len(test.expect["variants"]) + 1)]


def probeable(test):
    return False


def shows_document(rec):
    return True


def text(rec):
    fp = rec.get("fingerprint")
    if not fp:
        return []
    lines = [f"{rec['test_id']}: fingerprint in strict mode (compared exactly)"]
    for run in fp["runs"]:
        which = "as written" if not run["break"] else f"tests {', '.join(map(str, run['break']))} broken"
        lines.append(f"  {which}: page claims {'passes' if run['expected'] else 'fails'}; Sensible {'passed' if run['actual'] else 'failed'}  (extraction {run['extraction_id']})")
        if run.get("editor"):
            lines.append(f"    Editor: {run['editor']}")
    return lines


def html(rec, links):
    fp = rec.get("fingerprint")
    if not fp:
        return []
    out = ["<h3>Fingerprint, strict mode</h3>",
           '<p class="muted">In strict fingerprint mode, Sensible runs the config only if its fingerprint passes. '
           'Each row runs the page\'s config, as written or with tests replaced by a match no document has; '
           'the Config column opens each one in the SenseML editor. No LLM, so no judge and no envelope.</p>',
           f'<p class="muted">{e(samples.LINKS_NOTE)}</p>',
           "<table><tr><th>Config</th><th>Page claims</th><th>Sensible</th><th>Extraction</th></tr>"]
    for run in fp["runs"]:
        which = "as written" if not run["break"] else f"tests {', '.join(map(str, run['break']))} broken (0-based)"
        verdict = lambda passed: "passes" if passed else "fails"
        ok = "pass" if run["actual"] == run["expected"] else "fail"
        link = f"https://app.sensible.so/extraction/?e={run['extraction_id']}"
        config = f'<a href="{e(run["editor"])}">{e(which)}</a>' if run.get("editor") else e(which)
        out.append(f'<tr><td>{config}</td><td>{verdict(run["expected"])}</td><td>{chip(ok, verdict(run["actual"]))}</td>'
                   f'<td><a href="{e(link)}">{e(run["extraction_id"][:8])}…</a></td></tr>')
    out.append("</table>")
    return out


def details(test, rec):
    fp = rec.get("fingerprint")
    if not fp:
        return f"{test.test_id}: fingerprint"
    claims = ", ".join(("as written" if not r["break"] else f"{len(r['break'])} broken") + (" passes" if r["expected"] else " fails") for r in fp["runs"])
    return f"{test.test_id}: fingerprint {claims}"


def checked(test, rec):
    return details(test, rec) if rec.get("fingerprint") else ""
