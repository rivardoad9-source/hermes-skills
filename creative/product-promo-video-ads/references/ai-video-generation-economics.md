# Menjual video AI: stack, biaya per detik, dan harga jual

Dipakai saat pertanyaannya bukan "render video ini" tapi "layak nggak jualan video AI / harga berapa /
modalnya berapa". Angka tool berubah tiap kuartal — verifikasi ulang sebelum dikutip ke user, dan selalu
sebut tanggal verifikasi.

## 1. Stack minimum (tanpa langganan tahunan)

| Lapisan | Tool | Catatan |
| --- | --- | --- |
| Video | Kling (murah, kontrol gerak), Veo Fast (audio native), Seedance, Runway (konsistensi kamera) | bayar per detik lewat API; Sora API ditutup Sep 2026 — jangan bangun pipeline di situ |
| Gambar referensi | GPT Image / Nano Banana / Flux, atau ComfyUI lokal | image-to-video jauh lebih konsisten untuk produk daripada text-to-video |
| Avatar/UGC | Arcads, Creatify, HeyGen, Higgsfield | langganan bulanan; pakai hanya kalau klien minta wajah |
| Suara | ElevenLabs | biaya riil beberapa sen per 30 detik |
| Musik | Suno / stok berlisensi | jangan pakai musik tanpa lisensi untuk iklan |
| Edit | ffmpeg + Remotion (pipeline sendiri), CapCut untuk kerja cepat | subtitle/whisper yang sudah ada dipakai ulang |

## 2. Biaya marginal satu iklan 30 detik

Rumus: `detik_jadi × faktor_pemborosan × harga_per_detik`.

- Kebutuhan: 6–8 shot × 5 detik = 30–40 detik jadi.
- Faktor pemborosan realistis **2–2,5×** (take gagal, gerakan aneh, tangan, teks).
- Jadi sekitar 90–110 detik yang digenerate untuk satu video 30 detik.

Contoh tarif API (verifikasi Okt 2026): Kling ~$0,084/detik; Seedance ~$0,09; Veo 3.1 Fast $0,15; Runway
Gen-4.5 ~$0,20. Untuk 110 detik: **$9–17 per video**, plus VO/musik $0,30–0,60. Biaya riil per video jadi
sekitar Rp155rb–280rb.

Waktu per video **setelah template jadi** ±3 jam (brief, script, referensi, generate, seleksi, edit,
subtitle, revisi). Video pertama 6–8 jam. Hitung ulang dengan jam kerja riil setelah 3 video — jangan
pakai estimasi ini sebagai janji ke klien.

## 3. Harga jual dan kenapa lantai pasar itu jebakan

Lantai marketplace (Sribu/Fastwork) Rp99rb–150rb per video, sementara biaya komputasi saja sudah
Rp155rb–280rb. Masuk di situ = kerja gratis. Band yang bisa dipertahankan: Rp500–750rb per video,
paket 4 video/bulan Rp1,2–2jt, white-label ke agensi Rp750rb–1,5jt per video.

Yang dijual bukan satu video hero, tapi **varian untuk testing**: 5–10 hook berbeda dari satu produk
supaya klien bisa cari mana yang CTR-nya jalan. Itu yang jadi retainer bulanan; video tunggal membuat
klien hilang setelah sekali bayar.

## 4. Dua pintu masuk, pilih satu

1. **Seller UMKM / TikTok Shop**: volume, harga rendah, retainer, kerja berulang. Menang lewat kecepatan dan
   pemahaman produk, bukan sinematografi.
2. **White-label agensi**: bayaran lebih tinggi, tidak perlu jualan sendiri, tapi butuh konsistensi brief dan
   tenggat ketat.

Jangan dua-duanya di bulan pertama — cara jualan dan SLA-nya beda.

## 5. Kurikulum yang cukup 3 minggu (untuk yang sudah bisa editing)

1. Hari 1–2: satu model saja, 20 eksperimen image-to-video dari foto produk sendiri. Tujuannya memetakan
   batas model (teks di layar, tangan, fisika, konsistensi wajah), bukan bikin hasil bagus.
2. Minggu 1: kosakata shot — hero push-in, orbit, hand interaction, before-after, UGC selfie, unboxing —
   plus 10 varian hook untuk satu produk.
3. Minggu 2: pipeline penuh satu produk + 3 portfolio dari 3 kategori, dan SOP berisi jam serta biaya per video.
4. Minggu 3: satu klien pertama di harga rendah tapi tidak gratis. Ukur jam riil; kalau >5 jam untuk
   Rp500rb, naikkan harga atau perbaiki template.

## 6. Pitfall yang mahal

- Model makin murah tiap kuartal → **operator prompt bukan moat**. Yang bertahan: terjemah brief jadi konsep,
  art direction, dan editing rhythm.
- Klien premium minta hasilnya "jangan kelihatan AI" — itu skill editing dan casting shot, bukan skill tool.
- TikTok/Meta mewajibkan penandaan konten AI; review/testimoni yang dipresentasikan sebagai pelanggan asli
  melanggar aturan iklan. Ini risiko akun klien, sebutkan sebelum deal.
- Blocker praktis nomor satu di Indonesia bukan kualitas, tapi pembayaran dan gating region tool. Cek metode
  bayar sebelum menjanjikan tenggat.
- Wajah orang butuh izin; musik butuh lisensi. Jangan render wajah dari foto klien tanpa pernyataan tertulis.
