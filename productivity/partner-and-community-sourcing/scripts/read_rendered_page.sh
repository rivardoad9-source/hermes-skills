#!/usr/bin/env bash
# Read text, JSON-LD and community links out of a page that may be JS-rendered.
#
# Usage: read_rendered_page.sh URL [max_text_lines]
#
# Strategy: curl first; if the HTML looks empty of content (no JSON-LD, no
# __NEXT_DATA__, no event markers), retry with headless Chromium --dump-dom.
# Works for Luma / Next.js / React event and hackathon pages, which carry the
# date, deadline, prize and attendance count in JSON-LD or embedded props.
set -uo pipefail

url="${1:?usage: read_rendered_page.sh URL [max_text_lines]}"
max="${2:-120}"
tmp=$(mktemp /tmp/rendered.XXXXXX.html)

curl -sL --max-time 25 -A 'Mozilla/5.0' "$url" -o "$tmp" 2>/dev/null || true

if ! grep -qiE 'application/ld\+json|__NEXT_DATA__|going|deadline|prize' "$tmp" 2>/dev/null; then
  ch=$(ls -d "$HOME"/.cache/ms-playwright/chromium-*/chrome-linux64/chrome 2>/dev/null | head -1)
  if [ -n "$ch" ]; then
    "$ch" --headless --no-sandbox --disable-gpu --hide-scrollbars \
      --virtual-time-budget=9000 --dump-dom "$url" > "$tmp" 2>/dev/null || true
  fi
fi

python3 - "$tmp" "$max" <<'PY'
import html, json, re, sys

path, max_lines = sys.argv[1], int(sys.argv[2])
src = open(path, encoding="utf-8", errors="ignore").read()

print("=== JSON-LD / structured ===")
blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', src, re.S)
if not blocks:
    for key in ("__NEXT_DATA__", "pageProps", "EventScheduled"):
        for m in re.finditer(re.escape(key), src):
            print(re.sub(r'\s+', ' ', src[max(0, m.start() - 200):m.start() + 600])[:800])
            break
for b in blocks[:4]:
    try:
        obj = json.loads(b.strip())
        print(re.sub(r'\s+', ' ', json.dumps(obj, ensure_ascii=False))[:1200])
    except Exception:
        print(re.sub(r'\s+', ' ', b)[:1200])

text = re.sub(r'<script[^>]*>.*?</script>', ' ', src, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.S)
text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
lines = [l.strip() for l in re.sub(r'[ \t]+', ' ', text).splitlines() if l.strip()]
print("=== TEXT ===")
for line in lines[:max_lines]:
    print(line[:200])

print("=== COMMUNITY / SHORT LINKS ===")
links = sorted(set(re.findall(
    r'https?://(?:t\.me|discord(?:\.gg|\.com/invite)|linktr\.ee|bit\.ly|luma\.com|lu\.ma|forms\.gle|docs\.google\.com/forms)'
    r'[^\s"\'<>)]*', src)))
for l in links[:40]:
    print(l)
if not links:
    print("(none found)")
PY

rm -f "$tmp"
