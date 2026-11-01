# Macro checklist & "Fed injection" rumors — audit before acting

Trigger: user drops a bullet list of macro claims as the reason to take a position ("oil above $100, AI perps
crashing, banks dumping, VIX 4-month high, yields surging, inflation hot, war risk, AI fund blowup rumors"),
or a headline like "Fed injects $X tomorrow". The deliverable is a per-claim verdict plus a rewritten premise
— not agreement with the mood.

## 1. One number per claim, then a count

Untuk tiap poin, ambil **satu** angka live dan beri label: BENAR / SALAH / MENYESATKAN / TIDAK TERVERIFIKASI.
Tutup dengan hitungan ("3 solid, 2 salah, 2 belum terverifikasi, 1 dibesar-besarkan"). Ini jauh lebih kuat
dari membantah keseluruhan daftar sekaligus.

Cara memilih angka — di sinilah kesalahan biasanya terjadi:

- **Level vs perubahan.** Klaim "yields surging" salah kalau yield 5,08% tapi **turun 3% seminggu**. Kutip
  level, perubahan 1 minggu, dan perubahan 1 bulan; baru nilai klaimnya.
- **Indeks vs sektor.** "Banks dumping" salah kalau XLF +0,45% hari itu dan **+2,34% seminggu** — sektor bank
  justru satu-satunya yang hijau saat S&P −1,1%.
- **Intraday vs close.** "VIX 4-month high" bisa benar intraday (high 22,31) dan salah di close (19,99).
  Sebut keduanya.
- **Harga vs arus.** "AUM ETF melonjak" beda dari "arus masuk melonjak"; YTD beda dari sesi terakhir.
  Lihat `crypto-portfolio-advisory` → `references/etf-filing-catalyst-and-launch-base-rate.md`.
- **Rumor tetap rumor.** Klaim "inflasi panas" atau "AI fund blowout" tanpa print/resmi = TIDAK
  TERVERIFIKASI. Jangan dihitung sebagai bearish evidence, dan jangan dipakai sebagai alasan posisi.

Sumber angka: TradingView scanner (VIX, US10Y/2Y, WTI/Brent, DXY, SPY, XLF, gold, ES) —
`crypto-portfolio-advisory` → `references/live-market-data-sources.md` §8. Satu request, keyless.

## 2. Klaim likuiditas: bedakan injeksi dari drainase

Urutan cek, semuanya sumber primer:

1. **NY Fed desk operations** (`newyorkfed.org/markets/desk-operations/repo` dan `/reverse-repo`). Reverse repo
   **menarik** kas dari money market fund; repo **menyuntik**. Operasi Senin yang tercatat di kalender hampir
   selalu reverse repo harian, bukan rescue.
2. **Program pembelian Treasury** (`Treasury Securities Operational Details`). Reserve management purchases dan
   reinvestment purchases memang menambah reserve, tapi **rutin, sudah diumumkan di awal periode, dan kecil**.
   Angka "$8,6 miliar" yang beredar biasanya satu potong dari program bulanan $17–18 miliar + $10 miliar RMP.
3. **SOFR** (`markets.newyorkfed.org/api/rates/secured/sofr/last/10.json`). Kalau 3,87–3,89% dan stabil, tidak
   ada stress funding — apa pun kata rumor.
4. **FOMC calendar + blackout** (`federalreserve.gov/monetarypolicy/fomccalendars.htm`). Mulai Sabtu kedua
   sebelum meeting, tidak ada pejabat Fed yang bisa mengumumkan sesuatu; "injeksi mendadak" harus lewat
   operasi pasar, dan itu terlihat di angka repo lebih dulu.
5. **Skala.** Bandingkan dengan balance sheet (~$6,5T): $8,6 miliar ≈ 0,13%. Bandingkan juga dengan volume
   harian aset yang mau ditradingkan sebelum menyebutnya katalis.

Kalau benar ada injeksi darurat, tanda yang muncul lebih dulu: SOFR melonjak di atas batas atas koridor,
repo rate di atas IORB, dan RRP terkuras. Sebutkan tanda itu; kalau tidak ada, klaimnya belum nyata.

## 3. Tutup dengan premis yang sudah diperbaiki

Setelah audit, tulis ulang: "katalis yang lu tunggu tidak ada di kalender; yang menggerakkan besok adalah X, Y,
Z." Lalu sambungkan ke posisi user (kas %, beta, ukuran) — audit yang benar tapi tidak menyentuh keputusan
adalah pekerjaan setengah.

## 4. Pitfall

- **Jangan bantah pakai opini; bantah pakai satu angka per klaim.** Daftar 8 poin yang dibantah dengan 8 angka
  jauh lebih meyakinkan daripada satu paragraf "menurut gw".
- **Jangan mengulang framing sumbernya.** Postingan sosial mendaur ulang operasi rutin jadi "Fed injects $X".
  Angkanya asli, konteksnya dibuang. Selalu buka halaman operasi NY Fed untuk tanggal + tipe operasi.
- **Jangan pakai klaim yang tidak bisa diverifikasi sebagai bagian dari hitungan benar/salah.** Pisahkan ke
  kategori sendiri supaya user tahu mana yang cuma narasi.
- **Jangan menyimpulkan arah dari audit.** Audit mengubah keyakinan pada premis, bukan menghasilkan probabilitas;
  kalau user minta probabilitas, lanjut ke `crypto-portfolio-advisory` → `references/next-day-probability-base-rates.md`.
