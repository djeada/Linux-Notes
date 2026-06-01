#!/usr/bin/env bash
set -euo pipefail

find "$(dirname "$0")/../notes" -type f -print0 |
while IFS= read -r -d '' file; do
  tmp="$(mktemp)"
  awk '
    function is_fence(line) {
      if (substr(line, 1, 3) == "   ") {
        line = substr(line, 4)
      } else if (substr(line, 1, 2) == "  ") {
        line = substr(line, 3)
      } else if (substr(line, 1, 1) == " ") {
        line = substr(line, 2)
      }

      return substr(line, 1, 3) == "```"
    }

    function is_interpretation_header(line) {
      line = tolower(line)
      sub(/^[[:space:]]*/, "", line)

      while (substr(line, 1, 1) == "#") {
        line = substr(line, 2)
      }

      sub(/^[[:space:]]*/, "", line)
      sub(/[[:space:]]*$/, "", line)

      return line == "interpretation" || line == "interpretations" || line == "interprtation" || line == "interprtations"
    }

    is_fence($0) {
      in_fence = !in_fence
      print
      next
    }

    !in_fence && is_interpretation_header($0) {
      print "Interpretation:"
      next
    }

    {
      print
    }
  ' "$file" > "$tmp"
  cat "$tmp" > "$file"
  rm "$tmp"
done
