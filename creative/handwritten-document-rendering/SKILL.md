---
name: handwritten-document-rendering
description: "Use when a doc must look handwritten (notes, tugas)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [handwriting, pil, render, pdf, notes, tugas, typography]
---

# Render dokumen jadi halaman bergaya tulisan tangan

## When to Use / Kapan pakai
- User bilang hal seperti “jadiin kayak **tulisan tangan**”, “gaya tulis gw kayak gini” (sambil kirim foto
  catatan), “buat **senatural mungkin**” untuk isi teks / tugas / kertas jawaban.
- Perlu halaman A4 yang tampil seperti ditulis pulpen di kertas bergaris, dikirim sebagai PNG atau PDF.
- Bukan untuk dokumen formal/resmi — untuk itu pakai skill `docx` / `pdf`.

## Alat & aset
- Pillow sudah tersedia (`python3 -c "import PIL"`, PIL 12.x di mesin ini). PDF multi-halaman tidak perlu
  `img2pdf` — `PIL.Image.save(pdf, save_all=True, append_images=[...], resolution=200.0)` cukup.
- Font handwriting: `~/.hermes/assets/fonts/`. Kalau kosong, unduh sekali dengan
  `curl -sL -o <file>.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/<path>"`.
  Yang terbukti jalan: `kalam/Kalam-Regular.ttf` (+ `-Bold`, `-Light`), `handlee/Handlee-Regular.ttf`,
  `patrickhand/PatrickHand-Regular.ttf`, `indieflower/IndieFlower-Regular.ttf`,
  `architectsdaughter/ArchitectsDaughter-Regular.ttf`,
  `shadowsintolight/ShadowsIntoLight.ttf`, `gloriahallelujah/GloriaHallelujah.ttf`,
  `caveat/Caveat%5Bwght%5D.ttf` (variable).
  Cek ukuran file setelah unduh: **14 byte = 404**, nama path-nya beda.
- Pilihan font: **Kalam** = paling mirip tulisan print semi-sambung mahasiswa Indonesia (dipakai user ini);
  **Caveat** = lebih cursive/loose; Handlee/PatrickHand = print terlalu rapi (malah kelihatan font).
- Renderer siap pakai: `scripts/hw_engine.py`. Contoh struktur konten: `templates/hw_content_example.py`.

## Langkah
1. **Lirik contoh tulisan user** kalau ada (foto catatan) → `vision_analyze` dan catat: print vs cursive,
   kemiringan, warna tinta (pulpen hitam?), kertas (bergaris/plain), kebiasaan (panah `→`, bullet `*`/`-`,
   judul digaris bawah, indentasi bertingkat). Pilih font + setelan yang mendekati.
2. **Susun konten sebagai list bertipe**, bukan string bebas:
   `(kind, teks, indent)` dengan `kind ∈ {"h1","h2","num","bul","p","f","blank"}`.
   - `f` = baris angka/formula. Pakai `"label|Rp1.234.000"` → angka otomatis rata kanan di kolom angka.
     **Jangan** padding pakai spasi manual — font proporsional, kolomnya bakal berantakan.
   - Token `->` yang berdiri sendiri (dipisah spasi) digambar jadi panah tangan.
   - Judul `h1` otomatis dapat garis bawah tangan; `h2` bold.
3. **Render**: `python3 <file_konten>.py` → PNG per halaman + PDF di `~/tugas/` (default `out_dir`).
   A4 200 dpi = 1654×2339 px; `RULE_GAP` 52 px = jarak garis kertas.
4. **Verifikasi pakai `vision_analyze`** — minimal halaman 1 dan halaman terakhir. Tanya eksplisit:
   “kelihatan font-generated nggak? ada kata overlap, kepotong, atau lewat margin? kalimat terakhir utuh?”
   Wajib dicek: halaman terakhir berakhir kalimat utuh, tidak ada heading menggantung di dasar halaman,
   tidak ada glyph kotak/tofu.
5. **Iterasi naturalness** kalau vision bilang “too perfect / obviously font-generated”. Ini urutan
   perbaikan yang terbukti (dari yang paling ngefek):
   goyangan baseline per baris (`drift ±5.0`, `rate ±0.010`) → variasi lebar huruf per kata
   (`scale 0.955–1.045`) → variasi ukuran font (30/31/32 px) → sesekali font Light atau dobel-draw
   (tekanan pulpen) → spasi antar kata bervariasi (`×0.78–1.22`) → kertas: `effect_noise` 0.05,
   gradasi cahaya, bintik kertas, garis bergaris yang variasi gelap + sedikit miring.
6. **Antar**: PDF sebagai dokumen + 1 PNG halaman pertama sebagai preview (jangan kirim 6 PNG sekaligus).

## Tell-tale “ini font, bukan tulisan orang” (dan fix-nya)
| Tell | Fix |
|---|---|
| Baseline lurus sempurna | `drift` + `rate` per baris, jitter per kata |
| Lebar huruf seragam | `sc = uniform(0.955, 1.045)` per kata |
| Tinta rata, nggak ada tekanan | alpha & warna ink acak per kata; 22% dobel-draw |
| Spasi antar kata seragam | `space * uniform(0.78, 1.22)` |
| Kertas terlalu bersih | noise + gradasi cahaya + bintik + garis bergaris bervariasi |
| Panah tampak “glyph font” | gambar sendiri: 1 garis + 2 coretan kepala panah (`draw_arrow`) |

## Jebakan
- **Glyph hilang (tofu)**: font handwriting sering TIDAK punya `→`, `↳`, kadang `×`/`±`/emoji.
  Cek dulu dengan `scripts/font_glyph_check.py` sebelum render panjang (tidak butuh `fontTools` — cara:
  bandingkan hash bitmap render sebuah char dengan render U+10FFFD/notdef; hash sama = glyph tidak ada).
  Solusi: jangan taruh `→` di teks mentah, pakai token `->`.
- **Jangan potong item di tengah halaman**: hitung dulu tinggi total item (wrap → jumlah baris × lh)
  sebelum menggambar; kalau tidak cukup ruang, pindah halaman. Kalau menggambar sambil jalan, baris
  bisa kepotong atau terulang di halaman berikutnya.
- PDF hasil ±2 MB untuk 6 halaman (200 dpi) — normal, tapi jangan kirim semua PNG sekaligus.
- Nama heading jangan dobel (mis. dua-duanya “c.”) — periksa penomoran setelah konten jadi; biasanya
  kelihatan justru dari hasil `vision_analyze`.
- **Kejujuran (penting untuk tugas kuliah)**: ini render font, bukan tulisan tangan asli user. Sebut eksplisit
  di chat. Kalau tugasnya mewajibkan tulis tangan, sarankan dipakai sebagai contekan untuk **disalin tangan**,
  bukan di-print lalu dikumpulkan seolah tulisan tangan — sampaikan sekali, singkat, tanpa ceramah.

## File pendukung
- `scripts/hw_engine.py` — renderer lengkap: kertas bergaris, tinta bervariasi, jitter, panah tangan,
  kolom angka rata kanan, PDF multi-halaman + PNG per halaman.
- `scripts/font_glyph_check.py` — cek cakupan glyph font handwriting tanpa `fontTools`.
- `templates/hw_content_example.py` — contoh struktur konten + cara panggil `build()`.
- `references/naturalness-iteration-log.md` — hasil iterasi nyata + komentar vision_analyze per putaran.
