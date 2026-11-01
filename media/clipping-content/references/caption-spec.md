# Spesifikasi caption vertikal (angka patokan, bukan "bikin yang kebaca")

Diadaptasi dari skill `media/subtitle-readability-brief` (MIT, prompt-only) dan
`media/caption-templates` (katalog 28 preset Palmier Pro). Dipakai buat semua klip 9:16.

## Angka yang dipegang

| Aturan | Target | Catatan |
|---|---|---|
| Maks karakter/baris | 32-42 (Latin) | pipeline ini lebih ketat: 22 (`doc`) / 18 (`punch`) |
| Maks baris di layar | 2 | baris ke-3 dilarang, potong cue-nya |
| Maks CPS | 17 dewasa, 12-14 anak | **info doang, jangan digepengin**: caption yang nempel suara ngikutin kecepatan ngomong. Realita klip kita: tengah ~15, puncak 40+ pas kata cepat |
| Durasi tampil minimum | 1,0s | 0,83s cuma buat tag amat pendek |
| Gap antar cue | minimal 2 frame | = 0,067s @30fps; pipeline pakai 0,07s |
| Safe area vertikal | `centerY` 0,72-0,74 | = 26-28% dari bawah; UI TikTok/IG makan ~20% bawah |

Di kanvas 1080x1920: `centerY 0,72` = 1.382px dari atas = 538px dari bawah = `MarginV` ~540 di ASS.
Pipeline sekarang pakai `MarginV 440` (~23%) - sedikit lebih rendah, masih aman, dan
lebih dekat ke kebiasaan caption short-form.

## Preset yang dipakai pipeline ini

- **Keyword Yellow** (vertikal) = patokan gaya `doc`: Inter/`Montserrat ExtraBold` bold ~70pt,
kata aktif jadi kuning `#FFD900`, shadow hitam blur 8 offset y3 opacity 0,45,
posisi `centerY` 0,72, maks 3 kata per cue. Di ASS: `{\c&H0000D9FF&}` (BBGGRR dari #FFD900)
+ `\fscx106\fscy106`, outline 4 + shadow 2 biar tetap kebaca di atas footage dokumenter.
- **Punch Zoom** (vertikal) = patokan gaya `punch`: Anton 100pt HURUF BESAR semua, 2 kata,
posisi tengah frame, tanpa animasi.
- **Meme Classic** = yang JANGAN dipakai di campaign film: Impact kapital + outline tebal 9,
posisi nempel bawah (`centerY` 0,88). Nada meme bentrok sama brief "jaga tone film".

## Prinsip dari katalog yang wajib diingat

1. **Pilih satu preset, tempel apa adanya.** Jangan campur dua preset atau "perbaiki" warnanya.
   Caption jelek hampir selalu hasil mencampur dua gaya.
2. satu sumbu sekali ubah. Mau lebih besar? cuma `fontSize`. Mau lebih tinggi? cuma posisi.
   Ubah dua sumbu sekaligus = jelek.
3. **Kanvas vertikal dan horizontal punya set terpisah**, rasio font-nya beda (vertikal 54-100pt
   di kanvas 1080 lebar, horizontal 30-72pt di kanvas 1920 lebar). Jangan silang.
4. Setelah render, **lihat frame-nya** (`vision_analyze`), jangan percaya konfigurasi doang.
5. `maxWords` adalah tombol kepadatan paling ngaruh: 1 = satu kata hipnotik, 3 = standar
   short-form, 5 = horizontal, 8 = kalimat penuh ala broadcast.

## QC sebelum kirim ke user

angka patokan ini ditulis buat subtitle siaran/youtube, sementara caption kita sinkron per kata.
Buat pipeline ini yang WAJIB cuma satu: cue nggak nabrak cue berikutnya. Sisanya info.

- [ ] `tumpang tindih cue: 0` (blok QC baca di akhir `build_clips_v2.py`)
- [ ] nggak ada kata terakhir yang tampil barengan kata pertama cue berikutnya
- [ ] CPS/durasi dibaca sebagai info: CPS tengah di bawah ~17 itu sehat, puncak tinggi
  pas satu-dua kata cepat itu wajar, yang salah cuma kalau kalimatnya panjang tapi
  ditayangin sekejap
- [ ] nggak lebih dari 2 baris
- [ ] caption nggak ketutup UI platform (lihat frame, bukan asumsi)
- [ ] nama orang dan angka sudah dikoreksi manual
