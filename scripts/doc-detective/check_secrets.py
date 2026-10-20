#!/usr/bin/env python3
"""Fail closed if a secret could leak from a docs-test run.

Doc Detective writes typed text, such as the test account password, into its reports in plain
text (doc-detective/doc-detective#204). scrub.sh replaces known secret values, but a scrub is
fail-open: a new secret, file type, or encoding it doesn't cover goes out unnoticed. This check
runs after the scrub and before anything is published, and exits 1 if:

1. Leak scan: a value of a registered secret appears anywhere under the output folder (any file,
   any type), as written or JSON-escaped, HTML-escaped, URL-encoded, or base64-encoded; or a
   credential-shaped string appears that nobody registered (Anthropic, GitHub, AWS keys, bearer
   tokens).
2. Coverage: something that can carry a secret isn't classified, so a future secret can't be
   missed silently:
   - a `${{ secrets.X }}` in a docs-test workflow whose environment variable isn't in
     config/secrets.txt
   - a workflow step that receives secrets, while the leak-check step doesn't receive them all
   - a `$VAR` in a docs page's test markup, or a variable in .env, that's in neither
     config/secrets.txt nor config/public-vars.txt

It never prints a secret value.

Usage:
  check_secrets.py [--output DIR] [--coverage-only | --scan-only]
"""

import argparse
import base64
import glob
import html
import json
import os
import re
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SECRETS_FILE = os.path.join(HERE, "config", "secrets.txt")
PUBLIC_FILE = os.path.join(HERE, "config", "public-vars.txt")
# Every docs-test workflow: doc-detective-*.yml, and doc-tests-*.yml for pages without UI tests
WORKFLOW_GLOBS = [os.path.join(REPO_ROOT, ".github", "workflows", g) for g in ("doc-detective*.yml", "doc-tests-*.yml")]
DOCS_GLOB = os.path.join(REPO_ROOT, "docs", "**", "*.md")
CHECK_STEP = "Check for leaked secrets"
# A secret shorter than this would match too much by chance; it's reported as a coverage error
MIN_SECRET_LENGTH = 6

# Credential shapes that should never appear in a report, registered or not
PATTERNS = {
    "Anthropic API key": re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})"),
    "AWS access key ID": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Bearer token": re.compile(r"Bearer\s+(?!\*{4})[A-Za-z0-9._~+/\-]{20,}=*"),
}
ENV_REF = re.compile(r"(?<!\$)\$([A-Z][A-Z0-9_]*)\b")
TEST_COMMENT = re.compile(r"<!--\s*(?:test|step|code test)\b(.*?)-->", re.S)


def read_names(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")]


def load_dotenv(path):
    """Names and values in .env (values win over the environment, as in run.sh)."""
    values = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    name, _, value = line.partition("=")
                    values[name.strip()] = value.strip()
    return values


def secret_values(names, dotenv):
    """{name: trimmed value} for every registered secret that has a value."""
    values = {}
    for name in names:
        value = (dotenv.get(name) or os.environ.get(name) or "").strip()
        if value:
            values[name] = value
    return values


def encodings(value):
    """Forms a value can take in a report file."""
    forms = {
        "as written": value,
        "JSON-escaped": json.dumps(value)[1:-1],
        "HTML-escaped": html.escape(value),
        "URL-encoded": urllib.parse.quote(value, safe=""),
        "base64": base64.b64encode(value.encode()).decode().rstrip("="),
    }
    unique = {}
    for label, form in forms.items():
        # A plain value is often identical in several encodings; report each distinct form once
        if form and form not in unique.values():
            unique[label] = form
    return unique


def scan(output_dir, secrets):
    """Return findings: (file, what was found). Never includes the value."""
    findings = []
    for path in sorted(glob.glob(os.path.join(output_dir, "**", "*"), recursive=True)):
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as f:
            text = f.read().decode("utf-8", errors="replace")
        rel = os.path.relpath(path, output_dir)
        for name, value in secrets.items():
            for label, form in encodings(value).items():
                if form in text:
                    findings.append((rel, f"the value of {name} ({label})"))
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append((rel, f"a string shaped like a {label}"))
    return findings


def workflow_secret_env(path):
    """{step name: set of env var names that step sets from ${{ secrets.* }}}."""
    steps, current = {}, "(job)"
    with open(path, encoding="utf-8") as f:
        for line in f:
            step = re.match(r"\s*-\s*name:\s*(.+?)\s*$", line)
            if step:
                current = step.group(1).strip("\"'")
            # Also a conditional value, such as ${{ contains(matrix.secrets, 'X') && secrets.X || '' }}
            env = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*):\s*\$\{\{[^}]*\bsecrets\.[A-Za-z0-9_]+[^}]*\}\}", line)
            if env:
                steps.setdefault(current, set()).add(env.group(1))
    return steps


