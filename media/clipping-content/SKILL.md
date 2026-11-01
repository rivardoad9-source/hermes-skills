---
name: clipping-content
description: Use when asked about clipping or paid-content bounties.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [clipping, short-form, monetization, video, ffmpeg]
    related_skills: [youtube-content, remotion-opus, video-deliverable-qa]
---

# Clipping content (dibayar per view)

## When to Use
- User nanya soal clipping, "dibayar per views", campaign Whop/Vyro, atau minta
  dijelaskan marketnya.
- User minta video panjang dipotong jadi klip vertikal 9:16 buat TikTok/Reels/Shorts.
- User nanya "lu bisa ngerjain ga", atau mau bikin/monitor campaign clipping, atau
  mau jual jasa klip.

Kelas kerjaan: potong konten panjang jadi klip vertikal, posting di TikTok/IG/YT,
dibayar per 1.000 views terverifikasi. Termasuk saat user tanya "marketnya gimana",
"campaign mana yang bayar paling oke", atau "lu bisa ngerjain ga".

## Aturan tetap untuk user ini
- **Jangan kirim ulang video/hasil revisi ke chat kecuali dia minta.** Kalau klip
  dirender ulang karena diperbaiki, cukup lapor apa yang berubah dan di mana filenya.
  Nge-drop beberapa file 10 MB tiap revisi dianggap spam.
- **Jangan pernah sarankan campaign casino/judi**, walau CPM-nya paling tinggi
  ($10+/1.000 views, ujung ekstrem pasar sampai $25). Promosi judi ilegal di
  Indonesia dan campaign casino sendiri nyaring lokasi penonton. Kalau dia tanya
  kenapa angkanya bisa segitu besar, jelaskan mekanismenya, tapi tetap bilang itu
  bukan jalurnya.
- **Angka jujur, nol hype.** Klaim "$6.500/bulan" di thumbnail YouTube itu tier atas.
  Selalu pasang ladder-nya: pemula $100-500/bulan, konsisten 5-15 post/hari
  $1-3k/bulan, top 1% baru $10k+. Sebut juga cara bulan jadi nol: budget campaign
  habis sebelum views keverifikasi, atau akun kena ban dan pending hangus.
- **Kalau dia tanya "bisa nggak", jawabnya artefak, bukan penjelasan.** Render satu
  klip contoh dari sumber nyata, kirim filenya, baru jelasin tahapannya. Dia menilai
  dari hasil.
- Nilai tawarnya ada di konteks crypto/Web3 + akuntansi. Niche crypto
  (exchange/wallet/token) dan jasa ke KOL/agency lokal lebih masuk daripada
  ngikut feed umum yang CPM-nya $0,35.

## Vyro (diverifikasi 13 Okt 2026, langsung dari situsnya)
- Indonesia **tidak** masuk daftar negara terlarang (yang diblokir: Thailand,
  Timor-Leste, Macao, Pakistan, Bangladesh, Turki, Mesir, Ukraina, dll ~70 negara).
- Syarat: 18+, residen di wilayah yang didukung, wajib sambung minimal 1 akun sosial.
- **Rate yang dipajang di situsnya $1,00-$2,00 per 1.000 views** (`$2,000 PER 1M VIEWS`
  = $2 CPM), bukan $3 seperti klaim artikel pihak ketiga. Live: Kevin Langue $2,
  Ghost Hunter $2, Kizik $2, Shark Tank S18 $2, Ketone-IQ $1,50, Valorant $1,50,
  iHeartPodcasts $1,50, MrBeast grocery $1. Cap $1.000 per klip.
- "Locked" = campaign udah deket end date / budget abis, ditutup biar yang udah
  masuk nggak kebagi. Bukan ban akun.
- Bayar: min $10, cash out maksimum sekali per 7 hari, cuma PayPal atau Stripe
  (nggak ada crypto/IBAN). Views keverifikasi per jam, tapi dana dilepas pas campaign
  ditutup, jadi ada masa pending — keluhan umum di Reddit.
