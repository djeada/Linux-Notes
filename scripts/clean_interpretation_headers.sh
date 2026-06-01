#!/usr/bin/env bash
set -euo pipefail

find "$(dirname "$0")/../notes" -type f -print0 |
while IFS= read -r -d '' file; do
  sed -i -E 's/^[[:space:]]*#*[[:space:]]*interpre?tations?[[:space:]]*$/Interpretation:/I' "$file"
done