def page_env_refs(paths):
    """{var name: first page that uses it} for $VAR references in docs test markup."""
    refs = {}
    for path in paths:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for comment in TEST_COMMENT.finditer(text):
            for name in ENV_REF.findall(comment.group(1)):
                refs.setdefault(name, os.path.relpath(path, REPO_ROOT))
    return refs


def workflow_files():
    """The docs-test workflows coverage checks."""
    return sorted(f for g in WORKFLOW_GLOBS for f in glob.glob(g))


def coverage(secret_names, public_names, dotenv, workflows, pages):
    """Return problems: things that can carry a secret but aren't classified."""
    problems = []
    known = set(secret_names) | set(public_names)
    for path in workflows:
        rel = os.path.relpath(path, REPO_ROOT)
        steps = workflow_secret_env(path)
        all_vars = set().union(*steps.values()) if steps else set()
        for var in sorted(all_vars - set(secret_names)):
            problems.append(f"{rel}: {var} is set from a GitHub secret but isn't in config/secrets.txt")
        if all_vars:
            if CHECK_STEP not in steps:
                problems.append(f"{rel}: steps receive secrets, but there's no \"{CHECK_STEP}\" step that receives them")
            else:
                missing = all_vars - steps[CHECK_STEP]
                if missing:
                    problems.append(f"{rel}: the \"{CHECK_STEP}\" step doesn't receive {', '.join(sorted(missing))}, "
                                    "so it can't scan for them")
    for name, page in sorted(page_env_refs(pages).items()):
        if name not in known:
            problems.append(f"{page}: test markup uses ${name}, which is in neither config/secrets.txt "
                            "nor config/public-vars.txt")
    for name in sorted(set(dotenv) - known):
        problems.append(f".env: {name} is in neither config/secrets.txt nor config/public-vars.txt")
    for name in sorted(set(secret_names) & set(public_names)):
        problems.append(f"{name} is in both config/secrets.txt and config/public-vars.txt")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", default=os.path.join(HERE, "output"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--coverage-only", action="store_true", help="Only check that every secret is classified")
    mode.add_argument("--scan-only", action="store_true", help="Only scan the output folder")
    args = parser.parse_args()

    secret_names, public_names = read_names(SECRETS_FILE), read_names(PUBLIC_FILE)
    dotenv = load_dotenv(os.path.join(REPO_ROOT, ".env"))
    failed = False

    if not args.scan_only:
        problems = coverage(secret_names, public_names, dotenv,
                            workflow_files(), sorted(glob.glob(DOCS_GLOB, recursive=True)))
        for problem in problems:
            print(f"FAIL coverage: {problem}")
        failed |= bool(problems)

    if not args.coverage_only:
        secrets = secret_values(secret_names, dotenv)
        for name, value in sorted(secrets.items()):
            if len(value) < MIN_SECRET_LENGTH:
                print(f"FAIL coverage: {name} is shorter than {MIN_SECRET_LENGTH} characters; too short to scan for reliably")
                failed = True
        if os.path.isdir(args.output):
            findings = scan(args.output, secrets)
            for rel, what in findings:
                print(f"FAIL leak: {rel} contains {what}")
            failed |= bool(findings)
        print(f"Scanned {args.output} for {len(secrets)} registered secret(s) and {len(PATTERNS)} credential patterns")

    if not failed:
        print("PASS no secrets found, and every secret is classified")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
