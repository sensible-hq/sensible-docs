#!/usr/bin/env bash
# PostToolUse hook: runs Vale on a Markdown doc right after Claude writes or
# edits it, and hands any warnings or errors back to Claude to fix.
# Wired up in .claude/settings.json. Check it with scripts/vale-doctor.sh.
#
# Exit codes, as Claude Code reads them:
#   0  nothing to report
#   1  Vale isn't installed (shown to you, not Claude)
#   2  alerts found (stderr goes to Claude)

file="$(jq -r '.tool_input.file_path // empty' 2>/dev/null)"

case "$file" in
  *.md | *.mdx) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0
# Only the published docs: docs/ and reference/ at the root of the file's checkout
root="$(git -C "$(dirname "$file")" rev-parse --show-toplevel 2>/dev/null)" || exit 0
case "${file#"$root"/}" in
  docs/* | reference/*) ;;
  *) exit 0 ;;
esac

vale="$(command -v vale || echo "$HOME/.local/bin/vale")"
if [ ! -x "$vale" ]; then
  echo "vale-check: Vale isn't installed or on PATH; skipping lint of $file" >&2
  exit 1
fi

# Run from the file's directory so Vale finds the .vale.ini of the checkout
# the file is in, which matters in worktrees
out="$(cd "$(dirname "$file")" && "$vale" --no-exit --no-wrap --output=line --minAlertLevel=warning "$file" 2>&1)"
[ -n "$out" ] || exit 0

{
  echo "Vale flagged $(grep -c . <<<"$out") warnings or errors in $file. Fix them, keeping the meaning."
  echo "If one is a false positive, such as a product term, code, or a quote, leave the text and say why."
  echo
  echo "$out"
} >&2
exit 2
