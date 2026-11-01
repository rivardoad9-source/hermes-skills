# Implied distribution dari tangga strike harian (BTC) — dan pakai buat jawab "arahnya kemana"

Dipakai 16 Sep 2026 untuk menjawab "BTC arahnya kemana" tanpa opini. Cara ini mengubah
"menurut saya naik/turun" jadi **distribusi yang di-price pasar**, plus level invalidasi.

## 1. Ambil tangga strike (gamma-api, tanpa key)

```python
# AKTIF: public-search  (JANGAN pakai /markets?question=... -> return 0 / filter diabaikan)
d = get("https://gamma-api.polymarket.com/public-search?q=Bitcoin%20above&limit_per_type=60")
for ev in d["events"]:
    for m in ev["markets"]:
        q = m["question"]          # "Will the price of Bitcoin be above $76,000 on September 17?"
        strike = float(mt.group(1).replace(",", ""))   # regex: r"above \$([\d,]+) on (\w+) (\d+)\?"
        p_yes  = dict(zip(json.loads(m["outcomes"]), json.loads(m["outcomePrices"])))["Yes"]
```

Hasil 16 Sep 2026: 11 rung per hari ($68k–$88k, step $2k), volume 24h $60k–$160k per rung
untuk hari berjalan. Tangga tersedia sampai ~1 minggu ke depan.

## 2. Ubah tangga jadi CDF, lalu baca median/IQR

- `P(BTC > X)` = interpolasi linear antar rung (`x` = strike, `y` = p_yes).
- `level_at(p)` = invers: interpolasi di tangga terbalik (`x` = p_yes, `y` = strike).
- Yang dilaporkan ke user: **median, Q1/Q3 (IQR), dan band 5%/95%**, plus `P(> spot)`.

Contoh output nyata (spot $75.700, 16 Sep 21:30 WIB):

| tanggal | median | IQR (50% tengah) | P(>spot) |
|---|---|---|---|
| 17 Sep | $75.727 | $74.363–$77.194 (3,7%) | 50,5% |
| 18 Sep | $75.746 | $74.159–$77.424 (4,3%) | 50,7% |
| 20 Sep | $75.811 | $73.881–$77.800 (5,2%) | 51,5% |

**Bacaan:** pasar memberi ~50:50 soal **arah**, tapi tegas soal **lebar gerakan** (IQR 3,7%
→ 5,2% makin jauh tanggal). Ini konsisten dengan temuan NewsAgent (24 kombinasi
indikator × aset × horizon = `NO_EDGE_DETECTED` untuk arah). Jadi: laporkan rentang +
level, jangan ramalan arah.

## 3. Track record keputusan FOMC (base rate, bukan opini)

```python
# HISTORIS: pakai closed=true + order=volumeNum, filter client-side "Fed" + tahun
get("https://gamma-api.polymarket.com/markets?limit=200&closed=true&order=volumeNum&ascending=false")
```

Bucket per meeting ("Fed increases interest rates by 25+ bps after <Month> <Year> meeting?",
"No change...", "Fed decreases...") → `outcomePrices` pasca-resolusi = `[1,0]`/`[0,1]`.
Hasil 16 Sep 2026: **9 keputusan terakhir (Jan 2025 → Jan 2026) bucket favorit pasar
menang 9/9** → keputusannya "aman", reaksinya yang tidak.

## 4. Pitfall yang benar-benar kejadian

1. `/markets?question=<teks>` **tidak** memfilter → balikin 0 hasil. Pakai `public-search`
   untuk yang aktif, `closed=true&order=volumeNum` lalu filter di Python untuk yang historis.
2. Tanggal yang sudah lewat bisa balikin `Yes=100%`/`No=0%` (artefak menjelang resolusi) →
   kuantil jadi ngawur (median $78.000 padahal spot $75.700). **Skip tanggal lampau**,
   atau cek `volume24hr` dulu.
3. Resolusi market harian ini pakai **snapshot harga** sesuai aturan pasarnya, bukan close
   harian Binance. Sebut caveat itu; jangan jadikan angkanya "target harga".
4. Data pendukung yang **gagal** ditarik dari server ini (jangan diklaim): **DXY (stooq
   diblokir, Yahoo 429)** dan **US10Y**. Yang jalan: Binance spot klines, Binance fapi
   (`fundingRate`, `openInterest`, `openInterestHist`, `globalLongShortAccountRatio`,
   `takerlongshortRatio`), FRED (key di `~/NewsAgent/.env`, seri `DFEDTARU` untuk step
   suku bunga), dan `defillama`.
5. Lengkapi selalu dengan positioning nyata — funding, OI 7 hari, long/short retail,
   taker buy/sell — supaya "semua orang yakin X" bisa diuji: 16 Sep 2026 funding cuma
   +0,0058%/8 jam (~+6,3%/tahun, tidak ekstrem) dan retail L/S 1,82 → tidak ada bahan squeeze.
