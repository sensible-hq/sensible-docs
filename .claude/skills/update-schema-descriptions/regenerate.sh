#!/usr/bin/env bash
# Regenerate the schemas built from src/engine/types.ts, the way scripts/build.ts does, without a full
# `pnpm install` of the engine repo.
#
#   regenerate.sh <engine-worktree>
#
# Installs ts-json-schema-generator and prettier at the versions the engine's package.json pins, in a
# cache directory outside the repo, then rewrites configuration.schema.json and
# doctype-settings.schema.json. Run it once before editing types.ts: if it changes anything then,
# the toolchain doesn't reproduce the committed schemas and its output can't be trusted.
set -euo pipefail

repo=$(cd "$1" && pwd)
pin() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))["devDependencies"][sys.argv[2]]; print(v.lstrip("^~"))' "$repo/package.json" "$1"; }
gen_v=$(pin ts-json-schema-generator)
prettier_v=$(pin prettier)

tools="${XDG_CACHE_HOME:-$HOME/.cache}/sensible-schema-tools/tsjsg-$gen_v-prettier-$prettier_v"
if [ ! -x "$tools/node_modules/.bin/ts-json-schema-generator" ]; then
  mkdir -p "$tools"
  (cd "$tools" && npm init -y >/dev/null && npm install --silent --no-audit --no-fund \
    "ts-json-schema-generator@$gen_v" "prettier@$prettier_v")
fi
bin="$tools/node_modules/.bin"

cd "$repo"
for pair in Configuration:configuration.schema.json DoctypeSettings:doctype-settings.schema.json; do
  type=${pair%%:*}
  out=src/engine/__generated__/${pair#*:}
  tmp=$(mktemp)
  "$bin/ts-json-schema-generator" --path src/engine/types.ts --type "$type" --no-type-check \
    | "$bin/prettier" --stdin-filepath "$out" > "$tmp"
  mv "$tmp" "$out"
  echo "regenerated $out (ts-json-schema-generator $gen_v, prettier $prettier_v)"
done
