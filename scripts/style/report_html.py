"""Standalone HTML reports for the style tooling, in the doc tests' house style.

The CSS and the chip and escape helpers come from scripts/doc-detective/codetests/reports/, so a
change to the doc test report's look reaches these reports too. They're read from the files rather
than imported as a package, because the package pulls in the doc tests' dependencies (jsonschema).
"""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "scripts/doc-detective/codetests/reports"


def _css() -> str:
    # A regex, not ast: html.py uses Python 3.12 f-string syntax, and CI's style tests run 3.11
    m = re.search(r'^CSS = """(.*?)"""', (REPORTS / "html.py").read_text(), re.S | re.M)
    if not m:
        raise RuntimeError("no CSS constant in scripts/doc-detective/codetests/reports/html.py")
    return m.group(1)


def _parts():
    spec = importlib.util.spec_from_file_location("doc_tests_report_parts", REPORTS / "parts.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CSS = _css()
_p = _parts()
JUDGE, chip, e = _p.JUDGE, _p.chip, _p.e

__all__ = ["CSS", "JUDGE", "chip", "e", "page", "table", "card", "write"]

TOOLBAR_JS = ("<script>document.querySelectorAll('.toolbar button').forEach(function(b){b.addEventListener('click',function(){"
              "document.querySelectorAll('details.test').forEach(function(d){d.open=b.dataset.open==='1';});});});</script>")


def table(headers: list[str], rows: list[list[str]]) -> str:
    """An HTML table. Cells are HTML already: escape text with e() before passing it."""
    head = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{head}</tr>{body}</table>"


def card(title: str, body: str, note: str = "", open_: bool | None = None, badge: str = "") -> str:
    """A section card. With open_ set, the card is a collapsible <details> that starts open or closed.
    badge is HTML shown after the title, such as JUDGE for sections an LLM decided."""
    sub = f'<p class="sub" style="margin:4px 0 12px">{note}</p>' if note else ""
    head = e(title) + (f" {badge}" if badge else "")
    if open_ is None:
        return f'<section class="card"><h2>{head}</h2>{sub}{body}</section>'
    return (f'<details class="test card"{" open" if open_ else ""}><summary><h2 style="display:inline">{head}</h2>'
            f"</summary>{sub}{body}</details>")


def page(title: str, subtitle: str, sections: list[str], status: tuple[str, str] | None = None) -> str:
    chip_html = chip(*status) if status else ""
    toolbar = ('<div class="toolbar"><button type="button" data-open="1">Expand all</button>'
               '<button type="button" data-open="0">Collapse all</button></div>')
    return "\n".join([
        "<!doctype html><html lang=en><head><meta charset=utf-8>",
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{e(title)}</title><style>{CSS}</style></head><body><main>",
        f'<div class="row"><h1>{e(title)}</h1>{chip_html}</div>',
        f'<p class="sub">{e(subtitle)}</p>',
        toolbar, *sections, TOOLBAR_JS, "</main></body></html>"])


def write(path: Path, html_text: str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")
    return path
