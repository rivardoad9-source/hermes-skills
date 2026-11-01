# "Hike = bearish ya?" dan "DCA sekarang atau tunggu turun?" — base rate yang terukur (17 Sep 2026)

Dua pertanyaan operator yang dijawab di sesi ini. Keduanya dijawab dari **data terukur + odds pasar +
level invalidasi**, bukan ramalan arah. Script: `scripts/base_rates_and_dip_sim.py`.

## 0. Langkah pertama selalu: odds pasar, bukan opini

Operator: *"suku bunga kan naik nih, berarti ekspektasi gw neutral ke bearish ya"*.
Jawab dulu apa yang **di-price pasar** (lihat `fomc_odds_watch.py --dry-run`, cron `b7cd755145b5`):

| bucket | peluang (17 Sep 2026, market `Fed Decision in October?`) |
|---|---|
| tahan | **54,5%** |
| hike +25bp | **45,5%** |
| cut −25bp | **1,1%** |
| ekspektasi | **+11,3 bp** (naik +1,2 poin sejak pesan terakhir) |

Bacaan yang benar: **"neutral" dari sisi likuiditas = bener** (cut dihargai ~nol → tidak ada tailwind),
tapi **"hike udah kelar" = salah** (hike berikutnya masih ~46%, bukan kasus dasar). Koreksi premisnya
lebih penting daripada setuju/tidak setuju.

## 1. Base rate setelah Fed hike (11 hike, 2022-03-16 → 2023-07-26, BTC, kontrak berjangka 1d)

| horizon | median | mean | naik |
|---|---|---|---|
| +1 hari | −0,48% | −0,87% | 4/11 |
| +7 hari | **−3,24%** | −5,50% | 3/11 |
| +30 hari | **−6,14%** | −6,24% | 3/11 |

Sebaran +7d: **+4,3%** (Mar 2022) sampai **−26,7%** (Mei 2022). Jadi lean bearish memang didukung,
tapi itu distribusi — bukan trade. Caveat regime wajib disebut: 2022 = hike bareng QT + kredit macet
(Luna/3AC); sekarang bukan apple-to-apple.

## 2. Simulasi "tunggu turun" vs "beli sekarang" (BTC, 2022-01-01 → 2026-09-17, 1.839 hari)

`--dips 3,5,8,10 --dip-horizons 7,30,60` (semua hari mulai):

| dip | H | kena | rata² selisih harga masuk | nunggu lebih murah |
|---|---|---|---|---|
| −3% | 7h | 66% | **−0,28%** | 71% |
| −5% | 7h | 43% | −0,03% | 58% |
| −3% | 30h | 83% | **+0,57%** | 84% |
| −5% | 30h | 70% | **+1,02%** | 72% |
| −5% | 60h | 80% | **+1,81%** | 80% |

**Ini temuan intinya (dan yang paling sering salah dibaca):** di 72–84% kasus menunggu memang dapat
harga lebih murah, **tapi rata-ratanya lebih MAHAL** — karena yang merugikan bukan yang sering, tapi
yang jarang: 16–28% kasus harga kabur naik sebelum limit kena. Keuntungan kecil yang sering, kerugian
besar yang jarang. Selalu cetak **median dan mean bersama-sama**; satu angka saja bisa dibalik maknanya.

Subset **pasca-hike** (regime sekarang, `--post-hike-only`, n=11):

| dip | H | kena | rata² masuk |
|---|---|---|---|
| −3% | 30h | 82% | **−2,10%** |
| −5% | 30h | 82% | **−3,74%** |
| −8% | 30h | 73% | −5,59% |

Pasca-hike "nunggu" menang lebih tegas — konsisten dengan tabel di §1. Tapi n=11: sebut angkanya.

## 3. Bentuk jawaban yang dipakai (dan yang TIDAK dipakai)

Jangan pilih binary "beli sekarang vs tunggu" — itu kalah di 2 dari 10 kasus tanpa perlu. Yang dipakai:

- **50–60% modal → DCA terjadwal** (mis. 4 tranche mingguan, jalan apa pun harganya). Ini yang
  menyelamatkan di skenario "harga kabur naik".
- **40–50% → limit bertingkat** di level dari script (`current_levels()`): BTC 76.180 → −2% 74.660 ·
  −5% 72.370 · −9% 69.320 · −16% 63.990; konteks: 7d low 74.968, 30d low 64.166, 30d high 82.300.
  Level 30d low = batas "bukan dip lagi, ini regime change".
- **Tanpa leverage**, dengan alasan terukur: funding perp saat itu cuma **+0,0084%/8 jam (~9%/tahun)**
  = long tidak menumpuk, tidak ada urgensi ikut posisi orang.
- **Level invalidasi untuk tesis**, bukan cuma satu arah: bearish terkonfirmasi kalau close di bawah
  7d low; tesis bearish BATAL kalau tahan di atas 7d high; trigger dari sisi rate = odds hike >60%
  (headwind beneran) atau <30% (takut tightening luntur = justru bullish risk).
- **Akui edge arah kita memang 45%** (terukur, window 1 jam pasca-rilis) → "gw nggak tau arahnya,
  karena itu pembagian ini" adalah jawaban yang jujur dan diterima, bukan kelemahan.

## 4. Yang juga harus ikut dilaporkan: reaksi tape vs cerita

FOMC Sep 2026 (hike +25bp pertama sejak 2023, target 3,75–4,00%) — reaksi BTC dari rilis 01:00 WIB:
open 75.770 → close candle 75.798 · +15m 76.015 · +1h 75.950 · +4h 75.892 · ~8 jam 76.396 (**+0,83%**),
rentang sejak rilis 75.065–76.774. Artinya "hike = dump" bukan yang tape bilang — yang pasar hadiahkan
bukan suku bunganya, tapi guidance-nya. **Sebut kontradiksi ini sebelum menyimpulkan**, jangan
mengarang penjelasan yang membuat tape cocok dengan teori.

## 5. Pitfall teknis

- **Histori klines butuh `startTime` berhalaman.** `limit` maksimum 1000 baris; `interval=1d&limit=400`
  hanya menjangkau ~13 bulan ke belakang → tanggal lama balik KOSONG, lalu formatter mati di `None`
  (`TypeError: unsupported format string passed to NoneType.__format__`). Halaman dengan `startTime`
  sampai halaman pendek; cek span yang dicetak (2022-01-01 → sekarang = 1.839 baris).
- Jam keputusan FOMC 18:00 UTC masuk ke candle harian UTC hari itu — untuk reaksi intraday pakai
  `interval=1h`/`15m` dengan `startTime` eksplisit (release − 6 jam), bukan 1d.
- Angka ini **base rate**, bukan hasil backtest berbiaya: tidak ada slippage/gas. Kalau dipakai untuk
  mesin trading, sebut bedanya.
- Data yang gagal dari host ini dan jangan diklaim: DXY (stooq diblokir, Yahoo 429), US10Y.
  Yang jalan: `api.binance.com` klines/ticker, `fapi.binance.com` premiumIndex (funding), Polymarket
  gamma-api, FRED (key di `~/NewsAgent/.env`).
