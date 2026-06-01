#!/usr/bin/env bash
set -euo pipefail

find "$(dirname "$0")/../notes" -type f -print0 |
while IFS= read -r -d '' file; do
  sed -i -E ':a; N; $!ba; s/\n[[:space:]]*\n+/\n\n/g' "$file"
done
