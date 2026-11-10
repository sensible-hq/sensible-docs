"""The Sensible client's fixture and portfolio logic, against a scripted stand-in for the API."""

import json
import os
import tempfile
import unittest
from unittest import mock

from codetests import sensible, settings
from codetests.errors import CodeTestError


class Response:
    def __init__(self, status=200, body=None):
        self.status_code, self.body = status, body
        self.ok = status < 400
        self.text = body if isinstance(body, str) else json.dumps(body)

    def json(self):
        if isinstance(self.body, str):
            raise json.JSONDecodeError("Expecting value", self.body, 0)
        return self.body

    def raise_for_status(self):
        if not self.ok:
            raise RuntimeError(f"HTTP {self.status_code}")


class ScriptedClient(sensible.SensibleClient):
    """Answers _api calls from `routes`, {"METHOD path": Response or [Responses, in order]}, and records them."""

    def __init__(self, routes):
        super().__init__("key")
        self.routes, self.calls = routes, []

    def _api(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs.get("json")))
        answer = self.routes[f"{method} {path.split('?')[0]}"]
        if isinstance(answer, list):
            answer = answer.pop(0) if len(answer) > 1 else answer[0]
        if isinstance(answer, Exception):
            raise answer
        return answer


@mock.patch("time.sleep", lambda s: None)
class ExtractPortfolioTest(unittest.TestCase):
    def client(self, *polls):
        return ScriptedClient({"POST /extract_from_url": Response(200, {"id": "e1"}), "GET /documents/e1": list(polls)})

    def test_returns_the_documents(self):
        docs = [{"configuration": "fixture_c", "startPage": 0, "endPage": 7}]
        client = self.client(Response(200, {"status": "PROCESSING"}), Response(200, {"status": "COMPLETE", "documents": docs}))
        self.assertEqual(client.extract_portfolio("u", ["fixture_d"], "n"), ("e1", docs))
        self.assertEqual(client.counts["extractions"], 1)

    def test_no_documents_is_a_result(self):
        client = self.client(Response(200, {"status": "COMPLETE", "documents": []}))
        self.assertEqual(client.extract_portfolio("u", ["fixture_d"], "n"), ("e1", []))

    def test_errors_or_a_missing_documents_list_fail(self):
        # Either would otherwise read as "no documents" and pass a row that expects none
        for body in ({"status": "COMPLETE", "documents": [], "errors": [{"message": "boom"}]}, {"status": "COMPLETE"}):
            with self.assertRaises(CodeTestError, msg=body) as caught:
                self.client(Response(200, body)).extract_portfolio("u", ["fixture_d"], "n")
            self.assertEqual(caught.exception.category, "EXTRACTION_ERROR")

    def test_transient_poll_errors_are_retried(self):
        import requests
        client = self.client(Response(502, "<html>bad gateway</html>"), requests.ConnectionError("reset"),
                             Response(200, {"status": "COMPLETE", "documents": []}))
        self.assertEqual(client.extract_portfolio("u", ["fixture_d"], "n"), ("e1", []))

    def test_extractions_are_capped_per_run(self):
        client = self.client(Response(200, {"status": "COMPLETE", "documents": []}))
        with mock.patch.dict(os.environ, {settings.MAX_EXTRACTIONS_VAR: "1"}):
            client.extract_portfolio("u", ["fixture_d"], "n")
            with self.assertRaises(CodeTestError) as caught:
                client.extract_portfolio("u", ["fixture_d"], "n")
        self.assertIn("per-run cap is 1", str(caught.exception))
        self.assertEqual(sum(1 for c in client.calls if c[0] == "POST"), 1)


