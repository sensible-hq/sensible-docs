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

# Agent-only rules (such as Sensible.EmDash) are off in .vale.ini so they never
# flag a person's writing. Run them on the lines changed since HEAD: in a Claude
# session, uncommitted lines are Claude's. An untracked file is all new lines.
# If the check can't run, say so on stderr but keep the exit code Vale's.
agent_lines="$root/scripts/style_sync/agent_lines.py"
if [ -f "$agent_lines" ]; then
  agent_out="$(cd "$(dirname "$file")" && python3 "$agent_lines" --base HEAD --vale "$vale" "$file" 2>&1)"
  case $? in
    1) out="$(printf '%s\n%s\n' "$out" "$agent_out" | grep .)" ;;
    0) ;;
    *) echo "vale-check: agent-only rules not checked: $agent_out" >&2 ;;
  esac
fi
[ -n "$out" ] || exit 0

{
  echo "Vale flagged $(grep -c . <<<"$out") warnings or errors in $file. Fix them, keeping the meaning."
  echo "If one is a false positive, such as a product term, code, or a quote, leave the text and say why."
  echo
  echo "$out"
} >&2
exit 2
