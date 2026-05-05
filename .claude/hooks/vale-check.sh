#!/usr/bin/env bash
# Runs vale on any .md file written or edited. Called as a PostToolUse hook.
# Exits 2 (injects feedback into Claude's context) if errors or warnings are found.

input=$(cat)
file=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || true)

[[ -z "$file" || "$file" != *.md ]] && exit 0
[[ "$file" == *"/.github/styles/"* ]] && exit 0

out=$(~/.local/bin/vale --no-wrap "$file" 2>&1) || true

if echo "$out" | grep -qE "[1-9][0-9]* (error|warning)"; then
  echo "Vale issues in $file — fix before proceeding:" >&2
  echo "$out" >&2
  exit 2
fi

exit 0
