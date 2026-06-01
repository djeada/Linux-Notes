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

    is_fence($0) {
      in_fence = !in_fence
      blank = 0
      print
      next
    }

    in_fence {
      print
      next
    }

    /^[[:space:]]*$/ {
      if (!blank) {
        print ""
        blank = 1
      }
      next
    }

    {
      blank = 0
      print
    }
  ' "$file" > "$tmp"
  cat "$tmp" > "$file"
  rm "$tmp"
done
