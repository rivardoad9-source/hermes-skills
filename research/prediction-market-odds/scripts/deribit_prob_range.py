#!/usr/bin/env python3
"""deribit_prob_range.py — rentang probabilitas harga BTC (atau ETH) dari opsi Deribit, tanpa key.

Kenapa script ini ada: pertanyaan "berapa kemungkinan BTC di harga X" punya DUA pasar yang bisa
dikutip, dan keduanya beda objek:
  - Polymarket  -> per-level, dan bisa "nyentuh" (touch) atau "di atas pada tanggal" (terminal)
  - opsi Deribit -> SATU distribusi penuh sekaligus (tiap strike = satu titik CDF)
Script ini yang kedua. Untuk yang pertama pakai `price_ladder_distribution.py` / `pull_prediction_markets.py`.

Pakai:
    python3 deribit_prob_range.py                                  # BTC, expiry 0.5-400 hari
    python3 deribit_prob_range.py --currency ETH
    python3 deribit_prob_range.py --json=~/.hermes/data/btc_prob_range.json
    python3 deribit_prob_range.py --days-min=5 --days-max=120 --ladder

Model: lognormal risk-neutral, drift 0, sigma = IV ATM per expiry.
P(S_T > K) = Phi( (ln S - sigma^2 T/2 - ln K) / (sigma sqrt(T)) )
Persentil   = exp( ln S - sigma^2 T/2 + z * sigma sqrt(T) )

Stdlib saja (urllib + statistics.NormalDist). Endpoint publik, tidak butuh API key.
Catatan lapangan: Deribit index sering beda ~0.4% dari Binance spot — kalau lapor, sebut dua-duanya.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import sys
import urllib.request
from statistics import NormalDist

API = "https://www.deribit.com/api/v2/public"
Z = {"P5": -1.645, "P25": -0.674, "P50": 0.0, "P75": 0.674, "P95": 1.645}
ND = NormalDist()


def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode())


def load(currency: str) -> tuple[float, dict[str, dict[float, float]], str]:
    """-> (index price, {expiry: {strike: mark_iv_pct}}, fetch time UTC)"""
    idx = get(f"{API}/get_index_price?index_name={currency.lower()}_usd")["result"]["index_price"]
    smm = get(f"{API}/get_book_summary_by_currency?currency={currency}&kind=option")["result"]
    byexp: dict[str, dict[float, float]] = {}
    for r in smm:
        parts = r["instrument_name"].split("-")          # BTC-31OCT26-90000-C
        if len(parts) != 4 or parts[3] not in ("C", "P"):
            continue
        iv = r.get("mark_iv") or r.get("bid_iv") or r.get("ask_iv")
        if not iv:
            continue
        try:
            byexp.setdefault(parts[1], {})[float(parts[2])] = float(iv)
        except ValueError:
            continue
    return float(idx), byexp, dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")


def exp_dt(tag: str) -> dt.datetime:
    # tag format Deribit: '8OCT26' (hari 1-2 digit) -> %d%b%y
    return dt.datetime.strptime(tag, "%d%b%y").replace(tzinfo=dt.timezone.utc)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--currency", default="BTC")
    ap.add_argument("--days-min", type=float, default=0.5)
    ap.add_argument("--days-max", type=float, default=400.0)
    ap.add_argument("--json", dest="json_path", default=None)
    ap.add_argument("--ladder", action="store_true", help="tambah P(>K) / P(<K) untuk K = spot x (1+x)")
    args = ap.parse_args()

    spot, byexp, fetched = load(args.currency)
    print(f"DERIBIT {args.currency} index ${spot:,.0f} · diambil {fetched} UTC · {len(byexp)} expiry")

    rows = []
    for tag in sorted(byexp, key=exp_dt):
        days = (exp_dt(tag) - dt.datetime.now(dt.timezone.utc)).total_seconds() / 86400
        if not (args.days_min <= days <= args.days_max):
            continue
        strikes = byexp[tag]
        atm = min(strikes, key=lambda k: abs(k - spot))     # ATM = strike terdekat index
        iv = strikes[atm] / 100.0
        T = days / 365.0
        mu = math.log(spot) - 0.5 * iv * iv * T
        sd = iv * math.sqrt(T)
        row = {
            "expiry": exp_dt(tag).strftime("%d %b %Y"),
            "days": round(days, 1),
            "atm_strike": atm,
            "iv_pct": round(iv * 100, 1),
            "pct": {k: round(math.exp(mu + z * sd)) for k, z in Z.items()},
        }
        if args.ladder:
            row["ladder"] = {}
            for x in (-0.30, -0.20, -0.15, -0.10, -0.05, 0.05, 0.10, 0.15, 0.20, 0.30):
                k = round(spot * (1 + x) / 1000) * 1000
                p_up = ND.cdf((mu - math.log(k)) / sd)
                row["ladder"][f"{'>' if x > 0 else '<'}${k:,.0f}"] = round((p_up if x > 0 else 1 - p_up) * 100)
        rows.append(row)
        print(f"  {row['expiry']:>12} T+{row['days']:>5} hari · ATM {atm:>9,.0f} · IV {row['iv_pct']:>4}% "
              f"· P5 {row['pct']['P5']:>7,} · P25 {row['pct']['P25']:>7,} · med {row['pct']['P50']:>7,} "
              f"· P75 {row['pct']['P75']:>7,} · P95 {row['pct']['P95']:>7,}")
        if args.ladder:
            print("      " + " · ".join(f"{k} {v}%" for k, v in row["ladder"].items()))

    if not rows:
        print("  (tidak ada expiry di rentang hari itu — lebarkan --days-min/--days-max)")
    if args.json_path:
        path = os.path.expanduser(args.json_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json.dump({"spot": spot, "fetched_utc": fetched, "rows": rows}, open(path, "w"), indent=1)
        print("json ->", path)

    print("\nCara baca: pita P25-P75 = 50% kemungkinan, P5-P95 = 90%. Median lognormal selalu < spot "
          "(exp(-sigma^2 T/2)) -> itu drift model, BUKAN bias bearish pasar; skew asli (smile) bikin "
          "ekor kiri lebih gemuk dari yang model ini kasih.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
