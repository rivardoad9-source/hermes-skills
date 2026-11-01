# Tahap 2 — resep foto buku (parameter nyata)

Kasus: setelah Tahap 1 (render per-kata) dianggap “masih terlalu bagus / mirip font”, user minta
“**kayak output foto buku beneran**”. Mesin: `~/.hermes/scripts/hw_photo.py` (numpy + PIL, ±380 baris).
Argumen 1 = seed. Konten tetap dipisah di `hw_content_*.py` (list `(kind, teks, indent)`).

## 1. Tulisan per-huruf (bukan per-kata)
| Aspek | Nilai | Catatan |
|---|---|---|
| font per huruf | 20% `Kalam-Light`, sisanya `Kalam-Regular` 30/31/32 px | jangan campur >2 keluarga |
| alpha tinta | 220–255 | |
| warna tinta | hitam + jitter ±(9, 9, 17) | kehangatan tinta variatif |
| rotasi per huruf | ±2.4° | jangan >3° (kata jadi ngawur) |
| tinggi huruf | ×0.95–1.06 | |
| lebar huruf | ×0.96–1.05 (`wsc`) | **wajib dipakai untuk advance** |
| shear (miring) | ±0.08, peluang 55% | ala nulis cepat |
| dobel-draw | 28% (offset +0.9/+0.3, alpha −45) | tekanan pulpen |
| baseline dalam kata | random walk langkah ±1.2, clamp ±4.4 px | |
| jitter posisi | x ±0.6, y ±1.1 | |
| drift/slope per baris | ±6.5 px / ±0.013 | |
| bleed tinta | layer di-blur 0.9–1.4 px, alpha 45%, di bawah layer tajam | tinta “menyerap” |
| serat kertas | multiply `0.945 + noise_blur/255*0.11` | berlaku ke tinta juga |

Kenapa penting: jitter per-kata masih menyisakan bentuk huruf yang identik di seluruh halaman — itu
tell-tale terkuat yang dibaca vision sebagai “font”.

## 2. Pipeline foto (urutan wajib)
1. **Kanvas meja** — kayu prosedural: `rings = sin(t*0.017 + 2.2*sin(x*0.0035 + y*0.0016))` +
   `rings2` (`t*0.09`) + `fine` (`t*0.42`) dengan `t = y*0.85 + x*0.45`; base RGB ~ (128+62v, 88+46v, 56+34v);
   multiply blotch `0.9 + 0.2*noise_blur6`; noise σ3.2; `GaussianBlur 2–3.6`; 4–9 goresan tipis.
2. **Warp** (numpy inverse mapping, bilinear): rotasi ±3.4°, bow `amp 8–24 px` `y -= amp*sin(pi*u)`,
   bow kedua `amp2 −16..16` `*0.6*sin(pi*v)`, keystone ±0.04. Mask halaman = gambar putih kosong
   di-warp dengan parameter yang sama → tepi kertas ikut melengkung.
3. **Lubang jilid** dipukul di mask (`ellipse [10,hy,34,hy+24] fill 0`, tiap 232 px) — **sebelum** warp.
4. **Tempel**: kertas bawah (offset +12..30 x, +16..34 y) → strip jilid gelap (92 px, blur 2.4, rotate ±1.3°)
   → bayangan kontak → halaman + alpha.
   Bayangan: alpha di-offset (+7..16, +8..20); `blur 4 @0.55` warna (34,22,14);
   `blur 17 @0.42` warna (52,36,24).
5. **Detail buku**: band gradasi 30 px di tepi kiri (alpha 120 menurun pangkat 1.6) = lipatan jilid;
   cincin spiral digambar di atas di pusat lubang (outline (150,152,158) width 5 + highlight arc + lubang gelap);
   pulpen di meja (badan gelap + ujung + clip metalik, rotate −11..−4°, bayangan blur 9).
6. **Cahaya**: `lux = 1.16 − 0.55·(x/cw−0.30)² − 0.42·(y/ch−0.22)²` + pool `0.10·exp(−((x−0.30cw)/0.30cw)² − ((y−0.22ch)/0.26ch)²)`;
   `vign = 1 − 0.34·((x−c/2)/(c/2))² + ((y−c/2)/(c/2))²)^1.25`; `clip(lux*vign, 0.30, 1.35)`;
   tint `+[8,4,−4]·(1−vign)`.
7. **Kamera**: `np.roll(R,+1)`, `np.roll(B,−1)` (chromatic aberration), `GaussianBlur 0.45–0.8`,
   `Image.blend(canvas, noise, 0.045)`, JPEG `quality=84`. Output ±2150×3134 px (~500 KB) — cukup untuk Telegram.

## 3. Jebakan yang benar-benar kejadian
| Gejala | Sebab | Fix |
|---|---|---|
| Foto keluar cuma meja kosong, `bright% = 0` | `Image.composite(black, alpha, hole_mask)` terbalik → alpha ≈0 → page tidak pernah ter-paste | `Image.composite(alpha, black, hole_mask)` |
| Kata terbaca ngawur / huruf tumpuk | tile huruf di-resize (`wsc`) tapi advance pakai `font.getlength` mentah | `char_tile` return `(tile, adv)` dengan `adv = getlength(ch)*wsc` |
| Warning `invalid value encountered in cast` + piksel rusak | `((x−c)/c)**1.4` → basis negatif pangkat pecahan = NaN | pakai kuadrat `((x/c−a)**2)` atau `abs()` |
| Vision bilang “halaman solid kelabu, blank” padahal foto OK | vision_analyze halusinasi pada gambar besar yang dikecilkan | cek dulu numerik: `bright% ≈ 45–50` = kertas ada di frame; mean per-band-x untuk lokasi |
| Vision sebut kata “garbled” | sering salah baca sendiri (JPEG + tulisan messy), bukan render | crop `region=[...]` → minta transkrip kata-per-kata; cek PNG mentah |
| Isi hilang tanpa terlihat | halaman terakhir diam-diam kehabisan ruang | setelah loop halaman: `state["i"] == len(ITEMS)` |
| Angka uang salah baca | digit pada JPEG kecil | verifikasi khusus crop bagian angka; pastikan tidak ambigu |

## 4. Sikap kerja (penting)
- Vision akan **selalu** bilang “masih terlihat AI” — berhenti saat glitch nyata sudah nol, jangan iterasi
  tanpa ujung. Perbaiki yang terukur (statistik pixel, transkrip crop), abaikan opini estetika umum.
- Urutan hemat: perbaiki bug composite dulu (bikin foto benar-benar ada) → baru realism.

## 5. Pengiriman
Kirim **1 JPG per halaman** (Telegram render inline sebagai foto). PDF bersih versi rapi tetap disimpan
di `~/tugas/` sebagai referensi contekan, dan disebutkan singkat di chat — jangan dikirim dua-duanya.
