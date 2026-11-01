#!/usr/bin/env python3
"""Daily "Will the price of <asset> be above $X on <date>?" ladder -> implied distribution.

Why this exists: a single odds bucket answers "will X happen"; a LADDER answers "where is the
price going", which is the question a trader actually asks ("menurut lu arahnya kemana"). Run
this before answering a direction question with opinion.

Usage:
    python3 price_ladder_distribution.py                      # Bitcoin, prints all upcoming dates
    python3 price_ladder_distribution.py --asset Bitcoin --spot 75700
    python3 price_ladder_distribution.py --asset Ethereum --days 2026-09-17 2026-09-20

Output per date: quantile levels (5/25/50/75/95%), IQR as % of spot, P(> spot), and a strike table.

Pitfalls baked in (all hit for real on 16 Sep 2026):
  * /markets?question=<text> does NOT filter server-side -> use public-search, then regex the
    question string yourself.
  * A date that has already passed can return Yes=100%/No=0% as a settlement artifact -> those
    quantiles are garbage (median $78k against a $75.7k spot). Past dates are skipped.
  * Daily markets resolve on a price SNAPSHOT per each market's rules, not the exchange daily
    close -> report it as a distribution, never as a price target.
Stdlib only; no key; works from a plain VM.
"""
import argparse
import json
import re
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
SEARCH = "https://gamma-api.polymarket.com/public-search?q={q}&limit_per_type=60"


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def pull_ladder(asset):
    """-> {iso_date: {strike: p_yes}} from every active '... be above $X on <Month> <D>?' market."""
    ladder = {}
    terms = [f"{asset} above", f"price of {asset} above", f"{asset} above $"]
    qre = re.compile(r"above \$([\d,]+) on ([A-Z][a-z]+) (\d{1,2})\?", re.I)
    for term in terms:
        try:
            payload = get(SEARCH.format(q=urllib.parse.quote(term)))
        except Exception as exc:  # network hiccup on one term shouldn't kill the run
            print(f"  ! search '{term}' failed: {type(exc).__name__}: {exc}")
            continue
        for ev in payload.get("events") or []:
            for m in ev.get("markets") or []:
                q = m.get("question") or ""
                if asset.lower() not in q.lower():
                    continue
                mt = qre.search(q)
                if not mt:
                    continue
                strike = float(mt.group(1).replace(",", ""))
                try:
                    month = datetime.strptime(mt.group(2)[:3], "%b").month
                    year = datetime.now(timezone.utc).year
                    day = date(year, month, int(mt.group(3))).isoformat()
                    prices = dict(zip(json.loads(m.get("outcomes") or "[]"),
                                      json.loads(m.get("outcomePrices") or "[]")))
                    p = float(prices["Yes"])
                except Exception:
                    continue
                ladder.setdefault(day, {})[strike] = p
    return ladder


def p_above(ladder, target):
    pts = sorted(ladder.items())
    if not pts:
        return None
    if target <= pts[0][0]:
        return pts[0][1]
    if target >= pts[-1][0]:
        return pts[-1][1]
    for (s1, p1), (s2, p2) in zip(pts, pts[1:]):
        if s1 <= target <= s2:
            return p1 if s2 == s1 else p1 + (target - s1) / (s2 - s1) * (p2 - p1)
    return None


def level_at(ladder, p_target):
    pts = sorted((p, s) for s, p in ladder.items())
    lo = [x for x in pts if x[0] <= p_target]
    hi = [x for x in pts if x[0] >= p_target]
    if not lo:
        return pts[0][1]
    if not hi:
        return pts[-1][1]
    p1, s1 = lo[-1]
    p2, s2 = hi[0]
    return s1 if p2 == p1 else s1 + (p_target - p1) / (p2 - p1) * (s2 - s1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asset", default="Bitcoin")
    ap.add_argument("--spot", type=float, default=None,
                    help="reference spot (else Binance BTCUSDT is fetched)")
    ap.add_argument("--days", nargs="*", default=None, help="ISO dates to report; default = all future")
    args = ap.parse_args()

    spot = args.spot
    if spot is None:
        sym = "BTCUSDT" if args.asset.lower().startswith("bit") else "ETHUSDT"
        try:
            spot = float(get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}")["price"])
        except Exception as exc:
            print(f"! could not fetch spot for {sym}: {exc}")
    print(f"asset={args.asset}  spot={spot}  fetched={datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}")

    ladder = pull_ladder(args.asset)
    today = date.today().isoformat()
    days = args.days or sorted(d for d in ladder if d >= today)
    for day in days:
        L = ladder.get(day) or {}
        rungs = sorted(L.keys())
        print(f"\n===== {day}  ({len(rungs)} rungs: {min(rungs):,.0f}-{max(rungs):,.0f}) =====" if rungs
              else f"\n===== {day}  (no ladder) =====")
        if not rungs:
            continue
        if day < today:
            print("  SKIPPED — past date, prices are settlement artifacts")
            continue
        q = {p: level_at(L, p) for p in (0.95, 0.75, 0.50, 0.25, 0.05)}
        print(f"  5% < ${q[0.95]:,.0f} | 25% < ${q[0.75]:,.0f} | median ${q[0.50]:,.0f} "
              f"| 75% < ${q[0.25]:,.0f} | 95% < ${q[0.05]:,.0f}")
        if spot:
            print(f"  median vs spot {(q[0.50] / spot - 1) * 100:+.1f}%   "
                  f"IQR ${q[0.75]:,.0f}-${q[0.25]:,.0f} ({(q[0.25] - q[0.75]) / spot * 100:.1f}% wide)")
            pu = p_above(L, spot)
            print(f"  P(above spot) = {pu * 100:.1f}%   ->  P(below) = {(1 - pu) * 100:.1f}%")
        for s in rungs:
            print(f"     P(> ${s:,.0f}) = {L[s] * 100:5.1f}%")
    print("\nReminder: quote the fetch time; report the RANGE (IQR) and invalidation levels, "
          "not a point forecast — our own event study shows no directional edge after macro prints.")


if __name__ == "__main__":
    main()
