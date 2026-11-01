# Klaim milestone protokol ("BREAKING: TVL/volume/holders all-time high")

Trigger: user nempel headline/PR/tweet berbentuk *"<protokol> hits all-time high of $X in TVL
across N assets"*, *"cumulative volume $Y"*, *"holders naik Z%"* — biasanya sambil megang token
protokol itu. Deliverable: angkanya real atau nggak, **apakah sudah di harga**, dan apakah
pertumbuhan itu nyambung ke token yang dipegang user.

Bedakan dari `onchain-flow-alarm-claims.md` (itu soal transfer wallet yang di-frame sebagai
distribusi). Yang ini soal **metrik pertumbuhan platform**.

## Checklist 5 langkah (worked case: Ondo Stocks $1,26B TVL, 1 Okt 2026)

1. **Verifikasi angkanya — akui duluan kalau real.** Cari sumber primer: tweet akun resmi
   (`api.fxtwitter.com/<screen>/status/<id>` → `.created_at`, `.likes`, `.views`), PR protokol,
   lalu liputan media. Kasus: post @Ondo 30 Sep 2026 17:24 UTC — "$1,26B+ TVL, 450+ tokenized
   stocks & ETFs, $28B cumulative volume" (908 likes, 42,5k views) + PR/blog Ondo + Crypto
   Briefing. Angka real. **Jangan mulai dari kritik** — mulai dari "angkanya bener".
2. **Sudah di harga? Ambil candle di sekitar jam rilis.** `api.binance.com/api/v3/klines?symbol=
   <SYM>USDT&interval=4h&limit=12` (keyless) sudah cukup. Kasus: candle 4 jam yang **memuat**
   pengumuman malah merah ($0,5015 → $0,4898, low $0,4773); lonjakan 7d +21,7% / 30d +46,1%
   kejadian **sebelum** rilis. Kalau begitu, headline = **bukan edge**. Saran entry: tunggu
   pullback ke MA20 daripada ngejar di harga yang +15% di atas MA20.
3. **TVL ≠ hak token (langkah yang paling sering dilewat).** Cek siapa yang menerima feenya:
   cari "fee switch", revenue share, buyback, burn. Kasus Ondo: fee produk ~$57,9M/tahun,
   revenue protokol ~$11,5M, **yang sampai ke pemegang ONDO $0**; fee switch belum di-vote; nggak
   ada buyback/burn; treasury di Foundation. Tanpa langkah ini lu bakal nyaranin user beli
   "pertumbuhan" yang nggak terhubung ke arus kas token. Sebut sumbernya sebagai laporan pihak
   ketiga (audit/blog + DefiLlama), jangan jadi fakta sendiri.
4. **Kualitas pertumbuhan: turnover, bukan cuma level.** Banding dua rilis berbeda waktu:
   kasus TVL $1,01B (15 Agu) → $1,26B (30 Sep) = **+24,7%**, tapi cumulative volume cuma
   $27B → $28B → rasio volume/TVL turun 26,7× → 22,2×. Fee datang dari **aktivitas**, jadi
   revenue ketinggalan dari TVL. Prasyarat: definisi metrik harus sama di dua rilis — kalau nggak,
   tulis "kalau definisinya sama".
5. **Banding sama beban supply terjadwal.** Unlock 18 Jan 2027 (1,71B ONDO ≈ $870M) = **69% dari
   seluruh TVL Ondo Stocks**. Event supply terjadwal hampir selalu mengalahkan angka headline.

## Konteks harga vs aset yang dikelola

`mcap ÷ TVL platform` = harga yang user bayar per dolar aset yang dikelola. Kasus: mcap ONDO
$2,49B vs TVL Ondo Stocks $1,26B → **~2×**; vs total distributed value Ondo ($3,62B, RWA.xyz) →
0,69×. Angka ini yang bikin "premi narasi" jadi kuantitatif, bukan opini.

## Aksi buat holder (jangan cuma jadi esai)

1. Rencana lama nggak berubah: cap posisi (ONDO ≤12% porto) + trim sebelum tanggal unlock.
2. Headline **bukan** alasan menambah. Kalau user tetap mau nambah karena narasi, sebut eksplisit:
   ini trade **narasi/momentum**, bukan cash-flow — sizing-nya harus ngikutin itu.
3. Jangan dismiss tesisnya: sektor RWA tokenized equities memang tumbuh (450+ aset, ~70% market
   share, izin EU/EEA ~30 negara, filing SEC, partnership JPM/Mastercard/Ripple). Bedakan
   **"tesis valid"** dari **"token-nya dapet arus kas"** — itu dua hal, dan user sering
   menyamakannya.

