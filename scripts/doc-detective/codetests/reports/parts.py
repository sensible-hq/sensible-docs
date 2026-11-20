"""HTML building blocks shared by report.html and the claim kinds' report sections (codetests/kinds/)."""

import html
import json

STATUS_CHIP = {"pass": ("pass", "Passed"), "warn": ("warn", "Passed with warnings"), "fail": ("fail", "Failed"), "not run": ("fail", "Not run")}
VERDICT_CHIP = {"pass": "pass", "warn": "warn", "fail": "fail", "error": "fail"}
JUDGE = '<span class="chip judge" title="Probabilistic: decided by an LLM judge">judge</span>'
ENVELOPE = '<span class="chip envelope" title="Compared with a baseline of earlier runs">envelope</span>'


def e(value):
    return html.escape(str(value))


def j(value):
    return e(json.dumps(value, ensure_ascii=False))


def chip(status, text=None):
    css, default = STATUS_CHIP.get(status, ("info", status))
    return f'<span class="chip {css}">{e(text or default)}</span>'


def restored_note(record, detail=":"):
    """The warning a test shows when the runner restored a fixture the test account didn't match."""
    restored = [w["text"] for w in record.get("warnings", []) if w["source"] == "fixture"]
    if not restored:
        return []
    return ['<p><span class="chip warn">fixture restored</span> The test account didn\'t match the committed fixture, '
            f'so the runner restored it before the run{detail}</p><ul>', *[f"<li><code>{e(r)}</code></li>" for r in restored], "</ul>"]