- Keunggulan buat user ini: sumber videonya resmi dikasih platform, jadi masalah
  "YouTube nolak IP server" hilang; nggak butuh follower.

## Whop Content Rewards (diverifikasi 13 Okt 2026 dari halaman campaign-nya)
- **Cap per klip jauh lebih kecil dari Vyro**: contoh nyata Lucide AI dan GymBeam
  dua-duanya `Max payout $150.00`, `Min payout $2.50-$4.50`. Vyro cap-nya $1.000/klip,
  jadi klip yang meledak dibayar 6-7x lebih besar di Vyro.
- **Banyak campaign nyaring bahasa/persona**, bukan cuma negara. Contoh: Lucide AI
  $2,50/1k tapi brief-nya "etudiant 18-25 ans, publie en francais, face cam" — clipper
  Indonesia nggak bisa ikut walau rate-nya paling gede di feed itu saat itu. Selalu
  baca brief dulu sebelum senang lihat CPM.
- Sumber video biasanya dari brand/creator dan nggak selalu disediakan buat diunduh →
  sering harus narik sendiri (YouTube blokir IP server). Ini pembeda praktis vs Vyro.
- Payout ASEAN aman: Whop resmi mendukung payout ke **200+ negara termasuk Indonesia**
  (daftar sanctioned cuma Afghanistan, Belarus, Kuba, Iran, Rusia, dll). Min $10,
  lewat Whop Payments (bank, KYC), PayPal, atau Coinbase.
- Feed campaign-nya bisa di-scrape tanpa login (dulu kepakai buat bikin scanner),
  jadi cocok buat dipantau otomatis tiap jam.

## Vyro: kenapa bisa KOSONG total (kejadian nyata 13 Okt 2026)
- Akun Vyro dari Indonesia bisa jadi **nggak lihat satu campaign pun**. Itu bukan bug
  dan bukan salah akun: halaman bantuan Vyro sendiri bilang visibilitas campaign
  tergantung region + negara akun, jadi kosong artinya "lagi nggak ada yang nyasar
  ke wilayah lu". Campaign MrBeast-nya praktis nargetin pasar US/global brand.
- Karena itu **jangan jadikan Vyro satu-satunya jalan**. Bikin akun tetap gratis,
  biarkan (campaign bisa muncul sewaktu-waktu), tapi jalan produksi dimulai dari Whop.
- Sebelum nyuruh user daftar ke platform baru, cek dulu apakah ada campaign yang
  beneran buka buat region user. Daftar itu murah, tapi nunggu campaign yang nggak
  pernah dateng itu yang mahal.

## Whop: yang penting buat produksi (diverifikasi 13 Okt 2026)
- **Feed-nya bisa discrape pakai curl biasa** (nggak butuh browser):
  `https://whop.com/contentrewards/` ~460 KB HTML, ada ~10 blok "Budget: $X" +
  "CPM: $Y per 1,000 views" + "Platforms: ..." + link campaign. Script sudah ada:
  `~/.hermes/scripts/clip_campaign_scan.py` (+ wrapper `.sh`, cron tiap jam, diam
  kalau nggak ada yang baru).
- **Halaman campaign-nya publik**: `contentrewards.com/c/campaigns/<uuid>` nampilin
  ringkasan, CPM, min/max payout, platform, dan "Reference materials N files" —
  jadi **bahan mentahnya juga disediakan** (masalah YouTube-blokir nggak relevan).
  Tampilan publiknya nyembunyiin detail brief di balik "Join to unlock", **tapi syarat
  personanya tetap kebaca**: payload JSON halaman itu memuat `creatorRequirements`,
  `contentTypes`, `requiresApplication`, dan `verified`. Jadi screening bahasa, umur,
  face-cam, dan status brand bisa dilakukan sebelum user join - yang beneran baru
  ketahuan setelah join cuma isi file referensinya. Yang **nggak ada** di payload: field
  negara/wilayah, jadi jangan bilang satu campaign "aman buat Indonesia" cuma karena
  halamannya kebuka; gate negara cuma muncul di dialog join.
- Cap payout per klip kecil: contoh nyata $100-$200 (Vyro $1.000). Min payout
  $1,00-$5,00 per campaign.
