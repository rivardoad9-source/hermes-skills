#!/usr/bin/env python3
"""Release-hour reaction study from Binance 1h klines (keyless) — the measurement half of
"predict lu gmn" / "harganya udah price in".

Method: base = the OPEN of the release-hour candle; then +1h / +4h / +24h closes and the
release-hour high-low range. Then stats: mean |move| per horizon, direction counts, hit rate,
range vs a baseline set of ordinary hours.

Clocks (verify per event from the primary venue — a wrong timestamp invalidates the answer):
  FOMC minutes AND decisions : 14:00 ET = 18:00 UTC = 01:00 WIB   (--hour 18, default)
  CPI / PPI / NFP            : 12:30 UTC = 19:30 WIB              (--hour 12)

Usage:
  python3 release_reaction_study.py                                  # default: FOMC minutes 2026
  python3 release_reaction_study.py --set decisions                  # FOMC decisions 2026
  python3 release_reaction_study.py --set both                       # minutes vs decision, side by side
  python3 release_reaction_study.py --dates 2026-10-14 --hour 12     # ad-hoc CPI/NFP
  python3 release_reaction_study.py --dates 2026-06-17 --symbol ETHUSDT
  python3 release_reaction_study.py --no-baseline                    # skip the ordinary-hour control

Stdlib only (json/urllib/argparse/datetime/statistics) — runs on plain python3 from a server IP.
"""
import argparse
import datetime as dt
import json
import statistics as st
import urllib.request

KLINE = ("https://api.binance.com/api/v3/klines?symbol={sym}&interval=1h"
         "&startTime={st}&endTime={et}&limit=100")
# Fallback host if the primary is geo-blocked: data-api.binance.vision

# 2026 sets (dates the RELEASE happened, not the meeting). Extend as the year progresses.
MINUTES_2026 = [("18 Feb 2026", "2026-02-18"), ("8 Apr 2026", "2026-04-08"),
                ("20 Mei 2026", "2026-05-20"), ("8 Jul 2026", "2026-07-08"),
                ("19 Agt 2026", "2026-08-19")]
DECISIONS_2026 = [("18 Mar 2026", "2026-03-18"), ("17 Jun 2026", "2026-06-17"),
                  ("16 Sep 2026", "2026-09-16")]
BASELINE = [("3 Mar 2026", "2026-03-03"), ("14 Jul 2026", "2026-07-14"),
            ("25 Agt 2026", "2026-08-25"), ("22 Sep 2026", "2026-09-22"),
            ("29 Sep 2026", "2026-09-29")]


def klines(sym, release_utc, hours=30):
    st_ms = int(release_utc.timestamp() * 1000)
    url = KLINE.format(sym=sym, st=st_ms, et=st_ms + hours * 3600 * 1000)
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    return json.load(urllib.request.urlopen(req, timeout=25))


def study(label, date_str, hour_utc=18, sym="BTCUSDT"):
    """Return (label, base, p1, p4, p24, range1h) or None when the candle is missing."""
    rel = dt.datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=hour_utc, tzinfo=dt.timezone.utc)
    try:
        k = klines(sym, rel)
    except Exception as e:                                  # network/geo problem — say so, don't fake it
        print(f"  {label:14} FETCH FAILED: {e}")
        return None
    idx = None
    for i, c in enumerate(k):
        ct = dt.datetime.fromtimestamp(c[0] / 1000, dt.timezone.utc)
        if ct.hour == hour_utc and ct.day == rel.day and ct.month == rel.month:
            idx = i
            break
    if idx is None or idx + 24 >= len(k):
        print(f"  {label:14} candle rilis tidak ketemu / data 24h belum lengkap")
        return None
    base = float(k[idx][1])
    p = lambda n: (float(k[idx + n][4]) / base - 1) * 100
    rng = (float(k[idx][2]) - float(k[idx][3])) / base * 100
    print(f"  {label:14} base ${base:>10,.0f} | +1h {p(1):>+6.2f}% | +4h {p(4):>+6.2f}% "
          f"| +24h {p(24):>+6.2f}% | range 1 jam {rng:>5.2f}%")
    return (label, base, p(1), p(4), p(24), rng)