class FixtureTest(unittest.TestCase):
    """ensure_fixture against a test account whose published config drifted from the committed one."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.doctype_file = os.path.join(self.dir.name, "fixture_d.doctype.json")
        self.config_file = os.path.join(self.dir.name, "fixture_d.fixture_c.config.json")
        with open(self.doctype_file, "w") as f:
            json.dump({"name": "fixture_d", "schema": {}}, f)
        with open(self.config_file, "w") as f:
            json.dump({"fields": [1]}, f)

    def routes(self, published_after_restore):
        versions = Response(200, [{"version_id": "v1", "environments": ["production"]}])
        return {
            "GET /document_types": Response(200, [{"id": "t1", "name": "fixture_d", "schema": {}}]),
            "GET /document_types/t1/configurations/fixture_c/versions": versions,
            "GET /document_types/t1/configurations/fixture_c/v1": [Response(200, {"configuration": '{"fields": [2]}'}),
                                                                     Response(200, {"configuration": published_after_restore})],
            "GET /document_types/t1/configurations/fixture_c": Response(200, {}),
            "PUT /document_types/t1/configurations/fixture_c": Response(200, {}),
        }

    def test_restores_and_warns(self):
        client = ScriptedClient(self.routes('{"fields": [1]}'))
        name, config, warnings = client.ensure_fixture(self.doctype_file, self.config_file)
        self.assertEqual((name, config), ("fixture_d", "fixture_c"))
        self.assertEqual(len(warnings), 1)
        self.assertIn(("PUT", "/document_types/t1/configurations/fixture_c"), [c[:2] for c in client.calls])

    def test_a_restore_that_didnt_take_fails(self):
        client = ScriptedClient(self.routes('{"fields": [2]}'))
        with self.assertRaises(CodeTestError) as caught:
            client.ensure_fixture(self.doctype_file, self.config_file)
        self.assertIn("still differs from the committed files after restoring it", str(caught.exception))

    def test_refuses_to_change_an_unprefixed_doc_type(self):
        with open(self.doctype_file, "w") as f:
            json.dump({"name": "invoices_prod", "schema": {}}, f)
        client = ScriptedClient({"GET /document_types": Response(200, [])})
        with self.assertRaises(CodeTestError) as caught:
            client.ensure_fixture(self.doctype_file, self.config_file)
        self.assertIn("refusing to restore", str(caught.exception))
        self.assertEqual([c[0] for c in client.calls], ["GET"])

    def test_failed_reference_upload_is_deleted_and_hides_the_url(self):
        import requests
        url = "https://bucket.s3.amazonaws.com/k?X-Amz-Credential=AKIAEXAMPLE&X-Amz-Signature=abc"
        client = ScriptedClient({"POST /document_types/t1/goldens": Response(200, {"upload_url": url}),
                                 "DELETE /document_types/t1/goldens/fixture_ref": Response(200, {})})
        ref = {"name": "fixture_ref", "configuration": "fixture_c", "pdf": self.config_file}
        with mock.patch("requests.put", side_effect=requests.ConnectionError(f"Max retries exceeded with url: {url}")):
            with self.assertRaises(CodeTestError) as caught:
                client._upload_reference("t1", ref)
        self.assertNotIn("X-Amz", str(caught.exception))
        self.assertIn(("DELETE", "/document_types/t1/goldens/fixture_ref"), [c[:2] for c in client.calls])


class HelpersTest(unittest.TestCase):
    def test_json_diff(self):
        self.assertEqual(sensible.json_diff({"a": 1, "b": [1]}, {"a": 1, "b": [1]}), [])
        diffs = sensible.json_diff({"a": 1, "b": 2}, {"a": 3, "c": 4})
        self.assertEqual(len(diffs), 3)
        self.assertTrue(any("$.b is missing" in d for d in diffs) and any("$.c was added" in d for d in diffs))

    def test_redact_hides_presigned_url_credentials(self):
        text = settings.redact("PUT https://b.s3.amazonaws.com/k?X-Amz-Credential=AKIAEXAMPLE%2F2026&X-Amz-Signature=abc123 failed")
        self.assertNotIn("AKIAEXAMPLE", text)
        self.assertNotIn("abc123", text)
        self.assertIn("X-Amz-Signature=********", text)


if __name__ == "__main__":
    unittest.main()
