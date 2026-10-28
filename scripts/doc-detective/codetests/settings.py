"""Paths, names, and secrets for code tests: the one place they're defined."""

import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scripts/doc-detective
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
CONFIG_DIR = os.path.join(HERE, "config")
SCHEMAS_DIR = os.path.join(HERE, "schemas")
FIXTURES_DIR = os.path.join(HERE, "fixtures")
OUTPUT_DIR = os.path.join(HERE, "output")
# One JSON record per code test, read by the reports
RECORDS_DIR = os.path.join(OUTPUT_DIR, "code-tests")
DEPS_DIR = os.path.join(HERE, ".deps")

# The Sensible API and the temporary document type that code tests run in.
# DOC_TESTS_ENV picks the Sensible environment: "prod" (default) or "dev", for features that aren't
# in production yet. Each has its own account key, so a dev run can't touch production.
ENV_VAR = "DOC_TESTS_ENV"
ENVS = {
    "prod": {"api": "https://api.sensible.so/v0", "key_var": "SENSIBLE_TEST_API_KEY"},
    "dev": {"api": "https://api.sensible.so/dev", "key_var": "SENSIBLE_DEV_API_KEY"},
}


def env():
    """The selected environment name. An unknown value is an error, never a silent fallback."""
    name = (os.environ.get(ENV_VAR) or "prod").strip().lower()
    if name not in ENVS:
        raise ValueError(f"{ENV_VAR}={name!r} isn't one of {', '.join(sorted(ENVS))}")
    return name


def api():
    return ENVS[env()]["api"]


def sensible_key_var():
    return ENVS[env()]["key_var"]


API = ENVS["prod"]["api"]  # production; code calls api() so DOC_TESTS_ENV applies
DOC_TYPE = "docs_ci_examples"
ENVIRONMENT = "development"
# Test-account fixtures (doc types and configs) that code tests can run instead of a page's code block.
# Same layout as the contract-test fixtures: <dir>/<doctype>.doctype.json and <dir>/<doctype>.<config>.config.json
TEST_FIXTURES_DIR = os.path.join(REPO_ROOT, "scripts", "test", "probe_endpoints", "contract", "fixtures")
# Fixture configs are published to this environment, and fixture extractions run in it
FIXTURE_ENVIRONMENT = "production"
# Fixture doc type and config names start with this, so they aren't deleted by accident in the app
FIXTURE_PREFIX = "fixture_"
# Inline fingerprint samples run in temporary doc types named with this prefix, deleted after each test
TEMP_DOC_TYPE_PREFIX = "docs_ci_tmp_"
# Fixture reference documents are PDFs from this folder, so a manifest can't upload other repo files
FIXTURE_PDFS_DIR = os.path.join(REPO_ROOT, "assets", "pdfs")
# A hard cap on extractions per run, so a page that grows or a bug can't spend the test account's budget
MAX_EXTRACTIONS_VAR = "DOC_TESTS_MAX_EXTRACTIONS"
MAX_EXTRACTIONS_DEFAULT = 20

# Keys. The Sensible key is the docs test account's (sensible_key_var() picks it per environment);
# there's deliberately no fallback to SENSIBLE_API_KEY, so a missing key can't run tests against
# another account.
SENSIBLE_KEY_VAR = "SENSIBLE_TEST_API_KEY"  # production's; prefer sensible_key_var()
JUDGE_KEY_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_KEY")  # ANTHROPIC_KEY: a name some local shells use
JUDGE_MODEL_VAR = "DOC_EXAMPLES_JUDGE_MODEL"
PROPOSE_FIXES_VAR = "DOC_EXAMPLES_PROPOSE_FIXES"
ENVELOPES_DIR_VAR = "DOC_EXAMPLES_ENVELOPES_DIR"
# Optional monthly budget, in charged extractions, for the test account; the report warns when it's used up
BUDGET_VAR = "DOC_TESTS_MONTHLY_BUDGET"
# This run's API usage, written by code_tests.py and read by the report
RUN_FILE = os.path.join(OUTPUT_DIR, "run.json")


def envelopes_dir():
    """Where baselines live. DOC_EXAMPLES_ENVELOPES_DIR points runs elsewhere, for example to rehearse a breach."""
    return os.environ.get(ENVELOPES_DIR_VAR) or os.path.join(HERE, "envelopes")


def load_dotenv():
    """Load .env at the repo root into the environment. Its values win, as with Doc Detective's loadVariables."""
    path = os.path.join(REPO_ROOT, ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, _, value = line.partition("=")
                if value:
                    os.environ[name.strip()] = value


def key(*names):
    """The first of these environment variables that has a value, or None.

    Values are trimmed: a secret pasted with a trailing newline would otherwise make an invalid
    HTTP header (which is what broke the first CI run).
    """
    for name in names:
        value = (os.environ.get(name) or "").strip()
        if value:
            return value
    return None


def secret_values():
    """The trimmed values of every variable in config/secrets.txt that's set."""
    path = os.path.join(HERE, "config", "secrets.txt")
    with open(path, encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return [v for v in (key(n) for n in names) if v]


def max_extractions():
    """The per-run extraction cap: DOC_TESTS_MAX_EXTRACTIONS, or MAX_EXTRACTIONS_DEFAULT."""
    value = (os.environ.get(MAX_EXTRACTIONS_VAR) or "").strip()
    return int(value) if value.isdigit() else MAX_EXTRACTIONS_DEFAULT


# Presigned S3 URLs (reference document uploads) carry credentials in their query string
PRESIGNED_RE = re.compile(r"(X-Amz-[A-Za-z-]+=)[^&\s'\"]+")


def redact(text):
    """Replace every secret value in `text` with ********, for messages that may echo a key, and
    the credentials in any presigned S3 URL."""
    for value in secret_values():
        text = text.replace(value, "********")
    return PRESIGNED_RE.sub(r"\1********", text)