## Pitfall

- Jangan pakai DefiLlama sebagai sumber tunggal untuk TVL protokol: 1 Okt 2026 listing
  `ondo-global-markets` di DefiLlama kebaca **$0** padahal PR + RWA.xyz bilang $1,26B. Kalau
  ada yang nol/kosong, bilang "nggak kebaca dari sini" dan pakai sumber lain.
- CoinGecko free tier gampang 429 di sesi yang banyak manggil — fallback ke Binance
  (`api.binance.com/api/v3/ticker/24hr`, `/klines`) buat harga & 7d/30d internal.
- Anchoring 7d beda sumber: Binance `klines` (close 7 candle lalu) vs CoinGecko (168 jam) bisa
  beda jauh di token yang baru spike (kasus ONDO: −2% vs +21,7%). Sebut anchor mana yang dipakai,
  atau pakai 24h + 30d sebagai angka utama.
- "Cumulative volume" di rilis lama vs baru bisa beda definisi (CEX+DEX+mint/redeem) — jangan
  banding tanpa catatan.

## Varian: milestone institusi (bursa/kliring) di-call sebagai keranjang koin

Shape pertanyaannya: "narasi X, ada yang call, koinnya A, B, C". Institusinya nyata dan PR-nya nyata —
yang diuji bukan PR-nya, tapi **apakah call-nya masih segar, siapa penerima alirannya, dan apakah
harganya belum jalan**. Filter cepat yang bisa langsung dilempar balik ke user: ada kejadian baru
bertanggal dalam 7 hari? harganya udah gerak sebelum dia masuk? koin yang dia beli itu penerima
alirannya, atau cuma tetangga ceritanya?

1. **Timeline bertanggal dari newsroom institusinya sendiri.** Susun PR → pilot → launch penuh dari
   situs resmi (halaman press-release + halaman program), bukan dari agregator, thread, atau judul
   video YouTube/IG — yang terakhir sering salah tanggal dan sering mengarang kaitan. Klasifikasi
   hasilnya: PRE / katalis baru / POST. PR pengumuman yang umurnya berbulan-bulan = daur ulang;
   launch yang baru jalan dan belum ada angka volume = infrastruktur, bukan trade.
2. **Uji penerima aliran, bukan daftar sebutan.** Tanya: jaringan/produk siapa yang dapet fee dari
   aktivitas itu. Kalau koin penerimanya tidak listed di venue yang user pakai, katakan eksplisit
   bahwa **yang di-call itu proksi** — koin yang cuma nyempil di daftar "colongan bisa masuk".
   "Disebut di PR/thread" ≠ "menerima arus kas".
3. **Uji harga satu keranjang, sekali panggil.** Satu `GET /api/v3/ticker/24hr` (tanpa param
   `symbols`, filter `.endswith("USDT")`) + `klines` 1d untuk 7d → tabel per koin: harga, 24j, 7d,
   volume, plus funding futures. Keranjang yang flat sampai turun 7d padahal katalisnya diumumkan di
   periode yang sama = pasar sudah melewatinya. Tulis angkanya; jangan bilang "belum naik".
4. **Katalis yang jatuh tempo belakangan diberi label sebagai katalis jauh.** Aset yang baru masuk
   venue lain 6–9 bulan lagi bukan alasan masuk hari ini — sebut tanggalnya dan turunkan bobotnya
   (lihat freshness ladder di skill `crypto-narrative-scan` → `references/catalyst-and-flow-verification.md`).
5. **Jawab lawan level milik user sendiri.** Sebelum nyebut level baru, cek yang sudah ada:
   `ls ~/.hermes/scripts/*watch*.py ~/.hermes/scripts/*alert*.py`+ nama job di `~/.hermes/cron/jobs.json`.
   Kalau dia sudah punya watcher level untuk token itu, kutip level itu dan nyatakan narasinya tidak
   mengubah rencananya (posisi leverage tinggi = taruhan, bukan tesis — bilang begitu di depan).

Worked shape (RWA/tokenisasi, DTCC Tokenization Service): PR multi-chain ke Stellar umur ~4,5 bulan,
pilot produksi terbatas, launch penuh bulan berjalan; venue yang beneran dipakai (Canton/CC) tidak
listed di Binance, sementara keranjang yang di-call (ONDO, XLM, LINK, AVAX) flat sampai −10,7% 7d,
funding ~0. Kesimpulan yang keluar: narasi sah, tapi post-catalyst dan pre-revenue, dan yang disebut
itu proksi. Sebut juga koin penerima yang tidak bisa dibeli user, bukan cuma menyebut yang bisa.

