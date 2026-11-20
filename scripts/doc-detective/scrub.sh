#!/usr/bin/env bash
# Replace the values of the secrets in config/secrets.txt with ******** in every text file under
# output/. Doc Detective writes typed text (the test account password) to its reports in plain text.
#
# run.sh calls this last. CI also runs it as its own step before uploading reports, so a run that
# is cancelled or times out mid-way never uploads an unscrubbed file.
#
# Usage: scripts/doc-detective/scrub.sh [OUTPUT_DIR]

set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
output_dir="${1:-$here/output}"
[[ -d "$output_dir" ]] || exit 0

# .env values win over the environment, as in run.sh
if [[ -f "$here/../../.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  . "$here/../../.env"
  set +a
fi

status=0
while read -r var; do
  [[ -z "$var" || "$var" == \#* ]] && continue
  value="${!var:-}"
  # Trim surrounding whitespace: a secret saved with a trailing newline still appears trimmed in reports
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  [[ -z "$value" ]] && continue
  VALUE="$value" find "$output_dir" -type f \( -name '*.json' -o -name '*.html' -o -name '*.txt' -o -name '*.md' \
    -o -name '*.log' -o -name '*.yaml' -o -name '*.yml' -o -name '*.csv' \) \
    -exec perl -pi -e 's/\Q$ENV{VALUE}\E/********/g' {} + || status=1
done < "$here/config/secrets.txt"

exit $status
