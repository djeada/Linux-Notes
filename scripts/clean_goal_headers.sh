#!/usr/bin/env bash
set -euo pipefail

find . -type f -print0 |
while IFS= read -r -d '' file; do
  sed -i -E 's/^[[:space:]]*#{1,6}[[:space:]]*goals?[[:space:]]*$/''/I' "$file"
done
