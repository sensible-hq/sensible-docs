"""DOC_TESTS_ENV: which Sensible environment, API address, and account key code tests use."""

import io
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from codetests import sensible, settings


class EnvSwitch(unittest.TestCase):
    def test_default_is_production(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(settings.env(), "prod")
            self.assertEqual(settings.api(), "https://api.sensible.so/v0")
            self.assertEqual(settings.sensible_key_var(), "SENSIBLE_TEST_API_KEY")

    def test_dev_uses_the_dev_api_and_the_dev_key(self):
        with mock.patch.dict(os.environ, {"DOC_TESTS_ENV": " Dev\n"}, clear=True):
            self.assertEqual(settings.env(), "dev")
            self.assertEqual(settings.api(), "https://api.sensible.so/dev")
            self.assertEqual(settings.sensible_key_var(), "SENSIBLE_DEV_API_KEY")

    def test_unknown_environment_is_an_error_not_a_fallback(self):
        with mock.patch.dict(os.environ, {"DOC_TESTS_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError):
                settings.api()

    def test_client_calls_the_selected_api(self):
        with mock.patch.dict(os.environ, {"DOC_TESTS_ENV": "dev"}, clear=True), \
             mock.patch("requests.request") as request:
            sensible.SensibleClient("k")._api("GET", "/document_types")
        self.assertTrue(request.call_args.args[1].startswith("https://api.sensible.so/dev/"))

    def test_dev_run_never_falls_back_to_the_production_key(self):
        import code_tests
        env = {"DOC_TESTS_ENV": "dev", "SENSIBLE_TEST_API_KEY": "prod-key"}
        err = io.StringIO()
        with mock.patch.dict(os.environ, env, clear=True), \
             mock.patch.object(settings, "load_dotenv", lambda *a, **k: None), \
             mock.patch.object(sys, "argv", ["code_tests.py", "--file", "docs/document extraction/getting-started.md"]), \
             redirect_stderr(err), redirect_stdout(io.StringIO()):
            code = code_tests.main()
        self.assertEqual(code, 2)
        self.assertIn("SENSIBLE_DEV_API_KEY", err.getvalue())

    def test_dev_key_is_a_registered_secret(self):
        with open(os.path.join(settings.CONFIG_DIR, "secrets.txt"), encoding="utf-8") as f:
            names = {line.strip() for line in f if line.strip() and not line.startswith("#")}
        self.assertIn("SENSIBLE_DEV_API_KEY", names)


if __name__ == "__main__":
    unittest.main()
