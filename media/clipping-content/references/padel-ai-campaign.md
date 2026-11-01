# Padel AI (Content Rewards / Whop) — aturan + pipeline produksi

Rate $1,50 per 1.000 views, cap $200/klip, pool $1.000, penyelenggara Clip Track.
Bedanya dari campaign lain: **cuma menerima TikTok PHOTO SLIDESHOW, bukan video.**

## Aturan keras (dari "Padel AI - Campaign Requirements.pdf")

- 6–7 slide, 9:16, dibikin **native di TikTok** (teks diketik pakai text tool TikTok,
  gaya **putih + outline hitam**). Teks yang di-bake ke gambar = kelihatan kayak iklan,
  dan "looks like an ad" masuk daftar penolakan.
- **App slide WAJIB di slide 2 atau 3.** Kalau di slide 4+ langsung ditolak. Slide itu
  harus nampilin: nama **Padel AI**, ikon app, **satu** screenshot fitur, dan **KEDUA**
  badge (App Store + Google Play), plus kalimat "Search Padel AI on the App Store &
  Google Play". Ditulis kayak list item ("1. Stop buying the wrong racket").
- **Struktur:** slide 1 = hook (angka + padel + bikin penasaran, jangan sebut app),
  slide 2/3 = app slide, sisanya satu tip per slide (heading tebal + 1–2 kalimat pendek).
- **Caption:** mulai dengan `@padel.ai.app`, lalu 1–2 kalimat, satu emoji, 3–5 hashtag.
- **Fitur wajib dirotasi** dan nggak boleh sama dua post berturut-turut: (1) AI padel scan
  / AI coach, (2) real rating 1.0–7.0, (3) racket finder.
- **Akun:** gaya pemain biasa, bukan akun app. Foto profil = orang/raket/kort (jangan logo,
  jangan ikon app). Follow + tag `@padel.ai.app` di bio ("My Padel Coach: @padel.ai.app"),
  link campaign di kolom website. Akun baru wajib warm-up 3 hari (scrolling padel 15–20 menit
  sehari) sebelum posting pertama.
- **Penonton:** minimal 50% views dari Tier-1 (UK, Spanyol, Belanda, Swedia, Italia, Prancis,
  Belgia, Jerman, Portugal, US). **Jangan VPN.** Posting 19.00–21.00 zona waktu penonton
  (= 00.00–02.00 WIB, pakai scheduler TikTok).
- Foto harus **foto padel asli**, jangan gambar AI. Sound = trending sound di editor TikTok.
- Ditolak kalau: app slide di posisi 4+, badge cuma satu, views Tier-1 <50%, nggak ada
  screenshot analytics, bukan soal padel, kelihatan kayak iklan/klaim palsu, post dihapus
  atau di-private sebelum 30 hari, ada tanda fake views. Save 30 hari.

## Pipeline kita

Semua di `~/.hermes/tools/video/padel/`:

- `fetch_pexels.py` — unduh foto padel asli dari Pexels lewat pola URL yang bisa ditebak
  dari ID foto: `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?w=1600`.
  ID-nya didapat dari web_search `site:pexels.com/photo padel ...`. Lisensi Pexels: gratis,
  termasuk komersial, nggak wajib atribusi (cocok, karena captionnya udah dipatok formatnya).
- `build_app_slides.py` — bikin app slide 1080x1920 dari file kit resmi (ikon, kedua badge,
  screenshot fitur). **Pakai file kit apa adanya**, jangan gambar ulang atau ganti warna.
  Tinggi kartu dihitung dari isi, lalu di-clamp supaya kartu selesai di y<=1500: teks nggak
  boleh masuk 20% bawah (UI TikTok) atau nyentuh tepi kanan.
- `build_post_packs.py` — rakit satu folder per post: `01_hook.jpg`, `02_app.jpg`, lalu 5 tip
  (`03..07`), plus `SCRIPT.txt` (teks per slide + caption).
- `slides.py` / `make_slideshow_video.sh` — versi video 18 detik. **Off-spec buat campaign
  ini** (mereka cuma terima photo post), jangan dikirim kecuali diminta.

## Jebakan yang udah kena

- **Commons API kena rate limit** (403 "Too Many Reqs") kalau dipanggil berturut-turut tanpa
  jeda; Pexels juga diblokir dari server ini waktu dibuka pakai browser. Yang jalan: pola URL
  Pexels + ID dari hasil web_search.
- **Foto stock = akun kelihatan kayak akun stock.** Foto padel punya user sendiri selalu lebih
  bagus; sediakan stock sebagai cadangan, bukan sebagai default.
- **Gate sebenarnya bukan editnya, tapi distribusi.** Minimal 50% views Tier-1 dari akun baru
  itu yang paling sering gagal, bukan kualitas slide. Jangan janjikan hasil dari sisi produksi.
