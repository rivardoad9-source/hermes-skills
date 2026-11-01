# Log iterasi naturalness (kasus nyata: 6 halaman jawaban audit, 1 Okt 2026)

Kasus: user kirim file teks jawaban ujian audit + foto catatan tulisan tangannya, minta “jadiin kayak
tulisan tangan, gaya tulis gw kayak gini, buat senatural mungkin”. Hasil: 6 halaman A4, PDF + PNG.

## Referensi tulisan user (dibaca dari fotonya)
`vision_analyze` pada foto catatan → print **semi-sambung** (bukan cursive), kemiringan agak ke kanan,
huruf rounded, kompak, **pulpen hitam**, kertas cream bergaris, banyak panah `→`, bullet `*`/`-`,
judul digaris bawah, indentasi bertingkat. → pilih **Kalam** (bukan Caveat, yang terlalu cursive).

## Urutan iterasi + respons vision
| Putaran | Setelan | Respons `vision_analyze` |
|---|---|---|
| 1 | font Kalam + jitter per kata ±1.3px, tilt halaman 0.5° | “obviously font-generated: baseline perfect, stroke width uniform, arrows printed glyph” |
| 2 | + drift baseline ±2.2px, ink alpha acak, dobel-draw 22%, gradasi cahaya + bintik kertas | “very close to genuine handwriting”, tapi masih “too perfect, letterforms extremely consistent” |
| 3 | + variasi lebar huruf per kata (0.955–1.045) + spasi antar kata ×0.78–1.22, drift ±3.4px | “baseline wavering looks very natural, tidak ada tabrakan/garbled” |
| 4 (final) | drift ±5.0px, rate ±0.010 | “wavering natural, fully readable like a neat student's page” |

Catatan: `→` **tidak ada** di Kalam (dan tidak ada juga di Caveat) → semua panah digambar manual
(`draw_arrow`). `×`, `±`, `•`, `–`, `—`, `≈`, `°` tersedia; jangan pasang emoji.

## Temuan layout dari verifikasi vision
- Kolom angka rekonsiliasi: padding spasi manual **tidak** sejajar (font proporsional) → ganti ke
  delimiter `|` + kolom rata kanan `AMT_X`; hasilnya langsung rapi satu kolom.
- Penomoran heading dobel (“c. Kasus 1” dan “c. Kasus 2”) baru ketahuan saat baca ulang halaman 4 →
  fix jadi `c.1` / `c.2`. Selalu cek penomoran di pass verifikasi.
- Halaman terakhir harus dicek terpisah: pastikan berakhir kalimat utuh dan tidak ada bagian yang hilang
  (di kasus ini berakhir di kesimpulan Soal 4c, aman).

## Pengiriman
PDF 6 halaman ±2 MB sebagai dokumen + 1 PNG halaman 1 sebagai preview. PNG semua halaman tetap disimpan
di `~/tugas/` dan disebutkan di chat, bukan dikirim semua (user ini nggak suka kiriman file berlebihan).