- Sering ada syarat bahasa/persona/wilayah yang bikin clipper Indonesia nggak bisa
  ikut walau CPM-nya paling gede (contoh: Lucide AI $2,50 tapi "etudiant 18-25 ans,
  publie en francais, face cam"). Scan wajib nandain ini, jangan cuma urut CPM.

## Kalau platform CPM nutup region: bounty konten (Superteam Earn)
Gerbang region itu fitur, bukan bug: platform CPM nargetin penonton US/EU, jadi
clipper Indonesia sering cuma lihat rak kosong. Jangan ngotot di situ dan jangan
sarankan VPN — pencairan plus verifikasi identitas bakal nyangkut, kerjaan kunci
di pintu bayar. Pindah ke bounty konten: hadiah tetap, dinilai juri, gerbang
regionnya nggak ada.
- API publik JSON, tanpa login: `https://earn.superteam.fun/api/listings?take=100`
  (field `title`, `slug`, `rewardAmount`, `token`, `deadline`, `type`). Halaman
  listing: `https://superteam.fun/earn/listing/<slug>`. Halaman region resmi:
  `https://superteam.fun/earn/regions/Indonesia/all`.
- Script pantau: `~/.hermes/scripts/superteam_scan.py` (+ wrapper `.sh`, cron tiap
  6 jam, diam kalau nggak ada yang baru, state `~/.hermes/state/superteam_seen.json`).
- **API-nya nggak bisa difilter per region** — `?region=Indonesia` diabaikan dan
  balikannya sama. Filter dari judul: kasih 🚩 kalau ada nama chapter lokal
  (Türkiye, Brazil, Madrid, Nigeria, Vietnam...) dan prioritaskan yang ditulis
  `Open | Global`.
- Tandai yang bentuknya konten/video/thread: itu yang cocok sama pipeline render.
- Ceritakan sebagai lomba, bukan penghasilan pasti: contoh nyata satu bounty 500 USDC
  dengan 26-38 submission, juara 1 ~$150-200 lalu turun ($125/$80/$60/$35). Selalu
  sebut jumlah submission-nya biar user tahu peluangnya.
- Pilih yang runway-nya mingguan. Bounty yang tutup dalam 24 jam bukan target
  pertama kecuali pipeline dan akun user sudah siap.

## Cara milih campaign (ini inti duitnya)
Skor = **rate x sisa kolam x persaingan**, bukan rate doang. Lihat CPM doang itu jebakan:
- **Baca angka asli campaign-nya, jangan cuma kartu di feed.** Halaman campaign nge-embed
  objek JSON di payload Next.js-nya, isinya `metrics` (`creatorCount`, `budgetSpentCents`,
  `totalViews`, `approvedSubmissionCount`), `payoutModel` per platform, `contentTypes`, dan
  `creatorRequirements`. Artinya jumlah pesaing dan sisa kolam kebaca **tanpa login**:
  `python3 ~/.hermes/scripts/cr_campaign_metrics.py <url>...` (atau `--from-scan <file>`).
  Rincian field, jebakan parsing, dan cara ngitungnya: `references/content-rewards-metrics.md`.
- **Satuannya sen**: `rate` = sen per 1.000 views (`125` = $1,25/1k), `maxPayout` juga sen
  (`20000` = $200). Jangan dibaca sebagai dolar. `views buat nembus cap = maxPayout/rate x 1000`.
- **Kolam utuh + `creatorCount` 0 menang atas rate lebih tinggi yang udah dikeroyok.**
  Window paling gemuk: campaign baru, `budgetSpentCents` 0, belum ada yang masuk.
- **Filter faceless vs face lebih nentuin daripada CPM.** `contentTypes` bilang
  `Clipping`/`Slideshows` (faceless, pipeline kita bisa kelarin sendiri sampai jadi) atau
  `UGC (With Face)` (butuh user di depan kamera; voice over Inggris user masih basic, jadi
  itu jalur dia, bukan jalur mesin). Buat kerjaan yang kita eksekusi end-to-end, ambil
  Clipping/Slideshows.
- **Saring yang mati**: `requiresApplication: true` + `creatorRequirements` minta
  bahasa/umur/domisili yang user nggak punya (contoh nyata: "etudiant 18-25 ans, publie en
  francais, face cam"), dan kategori judi atau streamer kasino.
- CPM tinggi dengan kolam kecil lebih buruk daripada CPM sedang dengan kolam dalam.
  Contoh nyata: Roobet $1,50 dengan pool $250k (kolam dalam) vs MUTUUM $6 dengan
  pool tipis (habis dalam beberapa hari).
- Budget **first come first served** dan bisa habis sebelum views keverifikasi.
- Masuk 2-3 kolam dalam, bukan 10 campaign kecil.
- **48 jam pertama campaign baru itu window paling gemuk**: pool penuh, pesaing
  sedikit. Pipeline produksi harus sudah siap sebelum join, jangan dibangun setelah.
- Akun posting WAJIB di-link sebelum posting (views dari akun tak ter-link nggak
  ketrack), dan link disubmit begitu post live.
- Baca rules campaign kayak kontrak: hashtag wajib, panjang minimum, gaya edit yang
  dilarang, cap payout per klip. Pelanggaran = klip ditolak setelah views-nya jalan
  (kerja gratis).

Struktur pasar, rate per platform, skema pembayaran, dan cara baca feed campaign:
`references/clipping-market.md`.

## Pipeline produksi (terverifikasi lokal)
1. **Sumber.** Minta file/link dari user. File yang dia kirim > narik sendiri:
   download YouTube dari IP server kena bot check yt-dlp ("Sign in to confirm you're
   not a bot"). Kalau tetap harus narik sendiri, butuh cookies browser user
   (`yt-dlp --cookies`) atau proxy residential; kalau dua-duanya nggak ada, minta
   filenya. Download dari CDN biasa (media.w3.org, samplelib, filesamples) jalan
   normal, jadi jangan simpulkan koneksinya mati cuma karena YouTube nolak.
2. **Transkrip.** Sumber YouTube: caption bawaan gratis (`--write-auto-subs`), nggak
   butuh GPU, ini jalur termurah. Twitch/Kick nggak punya caption -> butuh ASR.
   Lokal ternyata JUSTRU cepat, bukan lambat: faster-whisper int8 (venv di
   `~/.hermes/tools/video/v`) model `base` transkrip 52 detik audio dalam **1,8 detik**
   (25x realtime, RAM puncak 361 MB); `small` 9,2 detik (5,5x, RAM 749 MB); `tiny`
   1,0 detik (283 MB). Audio satu jam kelar ~2,5 menit, jadi nggak perlu API bayar.
   Jebakan: `av` bentrok sama faster-whisper 1.2.1 (`TypeError: open() got an
   unexpected keyword argument 'metadata_errors'`) — upgrade/downgrade av nggak nolong.
   Akalinnya lewatin PyAV: decode pakai `ffmpeg -f s16le -ac 1 -ar 16000`, baca jadi
   `np.ndarray` float32 (`/32768`), baru kasih ke `transcribe()`.
3. **Pilih momen.** Skor segmen transkrip pakai LLM, ambil kandidat 20-45 detik
   yang punya hook di 2 detik pertama.
4. **Potong, verticalize, burn caption.** Satu perintah ffmpeg di bawah.
5. **Metadata.** Hook, caption, hashtag. Wajib variasi per post (trim, frame
   pembuka, caption beda) karena platform ngeflag repost.
6. **Posting.** Token Buffer dan Threads API ada di env, tapi verifikasi dulu
   apakah plan-nya mendukung publishing TikTok/IG sebelum menjanjikan otomatis.
   Kalau nggak, user posting manual dari HP dan itu tetap jalur normal.

## Perintah render
```bash
FF=~/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg
$FF -y -ss 6 -t 14 -i sumber.mp4 -filter_complex \
"[0:v]split=2[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:2,eq=brightness=-0.08[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:520[comp];[comp]ass=captions.ass:fontsdir=/usr/share/fonts[vout]" \
-map "[vout]" -map 0:a:0 -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p \
-r 30 -c:a aac -b:a 128k -movflags +faststart klip.mp4
```
- Layout: background = salinan video yang di-blur dan di-crop cover, foreground =
  versi fit-width di tengah. Ini pengganti face-tracking (cv2 nggak terpasang) dan
  tetap kelihatan rapi untuk sumber lanskap/talking head.
- Caption ditaruh di sepertiga bawah (`MarginV` ~430 di ASS) dan foreground di
  `overlay y=520`, jadi nggak tabrakan. Kalau geser foreground, geser juga MarginV.
- Template caption bergaya hook: `templates/captions.ass` (font DejaVu Sans,
  highlight kata kunci pakai `{\c&H00E5FF&}`, pop-in pakai `\t(...)`).
- Referensi kecepatan: klip 14 detik 1080x1920 + blur bg + caption ~21 detik render
  di box 2 core. Satu VOD panjang jadi puluhan klip = urusan menit, bukan jam, jadi
  kecepatan produksi bukan bottleneck-nya.
- Cek dulu `$FF -filters | grep -E "subtitles|ass|drawtext"` dan `fc-list`: kalau
  libass/libfreetype ada, caption bisa langsung diburn; kalau nggak, fallback
  `drawtext`.

## Diagnosa klip 5-6 views (nol distribusi)
Kalau views tiap klip 5-6 dan semuanya dari akun user sendiri, itu **bukan soal kualitas klip —
klip-nya nggak pernah masuk distribusi**. Urutan ngeceknya: post beneran publik (bukan private /
partial / friends-only)? edit-nya unik per post (platform ngeflag repost)? akun masih dingin atau
baru? audio/footage kena copyright match? Jangan produksi klip baru sebelum salah satu ini ketemu,
klip tanpa distribusi = kerja gratis.
- **Buktikan kolamnya bisa bergerak dari angka campaign itu sendiri, bukan dari perasaan.**
  `cr_campaign_metrics.py` ngasih `creatorCount`, `approvedSubmissionCount`, `totalViews`: contoh
  nyata satu campaign film dengan 2 creator dan 15 klip disetujui udah narik ~296.709 views. Kalau
  campaign yang diikutin punya angka segitu, bottleneck-nya akun user, bukan campaign-nya — dan itu
  ngubah rencananya (hangatin akun 7-10 hari + cross-post TikTok/Reels/Shorts + edit unik per post),
  bukan nambah jumlah klip.
- **Min payout itu gerbangnya, cap cuma plafon.** Rate $0,50/1k dengan min payout $1,50 artinya klip
  harus lewat ~3.000 views dulu sebelum dibayar sepeser pun. Jadi 20 klip @ 200 views = $0, bukan
  $10. Hitung dua-duanya sebelum nyebut angka: `views min = minPayout/rate x 1000` dan
  `views cap = maxPayout/rate x 1000`.
- Kalau hambatannya distribusi, jalur jasa di bawah yang lebih masuk akal daripada nambah klip.

## Jalur jasa: sering lebih untung daripada ngejar CPM
Jual jasanya, bukan views-nya: $5-50 per klip atau retainer $500-5.000/bulan, dan
brand bisa habis $10k/bulan buat clipping. Tawarkan ini lebih awal kalau hambatan
user sebenarnya distribusi (akun + algoritma), bukan editing.

## Jangan dijanjikan
- Multi-akun farming (proxy, nomor HP, warm-up). Akun baru yang langsung posting =
  shadowban atau ban, dan itu nggak bisa dijamin selamat.
- Jangan klaim pencairan aman sebelum dites: Whop di dokumennya mendukung payout ke
  200+ negara termasuk Indonesia, Vyro cuma bilang "PayPal atau Stripe tergantung
  wilayah" dan buat Indonesia belum jelas mana yang kepakai. Suruh user tes cash out
  begitu saldo nyentuh minimum, jangan nunggu numpuk.

## Referensi per-campaign

- `references/padel-ai-campaign.md` — aturan lengkap + pipeline Padel AI: TikTok photo
  slideshow doang (bukan video), app slide wajib di slide 2/3, rotasi 3 fitur, gate views Tier-1.

## Campaign film MUSK (Whop/Clouted) - aset resmi di Google Drive
Campaign nyata pertama yang user bisa ikut (gate region Whop lolos buat yang ini).
- **Ekonomi**: $0,50 per 1.000 views, cap $250 per klip, min payout $1,50, budget
  $1.000 sisa. Jadi satu klip tembus 100k views = ~$50, tembus cap di 500k views.
- **Hashtag wajib di caption**: `#BleeckerStreetPartner` dan `#MuskMovie`. Post harus
  publik dan tetap bisa diakses. Submit URL post di Content Rewards, review <=24 jam.
  Post tanpa hashtag / pakai audio tambahan / keluar dari konteks film = ditolak.
- **Aturan teknis brief**: minimum 15 detik, **30 detik kalau mau YouTube Shorts** ->
  target 30-45 detik biar satu file layak untuk TikTok, Reels, dan Shorts sekaligus.
  Audio HANYA dari footage (jangan tambah musik/SFX). Subtitle, text overlay, dan cut
  kreatif boleh. **Jangan pakai background blur dan jangan ada black bar / ruang
  kosong** -> di campaign ini jangan pakai pipeline blur-bg default; pakai aset 9x16
  resminya saja. Tiap submission harus edit unik, repost aset mentah = low effort.
- **Aset**: folder Drive `1Eus9-vy8sM5ICiPtQl6Gtn8YQ3AdVrhU` (owner diego@clouted.com)
  isi 3 subfolder: `16x9` (5 klip), `9x16` (5 klip, sudah vertikal + watermark film),
  `Trailers` (4 file). Ambil dari `9x16` -> nggak perlu crop, nggak perlu blur, nggak
  ada black bar. Brief lengkapnya di Google Doc terpisah yang dikirim user.
- **Alur kerja**: unduh aset lewat Drive API pakai OAuth user (`google_api.py drive
  search "'<folderId>' in parents" --raw-query` lalu `drive download <id> --output`),
  transkrip pakai faster-whisper base, pilih window 30-45 detik yang ada hook di
  2 detik pertama, tulis hook + endcard, render, lalu QC.
- **Script produksi**: `~/.hermes/tools/video/musk/build_musk_clips.py` - dict `PLAN`
  per klip (src/start/dur/hook/endcard/slug). 5 klip 35-43 detik render ~2,5 menit
  total di box 2 core. Output ke `musk/clips/*.mp4` + `.ass` per klip.
- **QC wajib sebelum kirim**: ekstrak frame di detik hook dan di tengah klip, lalu
  lihat pakai `vision_analyze` (cek hook kebaca, subtitle pas, nggak ada bar hitam).
  Ini juga cara cepat mengecek sinkron subtitle - geser-an biasanya ketahuan di sini.
- **Jebakan**: nama file aset nggak seragam (sebagian pakai prefix `MUSK_Clip_`,
  sebagian nggak). Ambil persis dari listing Drive, kalau tidak ffmpeg gagal dengan
  "No such file or directory" dan klip itu diam-diam nggak jadi.
- **Disk server cuma 40GB**: trailer `.mov` 9x16 bisa 2,5 GB per file dan sempat bikin
  disk 94%. Unduh yang perlu saja, hapus file berat setelah dipakai.

## Repo yang layak dipinjam (dicek 13 Okt 2026 lewat GitHub API)
- **mutonby/openshorts** - 6.482 star, **MIT**, Python, di-push hari ini. Paling cocok
  dan aman dipinjam karena MIT. Isinya persis yang dibutuhin: pemilih momen pakai LLM
  (`clip_selection.py`, prompt "read the ENTIRE transcript and word-level timestamps to
  choose the 3-15 MOST VIRAL moments"), penulisan hook + **hook grounding**
  (`hook_grounding.py`: hook dicek dulu ke frame/transkrip biar nggak njipang dari isi),
  pembakar subtitle level-kata (`subtitles.py`, `generate_ass`), deteksi subtitle bawaan
  sumber biar nggak dobel (`burned_subtitles.py`), dan server MCP. Aturan cue-nya:
  `max_chars=20`, `max_duration=2.0`, margin bawah `SAFE_MARGIN_V=43` di kanvas PlayResY
  288 (= ~15% tinggi), plus preset gaya karaoke/pop/box/one-word.
- **Anil-matcha/AI-Youtube-Shorts-Generator** - 5.332 star, MIT, cuma 1,3 MB: enak buat
  baca desain prompt highlight + auto crop vertikal, tanpa nyeret dependensi berat.
- **m-bain/whisperX** (24,5k star, BSD-2) dan **jianfch/stable-ts** (2,3k star, MIT):
  word-level timestamp paling akurat + diarisasi. **Nggak dipakai di box ini**: dua-duanya
  butuh torch (ratusan MB) dan box cuma 2 core. faster-whisper sendiri sudah punya
  `word_timestamps=True` - itu sudah cukup, nol dependensi baru.
- **FujiwaraChoki/supoclip** - 1,3k star, **AGPL-3.0**: idenya bagus (`caption_templates.py`)
  tapi lisensinya copyleft, jangan comot kodenya ke pipeline sendiri.
- **buxuku/SmartSub** - 5,7k star, MIT, TypeScript/Electron: referensi UX subtitle +
  terjemahan, bukan buat server.

## Caption v2: yang bikin kelihatan nggak amatir
- **Transkrip pakai `small` + `word_timestamps=True`**, bukan `base`. Teksnya langsung
  lebih bener (tanda baca, nama, angka), dan timingnya bisa dipakai per kata.
- **Tata letak HARUS dipatok sekali per cue.** Kalau tiap kata dibungkus ulang, barisnya
  goyang ("Elon / Musk retweeted" -> "Elon Musk / retweeted") dan itu kelihatan murahan.
  Caranya: bagi baris sekali, lalu kata yang belum diucapkan disembunyikan dengan
  `{\alpha&HFF&}` - tetap makan ruang, jadi tata letaknya diam.
- **Kata aktif**: kuning (`{\c&H0000D4FF&}` di ASS = BBGGRR) + `\fscx106\fscy106`.
  Event-nya berakhir persis di awal kata berikutnya, jadi nggak ada teks dobel.
  Kata terakhir ditahan `+0,30s` tapi **dipotong kalau cue berikutnya udah mulai**.
- **Posisi**: `MarginV` 440 dari bawah di kanvas 1080x1920 (~23%). 330 (~17%) ternyata
  masih kena UI TikTok (username/caption/musik makan ~20% bawah) - ketahuan waktu frame
  QC dilihat pakai `vision_analyze`.
- **Font**: Anton (huruf kapital, gaya TikTok) dan Montserrat ExtraBold (huruf
  besar-kecil, nada dokumenter) di `~/.hermes/tools/video/fonts`, dipanggil lewat
  `fontsdir=` di filter `ass`.
- **FILE FONT WAJIB DICEK DENGAN `file`, JANGAN DIPERCAYA DARI NAMA.** Unduhan font yang
  gagal jatuh sebagai halaman HTML GitHub "Page not found" (kejadian nyata: file
  `Montserrat-ExtraBold.ttf` 264 KB ternyata HTML 404). libass **nggak error** kalau
  font-nya rusak — dia diam-diam pakai font sistem, jadi hasil render kelihatan wajar
  dan baru ketahuan waktu font-nya diperbaiki. Cek: `file font.ttf` harus bilang
  `TrueType Font data`. Sumber yang bener buat Montserrat:
  `https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-ExtraBold.ttf`.
  Bonus: libass mencoba nge-parse **semua** file di `fontsdir`, jadi file rusak/backup
  jangan ditaruh di folder itu (bikin log error dan sampah). Dua gaya ini yang ditawarin ke user buat dipilih.
- **Buang jeda mati**: kalau ada hening 5-6 detik di tengah sumber, potong jadi dua
  segmen lalu `concat` (`trim`+`setpts`, `atrim`+`asetpts`), baru caption dibuat di
  timeline hasil gabungan. Ngeluh "videonya nanggur" biasanya soal ini, bukan soal durasi.
- **Koreksi nama orang itu wajib, bukan opsional.** ASR nulis "Nibel Benavidez",
  yang bener **Nybel Benavidez** (korban tabrakan Autopilot 2019, diverifikasi lewat
  berita). Nama salah di caption = risiko fitnah + kelihatan asal-asalan.
- Script: `~/.hermes/tools/video/musk/build_clips_v2.py` (`--style doc|punch`,
  `--only <aset>`), transkrip kata di `transcripts/words_small.json`.

## Aturan baca: mana yang cacat, mana yang cuma info
Detail lengkap ada di `references/caption-spec.md` di skill ini.
- **Yang WAJIB dan dicek otomatis** (blok "QC baca" di akhir `build_clips_v2.py`, harus
  `tumpang tindih cue: 0`): **cue nggak boleh nabrak cue berikutnya**, sisain minimal
  2 frame (0,07s @30fps). Jangan kirim klip sebelum baris itu dibaca.
- **Percaya baris QC-nya, bukan notifikasi prosesnya.** Proses render yang di-`pkill` di
  tengah jalan masih bisa nyelesain perintah shell di belakangnya dan nimpa frame QC atau
  ngirim notifikasi "selesai". Kalau logika QC baru saja diubah, baris QC yang formatnya
  beda dari logika terbaru = hasil proses lama: cek mtime file klip, jalankan satu render
  bersih, baru lapor.
- **Cara nahan kata terakhir tanpa nabrak**: `hold = max(akhir_kata + 0,30s, mulai + 0,45s)`,
  lalu **cap ke `(mulai cue berikutnya - 0,07s)`** dan **jangan di-floor balik ke akhir
  kata ASR setelah di-cap**. Floor itu bikin kata terakhir cue ini tampil barengan kata
  pertama cue berikutnya (kejadian nyata: 84 cue jaraknya di bawah 2 frame, sebagian pas
  0,00s), dan caption dobel di frame yang sama itu kelihatan paling norak.
- **CPS dan durasi tampil itu INFO, bukan target.** Angka 17 karakter/detik dari pedoman
  subtitle siaran nggak berlaku buat caption yang nempel suara: kalau dipaksa, caption-nya
  ketinggalan dari audionya. Realita klip kita: CPS tengah ~15, puncak 40+ cuma pas satu
  kata diucap cepet. Yang digepengin cuma tumpang tindih cue.
- **Maks 2 baris** dan nggak lebih dari `line_chars` (22 `doc` / 18 `punch`) dijaga waktu
  bagi baris, bukan waktu QC.
- **Hook wajib kebaca dari frame 1**, jangan fade dari gelap: 85% orang nonton tanpa
  suara, dan hook yang nge-fade bikin frame pertama kosong. Pakai
  `{\fad(0,0)\fscx104\fscy104\t(0,200,\fscx100\fscy100)}`.
- **Safe area vertikal**: patokan `centerY` 0,72-0,74 (26-28% dari bawah); platform
  UI makan ~320px bawah di kanvas 1920. `MarginV 440` masih aman.
- Skill eksternal yang dipasang buat kerjaan ini (jangan di-patch, itu punya user):
  `media/subtitle-readability-brief` (angka CPS/gap/SDH), `media/caption-templates`
  (28 preset caption terverifikasi + tabel safe area), `media/short-form-video`
  (hook-retention-loop + safe area 900x1400 + pola interrupt 2-4 detik),
  `social-media/social` (di dalamnya ada short-form-video.md berisi bank hook dan
  template skrip, platform-limits.md, x-algorithm.md).
- **Yang masih belum dipakai**: pattern interrupt berupa punch-in zoom tiap 2-4 detik
  dan `loop` frame terakhir = frame pertama. Zoom belum dipakai karena barunya nambah
  waktu render di box 2 core; loop sengaja dihindari di campaign film (klip yang
  muter balik gampang dibaca sebagai repost, dan brief MUSK melarang itu).
