#!/usr/bin/env python3
"""Measured base rates from Binance daily klines — for timing questions, not opinions.

Two studies, keyless, stdlib only:

  1. forward returns after historical Fed rate HIKES (edit HIKE_DATES as new meetings resolve)
  2. "wait for a dip" vs "buy now": for every start day, does a limit at -X% fill within H days,
     and what entry price does that produce versus simply buying at the start

Usage:
  python3 base_rates_and_dip_sim.py                      # BTC, hikes 2022-2023 + 2026
  python3 base_rates_and_dip_sim.py --symbol ETHUSDT
  python3 base_rates_and_dip_sim.py --hikes 2022-06-15,2022-07-27
  python3 base_rates_and_dip_sim.py --start 2021-01-01 --dips 3,5,8,10 --dip-horizons 7,30,60
  python3 base_rates_and_dip_sim.py --post-hike-only     # study 2 restricted to hike windows

Why this exists: "hike = bearish ya?" and "DCA sekarang atau tunggu turun?" are answered with a
measured distribution (median AND mean, fill rate, n) plus price levels — never one direction call.
Worked numbers + the answer shape: references/dca-vs-wait-dip-base-rates.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics as st
import urllib.request

HOSTS = ("https://api.binance.com", "https://data-api.binance.vision")

# Fed hikes: 2022-03-16 (first of that cycle) → 2023-07-26 (last), plus later hikes as they resolve.
HIKE_DATES = ["2022-03-16", "2022-05-04", "2022-06-15", "2022-07-27", "2022-09-21",
              "2022-11-02", "2022-12-14", "2023-02-01", "2023-03-22", "2023-05-03",
              "2023-07-26", "2026-09-16"]


def _get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def daily(symbol: str, start: str) -> dict:
    """Daily OHLC from `start` (inclusive) to now, keyed by UTC date.

    ⚠️ `limit` is capped at 1000 rows, so a bare `interval=1d&limit=400` reaches only ~13 months
    back: older dates come back EMPTY (the symptom is "(no data)" lines and then a formatter crash
    on None). Page with `startTime` until a short page comes back.
    """
    out: list = []
    t = int(dt.datetime.fromisoformat(start).replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
    while True:
        rows = None
        for host in HOSTS:
            try:
                rows = _get(f"{host}/api/v3/klines?symbol={symbol}&interval=1d&startTime={t}&limit=1000")
                break
            except Exception:
                rows = None
        if not rows:
            raise SystemExit(f"klines fetch failed for {symbol} (both hosts)")
        out += rows
        if len(rows) < 1000:
            break
        t = rows[-1][0] + 86_400_000
    K = {}
    for r in out:
        d = dt.datetime.fromtimestamp(r[0] / 1000, dt.timezone.utc).date()
        K[d] = {"o": float(r[1]), "h": float(r[2]), "l": float(r[3]), "c": float(r[4])}
    return K


def fwd(K: dict, d: dt.date, n: int):
    """Close-to-close forward return in %, or None when the window runs past the data."""
    ds = sorted(K)
    if d not in K:
        return None
    i = ds.index(d)
    if i + n >= len(ds):
        return None
    return (K[ds[i + n]]["c"] / K[d]["c"] - 1) * 100


def stats_line(name: str, xs: list) -> None:
    if not xs:
        print(f"  {name}: n=0")
        return
    print(f"  {name}: n={len(xs)} median {st.median(xs):+.2f}%  mean {st.mean(xs):+.2f}%  "
          f"naik {sum(1 for v in xs if v > 0)}/{len(xs)}")


def study_hikes(K: dict, dates: list, horizons: list) -> None:
    print("\n=== 1. forward return setelah Fed HIKE ===")
    print(f"  {'tanggal':12}" + "".join(f"{'+' + str(h) + 'd':>9}" for h in horizons))
    cols = {h: [] for h in horizons}
    for s in dates:
        d = dt.date.fromisoformat(s)
        vals = [fwd(K, d, h) for h in horizons]
        for h, v in zip(horizons, vals):
            if v is not None:
                cols[h].append(v)
        print(f"  {s:12}" + "".join(f"{v:9.2f}" if v is not None else f"{'n/a':>9}" for v in vals))
    for h in horizons:
        stats_line(f"+{h}d", cols[h])
    print("  NOTE: on the decision day itself the 18:00 UTC release lands in that day's candle —")
    print("  use klines 1h/15m with an explicit startTime for the intraday reaction instead.")


def study_dips(K: dict, dips: list, horizons: list, start_dates=None) -> None:
    print("\n=== 2. 'tunggu turun' vs 'beli sekarang' ===")
    print("  (tiap hari mulai: limit -x% selama H hari; tidak kena = beli di close hari-H)")
    print(f"  {'dip':>5}{'H':>4}{'kena%':>8}{'rata2 selisih masuk':>22}{'nunggu lbh murah':>18}{'n':>7}")
    ds = sorted(K)
    for H in horizons:
        for x in dips:
            fill, imp, win, tot = 0, [], 0, 0
            for i, d in enumerate(ds):
                if i + H >= len(ds):
                    break
                if start_dates is not None and d not in start_dates:
                    continue
                s = K[d]["c"]
                lim = s * (1 - x / 100.0)
                hit = next((j for j in range(i, i + H + 1) if K[ds[j]]["l"] <= lim), None)
                ent = lim if hit is not None else K[ds[i + H]]["c"]
                fill += hit is not None
                imp.append((ent / s - 1) * 100)
                win += ent < s
                tot += 1
            if not tot:
                continue
            print(f"  {x:4.0f}%{H:4d}{100 * fill / tot:8.0f}{st.mean(imp):+16.2f}%"
                  f"{100 * win / tot:14.0f}%{tot:7d}")
    print("\n  BACA: kolom 5 = seberapa sering nunggu DAPAT harga lebih murah; kolom 4 = rata-rata")
    print("  hasilnya. Kolom 5 besar TAPI kolom 4 positif = menang tipis di mayoritas kasus, kalah")
    print("  besar di minoritas (harga kabur naik). Karena itu jawabannya 'pecah modal'")
    print("  (DCA terjadwal + limit bertingkat), bukan 'pilih salah satu'.")


def current_levels(K: dict, symbol: str) -> None:
    ds = sorted(K)
    last = K[ds[-1]]["c"]
    print(f"\n=== level ({symbol}, close terakhir {ds[-1]} = {last:,.0f}) ===")
    for x in (2, 5, 9, 16):
        print(f"  limit -{x:>2}% = {last * (1 - x / 100):,.0f}")
    h7 = max(K[d]["h"] for d in ds[-7:]); l7 = min(K[d]["l"] for d in ds[-7:])
    h30 = max(K[d]["h"] for d in ds[-30:]); l30 = min(K[d]["l"] for d in ds[-30:])
    print(f"  7d range {l7:,.0f} – {h7:,.0f}   30d range {l30:,.0f} – {h30:,.0f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTCUSDT")
    ap.add_argument("--start", default="2022-01-01")
    ap.add_argument("--hikes", default=",".join(HIKE_DATES))
    ap.add_argument("--horizons", default="1,7,30", help="study 1, in days")
    ap.add_argument("--dips", default="3,5,8,10", help="study 2, in %% below the start close")
    ap.add_argument("--dip-horizons", default="7,30,60", help="study 2, in days")
    ap.add_argument("--post-hike-only", action="store_true",
                    help="restrict study 2 to the hike dates (regime-conditional base rate)")
    a = ap.parse_args()

    K = daily(a.symbol, a.start)
    ds = sorted(K)
    print(f"{a.symbol}: {len(ds)} hari, {ds[0]} → {ds[-1]}")
    hikes = a.hikes.split(",")
    study_hikes(K, hikes, [int(h) for h in a.horizons.split(",")])
    only = {dt.date.fromisoformat(s) for s in hikes} if a.post_hike_only else None
    study_dips(K, [float(x) for x in a.dips.split(",")],
               [int(h) for h in a.dip_horizons.split(",")], only)
    current_levels(K, a.symbol)


if __name__ == "__main__":
    main()
