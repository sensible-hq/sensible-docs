"""Paths, names, and secrets for code tests: the one place they're defined."""

import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scripts/doc-detective
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
CONFIG_DIR = os.path.join(HERE, "config")
# Prompts the tooling sends to an LLM, one folder per use (prompts/judge/); settings for them stay in config/
PROMPTS_DIR = os.path.join(HERE, "prompts")
SCHEMAS_DIR = os.path.join(HERE, "schemas")
# The tooling's self-test pages: altered copies of real pages (tests/pages/build_fixtures.py)
SELF_TEST_PAGES_DIR = os.path.join(HERE, "tests", "pages")
OUTPUT_DIR = os.path.join(HERE, "output")
# One JSON record per code test, read by the reports
RECORDS_DIR = os.path.join(OUTPUT_DIR, "code-tests")
DEPS_DIR = os.path.join(HERE, ".deps")

# The Sensible API that code tests run against, and the environment their configs publish to.
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
ENVIRONMENT = "development"
# Test-account fixtures (doc types and configs) that code tests can run instead of a page's code block.
# One folder per group: <group>/<doctype>.doctype.json, <group>/<doctype>.<config>.config.json, a
# manifest.json listing reference documents, and the fixture's own files (test documents)
TEST_FIXTURES_DIR = os.path.join(HERE, "fixtures")
# Fixture configs are published to this environment, and fixture extractions run in it
FIXTURE_ENVIRONMENT = "production"
# Fixture doc type and config names start with this, so they aren't deleted by accident in the app
FIXTURE_PREFIX = "fixture_"
# A page's own configs (output tests, and fingerprint and portfolio samples) run in doc types named with
# this prefix. Each run recreates them, and they stay in the test account between runs, so the report
# can link to each config in the editor
SAMPLE_DOC_TYPE_PREFIX = "docs_ci_sample_"
# Example documents linked from this repo's v0 branch; the runner uploads the local copy as a reference document
DOCS_RAW_PREFIX = "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/"
# The docs' published example documents. A file a test sends to Sensible (a fixture reference document,
# a classification request) is either in its fixture's folder ("file") or here ("docs_pdf"), used in
# place, so a page or manifest can't send other repo files
DOCS_PDFS_DIR = os.path.join(REPO_ROOT, "assets", "pdfs")
# A fixture's reference document has one of these extensions, and uploads with the matching content type
REFERENCE_CONTENT_TYPES = {
    ".pdf": "application/pdf",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
    ".xlsm": "application/vnd.ms-excel.sheet.macroenabled.12",
    ".xlsb": "application/vnd.ms-excel.sheet.binary.macroenabled.12",
    ".csv": "text/csv",
}

# The document a code test runs on when it names none (no <!-- inline document -->): a blank page, for
# examples that don't read their document, such as a constant field and JsonLogic on it. Like the
# pages' example document links, it's the file's raw URL on v0, so it resolves only once it's merged there.
BLANK_DOCUMENT_PDF = os.path.join(DOCS_PDFS_DIR, "blank_page.pdf")
BLANK_DOCUMENT_URL = "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/blank_page.pdf"
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
