#!/usr/bin/env bash
# Run a docs page's tests: Doc Detective runs its UI tests, code_tests.py runs its code tests.
# Then write output/report.html and scrub secret values from every report file: Doc Detective
# writes typed text (the test account password) to its reports in plain text.
#
# Usage:   scripts/doc-detective/run.sh [Doc Detective options] PAGE
# Example: scripts/doc-detective/run.sh --no-auto-update "docs/document extraction/getting-started.md"
#
# Exits 1 if any step fails, including a UI test Doc Detective skipped. Each step still runs, so
# the report always covers the whole page.

set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo_root="$(cd "$here/../.." && pwd)"
output_dir="$here/output"
cd "$repo_root"

if (( $# < 1 )); then
  echo "Usage: $0 [Doc Detective options] PAGE" >&2
  exit 2
fi
page="${!#}"
dd_options=("${@:1:$#-1}")
if [[ ! -f "$page" ]]; then
  echo "No such page: $page" >&2
  exit 2
fi

# .env values win over the environment, as with Doc Detective's loadVariables
if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

rm -rf "$output_dir"
mkdir -p "$output_dir"
status=0

# Doc Detective runs only if the page has UI tests, so pages with only code tests don't need it installed
if python3 "$here/code_tests.py" --file "$page" --list | grep -q '^UI test'; then
  doc-detective -c .doc-detective.json "${dd_options[@]}" -i "$page" || status=1
  python3 "$here/report.py" verify-ui --page "$page" || status=1
else
  echo "No UI tests in $page; skipping Doc Detective"
fi
python3 "$here/code_tests.py" --file "$page" || status=1
python3 "$here/report.py" html --page "$page" || status=1

# Scrub secrets last, so it covers report.html and the code-test records too
while read -r var; do
  [[ -z "$var" || "$var" == \#* ]] && continue
  value="${!var:-}"
  # Trim surrounding whitespace: a secret saved with a trailing newline still appears trimmed in reports
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  [[ -z "$value" ]] && continue
  VALUE="$value" find "$output_dir" -type f \( -name '*.json' -o -name '*.html' \) \
    -exec perl -pi -e 's/\Q$ENV{VALUE}\E/********/g' {} +
done < "$here/config/secrets.txt"

exit $status
