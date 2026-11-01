#!/bin/bash
# Auto-sync Obsidian vault ke GitHub (commit + push). Aman dipanggil tiap jam.
# Kalau remote belum diset, script no-op (exit 0) — nggak error.
set -u
VAULT="$HOME/obsidian-vault"
cd "$VAULT" || exit 1

# Belum ada remote (belum setup GitHub) -> no-op
if ! git remote get-url origin >/dev/null 2>&1; then
  exit 0
fi

git add -A
if git diff --cached --quiet; then
  exit 0  # nggak ada perubahan
fi

git commit -m "vault sync $(date '+%Y-%m-%d %H:%M %Z')" >/dev/null 2>&1
git push origin main >/dev/null 2>&1 && echo "vault pushed: $(date '+%H:%M')"
