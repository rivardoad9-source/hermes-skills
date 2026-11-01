---
name: external-repo-vetting
description: Vet a third-party GitHub repo by running it, not reading it.
---

# Vetting a third-party repo (trading bot / tool / deliverable)

Trigger: user sends a GitHub URL ("cek repo ini"). Goal: state what it IS, whether it's
safe, whether it matches the promotion/narrative, and what it's worth — with real evidence,
never by reading the README alone.

## Steps

1. **Clone + shape** (one call):
   ```bash
   cd /tmp && rm -rf repo && git clone --depth 50 <url> repo
   cd repo && git log --pretty='%h|%ad|%an|%s' --date=short | head -40
   du -sh --exclude=.git .; du -sh */ | sort -h | tail -12
   ```
   Few squashed commits = delivered/exported project, not organic development. Check author
   account age + repo created/star/fork counts via `api.github.com/repos/<owner>/<name>` and
   `/users/<owner>`.

2. **Is it a fork/vendored upstream?** Look for a whole third-party package inside. Then diff
   byte-for-byte against the real upstream tag/commit:
   ```bash
   git clone --depth 1 --branch <tag> https://github.com/<upstream> up
   # or fetch the exact commit a doc claims: git fetch --depth 1 origin <sha> && git checkout FETCH_HEAD
   diff -rq --exclude=.git --exclude=__pycache__ up repo
   ```
   Identical => code is not the seller's work; value = upstream (often free, check LICENSE).
   Differences are the only part worth assessing.

3. **Malware/secret scan** (split into small commands — long inline payloads get blocked):
   ```bash
   grep -rInoE "\b[a-fA-F0-9]{64}\b" --include=*.py .          # private keys
   grep -rInoE "0x[a-fA-F0-9]{40}" --include=*.py .             # wallets
   grep -rhoE "https?://[a-zA-Z0-9./_-]+" --include=*.py . | sort | uniq -c | sort -rn | head -20
   git ls-files | grep -iE "^\.env$|secret|credential"          # committed secrets
   ```
   All-urls-are-example.com + no hex keys = clean.

4. **Run it** (this is the whole point — claims must be executed, not trusted):
   ```bash
   export PATH=$HOME/.hermes/bin:$PATH   # uv lives here, not on default PATH
   uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r <reqfile>
   ./.venv/bin/python -m <pkg> doctor      # inspect config, no orders
   ./.venv/bin/python -m unittest discover -s <tests dir> -v
   ```
   Record pass/fail counts and the real backtest result. `0 trades` is a result — report it.

5. **Read the wrapper, not the README**: LOC ratio (`find <pkg> -name '*.py' | xargs wc -l`) shows
   how much of the repo is the seller's code. Then check what the strategy actually is
   (indicators, exit rules: TP? trailing? cooldown?) and the real-money risk notes.

6. **Diff claims vs reality**: grep the README/docs for the promotional keywords (product names,
   P&L figures, "AI" model names) and see whether the repo says "not present" itself.

7. **Kalau repo dipromosikan bareng akun X / token / website** (repo cuma "bagian 1"; klaim
   sebenarnya biasanya di luar repo):
   - **Timeline X**: pakai nitter RSS, bukan API X:
     `curl -s -A "Mozilla/5.0 ... Chrome/124.0" "https://shitter.thepixora.com/<handle>/rss"`
     → semua klaim promo + jumlah post (akun baru = post dikit).
   - **Website**: `curl -sL <site> -o site.html`, lalu ekstrak JS inline
     (`re.findall(r'<script[^>]*>(.*?)</script>', h, re.S)`) → **formula asli hampir selalu di
     client-side JS**, bukan di backend. Cari: fungsi `score(`, threshold, flag/wash, `rng(`/`Math.random`.
   - **Placeholder = produk belum jalan**: config kosong seperti `telegram:''`, `botApi:''`,
     atau tabel "menunggu API" ⇒ fitur itu belum ada, cuma mockup.
   - **Token on-chain (keyless)**:
     `https://api.geckoterminal.com/api/v2/networks/<net>/tokens/<ca>` dan `.../tokens/<ca>/pools`
     → harga, FDV, likuiditas, volume 24h, transaksi/pembeli unik, umur pool, launchpad details.
     Trades: `.../networks/<net>/pools/<pool>/trades` → terapkan formula wash/bot punya mereka
     sendiri ke token mereka sendiri (bukti paling tajam: berapa % volume mereka yang "fake"
     menurut filter mereka sendiri).
   - **RPC langsung** (blockscout kena Cloudflare di curl): POST JSON-RPC ke RPC chain —
     `eth_call` `totalSupply` (0x18160ddd) dan `balanceOf` (0x70a08231+addr pad64) untuk cek
     distribusi supply (pool/curve/dead/dev). Retry dgn sleep, kadang 403 rate-limit.
     Cek klaim "supply burned": `eth_getTransactionReceipt` ke tt hash + balance alamat 0x…dEaD.
   - **Rasio volume/likuiditas**: volume 24h ≫ likuiditas (beberapa kali) di pool kecil = churn
     bot/wash, bukan minat organik. Bandingkan juga median trade size.

8. **Report shape (Indonesian, casual)**
What it is → what I verified by running (with numbers) → what it is NOT (promised features missing)
→ real-money risks → who it's useful for. Lead with the verdict on safety, end with the value call.

## Pitfalls
- Don't judge from README alone; sellers' docs can be honest while the promo around them isn't.
- `curl | python3` and giant one-liners get security-flagged/blocked — write small commands or a script file.
- GitHub API output can be huge (fork/user lists): always `grep` in the same pipe, never dump raw JSON.
- Check upstream **commit**, not just tag: a vendored copy may be upstream main between releases.
- Verify pyproject/requirements: missing `pip` on host is normal (PEP 668) — use uv, not system pip.
