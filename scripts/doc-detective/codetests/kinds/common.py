"""Helpers more than one claim kind uses."""

from ..errors import DOCS_MALFORMED, DOCUMENT_UNREACHABLE, CodeTestError


def require_document(test, seen, where):
    """A test that needs its own document: an <!-- inline document --> link or "from" another test."""
    if "document" not in seen:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: missing <!-- inline document --> ({where}). Only a test that compares an "
                            f"inline output can leave it out and run on a blank page")


def require_no_portfolio(test, where):
    """Portfolio parts (segment_documents_with, fixtures, portfolio inline configs) belong to "documents"."""
    if test.segment_documents_with or test.fixtures or test.inline_configs:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: \"segment_documents_with\", <!-- fixture -->, and portfolio inline configs need <!-- expect {{\"compare\": \"documents\", ...}} --> ({where})")


def check_document(client, url):
    status = client.document_status(url)
    if status != 200:
        raise CodeTestError(DOCUMENT_UNREACHABLE, f"{url} returned {status}")


def fixture_warnings(record):
    return [f"  [fixture] WARNING: {w['text']}" for w in record["warnings"] if w["source"] == "fixture"]
