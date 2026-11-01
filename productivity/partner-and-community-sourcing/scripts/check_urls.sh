#!/usr/bin/env bash
# Liveness + final-redirect check for a batch of URLs.
#
# Usage:
#   check_urls.sh https://a.com https://b.com
#   check_urls.sh -f urls.txt
#
# Prints: "<code>  <final-url-after-redirects>  <- <input-url>"
# Use this before recommending any link. Shorteners (bit.ly etc.) hide the real
# destination; the interesting payload is often a Google Form behind the redirect.
set -uo pipefail

urls=()
if [ "${1:-}" = "-f" ]; then
  while IFS= read -r line; do
    [ -n "${line// }" ] && urls+=("$line")
  done < "${2:?usage: check_urls.sh -f urls.txt}"
else
  urls=("$@")
fi

[ "${#urls[@]}" -eq 0 ] && { echo "no urls given"; exit 1; }

for u in "${urls[@]}"; do
  out=$(curl -sIL --max-time 20 -A 'Mozilla/5.0' -o /dev/null \
        -w '%{http_code}\t%{url_effective}' "$u" 2>/dev/null)
  code=${out%%$'\t'*}
  final=${out#*$'\t'}
  # Some servers reject HEAD: retry as a ranged GET before declaring failure.
  if [ "$code" = "000" ] || [ "$code" = "405" ] || [ "$code" = "403" ]; then
    out=$(curl -sL --max-time 25 -A 'Mozilla/5.0' -H 'Range: bytes=0-2048' -o /dev/null \
          -w '%{http_code}\t%{url_effective}' "$u" 2>/dev/null)
    code=${out%%$'\t'*}; final=${out#*$'\t'}
  fi
  printf '%s  %s  <- %s\n' "$code" "$final" "$u"
done
