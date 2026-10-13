#!/usr/bin/env bash
# Checks that the Vale setup works the way Claude Code actually runs it:
# hook commands under /bin/sh, with whatever PATH Claude was started with.
# Run from anywhere in the repo or a worktree: scripts/vale-doctor.sh

root="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "Not in a git repo"; exit 1; }
cd "$root" || exit 1
fails=0
pass() { echo "  ok    $1"; }
fail() { echo "  FAIL  $1"; fails=$((fails + 1)); }
note() { echo "  note  $1"; }

echo "Tools"
command -v jq >/dev/null && pass "jq" || fail "jq isn't installed; the hook needs it"
vale="$(command -v vale || echo "$HOME/.local/bin/vale")"
if [ -x "$vale" ]; then pass "vale: $("$vale" --version) at $vale"; else fail "Vale isn't installed"; fi

echo "Config"
if "$vale" ls-config >/dev/null 2>&1; then pass ".vale.ini loads"; else fail ".vale.ini doesn't load: $("$vale" ls-config 2>&1 | head -1)"; fi
[ -d .github/styles/Google ] && pass "Google style is committed" || fail ".github/styles/Google is missing"

echo "Hook"
cmd="$(jq -r '.hooks.PostToolUse[]?.hooks[]? | select(.command | contains("vale-check")) | .command' .claude/settings.json 2>/dev/null)"
if [ -z "$cmd" ]; then
  fail "no vale-check PostToolUse hook in .claude/settings.json"
else
  pass "wired up in .claude/settings.json"
  # Runs the hook the way Claude Code does: /bin/sh, the JSON event on stdin,
  # and a bare PATH, so it also proves the ~/.local/bin fallback works
  hook() {
    printf '{"tool_name":"Edit","tool_input":{"file_path":"%s"}}' "$1" |
      env -i HOME="$HOME" PATH=/usr/bin:/bin CLAUDE_PROJECT_DIR="$root" /bin/sh -c "$cmd" 2>&1
  }
  probe="$root/docs/vale-doctor-probe.md"
  outside="$root/vale-doctor-probe.md"
  trap 'rm -f "$probe" "$outside"' EXIT

  printf '# Probe\n\nWe will utilize this feature.\n' >"$probe"
  out="$(hook "$probe")"; code=$?
  if [ "$code" -eq 2 ] && grep -q 'Google.We' <<<"$out"; then pass "reports alerts to Claude (exit 2)"
  else fail "expected exit 2 with alerts, got exit $code: $(head -1 <<<"$out")"; fi

  printf '# Probe\n\nYou can use this feature.\n' >"$probe"
  out="$(hook "$probe")"; code=$?
  [ "$code" -eq 0 ] && [ -z "$out" ] && pass "quiet on a clean doc" || fail "clean doc gave exit $code: $(head -1 <<<"$out")"

  printf '# Probe\n\nWe will utilize this feature.\n' >"$outside"
  out="$(hook "$outside")"; code=$?
  [ "$code" -eq 0 ] && [ -z "$out" ] && pass "ignores Markdown outside docs/ and reference/" || fail "file outside docs/ gave exit $code: $(head -1 <<<"$out")"

  out="$(hook "$root/.claude/settings.json")"; code=$?
  [ "$code" -eq 0 ] && pass "ignores non-Markdown files" || fail "non-Markdown file gave exit $code"
fi

echo "Settings that switch hooks off"
off=0
for f in .claude/settings.json .claude/settings.local.json "$HOME/.claude/settings.json"; do
  [ "$(jq -r '.disableAllHooks // false' "$f" 2>/dev/null)" = true ] && { fail "disableAllHooks is on in $f"; off=1; }
done
[ "$off" -eq 0 ] && pass "none found"

echo "Leftovers from older Vale setups"
grep -q 'vale-changed' "$HOME/.claude/settings.json" 2>/dev/null && note "~/.claude/settings.json still has the old vale-changed hooks"
jq -e '.mcpServers | keys[] | select(test("vale"))' "$HOME/.claude.json" >/dev/null 2>&1 && note "~/.claude.json still lists a Vale MCP server"
pane="$(jq -r '.env.CLAUDE_CODE_PLUGIN_DIRS // empty' "$HOME/.claude/settings.json" 2>/dev/null)"
if [ -n "$pane" ]; then
  v="$(claude --version 2>/dev/null | cut -d' ' -f1)"
  if [ "$(printf '%s\n2.1.287\n' "$v" | sort -V | head -1)" = 2.1.287 ]; then note "vale pane: loaded from $pane; /vale is available"
  else note "vale pane: loaded from $pane, but /vale needs Claude Code 2.1.287+ (you have $v); run claude update"; fi
fi

echo
[ "$fails" -eq 0 ] && echo "All checks passed." || echo "$fails check(s) failed."
exit $((fails > 0))
