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

    function is_heading(line) {
      if (substr(line, 1, 3) == "   ") {
        line = substr(line, 4)
      } else if (substr(line, 1, 2) == "  ") {
        line = substr(line, 3)
      } else if (substr(line, 1, 1) == " ") {
        line = substr(line, 2)
      }

      if (substr(line, 1, 1) != "#") {
        return 0
      }

      marks = 0
      while (substr(line, marks + 1, 1) == "#") {
        marks++
      }

      return marks <= 6 && (length(line) == marks || substr(line, marks + 1, 1) ~ /[[:space:]]/)
    }

    {
      if (pending_header && $0 !~ /^[[:space:]]*$/) {
        print ""
        pending_header = 0
      } else if (pending_header && $0 ~ /^[[:space:]]*$/) {
        print ""
        pending_header = 0
        next
      }

      print

      if (is_fence($0)) {
        in_fence = !in_fence
        next
      }

      if (!in_fence && is_heading($0)) {
        pending_header = 1
      }
    }
  ' "$file" > "$tmp"
  cat "$tmp" > "$file"
  rm "$tmp"
done
