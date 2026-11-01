# Rentang probabilitas harga dari OPSI (Deribit) — sumber kedua, selain Polymarket

Dibuat 8 Okt 2026 saat user minta "bikin probability range harga BTC". Script:
`scripts/deribit_prob_range.py` (stdlib, tanpa key). Pola ini dipakai saat pertanyaannya bukan satu
level tunggal, tapi **seluruh distribusi**: "range-nya berapa", "kemungkinan BTC di X sampai bulan Y".

## Kenapa opsi lebih kaya dari prediksi-level

Satu pasar Polymarket = satu titik ("di atas $88.000 pada 8 Okt?"). Rantai opsi = **satu titik per
strike**, jadi seluruh CDF-nya kelihatan dari satu tarikan data, plus term structure IV-nya. Ini yang
dipakai waktu user mau *range*, bukan satu odds.

## Endpoint (publik, tanpa key, jalan dari VM biasa)

| Butuh | Endpoint |
|---|---|
| Harga index | `https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd` |
| Semua IV + underlying | `/public/get_book_summary_by_currency?currency=BTC&kind=option` (`mark_iv` dalam **persen**, `underlying_price`) |
| Metadata strike/expiry | `/public/get_instruments?currency=BTC&kind=option&expired=false` |
| ETH | sama, `currency=ETH`, `index_name=eth_usd` |

`get_book_summary_by_currency` mengembalikan ~950 instrumen; **jangan** print mentah — kelompokkan per
expiry dan ambil ATM saja.

## Metode (lognormal risk-neutral)

1. `ATM strike` = strike dengan |strike − index| terkecil untuk expiry itu → `sigma = mark_iv/100`.
2. `T = (expiry − sekarang) / 365` (hari kalender, bukan hari trading).
3. `mu = ln S − sigma²T/2`, `sd = sigma·sqrt(T)` (drift 0 = risk-neutral; itu sebabnya median < spot).
4. Persentil `= exp(mu + z·sd)`; `P(S_T > K) = Phi((mu − ln K)/sd)`.
5. Sebut asumsinya: drift 0, satu sigma ATM (abaikan smile), kalender 365.

Angka acuan 8 Okt 2026 (index $82,8k; IV ATM 34,8% 1 hari → 39,2% 1 tahun):

| horizon | P5 | P25 | median | P75 | P95 |
|---|---|---|---|---|---|
| 9 Okt | 80.536 | 81.855 | 82.783 | 83.722 | 85.093 |
| 16 Okt | 76.167 | 79.953 | 82.691 | 85.523 | 89.774 |
| 30 Okt | 71.730 | 77.902 | 82.496 | 87.361 | 94.878 |
| 25 Des | 61.462 | 72.642 | 81.577 | 91.611 | 108.276 |
| 24 Sep 27 | 40.825 | 59.321 | 76.886 | 99.652 | 144.798 |

## PITFALL PALING GAMPANG SALAH: touch vs terminal

Dua pasar ini mengukur objek BEDA dan angkanya bisa kelihatan kontradiktif:

- Polymarket *"Will Bitcoin **dip to** $80,000 in October?"* → probabilitas **NYENTUH** sekali saja
  dalam bulan itu = **69,5%**.
- Distribusi **terminal** opsi untuk 30 Okt → P(harga akhir < 80k) cuma **±15%**.
- Sama juga di atas: *"reach $100k by 31 Des"* (touch) **30,5%** vs opsi terminal P(>100k) di 25 Des **±12%**.

Dua-duanya benar. Kalau dicampur dalam satu kalimat ("pasar bilang 70% BTC ke 80k, tapi opsi bilang
cuma 15%") laporannya jadi kelihatan ngawur. **Selalu tulis "nyentuh" (touch) atau "di harga itu pada
tanggal X" (terminal)**, dan bilang itu memang dua ukuran yang beda. Touch selalu > terminal, dan
jaraknya makin lebar makin jauh horizon.

## Pitfalls lain

- **Format expiry Deribit** `'8OCT26'` (hari bisa 1 digit) → `strptime(..., "%d%b%y")`. Sorting
  expiry sebagai string = salah urut; parse dulu ke datetime.
- **Expiry hari ini / besok** (`T < 0.5 hari`) hampir selalu sampah untuk distribusi (IV-nya collapse,
  P95/P5-nya nyempit tak masuk akal) — skip, jangan dilaporkan sebagai "pasar sangat yakin".
- **Basis index.** Deribit index $82.794 vs Binance spot $83.129 pada menit yang sama (±0,4%). Kalau
  user lihat spot dichartnya, sebut dua angka itu atau dia mikir kita salah ambil harga.
- **Jangan sebut ini "ramalan" atau "target".** Ini harga yang di-price pasar opsi. Labelnya
  risk-neutral / market-implied, dan sebut IV-nya supaya user bisa menilai sendiri.
- Kualitas quote: pakai `mark_iv` (fallback `bid_iv`/`ask_iv`); strike tipis bisa mark_iv aneh —
  karena kita cuma pakai ATM, risikonya kecil, tapi jangan mengklaim presisi dari satu strike.

## Cara melaporkan (bentuk yang dipakai user)

1. Angka spot + jam fetch + jumlah instrumen ("950 opsi, live 10:44 WIB").
2. Tabel horizon × P5/P25/median/P75/P95 — **tabelnya yang dibaca, bukan prosa**.
3. Baca cepat 2–3 baris: "sampai 30 Okt 50% kemungkinan di 77,9k–87,4k; 90% di 71,7k–94,9k".
4. Sebut IV naik seiring horizon (35% → 39%), artinya pasar tidak makin yakin, makin lama makin lebar.
5. Cek silang ke Polymarket untuk level spesifik, dengan label touch/terminal.
6. Satu baris asumsi + apa yang bisa menggesernya (CPI 14 Okt, FOMC 28 Okt).
