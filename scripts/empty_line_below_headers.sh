#!/usr/bin/env bash
set -euo pipefail

find "$(dirname "$0")/../notes" -type f -print0 |
while IFS= read -r -d '' file; do
  sed -i -E '
    /^```/ {
      b
    }

    /^[[:space:]]*#/ {
      N
      s/^([^\n]*#.*)\n[[:space:]]*$/\1\n/
      t
      s/^([^\n]*#.*)\n([[:space:]]*\n)+/\1\n\n/
      t
      s/^([^\n]*#.*)\n([^\n].*)$/\1\n\n\2/
    }
  ' "$file"
done
