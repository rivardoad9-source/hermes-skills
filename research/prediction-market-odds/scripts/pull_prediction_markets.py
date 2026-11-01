#!/usr/bin/env python3
"""Pull live prediction-market odds + a realized price path, for probability questions.

Usage:
    python3 pull_prediction_markets.py                      # top macro/Fed markets + BTC/ETH/SOL
    python3 pull_prediction_markets.py fed rate cut          # filter markets by keywords
    python3 pull_prediction_markets.py --symbol ETHUSDT      # different spot symbol
    python3 pull_prediction_markets.py --days 30             # longer daily path

No API key. Env: HTTP_PROXY etc. are respected by urllib (nothing here needs auth).
Output is plain text meant to be pasted into an answer with its fetch timestamp.
"""
import argparse
import datetime as dt
import json
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}
DEFAULT_KEYWORDS = ("fed", "rate cut", "rate hike", "fomc", "interest rate", "cpi", "inflation", "recession")


def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def polymarket(keywords, limit=80, show=10):
    """Print markets whose question matches any keyword, plus every bucket of the top event."""
    print("== POLYMARKET (gamma-api, no key) ==")
    try:
        markets = get(f"https://gamma-api.polymarket.com/markets?limit={limit}&active=true&closed=false&order=volume24hr&ascending=false")
    except Exception as exc:  # network/geo — report, don't guess
        print(f"  FAILED: {exc}")
        return []
    hits = [m for m in markets if any(k in (m.get("question") or "").lower() for k in keywords)]
    if not hits:
        print(f"  no market matched {keywords!r} in the top {limit} by 24h volume")
    for m in hits[:show]:
        prices, outcomes = m.get("outcomePrices"), m.get("outcomes")
        try:
            prices = json.loads(prices) if isinstance(prices, str) else prices
            outcomes = json.loads(outcomes) if isinstance(outcomes, str) else outcomes
        except Exception:
            pass
        pairs = ", ".join(f"{o}={float(p)*100:.1f}%" for o, p in zip(outcomes or [], prices or []))
        print(f"  - {m.get('question')}")
        print(f"      {pairs or prices}")
        print(f"      vol24h={m.get('volume24hr')} resolves={m.get('endDate')}")
    return hits


def binance(symbol, days):
    """Spot last price + daily closes, trying the public hosts in order."""
    print(f"\n== {symbol} (Binance public REST) ==")
    for host in ("https://api.binance.com", "https://data-api.binance.vision"):
        try:
            t = get(f"{host}/api/v3/ticker/24hr?symbol={symbol}")
            print(f"  last={t['lastPrice']}  24h={t['priceChangePercent']}%  high={t['highPrice']} low={t['lowPrice']}")
            k = get(f"{host}/api/v3/klines?symbol={symbol}&interval=1d&limit={days}")
            prev = None
            for row in k:
                day = dt.datetime.utcfromtimestamp(row[0] / 1000).strftime("%m-%d")
                close = float(row[4])
                chg = "" if prev is None else f"{(close / prev - 1) * 100:+.2f}%"
                print(f"  {day}  {close:>12,.2f}  {chg}")
                prev = close
            return
        except Exception as exc:
            print(f"  {host} failed: {exc}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords", nargs="*", default=None, help="market question keywords (default: macro set)")
    ap.add_argument("--symbol", default="BTCUSDT")
    ap.add_argument("--days", type=int, default=14)
    args = ap.parse_args()

    stamp = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print(f"fetched {stamp}  (quote this timestamp — odds move within minutes of a data print)\n")
    keywords = tuple(k.lower() for k in (args.keywords or DEFAULT_KEYWORDS))
    polymarket(keywords)
    binance(args.symbol, args.days)
    print("\nreminder: pull EVERY bucket of the same event (cut/hold/hike) before interpreting, "
          "and state any feed you could not reach instead of implying a driver you did not measure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
