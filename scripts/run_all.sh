#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

bash "$script_dir/fix_fenced_code_opener.sh"
bash "$script_dir/clean_goal_headers.sh"
bash "$script_dir/clean_interpretation_headers.sh"
bash "$script_dir/single_empty_line.sh"
bash "$script_dir/empty_line_below_headers.sh"
bash "$script_dir/single_empty_line.sh"
