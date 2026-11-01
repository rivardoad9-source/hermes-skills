# Urutan layer & disiplin overlay (Tahap 2 — foto buku)

`references/photo-realism-recipe.md` isi *parameter*. File ini isi **z-order**: apa yang boleh
menutupi halaman dan apa yang tidak. Satu kesalahan urutan di sini menghasilkan foto yang secara
parameter sudah benar tapi jawabannya ketutup.

## Urutan tempel yang benar

1. kanvas meja (kayu prosedural, sudah di-blur 2–3.6 px)
2. kertas bawah (sheet2, offset +12..30 x / +16..34 y)
3. strip jilid gelap (92 px, blur 2.4, rotate ±1.3°)
4. bayangan kontak halaman (`blur 4 @0.55` tajam + `blur 17 @0.42` lebar)
5. **halaman + alpha** ← titik balik: semua yang "di bawah" sudah selesai
6. band gradasi lipatan jilid (30 px di tepi kiri halaman)
7. cincin spiral, di pusat lubang (harus di ATAS halaman — kawat memang menindih tepi kertas)
8. pulpen di meja + bayangannya
9. properti blur (botol, box)
10. cahaya/vignette → artefak kamera → noise → JPEG

## Aturan: apa yang boleh menyentuh rect halaman

Hanya dua hal yang boleh digambar di atas halaman:

- **band gradasi lipatan** di 30 px pertama tepi kiri (mensimulasikan jilid) — `alpha 120` menurun
  pangkat 1.6;
- **cincin spiral** di area lubang jilid (x ≈ 0..50 px halaman).

Segala properti lain (pulpen, botol, box, gelas) **wajib di luar rect halaman**.

## Bug yang benar-benar kejadian

Botol di-paste di `(-cw*0.10, -ch*0.05)` dengan ukuran `0.30cw × 0.62ch` → menutupi **182 px**
kolom kiri halaman, termasuk sebagian teks jawaban. Gejala yang dibaca vision: *"grey pill-shaped
object dengan label merah di atas halaman"* dan *"unexplained blurry object, kemungkinan artefak AI"*.

Fix: botol `-0.17cw` ukuran `0.26cw × 0.52ch` alpha ×0.92; box `0.70cw` tinggi `0.15ch` (masih di
luar halaman karena `oy ≈ 0.13ch`). Setelah dipindah, kedua properti berhenti disebut vision.

## Cara mendeteksi lebih cepat dari vision

Jangan tunggu vision. Hitung statistik per-band kolom:

```python
a = np.asarray(Image.open(foto).convert("RGB")).astype(float)
for i in range(0, a.shape[1], 250):
    band = a[:, i:i+250]
    print(i, band.reshape(-1, 3).mean(0).round(0), round((band.mean(2) > 180).mean()*100, 1))
```

- `bright%` keseluruhan ≈ **45–50** = kertas ada di frame. **0%** = halaman tidak ter-paste
  (cek polaritas `Image.composite`, lihat tabel bug di resep).
- Sebuah band yang seharusnya kertas-bright (≈230) tapi terbaca gelap ≈ meja (80–110) = ada objek
  yang menutupinya. Itu cara menemukan properti nyasar dalam 1 detik, bukan setelah 3 putaran vision.

## Aturan properti biar tidak jadi "glitch"

- alpha ≤ 0.95 dan blur ≥ 10 px — properti tajam di latar belakang langsung dibaca "artefak AI".
- cukup 1–2 properti, di tepi frame; gelas/botol penuh di tengah frame lebih buruk daripada tidak ada.
- bayangan properti digambar sebelum properti (`composite` warna gelap dengan mask alpha ×0.45,
  blur 15), bukan sesudahnya.
