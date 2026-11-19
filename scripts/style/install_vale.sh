#!/usr/bin/env bash
# Install the Vale version the style tooling is tested with into DIR, checking the release checksum.
#   scripts/style/install_vale.sh DIR
set -euo pipefail
VERSION=3.25.1
SHA256=4bf5c5176b682b1da0830f471584d3494f1c2e27ee3029e1ad6f6661d4962182
dir="${1:?usage: install_vale.sh DIR}"
mkdir -p "$dir"
tarball="$dir/vale.tar.gz"
curl -fsSL -o "$tarball" "https://github.com/errata-ai/vale/releases/download/v${VERSION}/vale_${VERSION}_Linux_64-bit.tar.gz"
echo "${SHA256}  ${tarball}" | sha256sum -c -
tar -xzf "$tarball" -C "$dir" vale
rm "$tarball"
"$dir/vale" --version
