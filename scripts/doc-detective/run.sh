#!/usr/bin/env bash
# Runs Doc Detective, then scrubs secret values from the report files.
# Doc Detective writes typed keys (for example, the test account password)
# to its JSON and HTML reports in plain text, and has no option to mask them.
#
# Usage: scripts/doc-detective/run.sh [doc-detective args...]
# Example: scripts/doc-detective/run.sh -i "docs/document extraction/getting-started.md"

set -uo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
output_dir="$repo_root/scripts/doc-detective/output"
secret_vars=(SENSIBLE_TEST_PASSWORD SENSIBLE_TEST_API_KEY)

cd "$repo_root"
doc-detective -c .doc-detective.json "$@"
status=$?

# Read secrets from the environment, falling back to .env (which Doc Detective
# also loads, and which takes precedence over the environment).
for var in "${secret_vars[@]}"; do
  value=""
  if [[ -f .env ]]; then
    value="$(grep -E "^${var}=" .env | tail -1 | cut -d= -f2-)"
  fi
  value="${value:-${!var:-}}"
  [[ -z "$value" ]] && continue
  VALUE="$value" find "$output_dir" -type f \( -name '*.json' -o -name '*.html' \) \
    -exec perl -pi -e 's/\Q$ENV{VALUE}\E/********/g' {} +
done

exit $status