def stats(rows, name):
    if not rows:
        print(f"=== {name}: no data ===")
        return
    h1 = [abs(r[2]) for r in rows]
    h4 = [abs(r[3]) for r in rows]
    h24 = [abs(r[4]) for r in rows]
    rng = [r[5] for r in rows]
    up = sum(1 for r in rows if r[4] > 0)
    dn = sum(1 for r in rows if r[4] < 0)
    flat = len(rows) - up - dn
    hit = max(up, dn) / len(rows) * 100
    print(f"=== {name} (n={len(rows)}) ===")
    print(f"  |move| 1 jam  : rata2 {st.mean(h1):.2f}%  (median {st.median(h1):.2f}%)")
    print(f"  |move| 4 jam  : rata2 {st.mean(h4):.2f}%")
    print(f"  |move| 24 jam : rata2 {st.mean(h24):.2f}%  (median {st.median(h24):.2f}%)")
    print(f"  arah 24 jam   : {up} naik / {dn} turun / {flat} flat  ->  hit rate {hit:.0f}% "
          f"(koin = 50%)")
    print(f"  range 1 jam   : rata2 {st.mean(rng):.2f}%  min {min(rng):.2f}% max {max(rng):.2f}%")
    return dict(n=len(rows), h1=st.mean(h1), h4=st.mean(h4), h24=st.mean(h24),
                rng=st.mean(rng))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTCUSDT")
    ap.add_argument("--hour", type=int, default=18, help="UTC hour of the release (FOMC=18, CPI=12)")
    ap.add_argument("--set", choices=["minutes", "decisions", "both"], default="minutes")
    ap.add_argument("--dates", nargs="*", default=None, help="YYYY-MM-DD list (label = date)")
    ap.add_argument("--no-baseline", action="store_true", help="skip ordinary-hour control")
    a = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=7)
    print(f"FETCH {now.strftime('%Y-%m-%d %H:%M WIB')} | {a.symbol} | release hour {a.hour}:00 UTC")
    print()

    groups = []
    if a.dates:
        groups.append((f"AD-HOC ({a.hour}:00 UTC)", [(d, d) for d in a.dates]))
    else:
        if a.set in ("minutes", "both"):
            groups.append(("FOMC MINUTES", MINUTES_2026))
        if a.set in ("decisions", "both"):
            groups.append(("FOMC DECISIONS", DECISIONS_2026))

    summ = []
    for name, dates in groups:
        print(f"=== {name} ===")
        rows = [r for r in (study(lbl, d, a.hour, a.symbol) for lbl, d in dates) if r]
        print()
        s = stats(rows, name)
        if s:
            summ.append((name, s))
        print()

    if not a.no_baseline and not a.dates:
        print("=== ORDINARY HOURS (control) ===")
        rows = [r for r in (study(lbl, d, a.hour, a.symbol) for lbl, d in BASELINE) if r]
        print()
        base = stats(rows, "ordinary hour")
        print()
        if base and summ:
            for name, s in summ:
                d = s["rng"] - base["rng"]
                verdict = ("NOT more volatile than an ordinary hour"
                           if abs(d) < 0.35 else "materially noisier than an ordinary hour")
                print(f"  {name}: release-hour range {s['rng']:.2f}% vs ordinary {base['rng']:.2f}% "
                      f"({d:+.2f} pts) -> {verdict}")
        print()

    print("Baca: report the RANGE and the hit rate, never a direction call. Then test a 'priced in'")
    print("claim by comparing the realized |move| against the market's own implied IQR half-width")
    print("(scripts/price_ladder_distribution.py) for that date: inside the band = claim survives.")


if __name__ == "__main__":
    main()
