# Vault sync pitfalls (observed 2026-09-14)

## 1. `vault_sync.sh` diam-diam no-op kalau remote belum diset

`~/.hermes/scripts/vault_sync.sh` melakukan `git remote get-url origin >/dev/null 2>&1` dan
**`exit 0` tanpa pesan** kalau remote tidak ada. Artinya: catatan bisa "berhasil disimpan",
ter-commit lokal, dan tetap **tidak pernah sampai ke device user** — tanpa satu pun sinyal.

**Cek dulu sebelum menjanjikan sinkronisasi:**

```bash
cd $HOME/obsidian-vault && git remote -v && git log --oneline -1 && git status -sb
```

Kalau `git remote -v` kosong: catatan cuma ada di server. Katakan itu ke user apa adanya, dan
tawarkan setup repo privat + remote (jangan diamkan). Setelah remote ada, `vault_sync.sh` baru
benar-benar push, dan aman dipanggil tiap jam.

## 2. Media dari CDN sosmed KEDALUWARSA — salin ke vault, jangan cuma link

URL gambar dari `scontent*.cdninstagram.com` (Threads/Instagram) membawa parameter `oe=<hex timestamp>`;
beberapa jam kemudian link-nya mati. `pbs.twimg.com` (X) juga bisa berubah/expire.

Jadi saat menyimpan catatan dari sebuah post: **unduh gambarnya dan taruh di vault**
(`attachments/<nama-deskriptif>.jpg`), lalu embed dengan `![[...]]` atau `![](attachments/...)`.
Catatan yang cuma berisi URL akan jadi catatan kosong dalam sehari. Bonus: transkrip isi gambarnya
ke dalam catatan (angka di screenshot itu sering bagian paling pentingnya).

## 3. Konvensi vault user (dari `Sistem yang Berjalan.md`)

- Bahasa Indonesia, judul `#`, baris `> ` sebagai snapshot/tanggal di bawah judul.
- Tabel markdown, dan penutup `Lihat juga: [[Note Lain]]`.
- Nama file deskriptif (`Ide Project - <produk> (<sumber>).md`), bukan tanggal saja.
- Simpan **angka mentah** yang dikutip dari sumber (klaim PnL, ukuran posisi, dsb) + tandai mana yang
  belum terverifikasi — vault user dipakai buat keputusan, jadi klaim tanpa label lebih bahaya daripada
  tidak ada catatan.
