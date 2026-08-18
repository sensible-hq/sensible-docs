#!/usr/bin/env bash
# run_eval.sh — monthly MCP search eval wrapper
#
# Cron fires every Tuesday; this script exits early unless it's the first
# Tuesday of the month (day-of-month 1–7).
#
# Crontab entry (add with: crontab -e):
#   TZ=America/Denver
#   15 12 * * 2 /home/franc/GitHub/sensible-docs/.claude/skills/mcp-search-eval/scripts/run_eval.sh
#
# Required env vars (set in crontab or ~/.profile):
#   EVAL_SMTP_HOST   EVAL_SMTP_PORT   EVAL_SMTP_USER   EVAL_SMTP_PASS
#   EVAL_EMAIL_TO    (optional; defaults to frances@sensible.so)

set -euo pipefail

[ "$(date +%d)" -le 7 ] || exit 0

REPO=/home/franc/GitHub/sensible-docs
SCRIPT="$REPO/.claude/skills/mcp-search-eval/scripts/run_eval.py"

cd "$REPO"
python3 "$SCRIPT" --send-email
