# Baca angka asli campaign Whop / Content Rewards

Feed dan halaman campaign nampilin angka yang dipilih-pilih (sering `Join to unlock`,
sering cuma CPM). Payload halaman-nya sendiri memuat objek campaign lengkap, termasuk
**jumlah pesaing dan sisa kolam**. Ini yang bikin pemilihan campaign jadi berbasis data,
bukan feeling.

## Cara ngekstrak
Halaman campaign (dan feed-nya) itu Next.js App Router: data-nya dikirim sebagai
baris-baris `self.__next_f.push([1,"<json di-escape>"])`. Gabungin semua chunk, decode
pakai `json.loads('"'+chunk+'"')` (itu yang ngebuka escape-nya), baru regex field-nya.
Bukan `__NEXT_DATA__` - itu nggak ada di sini.

```python
raw = urlopen(Request(url, headers=UA)).read().decode("utf-8", "ignore")
chunks = re.findall(r'self\.__next_f\.push\(\[1,\s*"((?:[^"\\]|\\.)*)"\]\)', raw)
blob = "".join(json.loads('"' + c + '"') for c in chunks)
```

Script siap pakai (sudah dites):

```bash
python3 ~/.hermes/scripts/cr_campaign_metrics.py <url> [<url>...]
python3 ~/.hermes/scripts/cr_campaign_metrics.py --from-scan ~/.hermes/cache/scratch/whop_all_*.txt
python3 ~/.hermes/scripts/cr_campaign_detail.py <url>   # versi teks halaman (rate/payout/aturan)
```

Untuk dapat daftar URL-nya dulu: `python3 ~/.hermes/scripts/clip_campaign_scan.py --all`,
lalu teeing ke file dan suapin ke `--from-scan`. Sekali jalan 10 campaign ~2 menit.

## Field yang penting
| Field | Arti |
|---|---|
| `budget` | kolam total campaign, **satuan sen** (`485000` = $4.850) |
| `payoutModel[]` | per platform: `platform`, `rate` (**sen per 1.000 views**, `125` = $1,25), `minPayout`, `maxPayout` (sen), kadang `budget` per platform |
| `metrics.creatorCount` | **jumlah clipper yang udah ikut** - ini angka persaingan |
| `metrics.budgetSpentCents` | kolam yang udah kepakai; `budget - ini` = sisa beneran |
| `metrics.paidOutCents` | yang udah cair (biasanya 0 walau klip udah disetujui - pencairan ada siklusnya) |
| `metrics.approvedSubmissionCount` | klip lolos review |
| `metrics.totalViews` | traksi campaign-nya |
| `metrics.budgetProgressBps` | kolam kepakai dalam basis point (`100` = 1%) |
| `contentTypes[]` | `clipping` / `slideshows` / `ugc-with-face` / `ugc-faceless` - nentuin bisa nggak kita kerjain |
| `creatorTypes[]` | `clipper` / `ugc` / `influencer` |
| `contentCategories[]` | gaming, music, technology, health-wellness, ... |
| `creatorRequirements[]` | syarat persona dalam teks bebas (bahasa, umur, face cam) |
| `contentRules[]` | aturan konten dalam teks bebas |
| `briefCounts` | jumlah contentRules / creatorRequirements / reference files |
| `requirement` | `preApproval`, `faceOnCamera`, `demographics`, `brandLogo`, `linkInBio(+Url)`, `botMonitoringDays` |
| `requiresApplication` | `true` = harus apply & disetujui dulu, bukan klik-join |
| `verified` | brand terverifikasi |
| `launchDate` / `statusChangedAt` | **UTC** (WIB = +7 jam) |
| `state` / `status` | `success` = hidup; `showOnDiscover`, `private` buat nyaring feed |

**Nggak ada field negara/wilayah** di objek campaign. Gate negara cuma muncul di dialog
join, jadi jangan bilang satu campaign "aman buat Indonesia" berdasarkan halaman publiknya.

## Cara nge-rank
Skor = `rate x sisa kolam` **dikoreksi persaingan**: kolam utuh + `creatorCount` 0 +
`budgetSpentCents` 0 itu window paling gemuk, sekalipun rate-nya cuma separuh campaign
lain yang udah dikeroyok. Tambah faktor eksekusi: pilih `clipping`/`slideshows`
(faceless, bisa kelarin sendiri) di atas `ugc-with-face` (butuh user di depan kamera).

Saring dulu yang mati: `requiresApplication: true` + `creatorRequirements` yang minta
bahasa/umur/domisili yang user nggak punya, dan kategori judi/streamer kasino.

Math buat ngasih harapan realistis ke user:

```
views buat nembus cap = maxPayout / rate x 1000
Rp100jt (~$6.000)    = $6.000 / rate x 1000 views  -> contoh rate $1,25: ~4,8 juta views
total views kolam    = budget / rate x 1000        -> contoh $4.850 di $1,25: ~3,9 juta views
```

Jadi nggak ada satu campaign yang bisa ngehasilin Rp100jt sendirian. Sebut ini sebelum
user nyangka lebih.

## Jebakan waktu parsing
- **`"metrics"` muncul lebih dari sekali** di payload dan yang pertama sering objek lain
  tanpa `creatorCount`. Ambil match yang isinya `creatorCount`, jangan `re.search` pertama.
- **Jangan ambil nama dari key `"name"`** - itu bisa nyangkut metadata Next.js
  (`Next.MetadataOutlet`). Ambil dari tag `<title>` lalu potong di `" by "`.
- Beberapa halaman (pernah kejadian di campaign EDC) nggak nge-embed objek `metrics` -nya;
  handle `None`, dan jangan ngeklaim jumlah pesaing buat campaign itu.
- `paidOutCents: 0` walaupun ada klip disetujui itu wajar (pencairan per siklus) - bukan
tanda campaign nggak bayar. Jangan dijadiin alasan buat skip.
- Halaman feed `whop.com/contentrewards/` gampang discrape pakai `urllib` + UA desktop,
tanpa login; kalau hasilnya kosong, cek UA dulu sebelum nyalahin situsnya.

## Ngelanjutin ke otomatisasi
Kalau mau alert cron `clip_campaign_scan.py` sekalian bawa angka pesaing, panggil
`cr_campaign_metrics.get(url)` dari script itu (fungsinya sudah dipisah, jadi bisa
di-import) dan masukin `creatorCount` + sisa kolam + rate + cap ke pesannya. Jalankan
`--dry` dulu sebelum nutup perubahan, karena script itunya jalan tiap jam.
